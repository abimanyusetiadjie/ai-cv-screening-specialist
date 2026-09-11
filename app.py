import json
import tempfile
import os
import glob
import streamlit as st

import config
from pipeline import run_batch_screening

st.set_page_config(page_title="AI CV Screening - POC", page_icon="🏭", layout="wide")

st.title("🏭 Sistem Seleksi CV Otomatis Berbasis AI/ML")
st.caption(
    "Dirancang khusus untuk Skalabilitas Rekrutmen Manufaktur — Hybrid Matching (Gemini Embedding + LLM Qualitative Reasoning) & Mitigasi Bias Otomatis"
)

# Pemuatan Job Presets
job_presets = {}
if os.path.exists("job_presets.json"):
    try:
        with open("job_presets.json", "r", encoding="utf-8") as f:
            job_presets = json.load(f)
    except Exception:
        pass

with st.sidebar:
    st.header("⚙️ Konfigurasi & Kriteria")
    
    # Konfigurasi API Key
    api_key_input = st.text_input(
        "Gemini API Key (Opsional jika sudah di .env)",
        value=config.GEMINI_API_KEY,
        type="password",
        help="Jika kosong, sistem akan menggunakan mode evaluasi heuristik cerdas tanpa error.",
    )
    if api_key_input != config.GEMINI_API_KEY:
        config.set_api_key(api_key_input)

    st.divider()
    st.subheader("Pilih Template Lowongan")
    preset_options = ["Plant CAD Drafter & 3D Designer (Cocok dengan Sample CV)", "Backend Engineer (Sistem Pabrik)", "Kustom"]
    selected_preset = st.selectbox("Preset Posisi Pekerjaan", preset_options)

    default_min_exp = 2
    default_skills = "AutoCAD, SketchUp"
    default_edu = "SMK"
    default_jd = ""

    if selected_preset.startswith("Plant CAD") and "plant_cad_drafter" in job_presets:
        p = job_presets["plant_cad_drafter"]
        default_min_exp = p["criteria"]["min_experience_years"]
        default_skills = ", ".join(p["criteria"]["required_skills"])
        default_edu = p["criteria"].get("min_education_level", "SMK")
        default_jd = p["job_description"]
    elif selected_preset.startswith("Backend") and "backend_engineer" in job_presets:
        p = job_presets["backend_engineer"]
        default_min_exp = p["criteria"]["min_experience_years"]
        default_skills = ", ".join(p["criteria"]["required_skills"])
        default_edu = p["criteria"].get("min_education_level", "S1")
        default_jd = p["job_description"]

    st.subheader("Kriteria Hard Filter")
    min_experience = st.number_input("Minimal Pengalaman (tahun)", min_value=0, value=default_min_exp)
    required_skills_input = st.text_input(
        "Skill Wajib (pisahkan dengan koma)", value=default_skills
    )
    required_skills = [s.strip() for s in required_skills_input.split(",") if s.strip()]

    edu_options = ["Tidak ada", "SMK", "D3", "S1", "S2"]
    edu_index = edu_options.index(default_edu) if default_edu in edu_options else 0
    min_education_level = st.selectbox("Jenjang Pendidikan Minimal", edu_options, index=edu_index)

    st.divider()
    st.caption(
        "🔒 **Mitigasi Bias & Privasi Data**: Nama, nomor telepon, email, gender, usia, dan foto "
        "DIPISAHKAN sebelum proses scoring AI (Blind Screening) sesuai UU PDP No. 27/2022."
    )

st.subheader("1. Deskripsi Pekerjaan (Job Description)")
job_description = st.text_area(
    "Detail Kebutuhan Posisi:",
    value=default_jd,
    height=140,
    placeholder="Tempelkan deskripsi pekerjaan di sini...",
)

st.subheader("2. Sumber Data CV Pelamar")
col_upload, col_demo = st.columns([2, 1])

with col_upload:
    uploaded_files = st.file_uploader(
        "Upload file CV mandiri (PDF / DOCX):",
        type=["pdf", "docx"],
        accept_multiple_files=True,
    )

with col_demo:
    st.markdown("**Uji Coba Cepat (One-Click Demo):**")
    st.caption("Jalankan otomatis terhadap 5 file CV anonim yang tersedia di folder `sample_cvs/`.")
    use_sample_cvs = st.button("📁 Proses 5 CV Bawaan (sample_cvs)", type="secondary")

process_custom = st.button("🚀 Proses CV Terunggah", type="primary")

# Tentukan file mana yang akan diproses
files_to_process = []
is_processing = False

if use_sample_cvs:
    sample_files = glob.glob("sample_cvs/*.pdf") + glob.glob("sample_cvs/*.docx")
    if not sample_files:
        st.error("Folder sample_cvs tidak ditemukan atau kosong.")
    else:
        files_to_process = sample_files
        is_processing = True

elif process_custom:
    if not job_description.strip():
        st.error("Deskripsi pekerjaan belum diisi.")
    elif not uploaded_files:
        st.error("Belum ada CV yang diunggah. Silakan upload file atau klik 'Proses 5 CV Bawaan'.")
    else:
        temp_dir = tempfile.mkdtemp()
        for uploaded_file in uploaded_files:
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            files_to_process.append(temp_path)
        is_processing = True

if is_processing and files_to_process:
    criteria = {
        "min_experience_years": min_experience,
        "required_skills": required_skills,
    }
    if min_education_level != "Tidak ada":
        criteria["min_education_level"] = min_education_level

    with st.spinner(f"Memproses {len(files_to_process)} CV... (Ekstraksi Informasi → Blind Filter → Hybrid Scoring)"):
        ranked_df, errors = run_batch_screening(files_to_process, job_description, criteria)

    if errors:
        with st.expander(f"⚠️ {len(errors)} file gagal diproses"):
            for err in errors:
                st.write(f"**{os.path.basename(err['file'])}**: {err['error']}")

    if not ranked_df.empty:
        # Metrik Ringkasan Eksekutif
        total_applicants = len(ranked_df)
        passed_filter_count = len(ranked_df[ranked_df["Lolos Syarat Wajib"] == "Ya"])
        avg_score = round(ranked_df[ranked_df["Lolos Syarat Wajib"] == "Ya"]["Skor Akhir"].mean() or 0, 1)
        shortlisted_count = len(ranked_df[(ranked_df["Lolos Syarat Wajib"] == "Ya") & (ranked_df["Skor Akhir"] >= 65)])

        st.divider()
        st.subheader("3. Ringkasan Eksekutif Hasil Seleksi")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total CV Masuk", f"{total_applicants} Kandidat")
        m2.metric("Lolos Syarat Wajib", f"{passed_filter_count} ({round(passed_filter_count/total_applicants*100)}%)")
        m3.metric("Rata-rata Skor Lolos", f"{avg_score} / 100")
        m4.metric("Rekomendasi Wawancara", f"{shortlisted_count} Kandidat", delta=f"{shortlisted_count} Siap Interview")

        st.subheader("4. Tabel Peringkat Kandidat (Ranked Shortlist)")
        display_cols = ["Nama", "Email", "No. Telepon", "Lolos Syarat Wajib", "Skor Embedding", "Skor LLM", "Skor Akhir"]
        st.dataframe(
            ranked_df[display_cols],
            use_container_width=True,
        )

        st.subheader("5. Analisis Kualitatif & Alasan Keputusan (Audit Trail)")
        for idx, row in ranked_df.iterrows():
            status_badge = "🟢 LOLOS FILTER" if row["Lolos Syarat Wajib"] == "Ya" else "🔴 GAGAL SYARAT WAJIB"
            with st.expander(f"Peringkat #{idx} — {row['Nama']} | Skor: {row['Skor Akhir']} ({status_badge})"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**✅ Kekuatan Utama (Strengths):**")
                    st.info(row["Kekuatan"] or "Tidak ada catatan kekuatan khusus.")
                with c2:
                    st.markdown("**⚠️ Kesenjangan / Catatan (Gaps):**")
                    st.warning(row["Kekurangan"] or "Tidak ada kekurangan signifikan.")
                
                st.markdown("**📝 Catatan Pertimbangan AI (Explainable Reasoning):**")
                st.write(row["Alasan"] or "-")

        # Download Report
        csv = ranked_df.to_csv(index=True).encode("utf-8")
        st.download_button(
            "⬇️ Download Laporan Rekrutmen (CSV)",
            data=csv,
            file_name="hasil_seleksi_cv_manufaktur.csv",
            mime="text/csv",
        )
    else:
        st.warning("Tidak ada kandidat yang berhasil diproses.")

st.divider()
st.caption(
    "Proof of Concept — Dirancang untuk evaluasi Technical Assessment AI Specialist. "
    "Mendukung integrasi ke HRIS/ATS perusahaan melalui Webhook & REST API."
)
