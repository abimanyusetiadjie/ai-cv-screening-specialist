"""
config.py
Konfigurasi global: API key Gemini, nama model, dan bobot scoring.

Cara set API key:
1. Di Colab: gunakan Secrets (kunci gembok di sidebar kiri) -> simpan sebagai GEMINI_API_KEY
2. Atau export sebagai environment variable sebelum menjalankan script:
   export GEMINI_API_KEY="isi-api-key-anda"
3. Atau (khusus development lokal, TIDAK disarankan untuk production) isi langsung
   di bawah pada variabel GEMINI_API_KEY.
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    # Aktif otomatis jika dijalankan di Google Colab dan secret sudah diset
    from google.colab import userdata  # type: ignore
    GEMINI_API_KEY = (userdata.get("GEMINI_API_KEY") or "").strip()
except Exception:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

def set_api_key(api_key: str):
    """Set API key secara dinamis (misal dari input Streamlit UI)."""
    global GEMINI_API_KEY
    clean_key = (api_key or "").strip()
    GEMINI_API_KEY = clean_key
    os.environ["GEMINI_API_KEY"] = clean_key
    try:
        import google.generativeai as genai
        genai.configure(api_key=clean_key)
    except Exception:
        pass

if not GEMINI_API_KEY:
    print(
        "[INFO] GEMINI_API_KEY belum diset. "
        "Dapat diisi via .env, Colab Secrets, environment variable, atau input UI Streamlit."
    )
else:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception:
        pass

# Model Gemini yang dipakai untuk ekstraksi & reasoning
GEMINI_TEXT_MODEL = "gemini-3.1-flash-lite"

# Model Gemini yang dipakai untuk embedding (semantic similarity)
GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-001"

# Bobot final scoring: kombinasi hybrid antara similarity embedding (cepat, murah, konsisten)
# dan penilaian kualitatif LLM (lebih kontekstual, bisa memberi alasan naratif)
WEIGHT_EMBEDDING_SCORE = 0.35
WEIGHT_LLM_SCORE = 0.65

# Ambang batas kelulusan filter wajib (hard filter) sebelum masuk ke tahap scoring mendalam
MIN_HARD_FILTER_PASS = True  # jika False, semua kandidat tetap discoring meski tidak penuhi syarat wajib

# Pemetaan standar jenjang pendidikan untuk komparasi objektif (Hard Filter)
EDUCATION_HIERARCHY = {
    "sma": 1,
    "smk": 1,
    "slta": 1,
    "d1": 2,
    "d2": 2,
    "d3": 3,
    "diploma": 3,
    "d4": 4,
    "s1": 4,
    "bachelor": 4,
    "sarjana": 4,
    "s2": 5,
    "master": 5,
    "magister": 5,
    "s3": 6,
    "doktor": 6,
    "phd": 6,
}
