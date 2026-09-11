"""
bias_mitigation.py
Modul untuk mengurangi risiko bias saat proses scoring oleh LLM.

Prinsip: field yang berpotensi memicu bias (nama, gender, usia/tanggal lahir,
alamat detail, foto) DIPISAHKAN dari data yang dikirim ke tahap scoring.
Field-field ini tetap disimpan untuk keperluan identifikasi kandidat
di laporan akhir, tapi tidak ikut memengaruhi penilaian kecocokan.
"""

import re
from typing import Dict, Any, Tuple

SENSITIVE_KEYS = [
    "name",
    "email",
    "phone",
    "gender",
    "date_of_birth",
    "age",
    "photo_url",
    "marital_status",
    "religion",
    "address",
]


def mask_free_text(text: str) -> str:
    """
    Masking pola umum yang berpotensi bocor identitas sensitif di teks bebas
    (raw CV text) sebelum dikirim ke LLM untuk tahap scoring/reasoning.
    Ini lapisan tambahan di luar pemisahan field terstruktur.
    """
    masked = text

    # Masking pola email
    masked = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL DIHAPUS]", masked)

    # Masking pola nomor telepon Indonesia (sederhana)
    masked = re.sub(r"(\+62|62|0)8[0-9]{8,12}", "[TELEPON DIHAPUS]", masked)

    return masked


def separate_sensitive_fields(extracted_info: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Memisahkan field sensitif dari data hasil ekstraksi.

    Return:
        identity_fields: dict berisi field sensitif (untuk laporan akhir saja)
        scoring_fields: dict tanpa field sensitif (dikirim ke tahap scoring LLM)
    """
    identity_fields = {}
    scoring_fields = {}

    for key, value in extracted_info.items():
        if key.lower() in SENSITIVE_KEYS:
            identity_fields[key] = value
        else:
            scoring_fields[key] = value

    return identity_fields, scoring_fields


def reattach_identity(identity_fields: Dict[str, Any], scoring_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Menggabungkan kembali identitas kandidat ke hasil scoring HANYA setelah
    proses penilaian selesai, untuk keperluan penyusunan laporan akhir.
    """
    final_result = {**identity_fields, **scoring_result}
    return final_result
