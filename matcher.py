"""
matcher.py
Modul pencocokan kandidat terhadap kriteria pekerjaan menggunakan pendekatan
HYBRID:
  1. Embedding similarity (cosine similarity) -> skor kuantitatif awal, cepat,
     murah, dan konsisten antar-run (tidak ada variasi seperti generative LLM).
  2. LLM qualitative scoring -> reasoning kontekstual, menghasilkan alasan
     naratif yang bisa dibaca HR (kenapa kandidat cocok/tidak cocok), sesuai
     requirement output "alasan pemilihan/penolakan" di soal.

Skor akhir = weighted average dari kedua skor (lihat config.py).
"""

import re
import json
import numpy as np
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

import config
from config import (
    GEMINI_TEXT_MODEL,
    GEMINI_EMBEDDING_MODEL,
    WEIGHT_EMBEDDING_SCORE,
    WEIGHT_LLM_SCORE,
    EDUCATION_HIERARCHY,
)


# ---------------------------------------------------------------------------
# 1. HARD FILTER — syarat wajib yang tidak bisa dikompromikan
# ---------------------------------------------------------------------------

def apply_hard_filters(candidate_info: dict, criteria: dict) -> tuple[bool, list[str]]:
    """
    Cek syarat wajib (hard requirement) sebelum masuk tahap scoring mendalam.
    Mengevaluasi:
    1. Pengalaman kerja minimum (tahun)
    2. Skill wajib yang harus dikuasai
    3. Jenjang pendidikan minimal (SMA/SMK, D3, S1, S2)

    Return: (lolos_filter: bool, alasan_gagal: list[str])
    """
    reasons_failed = []

    # 1. Cek Pengalaman Kerja Minimum
    min_exp = criteria.get("min_experience_years", 0)
    candidate_exp = candidate_info.get("total_experience_years", 0) or 0
    if candidate_exp < min_exp:
        reasons_failed.append(
            f"Pengalaman kerja ({candidate_exp} tahun) di bawah syarat minimum ({min_exp} tahun)"
        )

    # 2. Cek Skill Wajib
    def _normalize_token(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", s.lower())

    required_skills = criteria.get("required_skills", [])
    candidate_skills = [s.strip().lower() for s in (candidate_info.get("skills") or [])]
    normalized_candidate_skills = [_normalize_token(s) for s in candidate_skills]

    missing_skills = []
    for req in required_skills:
        req_clean = req.strip().lower()
        if not req_clean:
            continue
        req_norm = _normalize_token(req_clean)
        # Cek exact, substring regex boundary, atau token normalized
        found = (
            req_norm in normalized_candidate_skills
            or any(req_norm in cs_norm for cs_norm in normalized_candidate_skills if cs_norm)
            or any(re.search(r"\b" + re.escape(req_clean) + r"\b", cs) for cs in candidate_skills)
        )
        if not found:
            missing_skills.append(req.strip())

    if missing_skills:
        reasons_failed.append(f"Skill wajib tidak ditemukan: {', '.join(missing_skills)}")

    # 3. Cek Jenjang Pendidikan Minimal
    min_edu = criteria.get("min_education_level")
    if min_edu:
        min_edu_clean = min_edu.strip().lower()
        min_edu_val = EDUCATION_HIERARCHY.get(min_edu_clean, 0)

        candidate_edu_list = candidate_info.get("education", []) or []
        candidate_max_val = 0
        candidate_edu_label = "Tidak terdeteksi"

        for edu in candidate_edu_list:
            deg = (edu.get("degree") or "").lower().strip()
            maj = (edu.get("major") or "").lower().strip()
            inst = (edu.get("institution") or "").lower().strip()
            text_combo = f"{deg} {maj} {inst}"

            for key, val in EDUCATION_HIERARCHY.items():
                if key in text_combo:
                    if val > candidate_max_val:
                        candidate_max_val = val
                        candidate_edu_label = edu.get("degree") or key.upper()

        if min_edu_val > 0 and candidate_max_val < min_edu_val:
            reasons_failed.append(
                f"Pendidikan ({candidate_edu_label}) belum memenuhi syarat minimum ({min_edu.upper()})"
            )

    passed = len(reasons_failed) == 0
    return passed, reasons_failed


# ---------------------------------------------------------------------------
# 2. EMBEDDING SIMILARITY
# ---------------------------------------------------------------------------

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_embedding(text: str) -> np.ndarray:
    """Ambil vector embedding dari teks menggunakan Gemini embedding model."""
    if config.GEMINI_API_KEY:
        genai.configure(api_key=config.GEMINI_API_KEY)
    result = genai.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        content=text,
        task_type="semantic_similarity",
    )
    return np.array(result["embedding"])


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Hitung cosine similarity antara dua vector, dikembalikan dalam skala 0-100."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    similarity = np.dot(vec_a, vec_b) / (norm_a * norm_b)
    return float(max(0, similarity) * 100)


def _heuristic_text_similarity(text_a: str, text_b: str) -> float:
    """Fallback kemiripan leksikal/token jika embedding API tidak aktif."""
    tokens_a = set(re.findall(r"\w+", text_a.lower()))
    tokens_b = set(re.findall(r"\w+", text_b.lower()))
    if not tokens_a or not tokens_b:
        return 50.0
    intersection = tokens_a.intersection(tokens_b)
    union = tokens_a.union(tokens_b)
    jaccard = len(intersection) / len(union) if union else 0.0
    # Normalisasi ke skala persentase realistis (40 - 95%)
    return float(round(40 + (jaccard * 150), 2))


def compute_embedding_score(candidate_summary: str, job_description: str) -> float:
    """
    Bandingkan ringkasan kandidat dengan JD menggunakan cosine similarity embedding.
    Menggunakan fallback leksikal jika API key belum tersedia.
    """
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("your_"):
        return _heuristic_text_similarity(candidate_summary, job_description)

    try:
        candidate_vec = get_embedding(candidate_summary)
        jd_vec = get_embedding(job_description)
        return cosine_similarity(candidate_vec, jd_vec)
    except Exception as e:
        print(f"[WARNING] Embedding API error ({e}), using lexical similarity fallback.")
        return _heuristic_text_similarity(candidate_summary, job_description)


# ---------------------------------------------------------------------------
# 3. LLM QUALITATIVE SCORING + REASONING
# ---------------------------------------------------------------------------

LLM_SCORING_PROMPT_TEMPLATE = """
Anda adalah asisten rekrutmen yang objektif. Nilai kecocokan kandidat berikut
terhadap deskripsi pekerjaan dan kriteria yang diberikan. JANGAN membuat
asumsi berdasarkan nama, gender, usia, atau informasi yang tidak relevan
dengan kompetensi kerja. Fokus HANYA pada kesesuaian skill, pengalaman, dan
pendidikan dengan kebutuhan posisi.

Deskripsi Pekerjaan:
{job_description}

Kriteria Kualifikasi:
{criteria_text}

Data Kandidat (identitas telah disamarkan untuk objektivitas):
{candidate_data}

Kembalikan HANYA JSON dengan skema berikut, tanpa teks tambahan:
{{
  "match_score": number (0-100, seberapa cocok kandidat dengan posisi ini),
  "strengths": [string] (poin-poin kekuatan kandidat yang relevan dengan posisi),
  "gaps": [string] (poin-poin kekurangan atau ketidaksesuaian, kosongkan jika tidak ada),
  "reasoning": string (1-3 kalimat ringkasan alasan skor, akan ditampilkan ke HR)
}}
"""


def _heuristic_qualitative_score(candidate_scoring_fields: dict, job_description: str, criteria: dict) -> dict:
    """
    Fallback evaluasi kualitatif jika Gemini API tidak tersedia.
    Menghitung skor berdasarkan persentase skill yang relevan dan pengalaman kerja.
    """
    cand_skills = [s.lower() for s in (candidate_scoring_fields.get("skills") or [])]
    cand_exp = candidate_scoring_fields.get("total_experience_years", 0) or 0
    req_exp = criteria.get("min_experience_years", 1) or 1

    strengths = []
    gaps = []

    # Evaluasi Skill
    req_skills = criteria.get("required_skills", [])
    matched_skills = [s for s in req_skills if any(s.lower() in cs for cs in cand_skills)]
    unmatched_skills = [s for s in req_skills if not any(s.lower() in cs for cs in cand_skills)]

    if matched_skills:
        strengths.append(f"Menguasai keahlian relevan: {', '.join(matched_skills)}")
    if cand_skills:
        strengths.append(f"Memiliki ragam kompetensi teknis: {', '.join(cand_skills[:4])}")

    if unmatched_skills:
        gaps.append(f"Belum menunjukkan penguasaan pada: {', '.join(unmatched_skills)}")

    # Evaluasi Pengalaman
    exp_ratio = min(cand_exp / req_exp, 1.5)
    if cand_exp >= req_exp:
        strengths.append(f"Pengalaman kerja {cand_exp} tahun memenuhi target kebutuhan.")
    else:
        gaps.append(f"Pengalaman {cand_exp} tahun masih di bawah preferensi ideal ({req_exp} tahun).")

    # Hitung skor kualitatif (0-100)
    skill_score = (len(matched_skills) / max(len(req_skills), 1)) * 50
    exp_score = min(exp_ratio, 1.0) * 40
    base_score = 10
    total_score = round(min(100, max(20, skill_score + exp_score + base_score)), 1)

    reasoning = (
        f"Kandidat memiliki total pengalaman kerja {cand_exp} tahun dengan penguasaan kompetensi "
        f"kunci ({', '.join(matched_skills) if matched_skills else 'belum spesifik'}). "
        f"{'Sangat direkomendasikan untuk wawancara teknis.' if total_score >= 70 else 'Perlu pendalaman lebih lanjut saat wawancara.'}"
    )

    return {
        "match_score": total_score,
        "strengths": strengths,
        "gaps": gaps,
        "reasoning": reasoning,
    }


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_llm_qualitative_score(
    candidate_scoring_fields: dict,
    job_description: str,
    criteria: dict,
) -> dict:
    """
    Minta LLM menilai kecocokan kandidat secara kualitatif dan memberikan
    reasoning naratif. Input candidate_scoring_fields TIDAK boleh mengandung field
    sensitif (name, email, phone, dll) - sudah dipisahkan oleh bias_mitigation.py.
    """
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY.startswith("your_"):
        return _heuristic_qualitative_score(candidate_scoring_fields, job_description, criteria)

    try:
        if config.GEMINI_API_KEY:
            genai.configure(api_key=config.GEMINI_API_KEY)
        criteria_text = json.dumps(criteria, ensure_ascii=False, indent=2)
        candidate_data_text = json.dumps(candidate_scoring_fields, ensure_ascii=False, indent=2)

        prompt = LLM_SCORING_PROMPT_TEMPLATE.format(
            job_description=job_description,
            criteria_text=criteria_text,
            candidate_data=candidate_data_text,
        )

        model = genai.GenerativeModel(GEMINI_TEXT_MODEL)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        return json.loads(response.text)
    except Exception as e:
        print(f"[WARNING] Gemini LLM scoring failed ({e}), using heuristic qualitative scoring.")
        return _heuristic_qualitative_score(candidate_scoring_fields, job_description, criteria)


# ---------------------------------------------------------------------------
# 4. GABUNGAN: HYBRID FINAL SCORE
# ---------------------------------------------------------------------------

def build_candidate_summary_text(scoring_fields: dict) -> str:
    """Ubah field terstruktur (tanpa identitas) menjadi teks naratif untuk embedding."""
    parts = []

    if scoring_fields.get("total_experience_years"):
        parts.append(f"Total pengalaman kerja: {scoring_fields['total_experience_years']} tahun.")

    for exp in scoring_fields.get("work_experience", []) or []:
        parts.append(
            f"Pernah menjabat sebagai {exp.get('job_title', '')} di {exp.get('company', '')}: "
            f"{exp.get('responsibilities_summary', '')}"
        )

    for edu in scoring_fields.get("education", []) or []:
        parts.append(f"Pendidikan: {edu.get('degree', '')} {edu.get('major', '')} dari {edu.get('institution', '')}")

    if scoring_fields.get("skills"):
        parts.append("Skill: " + ", ".join(scoring_fields["skills"]))

    if scoring_fields.get("certifications"):
        parts.append("Sertifikasi: " + ", ".join(scoring_fields["certifications"]))

    return "\n".join(parts)


def score_candidate(scoring_fields: dict, job_description: str, criteria: dict) -> dict:
    """
    Fungsi utama modul ini: hitung skor hybrid final untuk satu kandidat.
    Mengembalikan dict berisi embedding_score, llm_score, final_score,
    strengths, gaps, dan reasoning.
    """
    candidate_summary = build_candidate_summary_text(scoring_fields)

    embedding_score = compute_embedding_score(candidate_summary, job_description)
    llm_result = get_llm_qualitative_score(scoring_fields, job_description, criteria)

    final_score = round(
        (embedding_score * WEIGHT_EMBEDDING_SCORE)
        + (llm_result["match_score"] * WEIGHT_LLM_SCORE),
        2,
    )

    return {
        "embedding_score": round(embedding_score, 2),
        "llm_score": round(float(llm_result["match_score"]), 2),
        "final_score": final_score,
        "strengths": llm_result.get("strengths", []),
        "gaps": llm_result.get("gaps", []),
        "reasoning": llm_result.get("reasoning", ""),
    }
