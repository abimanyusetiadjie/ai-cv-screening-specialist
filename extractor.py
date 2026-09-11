"""
extractor.py
Modul untuk mengekstrak informasi terstruktur (nama, pendidikan, pengalaman,
skill, dll) dari raw text CV menggunakan Gemini dengan output JSON terjadwal
(response_mime_type="application/json").
"""

import os
import re
import json
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

import config
from config import GEMINI_TEXT_MODEL

EXTRACTION_PROMPT_TEMPLATE = """
Anda adalah sistem ekstraksi informasi CV. Baca teks CV berikut dan ekstrak
informasi ke dalam format JSON PERSIS sesuai skema di bawah. Jangan menambah
field lain. Jika informasi tidak ditemukan, isi dengan null atau array kosong.
Jangan mengarang informasi yang tidak ada di teks.

Skema JSON:
{{
  "name": string atau null,
  "email": string atau null,
  "phone": string atau null,
  "total_experience_years": number (estimasi total tahun pengalaman kerja relevan),
  "education": [
    {{"degree": string, "major": string, "institution": string, "graduation_year": string}}
  ],
  "work_experience": [
    {{"job_title": string, "company": string, "duration": string, "responsibilities_summary": string}}
  ],
  "skills": [string],
  "certifications": [string]
}}

Teks CV:
---
{cv_text}
---

Kembalikan HANYA JSON, tanpa teks tambahan, tanpa markdown code fence.
"""


def _heuristic_extraction(cv_text: str) -> dict:
    """
    Ekstraksi heuristik berbasis aturan/regex sebagai fallback jika Gemini API
    tidak tersedia (misal API key belum diset atau offline).
    """
    lines = [l.strip() for l in cv_text.split("\n") if l.strip()]
    first_few = " ".join(lines[:10])

    # Ekstraksi Email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", cv_text)
    email = email_match.group(0) if email_match else None

    # Ekstraksi Phone
    phone_match = re.search(r"(\+62|62|0)8[0-9\- ]{7,14}", cv_text)
    phone = phone_match.group(0) if phone_match else None

    # Ekstraksi Nama (biasanya baris non-kosong pertama yang bukan kata kunci)
    name = None
    for line in lines[:5]:
        if not any(k in line.lower() for k in ["curriculum", "resume", "cv", "page", "phone", "email", "@"]):
            if len(line.split()) <= 4 and len(line) > 2:
                name = line
                break

    # Ekstraksi Estimasi Tahun Pengalaman
    total_exp = 0
    exp_matches = re.findall(r"(\d+)\s*(?:tahun|thn|years|year)", cv_text, re.IGNORECASE)
    if exp_matches:
        total_exp = max(int(m) for m in exp_matches if int(m) < 40)
    else:
        # Deteksi rentang tahun (cth: 2018-2022)
        year_ranges = re.findall(r"(20\d\d)\s*[-–]\s*(20\d\d|present|sekarang)", cv_text, re.IGNORECASE)
        if year_ranges:
            total_exp = len(year_ranges) * 2  # estimasi moderat

    # Ekstraksi Pendidikan
    education = []
    edu_keywords = ["sarjana", "bachelor", "master", "magister", "d3", "diploma", "smk", "sma", "vocational", "universit", "institut", "politeknik"]
    for line in lines:
        l_low = line.lower()
        if any(ek in l_low for ek in edu_keywords):
            degree = "S1"
            if "master" in l_low or "magister" in l_low or "s2" in l_low:
                degree = "S2"
            elif "smk" in l_low or "sma" in l_low or "vocational" in l_low:
                degree = "SMK"
            elif "d3" in l_low or "diploma" in l_low or "politeknik" in l_low:
                degree = "D3"
            education.append({"degree": degree, "major": line[:60], "institution": line[:60], "graduation_year": ""})
            break

    # Ekstraksi Skill Populer (termasuk variasi ejaan spasi/dash)
    known_skills = [
        "AutoCAD", "SketchUp", "Revit", "Lumion", "Enscape", "3D Max", "V-Ray", "Photoshop",
        "Python", "SQL", "PostgreSQL", "MySQL", "FastAPI", "Django", "Flask", "Docker",
        "REST API", "Git", "Linux", "Architecture", "Drafter", "Civil Engineering"
    ]
    detected_skills = []
    for skill in known_skills:
        skill_regex = r"\b" + re.escape(skill) + r"\b"
        if skill == "SketchUp":
            skill_regex = r"sketch\s*up"
        elif skill == "AutoCAD":
            skill_regex = r"auto\s*cad"
        elif skill == "REST API":
            skill_regex = r"rest\s*api"

        if re.search(skill_regex, cv_text, re.IGNORECASE):
            detected_skills.append(skill)

    return {
        "name": name or "Kandidat (Terdeteksi Heuristik)",
        "email": email,
        "phone": phone,
        "total_experience_years": total_exp,
        "education": education,
        "work_experience": [],
        "skills": detected_skills,
        "certifications": [],
    }


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_gemini_json(prompt: str) -> dict:
    """
    Pemanggilan Gemini dengan output JSON terstruktur.
    """
    if config.GEMINI_API_KEY:
        genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_TEXT_MODEL)
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        correction_prompt = (
            f"{prompt}\n\nOutput sebelumnya tidak valid JSON dengan error: {e}. "
            "Perbaiki dan kembalikan HANYA JSON valid."
        )
        model_retry = genai.GenerativeModel(GEMINI_TEXT_MODEL)
        retry_response = model_retry.generate_content(
            correction_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        return json.loads(retry_response.text)


def extract_cv_information(cv_text: str) -> dict:
    """
    Fungsi utama modul ini: raw CV text -> dict informasi terstruktur.
    Jika API key Gemini tersedia, gunakan LLM. Jika tidak tersedia atau gagal,
    gunakan fallback ekstraksi heuristik agar pipeline tidak terhenti.
    """
    defaults = {
        "name": None,
        "email": None,
        "phone": None,
        "total_experience_years": 0,
        "education": [],
        "work_experience": [],
        "skills": [],
        "certifications": [],
    }

    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("your_"):
        extracted = _heuristic_extraction(cv_text)
        defaults.update(extracted)
        return defaults

    try:
        prompt = EXTRACTION_PROMPT_TEMPLATE.format(cv_text=cv_text)
        extracted = _call_gemini_json(prompt)
        defaults.update(extracted)
        return defaults
    except Exception as e:
        print(f"[WARNING] Gemini API extraction failed ({e}), using heuristic fallback.")
        extracted = _heuristic_extraction(cv_text)
        defaults.update(extracted)
        return defaults
