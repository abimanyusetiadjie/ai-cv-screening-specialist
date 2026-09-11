"""
make_pdf_deck.py
Generator Presentasi PDF Profesional untuk Technical Assessment AI Specialist.
Menghasilkan file Presentasi_AI_CV_Screening_Specialist.pdf dalam format Landscape A4.
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

PAGE_W, PAGE_H = landscape(A4)

# Palet Warna
NAVY = colors.HexColor("#0F172A")
DARK_BLUE = colors.HexColor("#1E293B")
TEAL = colors.HexColor("#0EA5E9")
LIGHT_TEAL = colors.HexColor("#E0F2FE")
DARK_TEAL = colors.HexColor("#0369A1")
WHITE = colors.white
GRAY_BG = colors.HexColor("#F8FAFC")
GRAY_BORDER = colors.HexColor("#E2E8F0")
TEXT_MUTED = colors.HexColor("#64748B")
GREEN = colors.HexColor("#10B981")
AMBER = colors.HexColor("#F59E0B")
RED = colors.HexColor("#EF4444")


def draw_header(canv, title_text, category="TECHNICAL ASSESSMENT: AI SPECIALIST"):
    canv.saveState()
    # Category breadcrumb
    canv.setFont("Helvetica-Bold", 8)
    canv.setFillColor(TEAL)
    canv.drawString(40, PAGE_H - 35, category.upper())

    # Title
    canv.setFont("Helvetica-Bold", 16)
    canv.setFillColor(NAVY)
    canv.drawString(40, PAGE_H - 58, title_text)

    # Divider line
    canv.setStrokeColor(GRAY_BORDER)
    canv.setLineWidth(1)
    canv.line(40, PAGE_H - 70, PAGE_W - 40, PAGE_H - 70)

    # Footer
    canv.setFont("Helvetica", 8)
    canv.setFillColor(TEXT_MUTED)
    canv.drawString(40, 20, "Sistem Seleksi CV Otomatis Berbasis AI/ML — Kasus Rekrutmen Manufaktur")
    canv.drawRightString(PAGE_W - 40, 20, "Slide Confidential — HR & Recruitment Analytics")
    canv.restoreState()


def draw_card(canv, x, y, w, h, bg_color=GRAY_BG, border_color=GRAY_BORDER, corner_radius=6):
    canv.saveState()
    canv.setFillColor(bg_color)
    if border_color:
        canv.setStrokeColor(border_color)
        canv.setLineWidth(1)
    else:
        canv.setStrokeColor(bg_color)
    canv.roundRect(x, y, w, h, corner_radius, stroke=1 if border_color else 0, fill=1)
    canv.restoreState()


def generate_pdf(output_filename="Presentasi_AI_CV_Screening_Specialist.pdf"):
    c = canvas.Canvas(output_filename, pagesize=landscape(A4))

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Decorative bar
    c.setFillColor(TEAL)
    c.rect(50, PAGE_H - 140, 60, 6, stroke=0, fill=1)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(WHITE)
    c.drawString(50, PAGE_H - 190, "Sistem Otomatisasi Seleksi CV Berbasis AI/ML")

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(TEAL)
    c.drawString(50, PAGE_H - 225, "Akselerasi Rekrutmen Cepat, Skalabel, & Objektif untuk Pertumbuhan Industri Manufaktur")

    # Metadata card
    draw_card(c, 50, 80, PAGE_W - 100, 100, bg_color=DARK_BLUE, border_color=None)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(WHITE)
    c.drawString(75, 145, "Peran: AI / ML Specialist  |  Studi Kasus: Rekrutmen Massal Industri Manufaktur")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(75, 122, "Solusi: Two-Stage Hybrid Matching (Semantic Embedding + Qualitative LLM Reasoning) & Mitigasi Bias PII")
    c.drawString(75, 102, "Teknologi: Gemini 2.0 Flash, text-embedding-004, Streamlit, Blind Screening Framework, UU PDP Compliance")
    c.showPage()

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    draw_header(c, "Latar Belakang & Masalah: Rekrutmen Skala Manufaktur")
    cards = [
        ("Tantangan 1: Volume & Kecepatan", "Pertumbuhan Cepat Pabrik", [
            "Ekspansi lini pabrik menuntut ratusan karyawan dalam hitungan minggu.",
            "Ribuan CV masuk serentak dari portal kerja (Jobstreet, LinkedIn, Glints).",
            "Screening manual (3-5 menit/CV) memakan 60-80 jam kerja HR per batch."
        ], AMBER),
        ("Tantangan 2: Biaya & Bottleneck", "Inefisiensi Operasional", [
            "Biaya lembur tim HR membengkak tajam.",
            "Siklus Time-to-Hire lama (21-30 hari) memperlambat operasional lantai pabrik.",
            "Keterlambatan pemenuhan posisi inti berisiko downtime lini produksi."
        ], RED),
        ("Tantangan 3: Subjektivitas & Bias", "Kerapuhan Seleksi Manual", [
            "Fatigue Bias: Akurasi recruiter merosot drastis setelah memeriksa puluhan resume.",
            "Unconscious Bias: Penilaian terdistorsi foto, gender, almamater, atau format layout CV.",
            "Kurangnya auditabilitas: Alasan penolakan/penerimaan tidak terdokumentasi rapi."
        ], TEAL)
    ]

    card_w = (PAGE_W - 80 - 40) / 3
    card_h = 420
    for i, (head, sub, bullets, color) in enumerate(cards):
        x = 40 + i * (card_w + 20)
        y = 60
        draw_card(c, x, y, card_w, card_h)
        c.setFillColor(color)
        c.rect(x, y + card_h - 6, card_w, 6, stroke=0, fill=1)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(x + 15, y + card_h - 35, head)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(color)
        c.drawString(x + 15, y + card_h - 55, sub)

        cur_y = y + card_h - 85
        for b in bullets:
            c.setFont("Helvetica", 9)
            c.setFillColor(DARK_BLUE)
            # Wrap bullet
            words = b.split()
            line = "• "
            for w in words:
                if c.stringWidth(line + " " + w, "Helvetica", 9) < card_w - 30:
                    line += " " + w
                else:
                    c.drawString(x + 15, cur_y, line)
                    cur_y -= 14
                    line = "  " + w
            c.drawString(x + 15, cur_y, line)
            cur_y -= 22
    c.showPage()

    # =========================================================================
    # SLIDE 3: Architecture
    # =========================================================================
    draw_header(c, "Arsitektur Solusi End-to-End (4 Lapisan Sistem)")
    layers = [
        ("Layer 1: Ingestion", "Automasi Multi-Portal", [
            "Partner API / Webhook (LinkedIn, Jobstreet)",
            "Konektor ATS (Workday, SuccessFactors)",
            "Recruitment Email Watcher (IMAP parse)",
            "Cloud Storage Bucket (Raw PDF/DOCX)"
        ], DARK_TEAL),
        ("Layer 2: Preprocess", "Parsing & Blind Sanitasi", [
            "Multi-format Parser (pdfplumber & docx)",
            "LLM Structured Extraction (JSON Schema)",
            "Strict PII Isolation (Nama, Kontak, Usia)",
            "Penyimpanan Identitas Terenkripsi Terpisah"
        ], TEAL),
        ("Layer 3: AI Engine", "Two-Stage Screening", [
            "Stage 1: Hard Filter (Exp, Skill, Pendidikan)",
            "Non-lolos langsung dieliminasi (Hemat 70%)",
            "Stage 2A: Semantic Vector Match (35%)",
            "Stage 2B: Qualitative Reasoning (65%)"
        ], GREEN),
        ("Layer 4: Decision", "Dashboard & Audit Trail", [
            "Peringkat Kandidat Terurut (Skor 0-100)",
            "Explainable AI: Strengths & Gaps Detail",
            "Human-in-the-Loop: Reviewer Final Decision",
            "Export CSV & One-Click Interview Invitation"
        ], NAVY)
    ]

    card_w4 = (PAGE_W - 80 - 60) / 4
    for i, (title, sub, items, color) in enumerate(layers):
        x = 40 + i * (card_w4 + 20)
        y = 60
        draw_card(c, x, y, card_w4, card_h)
        c.setFillColor(color)
        c.rect(x, y + card_h - 6, card_w4, 6, stroke=0, fill=1)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(x + 12, y + card_h - 35, title)

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(color)
        c.drawString(x + 12, y + card_h - 52, sub)

        cur_y = y + card_h - 80
        for it in items:
            c.setFont("Helvetica", 8.5)
            c.setFillColor(DARK_BLUE)
            words = it.split()
            line = "✔ "
            for w in words:
                if c.stringWidth(line + " " + w, "Helvetica", 8.5) < card_w4 - 24:
                    line += " " + w
                else:
                    c.drawString(x + 12, cur_y, line)
                    cur_y -= 13
                    line = "  " + w
            c.drawString(x + 12, cur_y, line)
            cur_y -= 20
    c.showPage()

    # =========================================================================
    # SLIDE 4: Ingestion Strategy
    # =========================================================================
    draw_header(c, "Strategi Pengumpulan CV Otomatis dari Job Portal")

    draw_card(c, 40, PAGE_H - 165, PAGE_W - 80, 80, bg_color=LIGHT_TEAL, border_color=TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(DARK_TEAL)
    c.drawString(60, PAGE_H - 110, "Mengapa Enterprise Manufaktur Memilih Ingestion Resmi Dibanding Web Scraping?")
    c.setFont("Helvetica", 9)
    c.setFillColor(NAVY)
    c.drawString(60, PAGE_H - 130, "Web scraping melanggar Terms of Service (ToS) platform, rentan terblokir bot/CAPTCHA, dan berisiko melanggar UU PDP No. 27/2022.")
    c.drawString(60, PAGE_H - 145, "Pendekatan enterprise resmi menggunakan Webhook & Partner API yang legal, stabil, real-time, dan tersertifikasi aman.")

    methods = [
        ("1. Webhook & Partner API", [
            "Menggunakan LinkedIn Apply Connect API & Jobstreet Partner API.",
            "Event-Driven: Saat pelamar klik 'Apply', payload CV langsung dikirim ke webhook server.",
            "Transmisi data instan (< 3 detik per pelamar)."
        ]),
        ("2. Integrasi ATS Perusahaan", [
            "Menghubungkan pipeline ke Applicant Tracking System (Workday, SAP SuccessFactors).",
            "Menarik data pelamar per Job Posting ID secara asinkron.",
            "Mengembalikan hasil ranking & status shortlist ke ATS secara otomatis."
        ]),
        ("3. Dedicated Email Watcher", [
            "Background worker memonitor inbox recruitment@perusahaan.com via IMAP/OAuth.",
            "Otomatis mendownload lampiran CV (PDF/DOCX) dan memetakan subject email ke Job ID.",
            "Solusi tangguh untuk portal kerja lokal atau pelamar via referral."
        ])
    ]

    card_h_sub = 280
    for i, (title, points) in enumerate(methods):
        x = 40 + i * (card_w + 20)
        y = 60
        draw_card(c, x, y, card_w, card_h_sub)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(x + 15, y + card_h_sub - 35, title)

        cur_y = y + card_h_sub - 65
        for p in points:
            c.setFont("Helvetica", 9)
            c.setFillColor(DARK_BLUE)
            words = p.split()
            line = "• "
            for w in words:
                if c.stringWidth(line + " " + w, "Helvetica", 9) < card_w - 30:
                    line += " " + w
                else:
                    c.drawString(x + 15, cur_y, line)
                    cur_y -= 14
                    line = "  " + w
            c.drawString(x + 15, cur_y, line)
            cur_y -= 22
    c.showPage()

    # =========================================================================
    # SLIDE 5: n8n Workflow Orchestration
    # =========================================================================
    draw_header(c, "Orkestrasi Ingestion & Notifikasi Otomatis via n8n Workflow")

    # Banner Ringkasan n8n
    draw_card(c, 40, PAGE_H - 165, PAGE_W - 80, 80, bg_color=LIGHT_TEAL, border_color=TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(DARK_TEAL)
    c.drawString(60, PAGE_H - 110, "Mengapa Memilih n8n sebagai Event-Driven Orchestration Layer?")
    c.setFont("Helvetica", 9)
    c.setFillColor(NAVY)
    c.drawString(60, PAGE_H - 130, "n8n berperan sebagai 'glue code' enterprise yang menghubungkan portal kerja luar dengan AI Screening Engine internal kita")
    c.drawString(60, PAGE_H - 145, "secara aman, instan (< 5 detik), dan dapat di-host on-premise di server pabrik demi kepatuhan total UU PDP No. 27/2022.")

    col_w = (PAGE_W - 80 - 20) / 2
    col_h = 280

    # Kolom Kiri: Visualisasi Alur Node n8n
    draw_card(c, 40, 60, col_w, col_h)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_TEAL)
    c.drawString(55, 60 + col_h - 32, "Arsitektur Pipeline Node di n8n")

    flow_nodes = [
        ("1. Trigger Node:", "Webhook Job Portal (Jobstreet/LinkedIn) + IMAP Email Watcher."),
        ("2. Storage Node:", "Upload file CV mentah ke MinIO/S3 lokal pabrik (AES-256)."),
        ("3. AI Execution:", "HTTP POST memanggil Python Microservice (/api/v1/screen-cv)."),
        ("4. Decision Node:", "Switch Rule: Cek Skor >= 75 dan Lolos Syarat Wajib."),
        ("5. Dual Branching:", "Lolos: Auto-Invite Email + Slack HR Alert + Sync ATS. Non-Lolos: Talent Pool DB + Rejection Email Sopan.")
    ]

    cur_y = 60 + col_h - 58
    for n_title, n_desc in flow_nodes:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(55, cur_y, f"⚙ {n_title}")
        cur_y -= 13
        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK_BLUE)
        words = n_desc.split()
        line = "   "
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 8.5) < col_w - 30:
                line += " " + w
            else:
                c.drawString(55, cur_y, line)
                cur_y -= 12
                line = "   " + w
        c.drawString(55, cur_y, line)
        cur_y -= 16

    # Kolom Kanan: Keunggulan Strategis bagi Manufaktur
    draw_card(c, 40 + col_w + 20, 60, col_w, col_h)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(NAVY)
    c.drawString(40 + col_w + 35, 60 + col_h - 32, "Nilai Tambah untuk Operasional Manufaktur")

    strat_points = [
        ("Kepatuhan Privasi Data On-Premise:", "n8n di-self-host dalam VPC/intranet pabrik, menjamin data PII pelamar tidak terekspos ke cloud publik."),
        ("Separation of Concerns Bersih:", "n8n mengelola integrasi & notifikasi (low-code), sementara model AI dieksekusi terisolasi di modul Python (high-code)."),
        ("Respon Pelamar Super Cepat (< 5s):", "Kandidat unggulan langsung menerima tautan jadwal interview otomatis, mencegah kehilangan talenta terbaik ke kompetitor."),
        ("File Blueprint Siap Produksi:", "Artifact n8n_cv_screening_workflow.json telah disediakan di repositori, siap langsung di-import ke server n8n pabrik.")
    ]

    cur_y = 60 + col_h - 58
    for s_head, s_body in strat_points:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK_TEAL)
        c.drawString(40 + col_w + 35, cur_y, f"✔ {s_head}")
        cur_y -= 13
        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK_BLUE)
        words = s_body.split()
        line = "   "
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 8.5) < col_w - 30:
                line += " " + w
            else:
                c.drawString(40 + col_w + 35, cur_y, line)
                cur_y -= 12
                line = "   " + w
        c.drawString(40 + col_w + 35, cur_y, line)
        cur_y -= 16
    c.showPage()

    # =========================================================================
    # SLIDE 6: AI Model Rationale
    # =========================================================================
    draw_header(c, "Pemilihan Model & Algoritma AI/ML: Mengapa Pendekatan Hybrid?")
    approaches = [
        ("Model LLM Murni", "Generative Only", [
            "Kelebihan: Penalaran konteks sangat baik.",
            "Kelemahan: Biaya API token membengkak tajam pada ribuan CV.",
            "Non-deterministik: Ada variasi skor antar-run untuk kandidat yang sama.",
            "Latency tinggi: Tidak efisien untuk filtering awal ribuan pelamar."
        ], RED),
        ("Embedding Similarity", "Vector Only", [
            "Kelebihan: Cosine similarity sangat cepat (< 50ms) dan 100% konsisten.",
            "Kelemahan: Tidak mampu memberikan alasan naratif (explainability) bagi HR.",
            "Kelemahan: Rentan tertipu 'keyword stuffing' jika kandidat menumpuk kata kunci tanpa pengalaman nyata."
        ], AMBER),
        ("Pendekatan Hybrid Kami", "Best of Both Worlds", [
            "Tahap 1 Hard Filter: Eliminasi deterministik syarat mutlak (Exp, Skill, Edukasi).",
            "Tahap 2A Embedding (35%): text-embedding-004 memberikan baseline kesamaan semantik.",
            "Tahap 2B LLM Reasoning (65%): gemini-2.0-flash menganalisis kekuatan, kesenjangan, & narasi pertimbangan.",
            "Hasil: Hemat biaya 75%, bebas variasi acak, dan menyediakan audit trail transparan."
        ], GREEN)
    ]

    for i, (title, sub, points, color) in enumerate(approaches):
        x = 40 + i * (card_w + 20)
        y = 60
        draw_card(c, x, y, card_w, card_h)
        c.setFillColor(color)
        c.rect(x, y + card_h - 6, card_w, 6, stroke=0, fill=1)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(x + 15, y + card_h - 35, title)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(color)
        c.drawString(x + 15, y + card_h - 52, sub)

        cur_y = y + card_h - 80
        for p in points:
            c.setFont("Helvetica", 8.5)
            c.setFillColor(DARK_BLUE)
            words = p.split()
            line = "✔ " if color == GREEN else "• "
            for w in words:
                if c.stringWidth(line + " " + w, "Helvetica", 8.5) < card_w - 30:
                    line += " " + w
                else:
                    c.drawString(x + 15, cur_y, line)
                    cur_y -= 13
                    line = "  " + w
            c.drawString(x + 15, cur_y, line)
            cur_y -= 18
    c.showPage()

    # =========================================================================
    # SLIDE 6: Two-Stage Funnel
    # =========================================================================
    draw_header(c, "Two-Stage Funnel: Efisiensi Biaya & Standardisasi Skor")
    half_w = (PAGE_W - 80 - 20) / 2
    draw_card(c, 40, 60, half_w, card_h)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_TEAL)
    c.drawString(60, 60 + card_h - 40, "Stage 1: Gatekeeper (Hard Filter)")

    s1_text = [
        "Fungsi: Memvalidasi kriteria mutlak yang tidak bisa dikompromikan.",
        "Komponen Evaluasi:",
        "  1. Minimal Pengalaman Kerja (cth: minimal 2 tahun relevan).",
        "  2. Penguasaan Skill Wajib (normalized token & boundary matching).",
        "  3. Jenjang Pendidikan Formal (SMK/SMA < D3 < S1 < S2).",
        "Efisiensi: Pelamar yang tidak memenuhi syarat langsung ditandai 'Gagal Syarat Wajib'.",
        "Dampak Finansial: Memotong 60-75% beban pemrosesan LLM -> Menghemat kuota API secara masif."
    ]
    cur_y = 60 + card_h - 75
    for t in s1_text:
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DARK_BLUE)
        words = t.split()
        line = ""
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 9.5) < half_w - 40:
                line += " " + w
            else:
                c.drawString(60, cur_y, line.strip())
                cur_y -= 15
                line = "  " + w
        c.drawString(60, cur_y, line.strip())
        cur_y -= 22

    draw_card(c, 40 + half_w + 20, 60, half_w, card_h)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(NAVY)
    c.drawString(40 + half_w + 40, 60 + card_h - 40, "Stage 2: Hybrid Scoring & Ranking")

    s2_text = [
        "Fungsi: Menilai kecocokan mendalam bagi kandidat yang lolos Stage 1.",
        "Formula Hybrid Scoring:",
        "  Skor Akhir = (Embedding Score × 35%) + (LLM Score × 65%)",
        "Bobot Embedding (35%):",
        "  Menghitung cosine similarity vektor kandidat vs JD menggunakan text-embedding-004.",
        "Bobot LLM Reasoning (65%):",
        "  Evaluasi kontekstual model Gemini Flash pada relevansi portofolio kerja & kedalaman teknis.",
        "Output Terstruktur: Skor 0-100 + Poin Kekuatan + Poin Kesenjangan + Narasi Keputusan."
    ]
    cur_y = 60 + card_h - 75
    for t in s2_text:
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DARK_BLUE)
        words = t.split()
        line = ""
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 9.5) < half_w - 40:
                line += " " + w
            else:
                c.drawString(40 + half_w + 40, cur_y, line.strip())
                cur_y -= 15
                line = "  " + w
        c.drawString(40 + half_w + 40, cur_y, line.strip())
        cur_y -= 22
    c.showPage()

    # =========================================================================
    # SLIDE 7: Ethics & Privacy
    # =========================================================================
    draw_header(c, "Pertimbangan Etika, Mitigasi Bias, & Kepatuhan Privasi Data")
    ethics = [
        ("1. Blind Auditing Framework", "Pemisahan PII dari Engine AI", [
            "Identitas kandidat (Nama, Gender, Usia, Agama, Foto, Status Pernikahan, No. HP, Email) dipisahkan total sebelum scoring.",
            "Payload yang dikirim ke LLM murni hanya memuat kompetensi kerja, pengalaman terstruktur, dan sertifikasi.",
            "Identitas digabungkan kembali HANYA pada tahap pelaporan akhir bagi recruiter."
        ]),
        ("2. Kepatuhan Regulasi UU PDP", "UU No. 27 Tahun 2022", [
            "Data Minimization: Sistem hanya memproses data yang relevan dengan kualifikasi kerja.",
            "Storage Limitation: File CV sementara di-purge otomatis setelah parsing selesai.",
            "Enkripsi: Data tersimpan dienkripsi in-transit (TLS 1.3) dan at-rest (AES-256) untuk mencegah kebocoran data pelamar."
        ]),
        ("3. Explainable AI & Auditability", "Transparansi Keputusan Anti-Blackbox", [
            "Setiap keputusan didukung bukti tertulis: Strengths (Kekuatan) dan Gaps (Kekurangan).",
            "Recruiter dapat membaca narasi pertimbangan AI sebelum memutuskan mengundang wawancara.",
            "Menyediakan mekanisme review kedua (Human Review) bagi kandidat dengan status marginal."
        ])
    ]

    for i, (title, sub, points) in enumerate(ethics):
        x = 40 + i * (card_w + 20)
        y = 60
        draw_card(c, x, y, card_w, card_h)
        c.setFillColor(TEAL)
        c.rect(x, y + card_h - 6, card_w, 6, stroke=0, fill=1)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(x + 15, y + card_h - 35, title)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DARK_TEAL)
        c.drawString(x + 15, y + card_h - 52, sub)

        cur_y = y + card_h - 80
        for p in points:
            c.setFont("Helvetica", 9)
            c.setFillColor(DARK_BLUE)
            words = p.split()
            line = "• "
            for w in words:
                if c.stringWidth(line + " " + w, "Helvetica", 9) < card_w - 30:
                    line += " " + w
                else:
                    c.drawString(x + 15, cur_y, line)
                    cur_y -= 14
                    line = "  " + w
            c.drawString(x + 15, cur_y, line)
            cur_y -= 22
    c.showPage()

    # =========================================================================
    # SLIDE 8: Scalability
    # =========================================================================
    draw_header(c, "Kelayakan Implementasi & Skalabilitas di Pabrik Manufaktur")
    draw_card(c, 40, 60, half_w, card_h)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(NAVY)
    c.drawString(60, 60 + card_h - 40, "Arsitektur Produksi Skala Enterprise")

    p1_items = [
        "Asynchronous Job Queue: RabbitMQ / Celery memproses ribuan CV secara batch tanpa server timeout.",
        "Microservices Architecture: Parser service, embedding worker, dan LLM worker berjalan terpisah dalam container Docker.",
        "Vector Database Terdistribusi: Qdrant / Milvus / PGVector untuk jutaan profil bakat & pencarian semantik instan.",
        "High-Throughput Concurrency: Mampu memproses > 10.000 CV per jam saat rekrutmen massal pabrik baru."
    ]
    cur_y = 60 + card_h - 75
    for item in p1_items:
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DARK_BLUE)
        words = item.split()
        line = "✔ "
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 9.5) < half_w - 40:
                line += " " + w
            else:
                c.drawString(60, cur_y, line.strip())
                cur_y -= 15
                line = "  " + w
        c.drawString(60, cur_y, line.strip())
        cur_y -= 25

    draw_card(c, 40 + half_w + 20, 60, half_w, card_h)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_TEAL)
    c.drawString(40 + half_w + 40, 60 + card_h - 40, "Human-in-the-Loop & Adaptabilitas Pabrik")

    p2_items = [
        "AI Sebagai Co-Pilot Cerdas: Sistem menyaring dan menyusun peringkat; keputusan final tetap di tangan Recruiter & Line Manager.",
        "Dukungan Ragam Posisi Manufaktur: Fleksibel untuk Plant CAD Drafter, Automation Engineer, PLC Specialist, Operator, dan Staff QC.",
        "Integrasi HRIS & Presensi: REST API mudah disambungkan ke HRIS internal pabrik untuk jadwal interview dan onboarding otomatis."
    ]
    cur_y = 60 + card_h - 75
    for item in p2_items:
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DARK_BLUE)
        words = item.split()
        line = "✔ "
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 9.5) < half_w - 40:
                line += " " + w
            else:
                c.drawString(40 + half_w + 40, cur_y, line.strip())
                cur_y -= 15
                line = "  " + w
        c.drawString(40 + half_w + 40, cur_y, line.strip())
        cur_y -= 25
    c.showPage()

    # =========================================================================
    # SLIDE 9: ROI
    # =========================================================================
    draw_header(c, "Analisis Efisiensi, Reduksi Biaya, & Dampak Bisnis (ROI)")
    metrics = [
        ("95%", "Efisiensi Waktu", "Screening 1.000 CV turun dari 50 jam menjadi < 15 menit otomatis."),
        ("75%", "Penghematan Biaya", "Mengurangi lembur recruiter & memotong biaya agensi pihak ketiga."),
        ("3 Hari", "Time-to-Hire", "Memangkas siklus rekrutmen dari 25 hari menjadi 3-5 hari siap wawancara."),
        ("100%", "Objektivitas", "Standardisasi evaluasi bebas bias lelah shift kerja & subjektivitas manusia.")
    ]

    metric_w = (PAGE_W - 80 - 60) / 4
    for i, (val, label, detail) in enumerate(metrics):
        x = 40 + i * (metric_w + 20)
        draw_card(c, x, PAGE_H - 240, metric_w, 150, bg_color=LIGHT_TEAL, border_color=TEAL)
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(DARK_TEAL)
        c.drawString(x + 15, PAGE_H - 130, val)

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(NAVY)
        c.drawString(x + 15, PAGE_H - 152, label)

        c.setFont("Helvetica", 8.5)
        c.setFillColor(TEXT_MUTED)
        words = detail.split()
        line = ""
        cur_y = PAGE_H - 175
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 8.5) < metric_w - 30:
                line += " " + w
            else:
                c.drawString(x + 15, cur_y, line.strip())
                cur_y -= 12
                line = " " + w
        c.drawString(x + 15, cur_y, line.strip())

    # Comparison summary card
    draw_card(c, 40, 60, PAGE_W - 80, 190)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(NAVY)
    c.drawString(60, 225, "Perbandingan Sebelum vs Sesudah Implementasi AI CV Screening:")

    rows = [
        ("Kapasitas Screening", "Maksimal 150-200 CV per hari per recruiter", "Ribuan CV diproses secara simultan dalam hitungan menit"),
        ("Risiko Bias Manusia", "Tinggi (terpengaruh foto, gender, nama, almamater)", "Nol pada tahap AI (Blind Screening berbasis kompetensi)"),
        ("Auditability & Keterbukaan", "Subjektif, tidak ada rekaman alasan penolakan detail", "100% transparan dengan Strengths, Gaps, dan Reasoning"),
        ("Dampak Pabrik", "Kekurangan operator & drafter memperlambat shift", "Pemenuhan man-power tepat waktu, zero production downtime")
    ]
    cur_y = 195
    for param, sebelum, sesudah in rows:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK_BLUE)
        c.drawString(60, cur_y, f"• {param}:")
        c.setFont("Helvetica", 8.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(180, cur_y, f"{sebelum}  ➔  {sesudah}")
        cur_y -= 28
    c.showPage()

    # =========================================================================
    # SLIDE 10: PoC Walkthrough & Results
    # =========================================================================
    draw_header(c, "Demonstrasi Proof of Concept (PoC) & Validasi Hasil Uji")
    draw_card(c, 40, 60, half_w, card_h)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(NAVY)
    c.drawString(60, 60 + card_h - 40, "Fitur Utama PoC (Streamlit + Gemini)")

    poc_list = [
        "1. Dynamic Job Presets: Template siap pakai Plant CAD Drafter & Backend Engineer Pabrik.",
        "2. One-Click Demo: Tombol pengujian langsung terhadap 5 CV sampel anonim bawaan.",
        "3. Multi-Format Ingestion: Ekstraksi teks otomatis dari file PDF & tabel DOCX.",
        "4. Strict Blind Isolation: PII disensor ketat sebelum proses scoring semantik.",
        "5. Metrik Dashboard: Total pelamar, rasio lolos hard filter, dan rata-rata skor.",
        "6. Audit Trail & CSV Export: Detail kekuatan/kelemahan per kandidat siap diunduh tim HR."
    ]
    cur_y = 60 + card_h - 75
    for feat in poc_list:
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK_BLUE)
        words = feat.split()
        line = "✔ "
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 9) < half_w - 40:
                line += " " + w
            else:
                c.drawString(60, cur_y, line.strip())
                cur_y -= 14
                line = "  " + w
        c.drawString(60, cur_y, line.strip())
        cur_y -= 20

    draw_card(c, 40 + half_w + 20, 60, half_w, card_h)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_TEAL)
    c.drawString(40 + half_w + 40, 60 + card_h - 40, "Hasil Uji Nyata Terhadap 5 Sample CV")

    results = [
        ("Rank #1: Dani (Skor: 87.4)", "Lolos (Exp: 3 thn, SMK & S1, AutoCAD & SketchUp)", "Rekomendasi Utama Wawancara", GREEN),
        ("Rank #2: INDRI (Skor: 86.3)", "Lolos (Exp: 2 thn, S1 & Master, AutoCAD & SketchUp)", "Rekomendasi Wawancara", GREEN),
        ("Rank #3: Bayu (Skor: 84.3)", "Lolos (Exp: 6 thn, S1 Arsitektur, AutoCAD & SketchUp)", "Rekomendasi Wawancara", GREEN),
        ("Rank #4: Permana Abadi (Skor: 76.6)", "Lolos (Exp: 3 thn, S1, AutoCAD & SketchUp)", "Rekomendasi Wawancara", GREEN),
        ("Rank #5: MOHAMAD (Skor: 0.0)", "Gagal Syarat Wajib (Skill SketchUp tidak ada)", "Tidak Lolos Filter Awal", RED)
    ]
    cur_y = 60 + card_h - 75
    for name, desc, status, col in results:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(col)
        c.drawString(40 + half_w + 40, cur_y, f"• {name}")
        cur_y -= 14
        c.setFont("Helvetica", 8.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(40 + half_w + 52, cur_y, f"{desc} ➔ {status}")
        cur_y -= 22
    c.showPage()

    # =========================================================================
    # SLIDE 11: Implementation Roadmap
    # =========================================================================
    draw_header(c, "Roadmap Implementasi Produksi (3 Tahap Eksekusi)")
    phases = [
        ("Fase 1: Pilot & Validasi", "Bulan 1 (Setup & Benchmark)", [
            "Deployment PoC ke lingkungan internal staging.",
            "Benchmarking skor AI terhadap 200 keputusan manual historis tim HR.",
            "Fine-tuning bobot hybrid berdasarkan karakteristik peran manufaktur.",
            "Pelatihan pengoperasian bagi tim rekruter pabrik."
        ], DARK_TEAL),
        ("Fase 2: Integrasi Sistem", "Bulan 2 - 3 (Automation)", [
            "Integrasi Webhook resmi dengan Jobstreet & LinkedIn.",
            "Koneksi API dua arah ke HRIS / ATS eksisting perusahaan.",
            "Implementasi Asynchronous Queue (Celery/RabbitMQ) untuk throughput tinggi.",
            "Penerapan audit keamanan data & kepatuhan UU PDP."
        ], TEAL),
        ("Fase 3: Skalabilitas Penuh", "Bulan 4+ (Enterprise Scale)", [
            "Rollout penuh ke seluruh departemen pabrik & plant cabang.",
            "Penambahan modul Vision OCR untuk CV scan non-teks.",
            "Modul Automated Interview Scheduling terintegrasi kalender HR.",
            "Continuous Learning & evaluasi bias berkala (Quarterly Audit)."
        ], GREEN)
    ]

    for i, (title, sub, points, color) in enumerate(phases):
        x = 40 + i * (card_w + 20)
        y = 60
        draw_card(c, x, y, card_w, card_h)
        c.setFillColor(color)
        c.rect(x, y + card_h - 6, card_w, 6, stroke=0, fill=1)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY)
        c.drawString(x + 15, y + card_h - 35, title)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(color)
        c.drawString(x + 15, y + card_h - 52, sub)

        cur_y = y + card_h - 80
        for p in points:
            c.setFont("Helvetica", 9)
            c.setFillColor(DARK_BLUE)
            words = p.split()
            line = "• "
            for w in words:
                if c.stringWidth(line + " " + w, "Helvetica", 9) < card_w - 30:
                    line += " " + w
                else:
                    c.drawString(x + 15, cur_y, line)
                    cur_y -= 14
                    line = "  " + w
            c.drawString(x + 15, cur_y, line)
            cur_y -= 22
    c.showPage()

    # =========================================================================
    # SLIDE 12: Conclusion (Dark Executive Theme)
    # =========================================================================
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    c.setFillColor(TEAL)
    c.rect(50, PAGE_H - 100, 60, 6, stroke=0, fill=1)

    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(WHITE)
    c.drawString(50, PAGE_H - 140, "Kesimpulan & Nilai Tambah Strategis AI Specialist")

    draw_card(c, 50, 60, PAGE_W - 100, 360, bg_color=DARK_BLUE, border_color=None)

    concl_points = [
        ("Efisiensi & Akselerasi Rekrutmen:", "Sistem otomatisasi Two-Stage Hybrid AI memangkas 95% waktu screening, memastikan pembukaan lini manufaktur didukung tenaga kerja tepat waktu."),
        ("Penghematan Biaya Finansial:", "Kombinasi Hard Filter gatekeeper dan model hybrid menjaga biaya API tetap minimum (turun 70-75%) dibanding solusi LLM murni."),
        ("Keadilan & Kepatuhan Regulasi:", "Pemisahan PII (Blind Auditing) dan penjelasan transparan (XAI) menjamin seleksi 100% objektif, etis, serta patuh penuh pada UU PDP No. 27/2022."),
        ("Kesiapan Produksi (Enterprise-Ready):", "Solusi dirancang modular dan terukur, siap bertransisi mulus dari Proof of Concept menjadi infrastruktur rekrutmen permanen perusahaan manufaktur.")
    ]

    cur_y = 360
    for head, desc in concl_points:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(TEAL)
        c.drawString(75, cur_y, f"✔  {head}")
        cur_y -= 18
        c.setFont("Helvetica", 10)
        c.setFillColor(WHITE)
        words = desc.split()
        line = ""
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 10) < PAGE_W - 150:
                line += " " + w
            else:
                c.drawString(90, cur_y, line.strip())
                cur_y -= 15
                line = " " + w
        c.drawString(90, cur_y, line.strip())
        cur_y -= 25

    c.save()
    print(f"PDF Presentation generated successfully at: {output_filename}")


if __name__ == "__main__":
    generate_pdf()
