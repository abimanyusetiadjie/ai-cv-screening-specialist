"""
make_deck.py
Generator Presentasi Profesional untuk Technical Assessment: AI Specialist
Topik: Otomatisasi Seleksi CV Berbasis AI/ML di Industri Manufaktur
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


def generate_deck(output_filename="Presentasi_AI_CV_Screening_Specialist.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palet Warna Korporat Modern
    NAVY = RGBColor(15, 23, 42)           # #0F172A (Primary Dark)
    DARK_BLUE = RGBColor(30, 41, 59)      # #1E293B (Card Dark)
    TEAL = RGBColor(14, 165, 233)         # #0EA5E9 (Accent Vibrant)
    LIGHT_TEAL = RGBColor(224, 242, 254)  # #E0F2FE (Highlight Light)
    DARK_TEAL = RGBColor(3, 105, 161)     # #0369A1 (Brand Accent)
    WHITE = RGBColor(255, 255, 255)
    GRAY_BG = RGBColor(248, 250, 252)     # #F8FAFC
    GRAY_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    GREEN_ACCENT = RGBColor(16, 185, 129) # #10B981
    AMBER_ACCENT = RGBColor(245, 158, 11) # #F59E0B
    RED_ACCENT = RGBColor(239, 68, 68)    # #EF4444

    def add_bg(slide, color=WHITE):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="TECHNICAL ASSESSMENT: AI SPECIALIST"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = TEAL

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.7), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = GRAY_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=GRAY_BG, border_color=GRAY_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, NAVY)

    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(0.8), Inches(0.08))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = TEAL
    bar1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.3), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Sistem Otomatisasi Seleksi CV Berbasis AI/ML"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Akselerasi Rekrutmen Cepat, Skalabel, & Objektif untuk Pertumbuhan Industri Manufaktur"
    p2.font.size = Pt(20)
    p2.font.color.rgb = TEAL
    p2.space_before = Pt(14)

    add_card(s1, Inches(1.0), Inches(5.0), Inches(11.3), Inches(1.5), bg_color=DARK_BLUE, border_color=None)
    mb1 = s1.shapes.add_textbox(Inches(1.3), Inches(5.15), Inches(10.7), Inches(1.2))
    tf_m = mb1.text_frame
    pm1 = tf_m.paragraphs[0]
    pm1.text = "Peran: AI / ML Specialist  |  Studi Kasus: Rekrutmen Massal Perusahaan Manufaktur"
    pm1.font.size = Pt(13)
    pm1.font.bold = True
    pm1.font.color.rgb = WHITE

    pm2 = tf_m.add_paragraph()
    pm2.text = "Solusi: Two-Stage Hybrid Matching (Semantic Embedding + Qualitative LLM Reasoning) & Mitigasi Bias PII"
    pm2.font.size = Pt(12)
    pm2.font.color.rgb = RGBColor(148, 163, 184)
    pm2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 2: Problem Statement & Manufacturing Context
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Latar Belakang & Masalah: Rekrutmen Skala Manufaktur")

    cards_s2 = [
        ("Tantangan 1: Volume & Kecepatan", "Pertumbuhan Cepat Pabrik", [
            "Ekspansi lini pabrik menuntut ratusan karyawan dalam hitungan minggu.",
            "Ribuan CV masuk serentak dari portal kerja (Jobstreet, LinkedIn, Glints).",
            "Screening manual (3-5 menit/CV) memakan 60-80 jam kerja HR per batch."
        ], AMBER_ACCENT),
        ("Tantangan 2: Biaya & Bottleneck", "Inefisiensi Operasional", [
            "Biaya lembur tim HR membengkak tajam.",
            "Siklus Time-to-Hire lama (21-30 hari) memperlambat operasional lantai pabrik.",
            "Keterlambatan pemenuhan posisi inti (Drafter, Operator, Engineer) berisiko downtime produksi."
        ], RED_ACCENT),
        ("Tantangan 3: Subjektivitas & Bias", "Kerapuhan Seleksi Manual", [
            "Fatigue Bias: Akurasi recruiter merosot drastis setelah memeriksa puluhan resume.",
            "Unconscious Bias: Penilaian terdistorsi foto, gender, almamater, atau format layout CV.",
            "Kurangnya auditabilitas: Alasan penolakan/penerimaan tidak terdokumentasi rapi."
        ], TEAL)
    ]

    for i, (head, sub, bullets, color) in enumerate(cards_s2):
        x = Inches(0.8 + (i * 4.0))
        add_card(s2, x, Inches(1.8), Inches(3.7), Inches(5.0))
        top_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()

        cbox = s2.shapes.add_textbox(x + Inches(0.25), Inches(2.1), Inches(3.2), Inches(4.5))
        tf = cbox.text_frame
        tf.word_wrap = True
        ph = tf.paragraphs[0]
        ph.text = head
        ph.font.size = Pt(15)
        ph.font.bold = True
        ph.font.color.rgb = NAVY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(11.5)
        ps.font.bold = True
        ps.font.color.rgb = color
        ps.space_after = Pt(12)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_MUTED
            pb.space_before = Pt(6)

    # =========================================================================
    # SLIDE 3: End-to-End System Architecture (4 Pillars)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Arsitektur Solusi End-to-End (4 Lapisan Sistem)")

    layers = [
        ("Layer 1: Ingestion", "Automasi Multi-Portal", [
            "Partner API / Webhook (LinkedIn, Jobstreet, Glints)",
            "Konektor ATS (Workday, SuccessFactors, Greenhouse)",
            "Recruitment Email Watcher (IMAP auto-parse)",
            "Cloud Storage Bucket (Raw PDF/DOCX)"
        ], DARK_TEAL),
        ("Layer 2: Preprocessing", "Parsing & Blind Sanitasi", [
            "Multi-format Parser (pdfplumber & docx)",
            "LLM Structured Extraction (JSON Schema)",
            "Strict PII Isolation (Nama, Kontak, Usia, Gender)",
            "Penyimpanan Identitas Terenkripsi Terpisah"
        ], TEAL),
        ("Layer 3: AI/ML Engine", "Two-Stage Screening", [
            "Stage 1: Hard Filter (Pengalaman, Skill, Pendidikan)",
            "Non-lolos langsung dieliminasi (Hemat 70% Komputasi)",
            "Stage 2A: Semantic Vector Match (text-embedding-004)",
            "Stage 2B: Qualitative Reasoning (gemini-2.0-flash)"
        ], GREEN_ACCENT),
        ("Layer 4: HR Decision", "Dashboard & Audit Trail", [
            "Peringkat Kandidat Terurut (Skor 0-100)",
            "Explainable AI: Strengths, Gaps, & Narasi Alasan",
            "Human-in-the-Loop: Reviewer Final Decision",
            "Export CSV & One-Click Interview Invitation"
        ], NAVY)
    ]

    for i, (title, sub, items, color) in enumerate(layers):
        x = Inches(0.8 + (i * 2.95))
        add_card(s3, x, Inches(1.8), Inches(2.85), Inches(5.0))
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.85), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        box = s3.shapes.add_textbox(x + Inches(0.2), Inches(2.1), Inches(2.45), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = color
        p_s.space_after = Pt(14)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"✔  {it}"
            p_it.font.size = Pt(10.5)
            p_it.font.color.rgb = TEXT_MUTED
            p_it.space_before = Pt(8)

    # =========================================================================
    # SLIDE 4: Ingestion Strategy from Job Portals (Jawaban Soal No. 1)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Strategi Pengumpulan CV Otomatis dari Job Portal")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(11.7), Inches(1.15), bg_color=LIGHT_TEAL, border_color=TEAL)
    bb4 = s4.shapes.add_textbox(Inches(1.0), Inches(1.78), Inches(11.3), Inches(1.0))
    tf_b = bb4.text_frame
    tf_b.word_wrap = True
    pb1 = tf_b.paragraphs[0]
    pb1.text = "Mengapa Enterprise Manufaktur Memilih Ingestion Resmi Dibanding Web Scraping?"
    pb1.font.size = Pt(13)
    pb1.font.bold = True
    pb1.font.color.rgb = DARK_TEAL
    pb2 = tf_b.add_paragraph()
    pb2.text = "Web scraping melanggar Terms of Service portal kerja, rentan terblokir bot/CAPTCHA, dan bertentangan dengan UU PDP No. 27/2022. Solusi industri manufaktur modern menggunakan integrasi resmi (Webhook, Partner API, & ATS Connector) yang legal, stabil, real-time, dan aman."
    pb2.font.size = Pt(11)
    pb2.font.color.rgb = NAVY

    methods = [
        ("1. Webhook & Partner API", [
            "Menggunakan LinkedIn Apply Connect API & Jobstreet Partner API.",
            "Event-Driven: Setiap ada pelamar baru, portal kerja mengirim event webhook berisi file PDF & metadata kandidat.",
            "Transmisi data instan (< 3 detik per pelamar)."
        ]),
        ("2. Integrasi ATS Perusahaan", [
            "Menghubungkan pipeline ke Applicant Tracking System (Workday, SAP SuccessFactors, Greenhouse).",
            "Menarik data pelamar per Job Posting ID secara asinkron.",
            "Mengembalikan hasil ranking & status shortlist ke ATS secara otomatis."
        ]),
        ("3. Dedicated Email Watcher", [
            "Background worker memonitor inbox recruitment@perusahaan.com via IMAP/OAuth.",
            "Otomatis mendownload lampiran CV (PDF/DOCX) dan memetakan subject email ke Job ID.",
            "Solusi tangguh untuk portal kerja lokal atau pelamar via referral."
        ])
    ]

    for i, (title, points) in enumerate(methods):
        x = Inches(0.8 + (i * 4.0))
        add_card(s4, x, Inches(3.05), Inches(3.7), Inches(3.8))
        box = s4.shapes.add_textbox(x + Inches(0.25), Inches(3.25), Inches(3.2), Inches(3.4))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(15)
        pt.font.bold = True
        pt.font.color.rgb = NAVY
        pt.space_after = Pt(10)

        for p in points:
            pp = tf.add_paragraph()
            pp.text = f"•  {p}"
            pp.font.size = Pt(11.5)
            pp.font.color.rgb = TEXT_MUTED
            pp.space_before = Pt(8)

    # =========================================================================
    # SLIDE 5: n8n Workflow Orchestration (Nilai Plus Ingestion & Routing)
    # =========================================================================
    s_n8n = prs.slides.add_slide(blank_layout)
    add_bg(s_n8n)
    add_header(s_n8n, "Orkestrasi Ingestion & Notifikasi Otomatis via n8n Workflow")

    # Banner Ringkasan n8n
    add_card(s_n8n, Inches(0.8), Inches(1.68), Inches(11.7), Inches(1.1), bg_color=LIGHT_TEAL, border_color=TEAL)
    bb_n = s_n8n.shapes.add_textbox(Inches(1.0), Inches(1.72), Inches(11.3), Inches(0.95))
    tf_bn = bb_n.text_frame
    tf_bn.word_wrap = True
    pbn1 = tf_bn.paragraphs[0]
    pbn1.text = "Mengapa Memilih n8n sebagai Event-Driven Orchestration Layer?"
    pbn1.font.size = Pt(13)
    pbn1.font.bold = True
    pbn1.font.color.rgb = DARK_TEAL
    pbn2 = tf_bn.add_paragraph()
    pbn2.text = "n8n berperan sebagai 'glue code' enterprise yang menghubungkan portal kerja luar dengan AI Screening Engine internal kita secara aman, instan (< 5 detik), dan dapat di-host on-premise di server pabrik demi kepatuhan total UU PDP No. 27/2022."
    pbn2.font.size = Pt(11)
    pbn2.font.color.rgb = NAVY

    # Kolom Kiri: Visualisasi Alur Node n8n
    add_card(s_n8n, Inches(0.8), Inches(2.9), Inches(5.7), Inches(4.2))
    b_n1 = s_n8n.shapes.add_textbox(Inches(1.0), Inches(3.05), Inches(5.3), Inches(3.9))
    tf_n1 = b_n1.text_frame
    tf_n1.word_wrap = True
    pn1_title = tf_n1.paragraphs[0]
    pn1_title.text = "Arsitektur Pipeline 5-Node di n8n"
    pn1_title.font.size = Pt(15)
    pn1_title.font.bold = True
    pn1_title.font.color.rgb = DARK_TEAL
    pn1_title.space_after = Pt(8)

    flow_nodes = [
        ("1. Trigger Node:", "Webhook Job Portal (Jobstreet/LinkedIn) + IMAP Email Watcher."),
        ("2. Storage Node:", "Upload file CV mentah ke MinIO/S3 lokal pabrik (AES-256)."),
        ("3. AI Execution:", "HTTP Request POST memanggil Python Microservice (/api/v1/screen-cv)."),
        ("4. Decision Node:", "Switch Rule: Cek Skor >= 75 dan Lolos Syarat Wajib."),
        ("5. Dual Branching:", "Lolos ➔ Auto-Invite Email + Slack HR Alert + Sync ATS.\n    Tidak Lolos ➔ Arsipkan ke Talent Pool DB + Rejection Email Sopan.")
    ]
    for n_title, n_desc in flow_nodes:
        p_node = tf_n1.add_paragraph()
        p_node.text = f"⚙ {n_title} {n_desc}"
        p_node.font.size = Pt(10.5)
        p_node.font.color.rgb = TEXT_MUTED
        p_node.space_before = Pt(6)

    # Kolom Kanan: Keunggulan Strategis bagi Manufaktur
    add_card(s_n8n, Inches(6.8), Inches(2.9), Inches(5.7), Inches(4.2))
    b_n2 = s_n8n.shapes.add_textbox(Inches(7.0), Inches(3.05), Inches(5.3), Inches(3.9))
    tf_n2 = b_n2.text_frame
    tf_n2.word_wrap = True
    pn2_title = tf_n2.paragraphs[0]
    pn2_title.text = "Nilai Tambah untuk Operasional Manufaktur"
    pn2_title.font.size = Pt(15)
    pn2_title.font.bold = True
    pn2_title.font.color.rgb = NAVY
    pn2_title.space_after = Pt(8)

    strat_points = [
        ("Kepatuhan Privasi Data On-Premise:", "n8n di-self-host dalam VPC/intranet pabrik, menjamin data PII pelamar tidak terekspos ke cloud publik."),
        ("Separation of Concerns yang Bersih:", "n8n mengelola integrasi & notifikasi (low-code), sementara model AI dieksekusi terisolasi di modul Python (high-code)."),
        ("Kecepatan Respon Kandidat (< 5 Detik):", "Pelamar unggulan langsung menerima link jadwal wawancara sesaat setelah apply, mencegah kehilangan top talent ke kompetitor."),
        ("File Blueprint Siap Produksi:", "Artifact n8n_cv_screening_workflow.json telah disediakan di repositori, siap langsung di-import ke server pabrik.")
    ]
    for s_head, s_body in strat_points:
        p_strat = tf_n2.add_paragraph()
        p_strat.text = f"✔  {s_head} {s_body}"
        p_strat.font.size = Pt(10.5)
        p_strat.font.color.rgb = TEXT_MUTED
        p_strat.space_before = Pt(8)

    # =========================================================================
    # SLIDE 6: AI/ML Model Selection Rationale (Jawaban Soal No. 2 & 3)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Pemilihan Model & Algoritma AI/ML: Mengapa Pendekatan Hybrid?")

    approaches = [
        ("Model LLM Murni (Generative Only)", "Pintar, Namun Mahal & Fluktuatif", [
            "Kelebihan: Penalaran kualitatif sangat baik.",
            "Kelemahan: Biaya API token membengkak untuk volume ribuan CV.",
            "Non-deterministik: Ada fluktuasi skor antar-run untuk kandidat yang sama jika temperatur > 0.",
            "Latency tinggi: Tidak efisien untuk filtering awal ribuan pelamar."
        ], RED_ACCENT),
        ("Embedding Similarity Murni (Vector Only)", "Cepat & Murah, Tapi 'Buta' Narasi", [
            "Kelebihan: Cosine similarity sangat cepat (< 50ms) dan 100% konsisten.",
            "Kelemahan: Tidak mampu memberikan alasan naratif (explainability) bagi HR.",
            "Kelemahan: Rentan tertipu 'keyword stuffing' jika kandidat menumpuk kata kunci tanpa relevansi kerja nyata."
        ], AMBER_ACCENT),
        ("Pendekatan Hybrid Kami (Best of Both)", "Optimal: Akurat, Hemat, & Terang", [
            "Tahap 1 Hard Filter: Eliminasi deterministik syarat mutlak (Pengalaman, Skill, Pendidikan).",
            "Tahap 2A Embedding (35%): text-embedding-004 memberikan baseline kesamaan semantik yang konsisten.",
            "Tahap 2B LLM Reasoning (65%): gemini-2.0-flash menganalisis kekuatan, kekurangan, & narasi pertimbangan.",
            "Hasil: Hemat biaya 70-75%, bebas variasi acak, dan memberikan audit trail transparan bagi HR."
        ], GREEN_ACCENT)
    ]

    for i, (title, sub, points, color) in enumerate(approaches):
        x = Inches(0.8 + (i * 4.0))
        add_card(s5, x, Inches(1.8), Inches(3.7), Inches(5.0))
        top_bar = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()

        box = s5.shapes.add_textbox(x + Inches(0.25), Inches(2.1), Inches(3.2), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = NAVY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(11)
        ps.font.bold = True
        ps.font.color.rgb = color
        ps.space_after = Pt(10)

        for p in points:
            pp = tf.add_paragraph()
            pp.text = f"✔  {p}" if color == GREEN_ACCENT else f"•  {p}"
            pp.font.size = Pt(10.5)
            pp.font.color.rgb = NAVY if color == GREEN_ACCENT else TEXT_MUTED
            pp.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: Two-Stage Funnel & Scoring Methodology
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Two-Stage Funnel: Efisiensi Biaya & Standardisasi Skor")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b1_6 = s6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf1_6 = b1_6.text_frame
    tf1_6.word_wrap = True
    p1_6 = tf1_6.paragraphs[0]
    p1_6.text = "Stage 1: Gatekeeper (Hard Filter)"
    p1_6.font.size = Pt(16)
    p1_6.font.bold = True
    p1_6.font.color.rgb = DARK_TEAL
    p1_6.space_after = Pt(10)

    stage1_items = [
        "Fungsi: Memvalidasi kriteria mutlak yang tidak bisa dikompromikan.",
        "Komponen Evaluasi:",
        "  1. Minimal Pengalaman Kerja (cth: minimal 2 tahun relevan).",
        "  2. Penguasaan Skill Wajib (normalized token & boundary matching).",
        "  3. Jenjang Pendidikan Formal (SMK/SMA < D3 < S1 < S2).",
        "Efisiensi: Pelamar yang tidak memenuhi syarat langsung ditandai 'Gagal Syarat Wajib' beserta catatan kekurangannya.",
        "Dampak Finansial: Memotong 60-75% beban pemrosesan LLM -> Menjamin biaya API tetap terkendali pada volume besar."
    ]
    for item in stage1_items:
        pi = tf1_6.add_paragraph()
        pi.text = item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = TEXT_MUTED
        pi.space_before = Pt(6)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b2_6 = s6.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf2_6 = b2_6.text_frame
    tf2_6.word_wrap = True
    p2_6 = tf2_6.paragraphs[0]
    p2_6.text = "Stage 2: Hybrid Scoring & Ranking"
    p2_6.font.size = Pt(16)
    p2_6.font.bold = True
    p2_6.font.color.rgb = NAVY
    p2_6.space_after = Pt(10)

    stage2_items = [
        "Fungsi: Menilai kecocokan komprehensif bagi kandidat yang lolos Stage 1.",
        "Formula Hybrid Scoring:",
        "  Skor Akhir = (Embedding Score × 35%) + (LLM Score × 65%)",
        "Bobot Embedding (35%):",
        "  Menghitung cosine similarity vektor kandidat vs JD menggunakan model Google text-embedding-004.",
        "Bobot LLM Reasoning (65%):",
        "  Evaluasi mendalam model Gemini Flash pada relevansi portofolio kerja, variasi tanggung jawab, dan kedalaman teknis.",
        "Output Terstruktur: Skor 0-100 + Poin Kekuatan + Poin Kesenjangan + Narasi Keputusan untuk Tim Rekrutmen."
    ]
    for item in stage2_items:
        pi = tf2_6.add_paragraph()
        pi.text = item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = TEXT_MUTED
        pi.space_before = Pt(6)

    # =========================================================================
    # SLIDE 7: Ethics, Bias Mitigation & Data Privacy (UU PDP)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Pertimbangan Etika, Mitigasi Bias, & Kepatuhan Privasi Data")

    pillars_7 = [
        ("1. Blind Auditing Framework", "Pemisahan PII dari Engine AI", [
            "Identitas kandidat (Nama, Gender, Usia, Agama, Foto, Status Pernikahan, No. Telepon, Email) dipisahkan total sebelum scoring.",
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

    for i, (title, sub, points) in enumerate(pillars_7):
        x = Inches(0.8 + (i * 4.0))
        add_card(s7, x, Inches(1.8), Inches(3.7), Inches(5.0))
        top_bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = TEAL
        top_bar.line.fill.background()

        box = s7.shapes.add_textbox(x + Inches(0.25), Inches(2.1), Inches(3.2), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = NAVY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(11)
        ps.font.bold = True
        ps.font.color.rgb = DARK_TEAL
        ps.space_after = Pt(12)

        for p in points:
            pp = tf.add_paragraph()
            pp.text = f"•  {p}"
            pp.font.size = Pt(11)
            pp.font.color.rgb = TEXT_MUTED
            pp.space_before = Pt(8)

    # =========================================================================
    # SLIDE 8: Scalability & Manufacturing Implementation
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Kelayakan Implementasi & Skalabilitas di Pabrik Manufaktur")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b1_8 = s8.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf1_8 = b1_8.text_frame
    tf1_8.word_wrap = True
    p1_8 = tf1_8.paragraphs[0]
    p1_8.text = "Arsitektur Produksi Skala Enterprise"
    p1_8.font.size = Pt(16)
    p1_8.font.bold = True
    p1_8.font.color.rgb = NAVY
    p1_8.space_after = Pt(10)

    prod_points = [
        ("Asynchronous Job Queue:", "Memanfaatkan RabbitMQ / Redis Queue / Celery untuk memproses ribuan CV secara batch tanpa membuat server web freeze."),
        ("Microservices Architecture:", "Parser service, embedding worker, dan LLM worker berjalan terpisah dalam container Docker yang mudah di-scale horizontal."),
        ("Vector Database Terdistribusi:", "Qdrant / Milvus / PGVector untuk menyimpan jutaan profil bakat pabrik dan mendukung pencarian semantik instan."),
        ("High-Throughput Concurrency:", "Mampu memproses > 10.000 CV per jam saat rekrutmen massal pembukaan pabrik baru.")
    ]
    for title, desc in prod_points:
        pt = tf1_8.add_paragraph()
        pt.text = f"✔  {title} {desc}"
        pt.font.size = Pt(11.5)
        pt.font.color.rgb = TEXT_MUTED
        pt.space_before = Pt(8)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b2_8 = s8.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf2_8 = b2_8.text_frame
    tf2_8.word_wrap = True
    p2_8 = tf2_8.paragraphs[0]
    p2_8.text = "Human-in-the-Loop & Adaptabilitas Pabrik"
    p2_8.font.size = Pt(16)
    p2_8.font.bold = True
    p2_8.font.color.rgb = DARK_TEAL
    p2_8.space_after = Pt(10)

    hitl_points = [
        ("AI Sebagai Co-Pilot Cerdas:", "Sistem menyaring dan menyusun peringkat; keputusan final wawancara tetap berada di tangan Recruiter & Line Manager."),
        ("Dukungan Ragam Posisi Manufaktur:", "Fleksibel mengevaluasi Plant CAD Drafter, Automation Engineer, PLC Specialist, Operator Produksi, hingga Staff PPIC & QC."),
        ("Integrasi HRIS & Mesin Presensi:", "REST API mudah disambungkan ke HRIS internal pabrik untuk penjadwalan wawancara dan onboarding otomatis.")
    ]
    for title, desc in hitl_points:
        pt = tf2_8.add_paragraph()
        pt.text = f"✔  {title} {desc}"
        pt.font.size = Pt(11.5)
        pt.font.color.rgb = TEXT_MUTED
        pt.space_before = Pt(10)

    # =========================================================================
    # SLIDE 9: Business ROI & Cost-Benefit Analysis
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Analisis Efisiensi, Reduksi Biaya, & Dampak Bisnis (ROI)")

    metrics_9 = [
        ("95%", "Efisiensi Waktu", "Screening 1.000 CV turun dari 50 jam kerja menjadi < 15 menit pemrosesan otomatis."),
        ("75%", "Penghematan Biaya", "Mengurangi biaya lembur rekruter & mengeliminasi ketergantungan pada agensi rekrutmen pihak ketiga."),
        ("3 Hari", "Time-to-Hire", "Memangkas siklus dari rata-rata 21-25 hari menjadi 3-5 hari siap wawancara."),
        ("100%", "Objektivitas & Konsistensi", "Standardisasi evaluasi bebas bias lelah shift kerja dan subjektivitas manusia.")
    ]

    for i, (val, label, detail) in enumerate(metrics_9):
        x = Inches(0.8 + (i * 2.95))
        add_card(s9, x, Inches(1.8), Inches(2.85), Inches(2.2), bg_color=LIGHT_TEAL, border_color=TEAL)
        mb = s9.shapes.add_textbox(x + Inches(0.15), Inches(1.9), Inches(2.55), Inches(2.0))
        tf = mb.text_frame
        tf.word_wrap = True

        pv = tf.paragraphs[0]
        pv.text = val
        pv.font.size = Pt(32)
        pv.font.bold = True
        pv.font.color.rgb = DARK_TEAL

        pl = tf.add_paragraph()
        pl.text = label
        pl.font.size = Pt(13)
        pl.font.bold = True
        pl.font.color.rgb = NAVY
        pl.space_before = Pt(4)

        pd = tf.add_paragraph()
        pd.text = detail
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED
        pd.space_before = Pt(4)

    add_card(s9, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5))
    tb_9 = s9.shapes.add_textbox(Inches(1.1), Inches(4.5), Inches(11.1), Inches(2.1))
    tf_t9 = tb_9.text_frame
    tf_t9.word_wrap = True

    pt_9 = tf_t9.paragraphs[0]
    pt_9.text = "Perbandingan Sebelum vs Sesudah Implementasi AI CV Screening"
    pt_9.font.size = Pt(14)
    pt_9.font.bold = True
    pt_9.font.color.rgb = NAVY
    pt_9.space_after = Pt(8)

    table_rows = [
        ("Parameter Rekrutmen", "Proses Manual (Sebelumnya)", "Dengan AI CV Screening (Sesudah)"),
        ("Kapasitas Screening", "Maksimal 150-200 CV per hari per recruiter", "Ribuan CV diproses secara simultan dalam hitungan menit"),
        ("Risiko Bias Manusia", "Tinggi (terpengaruh foto, gender, nama, almamater)", "Nol pada tahap AI (Blind Screening berbasis kompetensi)"),
        ("Auditability & Keterbukaan", "Subjektif, tidak ada rekaman alasan penolakan detail", "100% transparan dengan Strengths, Gaps, dan Reasoning"),
        ("Dampak pada Operasional Pabrik", "Kekurangan operator & drafter memperlambat shift", "Pemenuhan man-power tepat waktu, zero production downtime")
    ]
    for row in table_rows[1:]:
        p_row = tf_t9.add_paragraph()
        p_row.text = f"• {row[0]}: {row[1]}  ➔  {row[2]}"
        p_row.font.size = Pt(11)
        p_row.font.color.rgb = TEXT_MUTED
        p_row.space_before = Pt(4)

    # =========================================================================
    # SLIDE 10: Proof of Concept & Live Validation Results
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Demonstrasi Proof of Concept (PoC) & Validasi Hasil Uji")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b1_10 = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf1_10 = b1_10.text_frame
    tf1_10.word_wrap = True
    p1_10 = tf1_10.paragraphs[0]
    p1_10.text = "Fitur Utama PoC (Streamlit + Gemini)"
    p1_10.font.size = Pt(16)
    p1_10.font.bold = True
    p1_10.font.color.rgb = NAVY
    p1_10.space_after = Pt(10)

    poc_features = [
        "1. Dynamic Job Presets: Template siap pakai untuk Plant CAD Drafter & Backend Engineer Pabrik.",
        "2. One-Click Demo: Tombol pengujian langsung terhadap 5 CV sampel anonim bawaan.",
        "3. Multi-Format Ingestion: Ekstraksi teks otomatis dari file PDF & tabel DOCX.",
        "4. Strict Blind Isolation: PII disensor ketat sebelum proses scoring semantik.",
        "5. Metrik Dashboard: Total pelamar, rasio lolos hard filter, dan rata-rata skor.",
        "6. Audit Trail & CSV Export: Detail kekuatan/kelemahan per kandidat siap diunduh tim HR."
    ]
    for feat in poc_features:
        pf = tf1_10.add_paragraph()
        pf.text = f"✔  {feat}"
        pf.font.size = Pt(11)
        pf.font.color.rgb = TEXT_MUTED
        pf.space_before = Pt(6)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b2_10 = s10.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf2_10 = b2_10.text_frame
    tf2_10.word_wrap = True
    p2_10 = tf2_10.paragraphs[0]
    p2_10.text = "Hasil Uji Nyata Terhadap 5 Sample CV"
    p2_10.font.size = Pt(16)
    p2_10.font.bold = True
    p2_10.font.color.rgb = DARK_TEAL
    p2_10.space_after = Pt(10)

    cv_results = [
        ("Rank #1: Dani (Skor: 87.4)", "Lolos (Exp: 3 thn, SMK & S1, AutoCAD & SketchUp)", "Rekomendasi Utama Wawancara"),
        ("Rank #2: INDRI (Skor: 86.3)", "Lolos (Exp: 2 thn, S1 & Master, AutoCAD & SketchUp)", "Rekomendasi Wawancara"),
        ("Rank #3: Bayu (Skor: 84.3)", "Lolos (Exp: 6 thn, S1 Arsitektur, AutoCAD & SketchUp)", "Rekomendasi Wawancara"),
        ("Rank #4: Permana Abadi (Skor: 76.6)", "Lolos (Exp: 3 thn, S1, AutoCAD & SketchUp)", "Rekomendasi Wawancara"),
        ("Rank #5: MOHAMAD (Skor: 0.0)", "Gagal Syarat Wajib (Skill SketchUp tidak ada)", "Tidak Lolos Filter Awal")
    ]
    for name, desc, status in cv_results:
        p_c = tf2_10.add_paragraph()
        p_c.text = f"• {name}"
        p_c.font.size = Pt(11.5)
        p_c.font.bold = True
        p_c.font.color.rgb = NAVY if "Lolos" in status else RED_ACCENT

        p_d = tf2_10.add_paragraph()
        p_d.text = f"   {desc} ➔ {status}"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_after = Pt(4)

    # =========================================================================
    # SLIDE 11: Production Implementation Roadmap
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Roadmap Implementasi Produksi (3 Tahap Eksekusi)")

    phases_11 = [
        ("Fase 1: Pilot & Validasi", "Bulan 1 (Setup & Benchmark)", [
            "Deployment PoC ke lingkungan internal staging.",
            "Benchmarking skor AI terhadap 200 keputusan manual historis tim HR.",
            "Fine-tuning bobot hybrid (embedding vs LLM) berdasarkan karakteristik peran manufaktur.",
            "Pelatihan pengoperasian bagi tim rekruter pabrik."
        ], DARK_TEAL),
        ("Fase 2: Integrasi Sistem", "Bulan 2 - 3 (Automation)", [
            "Integrasi Webhook resmi dengan Jobstreet & LinkedIn.",
            "Koneksi API dua arah ke HRIS / ATS eksisting perusahaan.",
            "Implementasi Asynchronous Queue (Celery/RabbitMQ) untuk throughput tinggi.",
            "Penerapan audit keamanan data & audit kepatuhan UU PDP."
        ], TEAL),
        ("Fase 3: Skalabilitas Penuh", "Bulan 4+ (Enterprise Scale)", [
            "Rollout penuh ke seluruh departemen pabrik & plant cabang.",
            "Penambahan modul Vision OCR untuk CV scan/gambar non-teks.",
            "Modul Automated Interview Scheduling terintegrasi kalender HR.",
            "Continuous Learning & evaluasi bias berkala (Quarterly Audit)."
        ], GREEN_ACCENT)
    ]

    for i, (title, sub, points, color) in enumerate(phases_11):
        x = Inches(0.8 + (i * 4.0))
        add_card(s11, x, Inches(1.8), Inches(3.7), Inches(5.0))
        top_bar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()

        box = s11.shapes.add_textbox(x + Inches(0.25), Inches(2.1), Inches(3.2), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = NAVY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(11)
        ps.font.bold = True
        ps.font.color.rgb = color
        ps.space_after = Pt(12)

        for p in points:
            pp = tf.add_paragraph()
            pp.text = f"•  {p}"
            pp.font.size = Pt(11)
            pp.font.color.rgb = TEXT_MUTED
            pp.space_before = Pt(8)

    # =========================================================================
    # SLIDE 12: Strategic Conclusion (Dark Executive Theme)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12, NAVY)

    bar12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.8), Inches(0.08))
    bar12.fill.solid()
    bar12.fill.fore_color.rgb = TEAL
    bar12.line.fill.background()

    tbox12 = s12.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.2))
    tf12 = tbox12.text_frame
    tf12.word_wrap = True
    p1_12 = tf12.paragraphs[0]
    p1_12.text = "Kesimpulan & Nilai Tambah Strategis AI Specialist"
    p1_12.font.size = Pt(30)
    p1_12.font.bold = True
    p1_12.font.color.rgb = WHITE

    add_card(s12, Inches(1.0), Inches(2.8), Inches(11.3), Inches(4.0), bg_color=DARK_BLUE, border_color=None)
    cbox12 = s12.shapes.add_textbox(Inches(1.3), Inches(3.0), Inches(10.7), Inches(3.5))
    tf_c12 = cbox12.text_frame
    tf_c12.word_wrap = True

    recs_12 = [
        ("Efisiensi & Akselerasi Rekrutmen:", "Sistem otomatisasi Two-Stage Hybrid AI memangkas 95% waktu screening, memastikan pembukaan lini manufaktur didukung tenaga kerja tepat waktu."),
        ("Penghematan Biaya Finansial:", "Kombinasi Hard Filter gatekeeper dan model hybrid menjaga biaya API tetap minimum (turun 70-75%) dibanding solusi LLM murni."),
        ("Keadilan & Kepatuhan Regulasi:", "Pemisahan PII (Blind Auditing) dan penjelasan transparan (XAI) menjamin seleksi 100% objektif, etis, serta patuh penuh pada UU PDP No. 27/2022."),
        ("Kesiapan Produksi (Enterprise-Ready):", "Solusi dirancang modular dan terukur, siap bertransisi mulus dari Proof of Concept menjadi infrastruktur rekrutmen permanen perusahaan manufaktur.")
    ]

    for title, desc in recs_12:
        p = tf_c12.add_paragraph()
        p.text = f"✔  {title} {desc}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(12)

    try:
        prs.save(output_filename)
        print(f"Presentation saved successfully to: {output_filename}")
    except PermissionError:
        fallback_name = "Presentasi_AI_CV_Screening_Specialist_Updated.pptx"
        prs.save(fallback_name)
        print(f"Catatan: '{output_filename}' sedang dibuka. File terbaru berhasil disimpan ke: {fallback_name}")


if __name__ == "__main__":
    generate_deck()
