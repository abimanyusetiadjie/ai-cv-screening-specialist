"""
ranker.py
Modul untuk menyusun daftar kandidat terurut (ranked) berdasarkan skor akhir,
lengkap dengan status kelulusan hard filter dan alasan.
"""

import pandas as pd


def rank_candidates(candidate_results: list[dict]) -> pd.DataFrame:
    """
    Ubah list hasil scoring per kandidat menjadi DataFrame terurut.

    Setiap item candidate_results diharapkan berbentuk:
    {
        "name": str,
        "email": str,
        "hard_filter_passed": bool,
        "hard_filter_reasons": list[str],
        "embedding_score": float,
        "llm_score": float,
        "final_score": float,
        "strengths": list[str],
        "gaps": list[str],
        "reasoning": str,
    }
    """
    rows = []
    for c in candidate_results:
        rows.append({
            "Nama": c.get("name") or "(tidak terdeteksi)",
            "Email": c.get("email") or "-",
            "No. Telepon": c.get("phone") or "-",
            "Lolos Syarat Wajib": "Ya" if c.get("hard_filter_passed") else "Tidak",
            "Skor Embedding": c.get("embedding_score", "-"),
            "Skor LLM": c.get("llm_score", "-"),
            "Skor Akhir": c.get("final_score", 0),
            "Kekuatan": "; ".join(c.get("strengths", []) or []),
            "Kekurangan": "; ".join(c.get("gaps", []) or c.get("hard_filter_reasons", [])),
            "Alasan": c.get("reasoning", ""),
        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Kandidat yang tidak lolos syarat wajib ditempatkan di bawah,
    # sisanya diurutkan berdasarkan skor akhir tertinggi
    df["_sort_priority"] = df["Lolos Syarat Wajib"].apply(lambda x: 0 if x == "Ya" else 1)
    df = df.sort_values(by=["_sort_priority", "Skor Akhir"], ascending=[True, False])
    df = df.drop(columns=["_sort_priority"]).reset_index(drop=True)
    df.index = df.index + 1  # ranking mulai dari 1

    return df
