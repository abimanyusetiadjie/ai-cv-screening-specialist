"""
pipeline.py
Orkestrasi end-to-end: raw file CV -> parsing -> ekstraksi -> bias mitigation
-> hard filter -> hybrid scoring -> ranked output.

Modul ini dipakai baik dari Colab notebook (loop manual/testing) maupun
dari app.py (Streamlit UI).
"""

from cv_parser import parse_cv
from extractor import extract_cv_information
from bias_mitigation import mask_free_text, separate_sensitive_fields, reattach_identity
from matcher import apply_hard_filters, score_candidate
from ranker import rank_candidates
from config import MIN_HARD_FILTER_PASS


def process_single_cv(file_path: str, job_description: str, criteria: dict) -> dict:
    """
    Proses satu file CV dari awal sampai akhir. Mengembalikan dict hasil
    lengkap untuk satu kandidat (siap dimasukkan ke rank_candidates).

    Jika terjadi error di tengah proses (misal file tidak terbaca), fungsi
    ini mengembalikan dict dengan flag "error" agar UI bisa menampilkan
    pesan yang jelas tanpa menghentikan proses kandidat lain.
    """
    try:
        # 1. Parsing file -> raw text
        raw_text = parse_cv(file_path)

        # 2. Ekstraksi informasi terstruktur (identitas & kompetensi)
        extracted_info = extract_cv_information(raw_text)

        # 3. Pisahkan identitas & PII (nama, email, no HP) dari kompetensi kerja (Blind Screening)
        identity_fields, scoring_fields = separate_sensitive_fields(extracted_info)

        # 4. Hard filter (syarat wajib: pengalaman, skill, pendidikan)
        hard_filter_passed, hard_filter_reasons = apply_hard_filters(scoring_fields, criteria)

        if not hard_filter_passed and MIN_HARD_FILTER_PASS:
            # Tetap disertakan di laporan akhir (transparansi), tapi tidak
            # dilanjutkan ke tahap scoring mendalam untuk hemat biaya API
            result = {
                "hard_filter_passed": False,
                "hard_filter_reasons": hard_filter_reasons,
                "embedding_score": 0,
                "llm_score": 0,
                "final_score": 0,
                "strengths": [],
                "gaps": hard_filter_reasons,
                "reasoning": "Tidak lolos syarat wajib, tidak dilanjutkan ke tahap scoring mendalam.",
            }
        else:
            # 5. Hybrid scoring (embedding similarity + LLM reasoning tanpa data identitas)
            scoring_result = score_candidate(scoring_fields, job_description, criteria)
            result = {
                "hard_filter_passed": hard_filter_passed,
                "hard_filter_reasons": hard_filter_reasons,
                **scoring_result,
            }

        # 6. Gabungkan kembali identitas untuk laporan akhir HR
        final_result = reattach_identity(identity_fields, result)
        final_result["source_file"] = file_path
        final_result["error"] = None
        return final_result

    except Exception as e:
        return {
            "name": None,
            "email": None,
            "phone": None,
            "source_file": file_path,
            "hard_filter_passed": False,
            "hard_filter_reasons": [],
            "embedding_score": 0,
            "llm_score": 0,
            "final_score": 0,
            "strengths": [],
            "gaps": [],
            "reasoning": "",
            "error": str(e),
        }


def run_batch_screening(file_paths: list[str], job_description: str, criteria: dict):
    """
    Proses banyak file CV sekaligus. Mengembalikan tuple:
    (ranked_dataframe, list_of_errors)
    """
    results = []
    errors = []

    for file_path in file_paths:
        result = process_single_cv(file_path, job_description, criteria)
        if result.get("error"):
            errors.append({"file": file_path, "error": result["error"]})
        else:
            results.append(result)

    ranked_df = rank_candidates(results)
    return ranked_df, errors
