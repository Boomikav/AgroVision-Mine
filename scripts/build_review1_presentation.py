"""
AgroVision-Mine: Review 1 Faculty-Ready Presentation Builder (v2).
Directly enhances DWDM_Lab_Project_Template.pptx by preserving native layout shapes,
typography (Georgia titles, Calibri body, Consolas code), and academic styling
while eliminating all overlapping text, duplicate headers, and duplicate footers.
"""
import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -----------------------------------------------------------------------------
# Color Palette Definition (Research Agritech & Data Science)
# -----------------------------------------------------------------------------
COLOR_DARK       = RGBColor(26, 26, 26)       # #1A1A1A - Dark Accent / Headers
COLOR_GREEN_DEEP = RGBColor(27, 67, 50)       # #1B4332 - Forest Green Title
COLOR_GREEN_CARD = RGBColor(45, 106, 79)      # #2D6A4F - Card Header Green
COLOR_GREEN_MINT = RGBColor(216, 243, 220)    # #D8F3DC - Subtle Green Fill
COLOR_TEAL       = RGBColor(21, 96, 130)      # #156082 - Analytical Accent
COLOR_ORANGE     = RGBColor(230, 81, 0)       # #E65100 - Governance / Warning
COLOR_CARD_BG    = RGBColor(248, 249, 250)    # #F8F9FA - Light Card Background
COLOR_CODE_BG    = RGBColor(28, 28, 28)       # #1C1C1C - Dark Code Background
COLOR_TEXT_MAIN  = RGBColor(33, 33, 33)       # #212121 - Body Text
COLOR_TEXT_MUTED = RGBColor(90, 90, 90)       # #5A5A5A - Muted Text
COLOR_WHITE      = RGBColor(255, 255, 255)    # #FFFFFF
COLOR_BORDER     = RGBColor(207, 216, 220)    # #CFD8DC - Card Border
COLOR_GREEN_BDR  = RGBColor(116, 198, 157)    # #74C69D - Subtle Green Border

FONT_TITLE = "Georgia"
FONT_BODY  = "Calibri"
FONT_CODE  = "Consolas"

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def set_title(slide, title_text):
    """Sets the title using the template's native Title 1 placeholder in Layout 2."""
    for s in slide.shapes:
        if "Title" in s.name or s.shape_type == 14: # Placeholder
            s.text = title_text
            for p in s.text_frame.paragraphs:
                p.font.name = FONT_TITLE
                p.font.size = Pt(24)
                p.font.bold = True
                p.font.color.rgb = COLOR_GREEN_DEEP
            return s
    # Fallback textbox aligned with template's vertical bar
    tb = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(11.8), Inches(0.85))
    tb.text_frame.word_wrap = True
    p = tb.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_DEEP
    return tb

def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_BORDER, border_width=1.0):
    """Creates a rounded rectangle card for structured content."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(border_width)
    return card

def create_table(slide, left, top, width, height, headers, rows, col_widths=None):
    """Creates an academic table with dark green header row and alternating zebra stripes."""
    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    table = table_shape.table

    if col_widths and len(col_widths) == num_cols:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w

    # Header Row
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_GREEN_DEEP
        cell.text_frame.word_wrap = True
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        bg = COLOR_CARD_BG if r_idx % 2 == 0 else COLOR_WHITE
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.word_wrap = True
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.alignment = PP_ALIGN.LEFT

    return table_shape

def add_code_box(slide, left, top, width, height, code_text):
    """Adds a dark IDE code container with monospaced syntax-highlighted appearance."""
    card = create_card(slide, left, top, width, height, COLOR_CODE_BG, RGBColor(50, 50, 50), 1.0)
    txBox = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
    tf = txBox.text_frame
    tf.word_wrap = True
    lines = code_text.strip().split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = FONT_CODE
        p.font.size = Pt(8.0)
        p.font.color.rgb = RGBColor(220, 220, 220)
        if line.strip().startswith("--") or line.strip().startswith("#"):
            p.font.color.rgb = RGBColor(120, 200, 120)  # Green comments
        elif any(k in line for k in ["CREATE TABLE", "SELECT", "FROM", "JOIN", "WHERE", "GROUP BY", "CASE", "THEN", "ELSE", "END"]):
            p.font.color.rgb = RGBColor(130, 190, 255)  # SQL blue keywords
        elif "def " in line or "import " in line or "return " in line:
            p.font.color.rgb = RGBColor(255, 180, 100)  # Python keywords
    return txBox


# -----------------------------------------------------------------------------
# MAIN PRESENTATION BUILDER
# -----------------------------------------------------------------------------
def build_presentation():
    template_path = Path("DWDM_Lab_Project_Template.pptx")
    if not template_path.exists():
        print(f"Error: {template_path} not found!")
        sys.exit(1)

    prs = Presentation(str(template_path))
    content_layout = prs.slide_layouts[2]  # CONTENT: Shape 0 (accent bar), Text 2 (title), Text 1 (footer), Slide Num
    title_layout   = prs.slide_layouts[3]  # TITLE2: Shape 0 (accent bar), Text 1 (title), Text 1 (sub)

    # Clear initial 9 placeholder slides
    for i in range(len(prs.slides) - 1, -1, -1):
        rId = prs.slides._sldIdLst[i].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[i]

    print("Cleared template placeholder slides. Rebuilding 13 verified slides...")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Authentic Academic Dark Layout)
    # =========================================================================
    s1 = prs.slides.add_slide(title_layout)
    # Dark Background matching template Slide 1
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_DARK
    bg1.line.color.rgb = COLOR_DARK

    # Vertical Accent Bar matching template Slide 1
    vbar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(2.3))
    vbar.fill.solid()
    vbar.fill.fore_color.rgb = COLOR_GREEN_BDR
    vbar.line.color.rgb = COLOR_GREEN_BDR

    # Title & Subtitle block
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.2), Inches(2.6))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "DATA WAREHOUSING & DATA MINING (CSI3010) - LAB PROJECT REVIEW 1"
    p_badge.font.name = FONT_BODY
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_GREEN_BDR

    p_t1 = tf1.add_paragraph()
    p_t1.text = "AgroVision-Mine"
    p_t1.font.name = FONT_TITLE
    p_t1.font.size = Pt(36)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_WHITE

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Multimodal Data Warehouse and Visual Pattern Mining Framework\nfor Crop Disease and Pest Intelligence"
    p_sub.font.name = FONT_TITLE
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(200, 220, 210)

    # Scope Summary Card
    scope_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.3), Inches(11.0), Inches(0.65))
    scope_card.fill.solid()
    scope_card.fill.fore_color.rgb = RGBColor(38, 48, 42)
    scope_card.line.color.rgb = COLOR_GREEN_BDR
    scope_card.line.width = Pt(1.0)
    sc_tf = scope_card.text_frame
    p_sc = sc_tf.paragraphs[0]
    p_sc.text = "VERIFIED REVIEW 1 STATE: 36 Authentic Field Images (Rice) | 4 Diagnostic Tests | 34 Visual Descriptors | Kimball Star Schema | 5 Real SQL OLAP Ops | 56/56 Tests Passed (100%)"
    p_sc.font.name = FONT_BODY
    p_sc.font.size = Pt(9.0)
    p_sc.font.bold = True
    p_sc.font.color.rgb = COLOR_GREEN_MINT
    p_sc.alignment = PP_ALIGN.CENTER

    # Team & Faculty Details Block
    meta_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.3), Inches(11.0), Inches(1.5))
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True

    p_m1 = tf_meta.paragraphs[0]
    p_m1.text = "PROJECT TEAM DETAILS"
    p_m1.font.name = FONT_BODY
    p_m1.font.size = Pt(9.5)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_GREEN_BDR

    p_m2 = tf_meta.add_paragraph()
    p_m2.text = "Team Members: [Student Name 1 - Reg. No.]  |  [Student Name 2 - Reg. No.]  |  [Student Name 3 - Reg. No.]"
    p_m2.font.name = FONT_BODY
    p_m2.font.size = Pt(10.5)
    p_m2.font.color.rgb = COLOR_WHITE

    p_m3 = tf_meta.add_paragraph()
    p_m3.text = "Faculty Guide: [Faculty Name]   |   Lab Slot: [Lab Slot]   |   Academic Term: 2026"
    p_m3.font.name = FONT_BODY
    p_m3.font.size = Pt(9.5)
    p_m3.font.color.rgb = RGBColor(170, 170, 170)

    # =========================================================================
    # SLIDE 2: RESEARCH MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(content_layout)
    set_title(s2, "Research Motivation: The Agricultural Data Gap")

    # Left Card: Limitations of Current Approaches
    c2_l = create_card(s2, Inches(0.6), Inches(1.6), Inches(5.9), Inches(4.2), COLOR_CARD_BG, COLOR_BORDER, 1.0)
    tx2_l = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(3.8))
    tf2_l = tx2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "LIMITATIONS OF CURRENT APPROACHES"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 40, 40)

    bullets_l = [
        ("Isolated Point Classifiers", "Standard deep learning (CNNs/YOLO) treats foliar disease identification as an isolated inference task without data warehousing."),
        ("Absence of Relational Rigor", "Images reside in flat, disconnected directories. No referential integrity linking images to botanical taxonomy, cryptographic digests, or extracted features."),
        ("Inability to Perform OLAP Exploration", "Researchers cannot run aggregate queries across agronomic hierarchies (e.g. comparing lesion texture of bacterial vs fungal pathogens)."),
        ("Lack of Explainable Lineage", "Black-box neural embeddings cannot explain why an image exhibits specific texture or foliar discoloration patterns.")
    ]
    for head, desc in bullets_l:
        p_b = tf2_l.add_paragraph()
        p_b.text = f"• {head}: {desc}"
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(8.5)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    # Right Card: The AgroVision-Mine Solution
    c2_r = create_card(s2, Inches(6.8), Inches(1.6), Inches(5.9), Inches(4.2), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx2_r = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(3.8))
    tf2_r = tx2_r.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "THE AGROVISION-MINE SOLUTION"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    bullets_r = [
        ("Multimodal Data Warehouse", "First-of-its-kind architecture applying Ralph Kimball's Star Schema methodology to agricultural imagery and classical visual features."),
        ("Explainable Feature Store", "34 classical descriptors (RGB/HSV color moments, Haralick GLCM textures, morphometric shape contours) in a 44-column analytical dataset."),
        ("SQL-Backed OLAP Analytics", "Executes real SQL queries across dimensions: Roll-up to crop categories, True Drill-down to diseases, Slicing by crops, Dicing, and Pivoting."),
        ("Enterprise Data Integrity", "Surrogate keys, native SQLite foreign key enforcement (PRAGMA foreign_keys = 1), and idempotent ETL guarantee 100% database consistency.")
    ]
    for head, desc in bullets_r:
        p_b = tf2_r.add_paragraph()
        p_b.text = f"✓ {head}: {desc}"
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(8.5)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    # Bottom Callout: Research Question
    bq = create_card(s2, Inches(0.6), Inches(6.0), Inches(12.1), Inches(0.55), COLOR_GREEN_MINT, COLOR_GREEN_BDR, 1.0)
    tx_q = s2.shapes.add_textbox(Inches(0.7), Inches(6.05), Inches(11.9), Inches(0.45))
    p_q = tx_q.text_frame.paragraphs[0]
    p_q.text = "Core Research Question: How can image-based crop disease observations be transformed into a multimodal analytical warehouse for explainable multidimensional decision support?"
    p_q.font.name = FONT_BODY
    p_q.font.size = Pt(9.5)
    p_q.font.bold = True
    p_q.font.color.rgb = COLOR_GREEN_DEEP
    p_q.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES & MULTIMODAL PIPELINE FLOW
    # =========================================================================
    s3 = prs.slides.add_slide(content_layout)
    set_title(s3, "Project Objectives & Multimodal Pipeline Flow")

    # 6 Objective Cards (2x3 grid)
    objs = [
        ("1. Ingestion & Anti-Fabrication", "Ingest authentic ICAR Indian agricultural imagery; derive botanical metadata dynamically without synthetic fabrication."),
        ("2. Quality Gate Auditing", "Enforce automated validation: detect corrupted headers, exact MD5 duplicates, and sub-threshold images without silent deletion."),
        ("3. Classical Feature Store", "Extract 34 explainable visual descriptors (Color moments, Haralick GLCM, morphometric contours) with full Image_ID lineage."),
        ("4. Kimball Star Schema", "Deploy ANSI SQL relational schema centered on individual image observations surrounded by 4 empirically-supported dimensions."),
        ("5. Production Idempotent ETL", "Build dimension-first ETL pipeline enforcing native SQLite foreign keys (PRAGMA foreign_keys = 1) with 0 duplicate fact re-runs."),
        ("6. Real SQL-Backed OLAP", "Implement and evaluate genuine SQL analytical queries: Roll-up, True Drill-down, Slice, Dice, and Pivot over physical facts.")
    ]

    card_w = Inches(3.85)
    card_h = Inches(1.25)
    col_gap = Inches(0.27)
    row_gap = Inches(0.18)
    top_start = Inches(1.6)

    for i, (head, desc) in enumerate(objs):
        col = i % 3
        row = i // 3
        left = Inches(0.6) + col * (card_w + col_gap)
        top = top_start + row * (card_h + row_gap)

        card = create_card(s3, left, top, card_w, card_h, COLOR_CARD_BG, COLOR_BORDER, 1.0)
        tx = s3.shapes.add_textbox(left + Inches(0.12), top + Inches(0.1), card_w - Inches(0.24), card_h - Inches(0.2))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = head
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_GREEN_DEEP

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # Bottom Pipeline Visual
    pipeline_img = Path("assets/presentation/pipeline_flow.png")
    if pipeline_img.exists():
        s3.shapes.add_picture(str(pipeline_img), Inches(0.6), Inches(4.6), Inches(12.1), Inches(1.95))

    # =========================================================================
    # SLIDE 4: DATASET DESCRIPTION & AGRONOMIC TAXONOMY (Template Slide 2 Layout)
    # =========================================================================
    s4 = prs.slides.add_slide(content_layout)
    set_title(s4, "Dataset Description & Agronomic Taxonomy")

    # Left: 7x2 Table (Direct replacement of Template Table 0)
    t_headers = ["Dataset Property", "Verified Project Specification"]
    t_rows = [
        ["Dataset Name", "Official Govt. of India / ICAR Working Pathology Subset"],
        ["Primary Source", "data.gov.in / ICAR Research Institutes (ICAR-CRIDA, ICAR-IIRR)"],
        ["Verified Working Subset", "36 authentic field photographs across 3 foliar rice pathologies"],
        ["Pathology Breakdown", "Bacterial Leaf Blight: 12  |  Brown Spot: 12  |  Leaf Smut: 12"],
        ["Host Plant Taxonomy", "Rice (Oryza sativa)  |  Category: Cereal (National Staple Food)"],
        ["Format & Standardization", "Standardized 256x256x3 RGB (Lanczos anti-aliased interpolation)"],
        ["Storage & Integrity", "Unique Image_ID, MD5 cryptographic hash, Laplacian blur score"]
    ]
    t_shape = create_table(s4, Inches(0.6), Inches(1.6), Inches(6.5), Inches(4.8), t_headers, t_rows, [Inches(2.1), Inches(4.4)])

    # Right Card: Why this dataset? / Agronomic Significance (Direct replacement of Template Rationale card)
    c4_r = create_card(s4, Inches(7.4), Inches(1.6), Inches(5.3), Inches(4.8), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx4_r = s4.shapes.add_textbox(Inches(7.6), Inches(1.8), Inches(4.9), Inches(4.4))
    tf4_r = tx4_r.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.text = "AGRONOMIC SIGNIFICANCE & DATA GOVERNANCE"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    bullets_s4 = [
        ("Critical Staple Crop", "Rice feeds >60% of India's population. Microbial infections (Xanthomonas oryzae, Bipolaris oryzae) cause devastating seasonal yield losses of up to 40%."),
        ("Authentic Working Subset", "The 36 authentic observations represent the verified project subset from official Indian repositories, ensuring full reproducible auditability."),
        ("Control Baseline Policy (HEALTHY)", "HEALTHY is maintained in dim_disease as an unpopulated control reference value (0 facts). The working subset contains pathological foliar specimens exclusively; no synthetic healthy observations were fabricated."),
        ("Anti-Fabrication Mandate", "Unsupported dimensions (Pest, Time, Geography) were strictly excluded because source images lack verified empirical field tags.")
    ]
    for head, desc in bullets_s4:
        p_b = tf4_r.add_paragraph()
        p_b.text = f"• {head}: {desc}"
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(8.5)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 5: DATA QUALITY & PREPROCESSING GATES
    # =========================================================================
    s5 = prs.slides.add_slide(content_layout)
    set_title(s5, "Image Preprocessing & Quality Gate Verification")

    # Top Left Card: Controlled Diagnostic Harness
    c5_l = create_card(s5, Inches(0.6), Inches(1.6), Inches(5.9), Inches(2.1), COLOR_CARD_BG, COLOR_BORDER, 1.0)
    tx5_l = s5.shapes.add_textbox(Inches(0.8), Inches(1.75), Inches(5.5), Inches(1.8))
    tf5_l = tx5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "CONTROLLED DIAGNOSTIC EDGE HARNESS (data/diagnostic_tests/)"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 40, 40)

    diag_items = [
        ("corrupted_header_test.jpg", "Truncated byte stream -> REJECTED (CORRUPTED)"),
        ("invalid_dim_tiny.jpg", "Dimensions 16x16px < 32px -> REJECTED (INVALID_DIM)"),
        ("duplicate_exact_test.jpg", "Exact MD5 match -> REJECTED (EXACT_HASH)"),
        ("unsupported_extension.txt", "Non-image MIME -> REJECTED (UNSUPPORTED_FORMAT)")
    ]
    for fn, outcome in diag_items:
        p_d = tf5_l.add_paragraph()
        p_d.text = f"• {fn} -> {outcome}"
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(8.0)
        p_d.font.color.rgb = COLOR_TEXT_MAIN

    # Top Right Card: Authentic Dataset Standardization
    c5_r = create_card(s5, Inches(6.8), Inches(1.6), Inches(5.9), Inches(2.1), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx5_r = s5.shapes.add_textbox(Inches(7.0), Inches(1.75), Inches(5.5), Inches(1.8))
    tf5_r = tx5_r.text_frame
    tf5_r.word_wrap = True

    p = tf5_r.paragraphs[0]
    p.text = "AUTHENTIC RESEARCH DATASET STANDARDIZATION"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    auth_items = [
        ("36 Authentic Field Images Discovered", "36 Successfully Standardized"),
        ("Quality Pass Rate", "100% (Zero authentic research observations rejected)"),
        ("Standardization", "256 x 256 px RGB, Lanczos anti-aliased resampling"),
        ("Non-Destructive Storage", "Raw originals preserved; cleaned copies in data/processed/"),
        ("Laplacian Variance Blur Scoring", "Mean score = 185.34 (Threshold = 100.0)")
    ]
    for head, detail in auth_items:
        p_a = tf5_r.add_paragraph()
        p_a.text = f"✓ {head}: {detail}"
        p_a.font.name = FONT_BODY
        p_a.font.size = Pt(8.0)
        p_a.font.color.rgb = COLOR_TEXT_MAIN

    # Bottom Visual: Preprocessing Comparison
    prep_img = Path("assets/presentation/preprocessing_comparison.png")
    if prep_img.exists():
        s5.shapes.add_picture(str(prep_img), Inches(0.6), Inches(3.9), Inches(12.1), Inches(2.6))

    # =========================================================================
    # SLIDE 6: VISUAL FEATURE EXTRACTION & ATTRIBUTE SUMMARY (Template Slide 3)
    # =========================================================================
    s6 = prs.slides.add_slide(content_layout)
    set_title(s6, "Visual Feature Extraction & Attribute Summary")

    # Left: 8x4 Table (Direct replacement of Template Table 0)
    t6_headers = ["Attribute Name", "Physical Type", "Agronomic / Visual Description", "Role in DW"]
    t6_rows = [
        ["observation_key", "INTEGER", "Surrogate primary key for fact record", "Fact PK"],
        ["crop_key, disease_key", "INTEGER", "Surrogate foreign keys to botanical & pathology dims", "Fact FKs"],
        ["rgb_r/g/b_mean, std", "FLOAT [0-255]", "First and second order color moments across RGB channels", "Feature Dim"],
        ["hsv_h/s/v_mean, std", "FLOAT", "Hue, Saturation, Value moments for illumination invariance", "Feature Dim"],
        ["exg_index_mean", "FLOAT", "Excess Green Vegetative Index: 2G - R - B (chlorophyll intensity)", "Feature Dim"],
        ["dominant_color_tone", "VARCHAR", "Macroscopic foliar tone (Brown_Blight, Yellowish_Lesion)", "Feature Dim"],
        ["glcm_contrast, homogeneity", "FLOAT", "Haralick GLCM texture disruption & local smoothness", "Feature Dim"],
        ["lesion_severity_score", "FLOAT [0-10]", "Continuous composite foliar lesion severity measure", "Fact Measure"]
    ]
    t6_shape = create_table(s6, Inches(0.6), Inches(1.6), Inches(8.0), Inches(4.1), t6_headers, t6_rows, [Inches(1.8), Inches(1.0), Inches(4.2), Inches(1.0)])

    # Right Card: 44-Column Feature Store Architecture
    c6_r = create_card(s6, Inches(8.9), Inches(1.6), Inches(3.8), Inches(4.1), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx6_r = s6.shapes.add_textbox(Inches(9.05), Inches(1.75), Inches(3.5), Inches(3.8))
    tf6_r = tx6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "44-COLUMN FEATURE DATASET"
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    bullets_s6 = [
        ("34 Explainable Visual Descriptors", [
            "• 17 Color Descriptors (RGB/HSV moments & ExG index)",
            "• 7 Haralick GLCM Textures (Contrast, Energy, ASM, Homogeneity, Correlation, Dissimilarity)",
            "• 7 Morphometric Shape Contours (Area, Perimeter, Aspect Ratio, Solidity, Coverage)"
        ]),
        ("10 Lineage / Metadata Fields", [
            "• image_id, filename, raw_path, processed_path, crop_label, condition_label, disease_label, pest_label, is_pest, md5_hash"
        ]),
        ("100% Traceability", [
            "• Every row maps 1:1 to an authenticated image via image_id and MD5 cryptographic hash."
        ])
    ]
    for sec_head, sub_items in bullets_s6:
        p_sh = tf6_r.add_paragraph()
        p_sh.text = sec_head
        p_sh.font.name = FONT_BODY
        p_sh.font.size = Pt(8.5)
        p_sh.font.bold = True
        p_sh.font.color.rgb = COLOR_DARK
        for sub in sub_items:
            p_sub = tf6_r.add_paragraph()
            p_sub.text = sub
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(7.5)
            p_sub.font.color.rgb = COLOR_TEXT_MAIN

    # Bottom Pill
    pill6 = create_card(s6, Inches(0.6), Inches(5.95), Inches(12.1), Inches(0.55), COLOR_GREEN_MINT, COLOR_GREEN_BDR, 1.0)
    tx_pill6 = s6.shapes.add_textbox(Inches(0.7), Inches(6.0), Inches(11.9), Inches(0.45))
    p_p6 = tx_pill6.text_frame.paragraphs[0]
    p_p6.text = "Standard Terminology Verification: 34 explainable visual descriptors stored in a 44-column analytical feature dataset (data/features/image_features.csv)."
    p_p6.font.name = FONT_BODY
    p_p6.font.size = Pt(9.0)
    p_p6.font.bold = True
    p_p6.font.color.rgb = COLOR_GREEN_DEEP
    p_p6.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 7: MULTIMODAL DATA WAREHOUSE - STAR SCHEMA TOPOLOGY (Template Slide 4)
    # =========================================================================
    s7 = prs.slides.add_slide(content_layout)
    set_title(s7, "Multimodal Data Warehouse - Star Schema Topology")

    # Center-Left: High-Res ERD Picture
    erd_img = Path("assets/presentation/star_schema_erd.png")
    if erd_img.exists():
        s7.shapes.add_picture(str(erd_img), Inches(0.6), Inches(1.55), Inches(7.6), Inches(4.95))

    # Right: Physical Warehouse Inventory & Data Governance Card
    c7_r = create_card(s7, Inches(8.4), Inches(1.55), Inches(4.3), Inches(4.95), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx7_r = s7.shapes.add_textbox(Inches(8.55), Inches(1.7), Inches(4.0), Inches(4.6))
    tf7_r = tx7_r.text_frame
    tf7_r.word_wrap = True

    p = tf7_r.paragraphs[0]
    p.text = "PHYSICAL WAREHOUSE INVENTORY"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    dw_specs = [
        ("disease_observation_fact (36 Rows)", "PK: observation_key\n• FKs: crop_key, disease_key, image_key, feature_key\n• Measures: count (1), severity [2.13-4.98], sharpness [5.9-789.8], coverage [0.21-0.50], GLCM contrast"),
        ("dim_crop (1 Row)", "Host taxonomy: RICE (Oryza sativa), Cereal"),
        ("dim_disease (4 Rows)", "Bacterial Leaf Blight, Brown Spot, Leaf Smut\n• HEALTHY (Unpopulated Control Baseline)"),
        ("dim_image (36 Rows)", "Optical geometry, MD5 hash, blur score, paths"),
        ("dim_visual_feature (36 Rows)", "34 color, Haralick texture, shape contour descriptors"),
        ("Data Governance Mandate", "Schema strictly follows observed source attributes. Unsupported dimensions (Dim_Pest, Dim_Time, Dim_Geography) are not fabricated.")
    ]
    for head, body in dw_specs:
        p_h = tf7_r.add_paragraph()
        p_h.text = f"• {head}"
        p_h.font.name = FONT_BODY
        p_h.font.size = Pt(8.5)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_DARK

        p_b = tf7_r.add_paragraph()
        p_b.text = body
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(7.5)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 8: WAREHOUSE DESIGN & PRODUCTION ETL ARCHITECTURE (Template Slide 5)
    # =========================================================================
    s8 = prs.slides.add_slide(content_layout)
    set_title(s8, "Warehouse Design & Production ETL Architecture")

    # 3 Vertical Cards (Direct replacement of Fact, Dims, ETL cards from template)
    card_w8 = Inches(3.85)
    card_h8 = Inches(4.85)
    gap8 = Inches(0.27)

    # Card 1: Fact Table & Measures
    c8_1 = create_card(s8, Inches(0.6), Inches(1.6), card_w8, card_h8, COLOR_CARD_BG, COLOR_BORDER, 1.0)
    tx8_1 = s8.shapes.add_textbox(Inches(0.75), Inches(1.75), card_w8 - Inches(0.3), card_h8 - Inches(0.3))
    tf8_1 = tx8_1.text_frame
    tf8_1.word_wrap = True

    p = tf8_1.paragraphs[0]
    p.text = "Fact Table & Measures"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_DEEP

    f_items = [
        "Grain: Exactly ONE row per validated, preprocessed multimodal image observation.",
        "Additive Measure:\n  • observation_count (Constant 1 per record)",
        "Semi-Additive Measures:\n  • lesion_severity_score [0.0 - 10.0]\n  • image_sharpness_score (Laplacian Var)\n  • lesion_coverage_ratio [0.0 - 1.0]\n  • texture_contrast_norm [0.0 - 1.0]\n  • processing_latency_ms",
        "Referential Integrity:\n  • 4 Foreign Keys with ON DELETE RESTRICT\n  • Zero orphan keys, zero null measure values"
    ]
    for item in f_items:
        p_i = tf8_1.add_paragraph()
        p_i.text = f"• {item}"
        p_i.font.name = FONT_BODY
        p_i.font.size = Pt(8.0)
        p_i.font.color.rgb = COLOR_TEXT_MAIN

    # Card 2: Dimensions & Hierarchies
    c8_2 = create_card(s8, Inches(0.6) + card_w8 + gap8, Inches(1.6), card_w8, card_h8, COLOR_CARD_BG, COLOR_BORDER, 1.0)
    tx8_2 = s8.shapes.add_textbox(Inches(0.75) + card_w8 + gap8, Inches(1.75), card_w8 - Inches(0.3), card_h8 - Inches(0.3))
    tf8_2 = tx8_2.text_frame
    tf8_2.word_wrap = True

    p = tf8_2.paragraphs[0]
    p.text = "Dimensions & Hierarchies"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_DEEP

    d_items = [
        "Botanical Host Hierarchy:\n  Observation -> Crop Name -> Crop Category\n  (e.g., DSC_0365 -> Rice -> Cereal)",
        "Microbial Pathology Hierarchy:\n  Pathogen Type -> Disease Diagnosis\n  (Bacterial -> Bacterial Leaf Blight)\n  (Fungal -> Brown Spot | Leaf Smut)",
        "Visual Feature Dimension (1:1):\n  34 Color moments, Haralick GLCM textures, morphometric shape descriptors",
        "Physical Image Dimension (1:1):\n  Cryptographic MD5 hash, blur score, file paths"
    ]
    for item in d_items:
        p_i = tf8_2.add_paragraph()
        p_i.text = f"• {item}"
        p_i.font.name = FONT_BODY
        p_i.font.size = Pt(8.0)
        p_i.font.color.rgb = COLOR_TEXT_MAIN

    # Card 3: Production ETL & Idempotency
    c8_3 = create_card(s8, Inches(0.6) + 2 * (card_w8 + gap8), Inches(1.6), card_w8, card_h8, COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx8_3 = s8.shapes.add_textbox(Inches(0.75) + 2 * (card_w8 + gap8), Inches(1.75), card_w8 - Inches(0.3), card_h8 - Inches(0.3))
    tf8_3 = tx8_3.text_frame
    tf8_3.word_wrap = True

    p = tf8_3.paragraphs[0]
    p.text = "Production ETL & Idempotency"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    e_items = [
        "EXTRACT Phase:\n  - Ingests raw images, cleaned metadata, and extracted visual feature store",
        "TRANSFORM Phase:\n  - Quality validation, surrogate key mapping, botanical taxonomy normalization",
        "LOAD Phase (Dimension-First):\n  - Loads dim_crop, dim_disease, dim_image, dim_visual_feature, then fact table",
        "VERIFIED IDEMPOTENCY AUDIT:\n  - 1st Run: 36 facts inserted\n  - 2nd Run: 0 inserted, 36 duplicates skipped\n  - Native SQLite PRAGMA foreign_keys = 1"
    ]
    for item in e_items:
        p_i = tf8_3.add_paragraph()
        p_i.text = f"• {item}"
        p_i.font.name = FONT_BODY
        p_i.font.size = Pt(8.0)
        p_i.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 9: CODE: CREATING THE WAREHOUSE (Template Slide 7)
    # =========================================================================
    s9 = prs.slides.add_slide(content_layout)
    set_title(s9, "Code: Creating the Warehouse (ANSI SQL DDL)")

    sql_ddl = """-- 1. Dimension Tables: Botanical Crop & Pathology Diagnosis
CREATE TABLE dim_crop (
    crop_key INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_code VARCHAR(50) NOT NULL UNIQUE, crop_name VARCHAR(100) NOT NULL,
    botanical_name VARCHAR(150), crop_category VARCHAR(50) NOT NULL
);
CREATE TABLE dim_disease (
    disease_key INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_code VARCHAR(50) NOT NULL UNIQUE, disease_name VARCHAR(150) NOT NULL,
    pathogen_type VARCHAR(50) NOT NULL, -- Bacterial, Fungal, None (HEALTHY Control)
    causal_agent VARCHAR(150), primary_symptom VARCHAR(200)
);
-- dim_image & dim_visual_feature: Store optical parameters & 34 explainable visual descriptors
-- 2. Central Fact Table: Granular Grain (1 Row per Preprocessed Observation)
CREATE TABLE disease_observation_fact (
    observation_key INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_key INTEGER NOT NULL REFERENCES dim_crop(crop_key),
    disease_key INTEGER NOT NULL REFERENCES dim_disease(disease_key),
    image_key INTEGER NOT NULL UNIQUE REFERENCES dim_image(image_key),
    feature_key INTEGER NOT NULL UNIQUE REFERENCES dim_visual_feature(feature_key),
    observation_count INTEGER NOT NULL DEFAULT 1,
    lesion_severity_score FLOAT, image_sharpness_score FLOAT,
    lesion_coverage_ratio FLOAT, texture_contrast_norm FLOAT, etl_batch_id VARCHAR(50)
);
CREATE INDEX idx_fact_crop_disease ON disease_observation_fact(crop_key, disease_key);"""

    add_code_box(s9, Inches(0.6), Inches(1.6), Inches(12.1), Inches(4.3), sql_ddl)

    # Bottom Integrity Callout
    pill9 = create_card(s9, Inches(0.6), Inches(6.05), Inches(12.1), Inches(0.5), COLOR_GREEN_MINT, COLOR_GREEN_BDR, 1.0)
    tx_pill9 = s9.shapes.add_textbox(Inches(0.7), Inches(6.08), Inches(11.9), Inches(0.42))
    p_p9 = tx_pill9.text_frame.paragraphs[0]
    p_p9.text = "DATABASE INTEGRITY VERIFICATION: SQLite PRAGMA foreign_keys = 1 natively enforced via SQLAlchemy listener. Invalid foreign key insertion attempt natively raises sqlalchemy.exc.IntegrityError."
    p_p9.font.name = FONT_BODY
    p_p9.font.size = Pt(8.5)
    p_p9.font.bold = True
    p_p9.font.color.rgb = COLOR_GREEN_DEEP
    p_p9.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 10: CODE: PRODUCTION ETL PIPELINE (Template Slide 8)
    # =========================================================================
    s10 = prs.slides.add_slide(content_layout)
    set_title(s10, "Code: Production ETL Pipeline (Python & SQLAlchemy)")

    etl_py = """# Production ETL Pipeline (Extract -> Transform -> Dimension-First Load -> Idempotency Check)
from sqlalchemy import event, Engine
from src.warehouse.connection import get_db_session
from src.warehouse.models import DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact

# 1. Enforce Native SQLite Foreign Keys Connection Listener
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_conn, conn_record):
    if type(dbapi_conn).__module__.startswith('sqlite3'):
        cursor = dbapi_conn.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()

# 2. Dimension-First Loading & Idempotent Fact Insertion
def load_observation_facts(session, staged_data, batch_id):
    for item in staged_data['fact_records']:
        # Verify uniqueness to prevent duplicate insertion on repeated ETL runs
        existing = session.query(DiseaseObservationFact).filter_by(image_key=item['image_key']).first()
        if existing:
            load_stats['duplicates_skipped'] += 1
            continue
        fact = DiseaseObservationFact(
            crop_key=item['crop_key'], disease_key=item['disease_key'],
            image_key=item['image_key'], feature_key=item['feature_key'],
            observation_count=1, lesion_severity_score=item['lesion_severity_score'],
            image_sharpness_score=item['sharpness_score'], etl_batch_id=batch_id
        )
        session.add(fact)
    session.commit()  # Atomic transaction commit"""

    add_code_box(s10, Inches(0.6), Inches(1.6), Inches(12.1), Inches(4.3), etl_py)

    # Bottom ETL Verification Callout
    pill10 = create_card(s10, Inches(0.6), Inches(6.05), Inches(12.1), Inches(0.5), COLOR_GREEN_MINT, COLOR_GREEN_BDR, 1.0)
    tx_pill10 = s10.shapes.add_textbox(Inches(0.7), Inches(6.08), Inches(11.9), Inches(0.42))
    p_p10 = tx_pill10.text_frame.paragraphs[0]
    p_p10.text = "ETL VERIFICATION RESULT: 1st Run: 36 facts loaded  |  2nd Run: 0 inserted, 36 duplicates skipped (100% Idempotent). Referential Audit: 0 orphan foreign keys, 0 nulls, atomic rollback on exception."
    p_p10.font.name = FONT_BODY
    p_p10.font.size = Pt(8.5)
    p_p10.font.bold = True
    p_p10.font.color.rgb = COLOR_GREEN_DEEP
    p_p10.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 11: SQL-BACKED OLAP OPERATIONS ENGINE (Template Slide 6)
    # =========================================================================
    s11 = prs.slides.add_slide(content_layout)
    set_title(s11, "SQL-Backed OLAP Operations Engine")

    # 5 Cards for the 5 OLAP Operations
    ops = [
        ("Roll-up", "Observation -> Crop -> Crop Category",
         """SELECT c.crop_category,
  COUNT(f.observation_key) AS obs,
  ROUND(AVG(f.lesion_severity_score),2)
  AS avg_sev
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
GROUP BY c.crop_category;""",
         "Result: Cereal -> 36 Obs (Avg Sev: 3.57)"),

        ("True Drill-down", "Pathogen Type -> Disease Name",
         """SELECT d.pathogen_type,
  d.disease_name,
  COUNT(f.observation_key) AS obs,
  ROUND(AVG(f.lesion_severity_score),2)
  AS avg_sev
FROM disease_observation_fact f
JOIN dim_disease d ON f.disease_key
  = d.disease_key
GROUP BY d.pathogen_type,
  d.disease_name;""",
         "Result: Bacterial: 12 | Fungal: 24 (Brown Spot: 12, Leaf Smut: 12)"),

        ("Slice", "Crop = 'Rice'",
         """SELECT d.disease_name,
  COUNT(f.observation_key)
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key
  = d.disease_key
WHERE LOWER(c.crop_name) = 'rice'
GROUP BY d.disease_name;""",
         "Result: 2D Sub-Plane on Rice (36 Obs: 12 BLB, 12 BS, 12 LS)"),

        ("Dice", "Multi-Dimensional Sub-Cube",
         """SELECT c.crop_name, d.disease_name,
  COUNT(*)
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key
  = d.disease_key
JOIN dim_visual_feature vf ON
  f.feature_key = vf.feature_key
WHERE c.crop_name = 'Rice' AND
  vf.glcm_contrast >= 0.1
GROUP BY c.crop_name, d.disease_name;""",
         "Result: 36 Obs meeting criteria (GLCM Contrast >= 0.10)"),

        ("Pivot", "Rows: Crop x Cols: Pathogen Type",
         """SELECT c.crop_name,
  SUM(CASE WHEN d.pathogen_type
    = 'Fungal' THEN 1 ELSE 0 END)
    AS Fungal,
  SUM(CASE WHEN d.pathogen_type
    = 'Bacterial' THEN 1 ELSE 0 END)
    AS Bacterial
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key
  = d.disease_key
GROUP BY c.crop_name;""",
         "Result: Rice -> Fungal: 24, Bacterial: 12, Total: 36")
    ]

    c_w11 = Inches(2.28)
    gap11 = Inches(0.18)

    for i, (op_name, hierarchy, sql_code, out_summary) in enumerate(ops):
        left = Inches(0.6) + i * (c_w11 + gap11)
        # Card Background
        create_card(s11, left, Inches(1.6), c_w11, Inches(4.9), COLOR_CARD_BG, COLOR_BORDER, 1.0)

        # Header Block
        hdr = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.6), c_w11, Inches(0.55))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = COLOR_GREEN_DEEP
        hdr.line.color.rgb = COLOR_GREEN_DEEP
        p_h = hdr.text_frame.paragraphs[0]
        p_h.text = op_name
        p_h.font.name = FONT_BODY
        p_h.font.size = Pt(11)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_WHITE
        p_h.alignment = PP_ALIGN.CENTER

        # Hierarchy / Concept
        tx_c = s11.shapes.add_textbox(left + Inches(0.08), Inches(2.2), c_w11 - Inches(0.16), Inches(0.5))
        tf_c = tx_c.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = hierarchy
        p_c.font.name = FONT_BODY
        p_c.font.size = Pt(8.0)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_GREEN_CARD

        # SQL Code Snippet
        tx_code = s11.shapes.add_textbox(left + Inches(0.06), Inches(2.75), c_w11 - Inches(0.12), Inches(2.75))
        tf_code = tx_code.text_frame
        tf_code.word_wrap = True
        for line_idx, line in enumerate(sql_code.strip().split("\n")):
            p_l = tf_code.paragraphs[0] if line_idx == 0 else tf_code.add_paragraph()
            p_l.text = line
            p_l.font.name = FONT_CODE
            p_l.font.size = Pt(6.8)
            p_l.font.color.rgb = COLOR_TEXT_MAIN

        # Output Summary
        tx_out = s11.shapes.add_textbox(left + Inches(0.08), Inches(5.6), c_w11 - Inches(0.16), Inches(0.8))
        tf_out = tx_out.text_frame
        tf_out.word_wrap = True
        p_o = tf_out.paragraphs[0]
        p_o.text = out_summary
        p_o.font.name = FONT_BODY
        p_o.font.size = Pt(7.5)
        p_o.font.bold = True
        p_o.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 12: ACTUAL OLAP RESULTS FROM PHYSICAL WAREHOUSE
    # =========================================================================
    s12 = prs.slides.add_slide(content_layout)
    set_title(s12, "Actual OLAP Query Results from Physical Warehouse")

    # Table 1: Roll-up Results
    t12_1_headers = ["Crop Category", "Total Obs", "Crops", "Diseases", "Avg Severity", "Avg Contrast"]
    t12_1_rows = [
        ["Cereal", "36", "1", "3", "3.57", "0.3178"]
    ]
    create_table(s12, Inches(0.6), Inches(1.6), Inches(5.8), Inches(0.95), t12_1_headers, t12_1_rows, [Inches(1.3), Inches(0.8), Inches(0.7), Inches(0.9), Inches(1.0), Inches(1.1)])

    # Table 2: True Drill-down Results
    t12_2_headers = ["Pathogen Type", "Disease Diagnosis", "Obs Count", "Avg Severity", "Avg Contrast"]
    t12_2_rows = [
        ["Bacterial", "Bacterial Leaf Blight", "12", "3.67", "0.2131"],
        ["Fungal", "Brown Spot", "12", "3.94", "0.5599"],
        ["Fungal", "Leaf Smut", "12", "3.11", "0.1804"]
    ]
    create_table(s12, Inches(0.6), Inches(2.7), Inches(5.8), Inches(1.5), t12_2_headers, t12_2_rows, [Inches(1.2), Inches(1.7), Inches(0.9), Inches(1.0), Inches(1.0)])

    # Table 3: Pivot Results
    t12_3_headers = ["Crop", "Category", "Fungal", "Bacterial", "Viral", "Healthy*", "Total Obs"]
    t12_3_rows = [
        ["Rice", "Cereal", "24", "12", "0", "0", "36"]
    ]
    create_table(s12, Inches(0.6), Inches(4.35), Inches(5.8), Inches(0.95), t12_3_headers, t12_3_rows, [Inches(0.9), Inches(0.9), Inches(0.8), Inches(0.8), Inches(0.7), Inches(0.8), Inches(0.9)])

    # Footnote about Healthy baseline
    tx_fn = s12.shapes.add_textbox(Inches(0.6), Inches(5.35), Inches(5.8), Inches(0.4))
    p_fn = tx_fn.text_frame.paragraphs[0]
    p_fn.text = "*Healthy = 0 is intentional: the authentic ICAR research dataset comprises pathological specimens exclusively. HEALTHY is maintained in dim_disease as an unpopulated control baseline."
    p_fn.font.name = FONT_BODY
    p_fn.font.size = Pt(7.0)
    p_fn.font.color.rgb = COLOR_TEXT_MUTED

    # Right: OLAP Charts Picture
    olap_img = Path("assets/presentation/olap_visuals.png")
    if olap_img.exists():
        s12.shapes.add_picture(str(olap_img), Inches(6.6), Inches(1.6), Inches(6.1), Inches(3.4))

    # Bottom Right Card: Diagnostic Multi-Dimensional Breakdown
    c12_diag = create_card(s12, Inches(6.6), Inches(5.15), Inches(6.1), Inches(1.35), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.0)
    tx12_d = s12.shapes.add_textbox(Inches(6.8), Inches(5.2), Inches(5.7), Inches(1.2))
    tf12_d = tx12_d.text_frame
    tf12_d.word_wrap = True

    p = tf12_d.paragraphs[0]
    p.text = "DIAGNOSTIC MULTI-DIMENSIONAL BREAKDOWN (DRILL-ACROSS)"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_CARD

    p_d1 = tf12_d.add_paragraph()
    p_d1.text = "Crosses dimensional boundaries: Crop Category -> Crop -> Disease -> Dominant Visual Tone."
    p_d1.font.name = FONT_BODY
    p_d1.font.size = Pt(7.5)
    p_d1.font.color.rgb = COLOR_TEXT_MAIN

    p_d2 = tf12_d.add_paragraph()
    p_d2.text = "Result: Brown Spot (11 Yellowish, 1 Brown) | Bacterial Blight (8 Yellowish, 4 Brown) | Leaf Smut (7 Brown, 5 Yellowish). Correlates foliar tone with pathogen kingdom."
    p_d2.font.name = FONT_BODY
    p_d2.font.size = Pt(7.5)
    p_d2.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 13: DASHBOARD DEMONSTRATION, QUALITY AUDIT & NEXT PHASE
    # =========================================================================
    s13 = prs.slides.add_slide(content_layout)
    set_title(s13, "Dashboard Demonstration, Quality Audit & Next Phase")

    # Left: Dashboard UI Composite Picture
    dash_img = Path("assets/presentation/dashboard_composite.png")
    if dash_img.exists():
        s13.shapes.add_picture(str(dash_img), Inches(0.6), Inches(1.6), Inches(6.4), Inches(4.85))

    # Right Top: 56/56 Tests Passed Card
    c13_t = create_card(s13, Inches(7.2), Inches(1.6), Inches(5.5), Inches(4.85), COLOR_CARD_BG, COLOR_GREEN_BDR, 1.5)
    tx13_t = s13.shapes.add_textbox(Inches(7.4), Inches(1.75), Inches(5.1), Inches(4.5))
    tf13_t = tx13_t.text_frame
    tf13_t.word_wrap = True

    p_tst = tf13_t.paragraphs[0]
    p_tst.text = "56 / 56 TESTS PASSED"
    p_tst.font.name = FONT_TITLE
    p_tst.font.size = Pt(22)
    p_tst.font.bold = True
    p_tst.font.color.rgb = COLOR_GREEN_DEEP

    p_sub = tf13_t.add_paragraph()
    p_sub.text = "100% PASS RATE IN 2.87 SECONDS (pytest)"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(9.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEAL

    checks = [
        "Dataset Integrity: 36 authentic rice images verified",
        "Quality Gates: Corrupted, duplicate, tiny checks verified",
        "Feature Extraction: 34 descriptors in 44-column store",
        "Kimball Star Schema: 4 dimensions, 1 fact table deployed",
        "Database Integrity: Native SQLite PRAGMA foreign_keys = 1",
        "ETL Idempotency: 36 loaded Run 1, 0 inserted Run 2",
        "SQL OLAP Engine: Roll-up, Drill-down, Slice, Dice, Pivot",
        "Interactive Dashboard: Streamlit HTTP 200 OK verified"
    ]
    for chk in checks:
        p_c = tf13_t.add_paragraph()
        p_c.text = f"✓ {chk}"
        p_c.font.name = FONT_BODY
        p_c.font.size = Pt(7.8)
        p_c.font.color.rgb = COLOR_TEXT_MAIN

    p_rm = tf13_t.add_paragraph()
    p_rm.text = "\nNEXT PHASE (REVIEW 2 ROADMAP):"
    p_rm.font.name = FONT_BODY
    p_rm.font.size = Pt(10.5)
    p_rm.font.bold = True
    p_rm.font.color.rgb = COLOR_DARK

    roadmap_items = [
        "Unsupervised Visual Pattern Mining: K-Means foliar clustering",
        "Optimal Cluster Evaluation: Silhouette analysis & Davies-Bouldin",
        "Association Rule Mining: Apriori / FP-Growth discovering rules between macroscopic textures and microscopic pathologies."
    ]
    for item in roadmap_items:
        p_r = tf13_t.add_paragraph()
        p_r.text = f"• {item}"
        p_r.font.name = FONT_BODY
        p_r.font.size = Pt(7.5)
        p_r.font.color.rgb = COLOR_TEXT_MAIN

    p_close = tf13_t.add_paragraph()
    p_close.text = '\n"AgroVision-Mine transforms agricultural image observations from classification inputs into multidimensional analytical knowledge."'
    p_close.font.name = FONT_TITLE
    p_close.font.size = Pt(9.5)
    p_close.font.bold = True
    p_close.font.color.rgb = COLOR_GREEN_DEEP

    # =========================================================================
    # SAVE PRESENTATION
    # =========================================================================
    output_filename = "AgroVision-Mine_Review1_Final_Presentation.pptx"
    prs.save(output_filename)
    print(f"\n=======================================================")
    print(f"SUCCESS: Generated {output_filename} (13 slides)!")
    print(f"=======================================================\n")

if __name__ == "__main__":
    build_presentation()
