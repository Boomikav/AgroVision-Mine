"""
AgroVision-Mine: Complete Final Project Review Presentation Builder
Generates AgroVision-Mine_Complete_Final_Project_Review.pptx
"""

import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE ---
DARK_GREEN = RGBColor(27, 67, 50)      # #1B4332 Primary Brand Dark Green
FOREST_GREEN = RGBColor(45, 106, 79)    # #2D6A4F Medium Forest Green
MINT_ACCENT = RGBColor(116, 198, 157)   # #74C69D Mint Green Accent
MINT_TINT = RGBColor(216, 243, 220)     # #D8F3DC Light Green Card / Badge
CARD_BG = RGBColor(248, 249, 250)       # #F8F9FA Off-white / Neutral Gray Card
CARD_WHITE = RGBColor(255, 255, 255)    # #FFFFFF Pure White
BORDER_GRAY = RGBColor(220, 225, 230)   # #DCE1E6 Subtle Border
TEXT_MAIN = RGBColor(26, 26, 26)        # #1A1A1A Main Body Text
TEXT_MUTED = RGBColor(90, 100, 110)     # #5A646E Muted Text
TEXT_WHITE = RGBColor(255, 255, 255)    # #FFFFFF White
AMBER_WARN = RGBColor(180, 83, 9)       # Warning Amber
NAVY_BLUE = RGBColor(30, 58, 138)       # Deep Navy Accent
CARD_DARK = RGBColor(28, 28, 28)        # Charcoal Dark Card (Code / DDL)

FONT_TITLE = "Bookman Old Style"
FONT_BODY = "Bookman Old Style"
FONT_CODE = "Consolas"

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def create_blank_slide(prs):
    blank_layout = prs.slide_layouts[6]
    return prs.slides.add_slide(blank_layout)


def add_slide_header(slide, title_text, category_tag="CSI3010: DATA WAREHOUSING & DATA MINING"):
    # Category Tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.3))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_tag.upper()
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = FOREST_GREEN

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = DARK_GREEN


def add_slide_footer(slide, slide_num, total_slides=24):
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_GRAY
    line.line.color.rgb = BORDER_GRAY

    foot_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.0), Inches(0.3))
    tf_l = foot_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "AgroVision-Mine: Multimodal Data Warehouse & Visual Pattern Mining Framework"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = TEXT_MUTED

    foot_right = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.033), Inches(0.3))
    tf_r = foot_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"{slide_num} / {total_slides}"
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(9.5)
    p_r.font.bold = True
    p_r.font.color.rgb = FOREST_GREEN


def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_GRAY):
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, height
    )
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card


def add_bullet_point(tf, bold_prefix, text, pt_size=12, bold_color=DARK_GREEN, text_color=TEXT_MAIN, space_after=6):
    p = tf.add_paragraph() if tf.paragraphs and tf.paragraphs[0].text else tf.paragraphs[0]
    p.space_after = Pt(space_after)
    if bold_prefix:
        r1 = p.add_run()
        r1.text = bold_prefix + " "
        r1.font.name = FONT_BODY
        r1.font.bold = True
        r1.font.size = Pt(pt_size)
        r1.font.color.rgb = bold_color
    r2 = p.add_run()
    r2.text = text
    r2.font.name = FONT_BODY
    r2.font.size = Pt(pt_size)
    r2.font.color.rgb = text_color


def add_table(slide, left, top, width, height, rows, cols, col_widths=None):
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    if col_widths:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w
    return table


def format_table_header(table, cols, headers, bg_color=DARK_GREEN, text_color=TEXT_WHITE):
    for col_idx in range(cols):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
        p = cell.text_frame.paragraphs[0]
        p.text = headers[col_idx]
        p.font.name = FONT_BODY
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = text_color
        p.alignment = PP_ALIGN.CENTER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE


def populate_table_row(table, row_idx, values, is_even=False, pt_size=10.5, aligns=None):
    bg = CARD_BG if is_even else CARD_WHITE
    for col_idx, val in enumerate(values):
        cell = table.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg
        p = cell.text_frame.paragraphs[0]
        p.text = str(val)
        p.font.name = FONT_BODY
        p.font.size = Pt(pt_size)
        p.font.color.rgb = TEXT_MAIN
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if aligns and col_idx < len(aligns):
            p.alignment = aligns[col_idx]
        else:
            p.alignment = PP_ALIGN.LEFT


# ==============================================================================
# SLIDE BUILDERS (SLIDES 1 TO 24)
# ==============================================================================

def build_slide_1(prs):
    """Slide 1: Professional Title Slide"""
    slide = create_blank_slide(prs)

    # Top accent header band
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.25))
    band.fill.solid()
    band.fill.fore_color.rgb = FOREST_GREEN
    band.line.fill.background()

    # Main Card
    add_card(slide, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5), bg_color=CARD_WHITE, border_color=BORDER_GRAY)

    # Inner decorative bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.6), Inches(1.5), Inches(0.15), Inches(2.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_GREEN
    bar.line.fill.background()

    # Title Box
    tbox = slide.shapes.add_textbox(Inches(1.9), Inches(1.4), Inches(9.8), Inches(2.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "AgroVision-Mine"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = DARK_GREEN
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "A Multimodal Data Warehouse and Visual Pattern Mining Framework\nfor Crop Disease and Pest Intelligence"
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(17)
    p2.font.color.rgb = FOREST_GREEN
    p2.space_after = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = "DATA WAREHOUSING & DATA MINING (CSI3010) — FINAL LAB PROJECT REVIEW"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = AMBER_WARN

    # Metadata Card (Lower half)
    add_card(slide, Inches(1.6), Inches(3.9), Inches(10.133), Inches(2.2), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    mbox = slide.shapes.add_textbox(Inches(1.9), Inches(4.05), Inches(9.5), Inches(1.9))
    mtf = mbox.text_frame
    mtf.word_wrap = True

    mp1 = mtf.paragraphs[0]
    mp1.text = "PROJECT TEAM DETAILS & ACADEMIC SUPERVISION"
    mp1.font.name = FONT_BODY
    mp1.font.size = Pt(13)
    mp1.font.bold = True
    mp1.font.color.rgb = DARK_GREEN
    mp1.space_after = Pt(8)

    mp2 = mtf.add_paragraph()
    mp2.text = "• Team Members:  Boomika V (23MID0326)   |   Ajay M (23MID0020)"
    mp2.font.name = FONT_BODY
    mp2.font.size = Pt(13.5)
    mp2.font.bold = True
    mp2.font.color.rgb = TEXT_MAIN
    mp2.space_after = Pt(6)

    mp3 = mtf.add_paragraph()
    mp3.text = "• Faculty Guide:  Dr. Devipriya A      • Lab Slot:  L41 + L42      • Academic Term:  Fall 2026-27"
    mp3.font.name = FONT_BODY
    mp3.font.size = Pt(12.5)
    mp3.font.color.rgb = FOREST_GREEN
    mp3.space_after = Pt(6)

    mp4 = mtf.add_paragraph()
    mp4.text = "• Department:  School of Computer Science and Engineering (SCOPE), VIT University"
    mp4.font.name = FONT_BODY
    mp4.font.size = Pt(11.5)
    mp4.font.color.rgb = TEXT_MUTED


def build_slide_2(prs):
    """Slide 2: Executive Summary"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Executive Summary: The Multimodal Analytical Bridge")
    add_slide_footer(slide, 2)

    # Left Column: Problem & Implemented Solution
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CORE CHALLENGE & IMPLEMENTED WORK"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(10)

    add_bullet_point(tf, "• Agricultural Data Fragmentation:", "Standard foliar image datasets reside in disconnected flat folders, lacking multidimensional taxonomy, referential integrity, and verifiable quality controls.")
    add_bullet_point(tf, "• Multimodal Data Warehousing:", "Engineered Ralph Kimball's Star Schema in SQLite with 1 Fact table and 4 Dimensions, enabling SQL-backed OLAP aggregation across 2,596 authentic specimens.")
    add_bullet_point(tf, "• Explainable Feature Engineering:", "Extracted 32 continuous morphological, textural (GLCM), and color moment descriptors into a 44-column feature store.")
    add_bullet_point(tf, "• Unsupervised Visual Mining:", "Fitted K-Means clustering (K=2 metric-supported, K=4 exploratory) and mined 880 visual association rules via Apriori and FP-Growth.")
    add_bullet_point(tf, "• Scientific Verification:", "104 automated tests (94 unit/integration + 10 Playwright browser tests across all 9 pages) pass with 100% cryptographic dataset hash invariance.")

    # Right Column: System Highlights & Scientific Boundary
    add_card(slide, Inches(6.8), Inches(1.5), Inches(5.733), Inches(3.2), bg_color=CARD_WHITE)
    tbox_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(2.8))
    tf_r = tbox_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "VERIFIED SYSTEM ARCHITECTURE OUTPUTS"
    pr0.font.name = FONT_BODY
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = DARK_GREEN
    pr0.space_after = Pt(8)

    add_bullet_point(tf_r, "• Frozen Canonical Dataset:", "2,596 authentic images across 14 crops (1,750 diseased, 846 healthy; PlantDoc: 2,560, ICAR/OGD: 36).")
    add_bullet_point(tf_r, "• Dimensional OLAP Engine:", "Roll-up, Drill-down, Slice, Dice, and Pivot queries executed in <10ms via parameterized SQL.")
    add_bullet_point(tf_r, "• Interactive Web Workbench:", "Production React 18 + TypeScript GUI + FastAPI asynchronous backend with live image similarity retrieval.")

    # Lower Right Card: Epistemological Boundary Disclaimer
    add_card(slide, Inches(6.8), Inches(4.9), Inches(5.733), Inches(1.8), bg_color=MINT_TINT, border_color=FOREST_GREEN)
    tbox_warn = slide.shapes.add_textbox(Inches(7.0), Inches(5.05), Inches(5.333), Inches(1.5))
    tf_w = tbox_warn.text_frame
    tf_w.word_wrap = True

    pw0 = tf_w.paragraphs[0]
    pw0.text = "SCIENTIFIC POSITIONING & METHODOLOGICAL BOUNDARY"
    pw0.font.name = FONT_BODY
    pw0.font.size = Pt(11.5)
    pw0.font.bold = True
    pw0.font.color.rgb = DARK_GREEN
    pw0.space_after = Pt(4)

    add_bullet_point(tf_w, "• Exploratory Mining Only:", "The system provides visual pattern clustering and reference specimen retrieval. It does NOT claim automated biological disease diagnosis.", pt_size=11, space_after=4)
    add_bullet_point(tf_w, "• Supervised Classification:", "Formally evaluated and rejected as unsupported due to single-condition crop confounding and class imbalance.", pt_size=11, space_after=0)


def build_slide_3(prs):
    """Slide 3: Research Motivation & Problem Statement"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Research Motivation: The Agricultural Data Gap")
    add_slide_footer(slide, 3)

    # Left Card: Limitations of Current Approaches
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.7), Inches(4.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(3.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "LIMITATIONS OF CONVENTIONAL APPROACHES"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(10)

    add_bullet_point(tf, "• Isolated Point Classifiers:", "Standard deep learning (CNNs/YOLO) treats foliar images as single-image black boxes without historical lineage or multi-attribute queryability.")
    add_bullet_point(tf, "• Metadata Fragmentation:", "Agronomic taxonomy, host plant varieties, acquisition modalities, and disease stages are trapped in disparate CSVs or directory paths.")
    add_bullet_point(tf, "• Absence of Quality Audits:", "Raw web corpora contain duplicate files, corrupted image headers, and uncalibrated aspect ratios that distort feature models.")
    add_bullet_point(tf, "• Lack of Dimensional Slicing:", "Agronomists cannot perform multi-attribute SQL drill-downs (e.g., comparing fungal vs bacterial texture across crop types).")

    # Right Card: The AgroVision-Mine Solution
    add_card(slide, Inches(6.8), Inches(1.5), Inches(5.733), Inches(4.2), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    tbox_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(3.8))
    tf_r = tbox_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "THE AGROVISION-MINE MULTIMODAL SOLUTION"
    pr0.font.name = FONT_BODY
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = DARK_GREEN
    pr0.space_after = Pt(10)

    add_bullet_point(tf_r, "• Kimball Star-Schema Warehouse:", "Integrates image technical metadata, botanical taxonomy, and visual metrics into a relational fact table with enforced foreign keys.")
    add_bullet_point(tf_r, "• Automated ETL Quality Gates:", "Validates byte headers, eliminates duplicate records via MD5 hashing, and enforces 256x256 RGB normalization.")
    add_bullet_point(tf_r, "• Explainable Computer Vision Descriptors:", "Color moments, Haralick GLCM textures, and morphometry provide transparent physical features instead of opaque hidden weights.")
    add_bullet_point(tf_r, "• Multi-Angle OLAP & Association Mining:", "Enables agronomists to slice observation cubes by host crop, disease severity, and textural co-occurrence patterns.")

    # Bottom Full-Width Banner: Research Question
    add_card(slide, Inches(0.8), Inches(5.9), Inches(11.733), Inches(0.9), bg_color=DARK_GREEN, border_color=None)
    tbox_bot = slide.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.8))
    tf_b = tbox_bot.text_frame
    tf_b.word_wrap = True
    pb = tf_b.paragraphs[0]
    pb.text = "CORE RESEARCH QUESTION: How can multimodal foliar observations and explainable visual features be integrated into an audited dimensional data warehouse to enable SQL OLAP analytics and unsupervised visual pattern discovery without misleading diagnostic overclaims?"
    pb.font.name = FONT_BODY
    pb.font.size = Pt(12)
    pb.font.bold = True
    pb.font.color.rgb = TEXT_WHITE


def build_slide_4(prs):
    """Slide 4: Implemented Objectives & Deliverables Mapping"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Project Objectives & Implemented Deliverables")
    add_slide_footer(slide, 4)

    # Table layout mapping Objectives -> Implemented Module -> Verified Artifact
    col_widths = [Inches(0.6), Inches(3.4), Inches(4.0), Inches(3.733)]
    table = add_table(slide, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2), 7, 4, col_widths)

    format_table_header(table, 4, ["#", "Objective & Scope", "Implemented Component / Logic", "Verified System Deliverable"])

    rows = [
        ("1", "Data Governance & Ingestion", "Ingest 2,596 specimens across 14 crops with SHA-256 cryptographic immutability", "canonical_dataset_v2.csv\n(c7fd16dc... invariant)"),
        ("2", "Automated Quality Gates", "5 validation gates: byte headers, formats, dimensions, duplicates, EXIF transpose", "5 quality gates verified;\nZero corrupt images ingested"),
        ("3", "Explainable Feature Store", "Extract 32 continuous descriptors (19 Color, 7 GLCM Texture, 6 Morphometry)", "image_features_v2.csv\n(44 columns, 2,596 rows)"),
        ("4", "Dimensional Data Warehouse", "Kimball Star Schema with SQLite PRAGMA foreign_keys = 1 enforced via SQLAlchemy", "agrovision_warehouse.db\n(1 Fact + 4 Dimension tables)"),
        ("5", "SQL-Backed OLAP Engine", "Parameterized SQL engine supporting Roll-up, Drill-down, Slice, Dice, Pivot", "Interactive OLAP Console;\nLatency <10ms per query"),
        ("6", "Unsupervised Visual Mining", "Dual-K K-Means clustering (K=2, K=4), 2D PCA, and Apriori / FP-Growth rule mining", "880 Mode A rules (parity Δ=0);\nK=2 Silhouette = 0.4060"),
    ]

    for idx, r in enumerate(rows):
        populate_table_row(table, idx + 1, r, is_even=(idx % 2 == 1), pt_size=10.5, aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])


def build_slide_5(prs):
    """Slide 5: Dataset Evolution, Provenance & Reconciliation"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Dataset Provenance: Reconciling Review 1 & Current Scope")
    add_slide_footer(slide, 5)

    # Left Column: Critical Reconciliation Explanation
    add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CRITICAL DATASET RECONCILIATION & LINEAGE"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(8)

    add_bullet_point(tf, "• Review 1 Baseline (36 Images):", "The initial prototype utilized 36 authentic rice pathology images from ICAR / Open Government Data (OGD) across 3 diseases (Bacterial Leaf Blight, Brown Spot, Leaf Smut) and healthy specimens. This subset forms the physical baseline for the relational warehouse (database/agrovision_warehouse.db).")
    add_bullet_point(tf, "• Current Frozen Dataset (2,596 Images):", "Expanded to 2,596 authentic specimens across 14 crops, sourced from PlantDoc (2,560 field images) + ICAR/OGD (36 studio scans). Frozen in data/manifests/canonical_dataset_v2.csv.")
    add_bullet_point(tf, "• Reconciliation of Tomato Count:", "Documented draft notes cited 736 vs 743. Verified that the frozen manifest contains exactly 743 Tomato records (736 was an uncurated pre-freeze draft totaling 2,668 records).")
    add_bullet_point(tf, "• Cryptographic Invariance:", "SHA-256 digests verified 100% invariant before and after all analytical executions, uploads, and automated test runs.")

    # Right Column: Distribution Table & Cryptographic Badges
    add_card(slide, Inches(7.1), Inches(1.5), Inches(5.433), Inches(5.2), bg_color=CARD_WHITE)
    rtbox = slide.shapes.add_textbox(Inches(7.3), Inches(1.7), Inches(5.033), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "CANONICAL TAXONOMIC DISTRIBUTION (N=2,596)"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(6)

    # Insert a mini-table inside right column
    table = add_table(slide, Inches(7.2), Inches(2.1), Inches(5.2), Inches(3.2), 9, 3, [Inches(2.2), Inches(1.5), Inches(1.5)])
    format_table_header(table, 3, ["Crop Species", "Record Count", "Percentage"])
    t_rows = [
        ("Tomato", "743", "28.62%"),
        ("Corn", "372", "14.33%"),
        ("Apple", "272", "10.48%"),
        ("Potato", "216", "8.32%"),
        ("Grape & Bell Pepper", "265 (133 + 132)", "10.20%"),
        ("Squash & Raspberry", "249 (130 + 119)", "9.59%"),
        ("Blueberry, Peach, Strawb.", "321 (114+111+96)", "12.36%"),
        ("Soybean, Cherry, Rice", "158 (65+57+36)", "6.09%"),
    ]
    for idx, tr in enumerate(t_rows):
        populate_table_row(table, idx + 1, tr, is_even=(idx % 2 == 1), pt_size=9.5, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER])

    # Summary cards below table
    add_card(slide, Inches(7.2), Inches(5.45), Inches(5.2), Inches(1.1), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    stbox = slide.shapes.add_textbox(Inches(7.3), Inches(5.5), Inches(5.0), Inches(1.0))
    stf = stbox.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "Condition Split: 1,750 Diseased (67.4%) | 846 Healthy (32.6%)\nSources: PlantDoc (2,560, 98.6%) | ICAR/OGD (36, 1.4%)\nManifest SHA-256: c7fd16dc...1cb8 (Verified Invariant)"
    sp1.font.name = FONT_BODY
    sp1.font.size = Pt(10)
    sp1.font.bold = True
    sp1.font.color.rgb = DARK_GREEN


def build_slide_6(prs):
    """Slide 6: Complete System Architecture"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "End-to-End System Architecture & Data Flow")
    add_slide_footer(slide, 6)

    # 4 Architecture Stage Cards across top/middle
    stages = [
        ("1. INGESTION & GATES", "• Ingests 2,596 images\n• 5 validation gates\n• Rejects corrupt bytes\n• MD5 deduplication", CARD_WHITE, DARK_GREEN),
        ("2. PREPROCESSING", "• 256x256 RGB resize\n• EXIF auto-transpose\n• RGBA canvas composite\n• Zero dataset mutation", CARD_WHITE, FOREST_GREEN),
        ("3. FEATURE STORE", "• 32 continuous features\n• Color moments (19)\n• Haralick GLCM (7)\n• Morphometry (6)", CARD_WHITE, NAVY_BLUE),
        ("4. WAREHOUSE & ETL", "• Kimball Star Schema\n• SQLite 3 database\n• Dimension-first load\n• 100% idempotent", CARD_WHITE, DARK_GREEN),
    ]

    card_width = Inches(2.75)
    gap = Inches(0.24)
    start_left = Inches(0.8)

    for i, (title, desc, bg, title_col) in enumerate(stages):
        l = start_left + i * (card_width + gap)
        add_card(slide, l, Inches(1.5), card_width, Inches(2.2), bg_color=bg, border_color=BORDER_GRAY)
        tbox = slide.shapes.add_textbox(l + Inches(0.15), Inches(1.65), card_width - Inches(0.3), Inches(1.9))
        tf = tbox.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_BODY
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = title_col
        p0.space_after = Pt(6)

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = TEXT_MAIN

    # Middle / Lower Architecture Tier (Engines & Presentation)
    add_card(slide, Inches(0.8), Inches(3.9), Inches(5.74), Inches(2.8), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    tbox_l = slide.shapes.add_textbox(Inches(1.0), Inches(4.05), Inches(5.34), Inches(2.5))
    tf_l = tbox_l.text_frame
    tf_l.word_wrap = True
    pl0 = tf_l.paragraphs[0]
    pl0.text = "5. ANALYTICAL MINING & OLAP ENGINES"
    pl0.font.name = FONT_BODY
    pl0.font.size = Pt(13)
    pl0.font.bold = True
    pl0.font.color.rgb = DARK_GREEN
    pl0.space_after = Pt(6)

    add_bullet_point(tf_l, "• SQL OLAP Engine:", "Executes parameterized Roll-up, Drill-down, Slice, Dice, and Pivot queries (<10ms).")
    add_bullet_point(tf_l, "• Dual-K K-Means Clustering:", "K=2 metric-supported (Silhouette=0.4060) and K=4 exploratory subpartition.")
    add_bullet_point(tf_l, "• 2D PCA Projection:", "Explains 52.11% variance (PC1=38.56%, PC2=13.55%).")
    add_bullet_point(tf_l, "• Association Mining:", "FP-Growth & Apriori produce 880 identical Mode A rules.")

    add_card(slide, Inches(6.78), Inches(3.9), Inches(5.75), Inches(2.8), bg_color=CARD_WHITE, border_color=BORDER_GRAY)
    tbox_r = slide.shapes.add_textbox(Inches(7.0), Inches(4.05), Inches(5.35), Inches(2.5))
    tf_r = tbox_r.text_frame
    tf_r.word_wrap = True
    pr0 = tf_r.paragraphs[0]
    pr0.text = "6. API & INTERACTIVE PRESENTATION TIER"
    pr0.font.name = FONT_BODY
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = DARK_GREEN
    pr0.space_after = Pt(6)

    add_bullet_point(tf_r, "• FastAPI Asynchronous Backend:", "9 RESTful endpoints delivering JSON telemetry for health, dataset, OLAP, and mining.")
    add_bullet_point(tf_r, "• React 18 + TypeScript GUI:", "Stitch-engineered 9-page responsive dashboard with interactive data exploration.")
    add_bullet_point(tf_r, "• Image Analysis Workbench:", "Real-time in-memory specimen extraction and reference Euclidean distance retrieval.")
    add_bullet_point(tf_r, "• Playwright Browser Automation:", "10 end-to-end automated tests driving system Chrome.")


def build_slide_7(prs):
    """Slide 7: Technology Stack & Architectural Rationale"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Technology Stack & Architectural Rationale")
    add_slide_footer(slide, 7)

    col_widths = [Inches(2.2), Inches(2.2), Inches(4.0), Inches(3.333)]
    table = add_table(slide, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2), 9, 4, col_widths)

    format_table_header(table, 4, ["Technology / Library", "Layer / Module", "Functional Implementation Role", "Architectural Rationale"])

    rows = [
        ("Python 3.11", "Core Runtime", "ETL pipeline, feature extraction, mining engines", "High performance, robust scientific computing ecosystem"),
        ("NumPy & Pandas", "Data Processing", "Vectorized calculations, 44-col feature store", "Fast matrix operations and tabular data transformation"),
        ("Pillow & OpenCV", "Image Engineering", "EXIF transposition, color conversion, contour geometry", "Robust multi-format decoding and geometric shape extraction"),
        ("scikit-image & sklearn", "Machine Learning", "GLCM gray-level matrix, StandardScaler, K-Means, PCA", "Gold-standard reproducible implementations of classical CV & ML"),
        ("mlxtend", "Pattern Mining", "Apriori & FP-Growth frequent itemset / rule generation", "Enables exact parity comparison between mining algorithms"),
        ("SQLite & SQLAlchemy", "Data Warehouse", "Kimball Star Schema with PRAGMA foreign_keys = 1", "Lightweight, zero-config ACID-compliant relational warehouse"),
        ("FastAPI", "API Backend", "Asynchronous REST endpoints for all analytical services", "Low-latency JSON serialization, automated OpenAPI documentation"),
        ("React 18 & TypeScript", "Frontend GUI", "Interactive 9-page responsive analytical dashboard", "Component-driven modularity with strict type-safety checks"),
    ]

    for idx, r in enumerate(rows):
        populate_table_row(table, idx + 1, r, is_even=(idx % 2 == 1), pt_size=10, aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])


def build_slide_8(prs):
    """Slide 8: Data Quality Gates & Preprocessing Pipeline"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Data Quality & Preprocessing: 5 Automated Gates")
    add_slide_footer(slide, 8)

    # Left Column: The 5 Gates
    add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "THE 5 AUTOMATED DATA QUALITY GATES"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(8)

    add_bullet_point(tf, "• Gate 1: Byte Header & Format Gate:", "Validates binary Magic Bytes. Rejects truncated streams and unsupported formats (.txt, .exe) with HTTP 400.")
    add_bullet_point(tf, "• Gate 2: Dimension & Aspect Ratio Gate:", "Enforces minimum resolution (100x100 px) and rejects extreme distortion (aspect ratio > 5.0).")
    add_bullet_point(tf, "• Gate 3: File Payload Limit Gate:", "Enforces a strict 15 MB payload ceiling to prevent denial-of-service memory exhaustion.")
    add_bullet_point(tf, "• Gate 4: Cryptographic Deduplication Gate:", "Calculates MD5 content digests to detect exact duplicate images regardless of file renaming.")
    add_bullet_point(tf, "• Gate 5: Channel & Orientation Normalization:", "Applies PIL ImageOps.exif_transpose for smartphone photos, composites RGBA onto white canvas, and resizes to 256x256 RGB.")

    # Right Column: Visual Evidence Asset + Diagnostic Summary
    add_card(slide, Inches(7.1), Inches(1.5), Inches(5.433), Inches(5.2), bg_color=CARD_WHITE)
    img_path = "data/reports/pptx_extracted_assets/slide_5_img_5.png"
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(7.2), Inches(1.6), width=Inches(5.233))

    add_card(slide, Inches(7.2), Inches(4.7), Inches(5.233), Inches(1.85), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    tbox_sub = slide.shapes.add_textbox(Inches(7.35), Inches(4.8), Inches(4.933), Inches(1.65))
    tf_s = tbox_sub.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = "CONTROLLED DIAGNOSTIC EDGE HARNESS AUDIT\n• 100% Rejection of Corrupt Diagnostic Fixtures: Truncated bytes, corrupt headers, unsupported extensions, and empty files reliably rejected.\n• Authentic Dataset Standardization: All 2,596 images standardized to 256x256 RGB with zero channel drops or orientation distortion."
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(10)
    p_s.font.bold = True
    p_s.font.color.rgb = DARK_GREEN


def build_slide_9(prs):
    """Slide 9: Explainable Feature Engineering (44-Column Store)"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Feature Engineering: 32 Continuous Descriptors")
    add_slide_footer(slide, 9)

    # 3 Cards for the 3 Feature Families
    families = [
        ("COLOR MOMENTS (19 FEATURES)", "• RGB Channel Means & Std Devs\n• Normalized RGB Color Means\n• HSV Hue, Saturation, Value Means\n• Excess Green Index (ExG = 2G - R - B)\n\nAgronomic Significance: Quantifies foliar chlorosis, yellowing, and necrotic spot discoloration.", Inches(0.8)),
        ("GLCM TEXTURE (7 FEATURES)", "• Contrast (local intensity variation)\n• Dissimilarity (gray-level difference)\n• Homogeneity (subtle smoothness)\n• Energy & Angular Second Moment (ASM)\n• Correlation (linear dependency)\n\nAgronomic Significance: Measures surface roughness, pustule mottling, and tissue degradation.", Inches(4.8)),
        ("MORPHOMETRIC SHAPE (6 FEATURES)", "• Contour Area & Perimeter\n• Circularity (4π·Area / Perimeter²)\n• Bounding Box Aspect Ratio\n• Extent (Area / Bounding Box Area)\n• Lesion Coverage Area Ratio\n\nAgronomic Significance: Captures boundary regularity and spot structural geometries.", Inches(8.8)),
    ]

    for title, desc, l in families:
        add_card(slide, l, Inches(1.5), Inches(3.733), Inches(4.1), bg_color=CARD_WHITE)
        tbox = slide.shapes.add_textbox(l + Inches(0.15), Inches(1.65), Inches(3.433), Inches(3.8))
        tf = tbox.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_BODY
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = DARK_GREEN
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = TEXT_MAIN

    # Bottom Full-Width Feature Store Summary Card
    add_card(slide, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.0), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    tbox_bot = slide.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(11.333), Inches(0.8))
    tf_b = tbox_bot.text_frame
    tf_b.word_wrap = True
    pb = tf_b.paragraphs[0]
    pb.text = "ANALYTICAL FEATURE STORE STRUCTURE (data/features/image_features_v2.csv)\n• 44 Total Columns: Exactly 32 continuous numerical features used by K-Means & PCA + 12 metadata columns (image_id, filename, crop_name, disease_name, condition, pathogen_type, split, dataset_source, dimensions)."
    pb.font.name = FONT_BODY
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = DARK_GREEN


def build_slide_10(prs):
    """Slide 10: Algorithm Selection & Rationale Matrix"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Algorithm Selection: Technical Rationale Matrix")
    add_slide_footer(slide, 10)

    col_widths = [Inches(1.8), Inches(2.2), Inches(3.6), Inches(2.2), Inches(1.933)]
    table = add_table(slide, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2), 7, 5, col_widths)

    format_table_header(table, 5, ["Algorithm / Technique", "Input Vector", "Why Selected (Rationale)", "Output Representation", "Limitations Disclosed"])

    rows = [
        ("StandardScaler", "32 continuous features", "Normalizes feature scales (z = (x-μ)/σ), preventing high-magnitude contour biases", "Standardized 32D matrix (μ=0, σ=1)", "Assumes Gaussian-like bell curves"),
        ("K-Means Clustering", "32 standardized features", "Discovers unsupervised structural groupings of foliar morphology; tested K=2 to 8", "Cluster labels (K=2 primary, K=4 exploratory)", "Groups visual appearance, NOT etiology"),
        ("PCA Projection", "32 standardized features", "Reduces 32D space to 2 principal components explaining 52.11% total variance", "2D orthogonal scatter coordinates (PC1, PC2)", "Linear projection loses 47.89% residual variance"),
        ("Apriori Mining", "12 discretized features", "Exhaustive level-wise breadth-first search for frequent visual itemsets", "Frequent itemsets and association rules", "Exponential candidate generation overhead"),
        ("FP-Growth Mining", "12 discretized features", "Compressed FP-Tree eliminates candidate generation; exact parity with Apriori", "Exact 880 Mode A rules (parity Δ = 0.00000000)", "Tree construction memory footprint"),
        ("Nearest Neighbors", "32D Euclidean metric", "Ranks authentic reference specimens by visual feature distance: d = ||zq - zr||2", "Ranked reference matches with distances", "Proximity index 1/(1+d) is uncalibrated"),
    ]

    for idx, r in enumerate(rows):
        populate_table_row(table, idx + 1, r, is_even=(idx % 2 == 1), pt_size=10, aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])


def build_slide_11(prs):
    """Slide 11: Data Warehouse Design & Kimball Star Schema"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Data Warehouse Design: Kimball Star Schema")
    add_slide_footer(slide, 11)

    # Left Column: Star Schema Diagram Image
    img_path = "data/reports/pptx_extracted_assets/slide_7_img_1.png"
    if os.path.exists(img_path):
        add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=CARD_WHITE)
        slide.shapes.add_picture(img_path, Inches(0.9), Inches(1.6), width=Inches(5.8))
    else:
        add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=MINT_TINT)

    # Right Column: Schema Details & Grain
    add_card(slide, Inches(7.1), Inches(1.5), Inches(5.433), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(7.3), Inches(1.7), Inches(5.033), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PHYSICAL STAR SCHEMA SPECIFICATION"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(8)

    add_bullet_point(tf, "• Central Fact Table:", "disease_observation_fact (Grain: Exactly ONE row per validated leaf specimen observation).")
    add_bullet_point(tf, "• Additive / Semi-Additive Measures:", "observation_count (1), lesion_severity_score (continuous 0.0–1.0), image_sharpness_score.")
    add_bullet_point(tf, "• Dimension 1 (dim_crop):", "Botanical Host hierarchy (crop_key, crop_name, botanical_name, crop_category).")
    add_bullet_point(tf, "• Dimension 2 (dim_disease):", "Pathology taxonomy (disease_key, disease_name, pathogen_type, causal_agent, primary_symptom).")
    add_bullet_point(tf, "• Dimension 3 (dim_image):", "Acquisition technical metadata (image_key, raw_id, file_format, dimensions, size_kb).")
    add_bullet_point(tf, "• Dimension 4 (dim_visual_feature):", "Extracted continuous features (feature_key, color moments, GLCM textures, morphometry).")


def build_slide_12(prs):
    """Slide 12: Production ETL Architecture & Idempotency"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Production ETL Pipeline: Dimension-First Loading")
    add_slide_footer(slide, 12)

    # Left Column: ETL Flow & Code
    add_card(slide, Inches(0.8), Inches(1.5), Inches(6.2), Inches(5.2), bg_color=CARD_DARK)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.8), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "# PRODUCTION ETL WORKFLOW (Extract -> Transform -> Load)"
    p0.font.name = FONT_CODE
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = MINT_ACCENT
    p0.space_after = Pt(6)

    code_lines = [
        "with engine.begin() as conn:",
        "    # 1. Enforce SQLite Foreign Key Pragma natively",
        "    conn.execute(text('PRAGMA foreign_keys = ON;'))",
        "",
        "    # 2. Dimension-First Loading (Idempotent Natural Keys)",
        "    crop_key = load_dim_crop(conn, row['crop_name'])",
        "    disease_key = load_dim_disease(conn, row['disease'])",
        "    image_key = load_dim_image(conn, row['metadata'])",
        "    feature_key = load_dim_features(conn, row['features'])",
        "",
        "    # 3. Fact Table Ingestion with Deduplication",
        "    stmt = insert(disease_observation_fact).values(",
        "        crop_key=crop_key, disease_key=disease_key,",
        "        image_key=image_key, feature_key=feature_key,",
        "        lesion_severity_score=row['severity']",
        "    ).prefix_with('OR IGNORE')",
        "    conn.execute(stmt)",
    ]
    for cl in code_lines:
        p = tf.add_paragraph()
        p.text = cl
        p.font.name = FONT_CODE
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right Column: Idempotency & Verification Result
    add_card(slide, Inches(7.3), Inches(1.5), Inches(5.233), Inches(5.2), bg_color=CARD_WHITE)
    rtbox = slide.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.833), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "VERIFIED ETL EXECUTION AUDIT"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(13)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(8)

    add_bullet_point(rtf, "• Strict Idempotency (100%):", "1st Run: 36 facts loaded into warehouse. 2nd Run: 0 inserted, 36 duplicates skipped cleanly.")
    add_bullet_point(rtf, "• Dimension-First Loading:", "Prevents foreign key orphan insertion errors by populating reference dimensions prior to fact records.")
    add_bullet_point(rtf, "• Transaction Atomicity:", "Utilizes SQLAlchemy context managers (engine.begin()) ensuring complete rollback upon any parsing error.")
    add_bullet_point(rtf, "• Zero Referential Drift:", "Verified that 100% of fact foreign keys resolve to valid dimension primary keys.")


def build_slide_13(prs):
    """Slide 13: Database Integrity & Data Governance Audit"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Data Governance & Integrity Verification")
    add_slide_footer(slide, 13)

    # 4 Governance Metric Cards
    metrics = [
        ("0.00% NULLS", "Zero null values across all primary keys, foreign keys, and 32 continuous descriptors.", DARK_GREEN, MINT_TINT),
        ("0 DUPLICATES", "100% deduplication via composite natural key and MD5 image content hashing.", FOREST_GREEN, CARD_WHITE),
        ("100% FK INTEGRITY", "PRAGMA foreign_keys = 1 enforced. Zero orphan fact rows detected.", NAVY_BLUE, CARD_WHITE),
        ("100% HASH INVARIANT", "Canonical manifest & feature store SHA-256 digests perfectly preserved.", DARK_GREEN, MINT_TINT),
    ]

    card_w = Inches(2.75)
    gap = Inches(0.24)
    for i, (m_title, m_desc, t_col, bg) in enumerate(metrics):
        l = Inches(0.8) + i * (card_w + gap)
        add_card(slide, l, Inches(1.5), card_w, Inches(2.0), bg_color=bg, border_color=BORDER_GRAY)
        tbox = slide.shapes.add_textbox(l + Inches(0.15), Inches(1.65), card_w - Inches(0.3), Inches(1.7))
        tf = tbox.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = m_title
        p0.font.name = FONT_BODY
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = t_col
        p0.space_after = Pt(6)

        p1 = tf.add_paragraph()
        p1.text = m_desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = TEXT_MAIN

    # Lower Table: Detailed Audit Evidence
    col_widths = [Inches(3.2), Inches(2.6), Inches(2.6), Inches(3.333)]
    table = add_table(slide, Inches(0.8), Inches(3.8), Inches(11.733), Inches(2.9), 5, 4, col_widths)

    format_table_header(table, 4, ["Audit Check", "Expected Threshold", "Measured Result", "Status & Evidence"])
    t_rows = [
        ("SQLite Foreign Key Constraints", "100% Enforced (PRAGMA=1)", "0 Violations", "PASS (Verified via SQLAlchemy listeners)"),
        ("Fact Table Primary Key Uniqueness", "100% Unique observation_key", "36 Unique PKs", "PASS (Zero orphan or duplicate rows)"),
        ("Feature Store Column Completeness", "44 Required Columns", "44 Columns Present", "PASS (Zero missing feature fields)"),
        ("Cryptographic Dataset Immutability", "Exact SHA-256 match", "c7fd...1cb8 & f6ca...093c1", "PASS (Zero post-run file mutations)"),
    ]
    for idx, tr in enumerate(t_rows):
        populate_table_row(table, idx + 1, tr, is_even=(idx % 2 == 1), pt_size=10, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT])


def build_slide_14(prs):
    """Slide 14: SQL-Backed OLAP Methodology"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "SQL-Backed OLAP Operations Engine")
    add_slide_footer(slide, 14)

    # Top Row: Roll-up & Drill-down
    ops_top = [
        ("1. ROLL-UP (Hierarchical Aggregation)",
         "Ascends hierarchy: Observation -> Crop -> Crop Category.\n"
         "SQL: SELECT c.crop_category, COUNT(f.observation_key) AS obs, ROUND(AVG(f.lesion_severity_score),2) AS avg_sev\n"
         "     FROM disease_observation_fact f JOIN dim_crop c USING(crop_key) GROUP BY c.crop_category;\n"
         "Agronomic Insight: Aggregates disease severity to macroeconomic host crop categories.",
         Inches(0.8), Inches(1.5), Inches(5.7), Inches(2.5)),
        ("2. DRILL-DOWN (Hierarchical Decomposition)",
         "Descends hierarchy: Crop Category -> Pathology Diagnosis -> Specific Pathogen.\n"
         "SQL: SELECT d.disease_name, d.pathogen_type, COUNT(f.observation_key) AS obs, ROUND(AVG(f.lesion_severity_score),2) AS avg_sev\n"
         "     FROM disease_observation_fact f JOIN dim_disease d USING(disease_key) GROUP BY d.disease_name;\n"
         "Agronomic Insight: Decomposes broad foliar symptoms into specific bacterial and fungal agents.",
         Inches(6.8), Inches(1.5), Inches(5.733), Inches(2.5)),
    ]
    for title, desc, l, t, w, h in ops_top:
        add_card(slide, l, t, w, h, bg_color=CARD_WHITE)
        tbox = slide.shapes.add_textbox(l + Inches(0.15), t + Inches(0.15), w - Inches(0.3), h - Inches(0.3))
        tf = tbox.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = DARK_GREEN
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = TEXT_MAIN

    # Bottom Row: Slice, Dice, Pivot
    ops_bot = [
        ("3A. SLICE (Single Dimension)",
         "Filters strictly on 1 dimension: WHERE crop_name = 'Rice'.\n"
         "SQL: SELECT c.crop_name, COUNT(f.observation_key) AS obs, ROUND(AVG(f.lesion_severity_score),2) AS avg_sev FROM disease_observation_fact f JOIN dim_crop c USING(crop_key) WHERE c.crop_name = 'Rice';\n"
         "Agronomic Value: Isolates host-specific baseline specimens for staple cereal disease analysis.",
         Inches(0.8), Inches(4.2), Inches(3.7), Inches(2.5)),
        ("3B. DICE (Multi-Dimension Sub-Cube)",
         "Filters across 2+ dimensions: WHERE crop IN ('Tomato','Corn') AND pathogen = 'Fungal'.\n"
         "SQL: SELECT c.crop_name, d.disease_name, ROUND(AVG(f.lesion_severity_score),2) FROM disease_observation_fact f JOIN dim_crop c USING(crop_key) JOIN dim_disease d USING(disease_key) WHERE c.crop_name IN ('Tomato','Corn') AND d.pathogen_type = 'Fungal';\n"
         "Agronomic Value: Compares cross-crop fungal vulnerability in commercial row crops.",
         Inches(4.8), Inches(4.2), Inches(3.7), Inches(2.5)),
        ("4. PIVOT (Cross-Tabulation Rotation)",
         "Cross-tabulates Crop Species (rows) vs Severity Tiers (columns).\n"
         "Matrix: Low Severity (<0.30), Moderate (0.30–0.60), Severe (>0.60).\n"
         "Agronomic Value: Exposes structural damage distribution across distinct host plant taxa in a compact 2D reporting matrix.",
         Inches(8.8), Inches(4.2), Inches(3.733), Inches(2.5)),
    ]
    for title, desc, l, t, w, h in ops_bot:
        add_card(slide, l, t, w, h, bg_color=CARD_WHITE)
        tbox = slide.shapes.add_textbox(l + Inches(0.15), t + Inches(0.15), w - Inches(0.3), h - Inches(0.3))
        tf = tbox.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = DARK_GREEN
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.0)
        p1.font.color.rgb = TEXT_MAIN


def build_slide_15(prs):
    """Slide 15: Actual OLAP Query Results from Physical Warehouse"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Physical Warehouse: Actual OLAP Query Outputs")
    add_slide_footer(slide, 15)

    # Left Column: OLAP Output Chart or Screenshot
    img_path = "data/reports/pptx_extracted_assets/slide_12_img_5.png"
    if os.path.exists(img_path):
        add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=CARD_WHITE)
        slide.shapes.add_picture(img_path, Inches(0.9), Inches(1.7), width=Inches(5.8))
    else:
        add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=MINT_TINT)

    # Right Column: Actual Result Tables
    add_card(slide, Inches(7.1), Inches(1.5), Inches(5.433), Inches(5.2), bg_color=CARD_WHITE)
    rtbox = slide.shapes.add_textbox(Inches(7.3), Inches(1.65), Inches(5.033), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "ACTUAL QUERY OUTPUTS & DRILL-DOWN BREAKDOWN"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(6)

    table = add_table(slide, Inches(7.2), Inches(2.1), Inches(5.2), Inches(2.6), 6, 4, [Inches(1.8), Inches(1.3), Inches(1.1), Inches(1.0)])
    format_table_header(table, 4, ["Disease Name", "Pathogen", "Obs Count", "Avg Sev"])
    t_rows = [
        ("Bacterial Leaf Blight", "Bacterial", "12", "0.41"),
        ("Brown Spot", "Fungal", "12", "0.33"),
        ("Leaf Smut", "Fungal", "12", "0.27"),
        ("Healthy Baseline*", "Unknown", "0*", "0.00"),
        ("Overall Rice Cohort", "Total", "36", "0.34"),
    ]
    for idx, tr in enumerate(t_rows):
        populate_table_row(table, idx + 1, tr, is_even=(idx % 2 == 1), pt_size=9.5, aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER])

    # Caveat Card below table
    add_card(slide, Inches(7.2), Inches(4.9), Inches(5.2), Inches(1.6), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    ctbox = slide.shapes.add_textbox(Inches(7.3), Inches(5.0), Inches(5.0), Inches(1.4))
    ctf = ctbox.text_frame
    ctf.word_wrap = True
    cp = ctf.paragraphs[0]
    cp.text = "*Agronomic Note on Baseline: Healthy=0 in the physical ICAR baseline is intentional, as the original repository collection comprises verified pathological specimens exclusively. HEALTHY is modeled as an active dimension member to ensure zero-schema-change extensibility."
    cp.font.name = FONT_BODY
    cp.font.size = Pt(9.5)
    cp.font.color.rgb = DARK_GREEN


def build_slide_16(prs):
    """Slide 16: Visual Pattern Mining: Clustering Evaluation"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Visual Pattern Mining: Dual-K Clustering Evaluation")
    add_slide_footer(slide, 16)

    # Left Column: Metrics & Evaluation Table
    add_card(slide, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.6), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "MULTI-K EVALUATION ON 32 STANDARDIZED FEATURES"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(6)

    table = add_table(slide, Inches(0.9), Inches(2.1), Inches(5.8), Inches(2.6), 6, 4, [Inches(1.0), Inches(1.6), Inches(1.6), Inches(1.6)])
    format_table_header(table, 4, ["K Value", "Silhouette (↑)", "Davies-Bouldin (↓)", "Calinski-Harabasz (↑)"])
    t_rows = [
        ("K = 2 (Best)", "0.4060", "1.0990", "1,154.38"),
        ("K = 3", "0.1821", "1.7629", "820.65"),
        ("K = 4 (Subpart)", "0.1651", "1.8339 / 1.6210*", "674.33"),
        ("K = 5", "0.1623", "1.7326", "589.29"),
        ("K = 6", "0.1648", "1.6312", "529.40"),
    ]
    for idx, tr in enumerate(t_rows):
        populate_table_row(table, idx + 1, tr, is_even=(idx % 2 == 1), pt_size=9.5, aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER])

    # Text explanation below table
    tbox_bot = slide.shapes.add_textbox(Inches(0.9), Inches(4.8), Inches(5.8), Inches(1.8))
    tf_b = tbox_bot.text_frame
    tf_b.word_wrap = True
    add_bullet_point(tf_b, "• K=2 Supported Solution:", "Cluster 0 (2,150 images, 82.8%) vs Cluster 1 (446 images, 17.2%). Distinguishes dark, dense foliage from high-luminance, pale backgrounds.", pt_size=10, space_after=3)
    add_bullet_point(tf_b, "• Reconciling K=4 DB Index:", "*Authoritative multi-K evaluation calculates DB=1.8339 on the full 32-feature matrix; 1.6210 was recorded in an exploratory subpartition report.", pt_size=10, space_after=3)
    add_bullet_point(tf_b, "• Multi-Seed Stability:", "Pairwise Adjusted Rand Index ARI = 1.0000 across seeds [0, 1, 42, 100, 999].", pt_size=10, space_after=0)

    # Right Column: Visual Mining Screenshot
    img_path = "data/reports/browser_screenshots/07_visual_mining.png"
    if os.path.exists(img_path):
        add_card(slide, Inches(7.1), Inches(1.5), Inches(5.433), Inches(5.2), bg_color=CARD_WHITE)
        slide.shapes.add_picture(img_path, Inches(7.2), Inches(1.6), width=Inches(5.233))
    else:
        add_card(slide, Inches(7.1), Inches(1.5), Inches(5.433), Inches(5.2), bg_color=MINT_TINT)


def build_slide_17(prs):
    """Slide 17: PCA and Exploratory 2D Projection"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Dimensionality Reduction: 2D PCA Loadings Analysis")
    add_slide_footer(slide, 17)

    # Left Column: PCA Explained Variance & Physical Loadings
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "2D PCA PROJECTION LOADINGS & VARIANCE"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(8)

    add_bullet_point(tf, "• Cumulative Explained Variance:", "52.11% across 2 principal components (PC1 = 38.56%, PC2 = 13.55%). Sufficient to visualize global cluster geometry.")
    add_bullet_point(tf, "• Physical Interpretation of PC1 (38.56%):", "Strongly positive on foliar luminance (rgb_r_mean, rgb_g_mean, hsv_v_mean) and strongly negative on contour perimeter and greenness. Distinguishes pale chlorotic/scanner images from dense green leaves.")
    add_bullet_point(tf, "• Physical Interpretation of PC2 (13.55%):", "Strongly positive on GLCM contrast and dissimilarity, strongly negative on GLCM homogeneity and energy. Captures surface mottling, necrotic lesions, and texture roughness.")
    add_bullet_point(tf, "• Epistemological Boundary:", "PCA is an unsupervised orthogonal linear transformation. It illustrates macroscopic geometric separation but cannot establish biological pathology.")

    # Right Column: Loadings Table & Cluster Placement
    add_card(slide, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.2), bg_color=CARD_WHITE)
    rtbox = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "EMPIRICAL COMPONENT LOADINGS TABLE"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(6)

    table = add_table(slide, Inches(6.95), Inches(2.1), Inches(5.4), Inches(2.3), 4, 4, [Inches(1.2), Inches(1.1), Inches(1.55), Inches(1.55)])
    format_table_header(table, 4, ["Component", "Variance", "Top Positive Loading", "Top Negative Loading"])
    t_rows = [
        ("PC1", "38.56%", "rgb_r_mean (+0.252)\nglcm_asm (+0.248)", "perimeter (-0.231)\nhsv_s_mean (-0.219)"),
        ("PC2", "13.55%", "glcm_contrast (+0.384)\ndissimilarity (+0.379)", "homogeneity (-0.362)\nglcm_energy (-0.315)"),
        ("Total 2D", "52.11%", "Covers 16.6x of single-feature baseline", "Orthogonal 2D Space"),
    ]
    for idx, tr in enumerate(t_rows):
        populate_table_row(table, idx + 1, tr, is_even=(idx % 2 == 1), pt_size=9.0, aligns=[PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT])

    # Lower placement card
    add_card(slide, Inches(6.95), Inches(4.6), Inches(5.4), Inches(1.95), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    tbox_plc = slide.shapes.add_textbox(Inches(7.1), Inches(4.7), Inches(5.1), Inches(1.75))
    tf_p = tbox_plc.text_frame
    tf_p.word_wrap = True
    pp1 = tf_p.paragraphs[0]
    pp1.text = "CLUSTER DISTRIBUTIONS & SOURCE DOMAIN SHIFT\n• Cluster 0 (N=2,150): Centered around negative PC1 / moderate PC2 (dense in-field PlantDoc foliar imagery).\n• Cluster 1 (N=446): High positive PC1 space. 32 of 36 ICAR Rice scans map here due to white scanner background reflection."
    pp1.font.name = FONT_BODY
    pp1.font.size = Pt(9.5)
    pp1.font.bold = True
    pp1.font.color.rgb = DARK_GREEN


def build_slide_18(prs):
    """Slide 18: Association-Rule Mining: Visual vs Label-Conditioned"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Association Rule Mining: Mode A vs Mode B")
    add_slide_footer(slide, 18)

    # Left Column: Mode A (Visual Only)
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "MODE A: VISUAL-ONLY UNSUPERVISED MINING"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(6)

    add_bullet_point(tf, "• Input Discretization:", "Equal-frequency tertile binning (Low, Medium, High) across 12 explainable visual descriptors.")
    add_bullet_point(tf, "• Declared Baseline Thresholds:", "Min Support = 0.15 (15.0%), Min Confidence = 0.60 (60.0%), Min Lift = 1.0.")
    add_bullet_point(tf, "• Algorithmic Parity (FP-Growth vs Apriori):", "Both algorithms produce exactly 223 frequent itemsets and 880 rules. Maximum absolute metric difference Δ = 0.00000000.")
    add_bullet_point(tf, "• Representative Rule 1:", "glcm_contrast_High AND contour_perimeter_High → glcm_energy_Low\n(Support = 0.1506, Confidence = 0.8728, Lift = 4.2429).")
    add_bullet_point(tf, "• Representative Rule 2:", "contour_perimeter_High AND glcm_energy_Low → glcm_contrast_High\n(Support = 0.1506, Confidence = 0.8907, Lift = 4.2270).")

    # Right Column: Mode B (Label Conditioned)
    add_card(slide, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.2), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    rtbox = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "MODE B: LABEL-CONDITIONED EXPLORATORY MINING"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(6)

    add_bullet_point(rtf, "• Purpose & Transaction Matrix:", "Appends condition status (Healthy, Diseased) and pathogen type to visual items for exploratory pattern inspection.")
    add_bullet_point(rtf, "• Reconciling Rule Counts (285 vs 276 vs 272):", "At 0.15 support / 0.60 confidence, Mode B generates 285 total rules. The default dashboard filter (lift ≥ 1.0) displays 276 rules. The historical 272 count was an earlier draft subset omitting condition-only rules.")
    add_bullet_point(rtf, "• Representative Rule:", "condition_Healthy AND contour_perimeter_Low → contour_circularity_High AND pathogen_Unknown\n(Support = 0.1529, Confidence = 0.9636, Lift = 6.0132).")
    add_bullet_point(rtf, "• Critical Causality Disclaimer:", "Association rules capture statistical co-occurrences in the current labeled collection. They do NOT establish biological or pathological causation.")


def build_slide_19(prs):
    """Slide 19: Image Analysis Workbench"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Image Analysis & Inference Workbench")
    add_slide_footer(slide, 19)

    # Left Column: Image Analysis Screenshot
    img_path = "data/reports/browser_screenshots/03_image_analysis.png"
    if os.path.exists(img_path):
        add_card(slide, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2), bg_color=CARD_WHITE)
        slide.shapes.add_picture(img_path, Inches(0.9), Inches(1.6), width=Inches(6.3))
    else:
        add_card(slide, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2), bg_color=MINT_TINT)

    # Right Column: Workflow & Distance Disclaimers
    add_card(slide, Inches(7.6), Inches(1.5), Inches(4.933), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(7.8), Inches(1.7), Inches(4.533), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "WORKBENCH INGESTION & INFERENCE FLOW"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(6)

    add_bullet_point(tf, "1. In-Memory Ingestion:", "Uploaded images (JPG/PNG) are validated, EXIF-transposed, and resized to 256x256 without persisting to frozen dataset files.")
    add_bullet_point(tf, "2. Real-Time Feature Extraction:", "Extracts 32 continuous descriptors in <150ms. Supports interactive toggling between Raw and Standardized values.")
    add_bullet_point(tf, "3. Fitted Cluster Projection:", "Assigns specimen into fitted K=2 and K=4 models using saved reference scalers and centroids.")
    add_bullet_point(tf, "4. Nearest Reference Retrieval:", "Calculates 32D standardized Euclidean distance against all 2,596 authentic reference specimens.")
    add_bullet_point(tf, "5. Strict Diagnostic Disclaimer:", "Prominent UI warning: Visual similarity does NOT constitute disease diagnosis. Proximity index 1/(1+d) is an uncalibrated geometric heuristic.")


def build_slide_20(prs):
    """Slide 20: Interactive Dashboard: Stitch Interface Walkthrough"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Interactive Dashboard: React 18 + TypeScript GUI")
    add_slide_footer(slide, 20)

    # 4 Page Showcase Tiles (2x2 Grid)
    pages = [
        ("DATASET EXPLORER (/dataset)", "data/reports/browser_screenshots/02_dataset_explorer.png", "Card Grid and Table views; case-insensitive crop filters (Tomato = 743); modal specimen detail inspection."),
        ("DATA WAREHOUSE SCHEMA (/warehouse)", "data/reports/browser_screenshots/05_warehouse.png", "Star schema topology; Central Observation Fact Table badge; relational foreign key integrity cards."),
        ("OLAP ANALYTICS CONSOLE (/olap)", "data/reports/browser_screenshots/06_olap_analytics.png", "Interactive SQL execution for Roll-up, Drill-down, Slice (Crop), Dice (Crop x Pathogen), Pivot (Crop x Severity)."),
        ("ASSOCIATION RULES (/association-rules)", "data/reports/browser_screenshots/08_association_rules.png", "Mode A (880 rules) and Mode B (276 filtered rules) with interactive support/confidence slider adjustments."),
    ]

    card_w = Inches(5.7)
    card_h = Inches(2.5)

    positions = [
        (Inches(0.8), Inches(1.5)),
        (Inches(6.8), Inches(1.5)),
        (Inches(0.8), Inches(4.2)),
        (Inches(6.8), Inches(4.2)),
    ]

    for (p_title, p_img, p_desc), (l, t) in zip(pages, positions):
        add_card(slide, l, t, card_w, card_h, bg_color=CARD_WHITE)
        if os.path.exists(p_img):
            slide.shapes.add_picture(p_img, l + Inches(0.15), t + Inches(0.4), width=Inches(3.0))
        tbox = slide.shapes.add_textbox(l + Inches(3.25), t + Inches(0.2), card_w - Inches(3.4), card_h - Inches(0.3))
        tf = tbox.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = p_title
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = DARK_GREEN
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = p_desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = TEXT_MAIN


def build_slide_21(prs):
    """Slide 21: Testing, Validation & Reproducibility"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Testing & Validation: Multi-Tier Verification")
    add_slide_footer(slide, 21)

    # Top Banner: 104 Passing Tests
    add_card(slide, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.0), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    tbox_top = slide.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(0.8))
    tf_top = tbox_top.text_frame
    tf_top.word_wrap = True
    pt = tf_top.paragraphs[0]
    pt.text = "104 AUTOMATED TESTS PASSED (100% SUCCESS RATE, 0 FAILURES, 1 DEPRECATION WARNING)\nRigorous separation into 4 distinct verification tiers ensures end-to-end reproducibility."
    pt.font.name = FONT_BODY
    pt.font.size = Pt(13)
    pt.font.bold = True
    pt.font.color.rgb = DARK_GREEN

    # 4 Verification Tiers Table
    col_widths = [Inches(2.5), Inches(2.2), Inches(3.5), Inches(3.533)]
    table = add_table(slide, Inches(0.8), Inches(2.7), Inches(11.733), Inches(4.0), 5, 4, col_widths)

    format_table_header(table, 4, ["Verification Tier", "Test Count / Scope", "Key Behaviors Tested", "Observed Outcome & Evidence"])

    rows = [
        ("Automated Unit & Integration", "94 Tests (pytest)", "ETL idempotency, GLCM textures, SQLite FK constraints, clustering reproducibility", "94 / 94 Passed in 34.12s\n(Starlette httpx warning)"),
        ("Real Browser Testing (Playwright)", "10 Tests (Playwright)", "Drove local Google Chrome across all 9 pages; filters, modal inspect, image upload/replace", "10 / 10 Passed in 31.70s;\n9 screenshots captured"),
        ("API Smoke & Contract Tests", "9 Endpoints (FastAPI)", "Health, overview, dataset (Tomato=743), schema, OLAP SQL, clustering, rules, analyze", "9 / 9 Live Endpoints 200 OK;\nZero HTTP 500 exceptions"),
        ("Production Build Compilation", "Vite + TypeScript", "Full production bundle compilation (tsc -b && vite build) of 31 modules", "Built in 677ms (0 errors);\nAssets: CSS (39kB), JS (354kB)"),
    ]

    for idx, r in enumerate(rows):
        populate_table_row(table, idx + 1, r, is_even=(idx % 2 == 1), pt_size=10, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT])


def build_slide_22(prs):
    """Slide 22: Performance Metrics and Evaluation"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "System Performance: Software & Mining Telemetry")
    add_slide_footer(slide, 22)

    col_widths = [Inches(2.8), Inches(2.2), Inches(3.4), Inches(3.333)]
    table = add_table(slide, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2), 7, 4, col_widths)

    format_table_header(table, 4, ["Performance Benchmark", "Measured Telemetry", "Measurement Environment & Scope", "Evaluation Assessment"])

    rows = [
        ("OLAP Analytical Query Latency", "< 10 ms per query", "SQLite relational warehouse, parameterized SQL aggregation across 2,596 rows", "Real-time interactive dashboard responsiveness"),
        ("Single-Image Extraction Latency", "~120 ms per image", "In-memory decoding, 256x256 resizing, 32 continuous descriptors extracted", "Rapid feedback loop for live specimen workbench"),
        ("K-Means Clustering Runtime", "0.18 seconds", "Scikit-learn K-Means on 2,596 x 32 standardized matrix (K=2 to 8)", "Fast retrainability and parameter tuning"),
        ("Frequent Pattern Mining Runtime", "FP-Growth: 0.066s\nApriori: 0.012s", "12 discretized features, min_support=0.15, min_confidence=0.60 (880 rules)", "Sub-second execution; exact metric parity"),
        ("Complete Test Suite Execution", "65.82 seconds", "104 automated tests (94 pytest unit/integration + 10 Playwright browser tests)", "CI/CD-ready rapid verification cycle"),
        ("Supervised Classification Accuracy", "NOT REPORTED\n(Scientifically Unsupported)", "Formal feasibility audit: dataset exhibits severe taxonomic confounding and imbalance", "Honest academic stance: visual pattern mining retained"),
    ]

    for idx, r in enumerate(rows):
        populate_table_row(table, idx + 1, r, is_even=(idx % 2 == 1), pt_size=10, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT])


def build_slide_23(prs):
    """Slide 23: Impact, Scientific Limitations & Feasibility Evaluation"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Impact, Feasibility Evaluation & Scientific Scope")
    add_slide_footer(slide, 23)

    # Left Column: Practical Impact & Use Cases
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PRACTICAL VALUE & USE CASES"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(8)

    add_bullet_point(tf, "• Research Image Cataloging:", "Provides agricultural extension services and universities with a structured Kimball warehouse for multimodal image collections.")
    add_bullet_point(tf, "• Quality Assurance for Agronomic Datasets:", "Automated quality gates prevent corrupt, distorted, or duplicate images from contaminating research archives.")
    add_bullet_point(tf, "• Multi-Angle OLAP Slicing:", "Allows researchers to query foliar severity distributions across botanical families, pathogen types, and acquisition settings.")
    add_bullet_point(tf, "• Reference Specimen Retrieval:", "Enables field workers to retrieve visually similar historical specimens with transparent 32D distance metrics.")

    # Right Column: Why Supervised Classification is Unsupported
    add_card(slide, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.2), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    rtbox = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "WHY SUPERVISED CLASSIFICATION IS UNSUPPORTED"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(8)

    add_bullet_point(rtf, "1. Taxonomic Shortcut Confounding:", "7 crops are 100% healthy-only (Blueberry, Raspberry, Peach, Strawberry, Soybean, Cherry) and 1 crop is 100% diseased-only (Squash). Classifiers learn leaf morphology, NOT disease.")
    add_bullet_point(rtf, "2. Extreme Class Imbalance:", "Support ranges from N=190 (Corn Blight) down to N=2 (Tomato Spider Mite). 8 classes have <20 specimens, making stratified 3-way train/val/test splits statistically unviable.")
    add_bullet_point(rtf, "3. Cross-Source Domain Shift:", "Rice (N=36) is from studio flatbed scanners (ICAR), while 2,560 images are in-field smartphone photos (PlantDoc). Sensor artifacts dominate visual features.")
    add_bullet_point(rtf, "4. Representational Limits:", "Global color/texture moments lack localized spatial attention required for clinical pathology diagnosis.")


def build_slide_24(prs):
    """Slide 24: Conclusion & Live Demonstration Plan"""
    slide = create_blank_slide(prs)
    add_slide_header(slide, "Conclusion & Live Demonstration Plan")
    add_slide_footer(slide, 24)

    # Left Column: Project Conclusion & Contributions
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2), bg_color=CARD_WHITE)
    tbox = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PROJECT CONTRIBUTIONS & KEY TAKEAWAYS"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DARK_GREEN
    p0.space_after = Pt(8)

    add_bullet_point(tf, "• Transformed Unstructured Images into Relational Warehouse:", "Successfully integrated 2,596 multimodal observations into a Kimball Star Schema with ACID referential integrity.")
    add_bullet_point(tf, "• Explainable Feature Engineering:", "Replaced black-box embeddings with 32 transparent morphological, textural (GLCM), and color moment descriptors.")
    add_bullet_point(tf, "• Dual-K Clustering & Parity-Validated Rules:", "Discovered robust visual clusters (K=2 Silhouette=0.4060) and 880 exact-parity association rules across FP-Growth and Apriori.")
    add_bullet_point(tf, "• Methodological Honesty:", "Transparently disclosed data sparsity and rejected unsupported disease classification claims in favor of verified pattern mining.")

    # Right Column: Live Demonstration Plan (Viva Sequence)
    add_card(slide, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.2), bg_color=MINT_TINT, border_color=MINT_ACCENT)
    rtbox = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.8))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "LIVE DEMONSTRATION WORKFLOW (VIVA ROADMAP)"
    rp0.font.name = FONT_BODY
    rp0.font.size = Pt(13)
    rp0.font.bold = True
    rp0.font.color.rgb = DARK_GREEN
    rp0.space_after = Pt(8)

    add_bullet_point(rtf, "Step 1 — Overview & Data Quality Gates:", "Showcase live KPIs (2,596 specimens, 14 crops) and 5 automated quality gates (/overview, /data-quality).")
    add_bullet_point(rtf, "Step 2 — Dataset Explorer & Filtering:", "Demonstrate card grid / table views, search queries, and crop filter (Tomato = 743 items) (/dataset).")
    add_bullet_point(rtf, "Step 3 — Warehouse Schema & OLAP Console:", "Inspect relational tables and execute parameterized Roll-up, Drill-down, Slice, Dice, Pivot (/warehouse, /olap).")
    add_bullet_point(rtf, "Step 4 — Visual Mining & PCA Scatter:", "Showcase dual-K clustering metrics, PCA 2D projections, and cluster profiles (/visual-mining).")
    add_bullet_point(rtf, "Step 5 — Association Rule Controls:", "Demonstrate Mode A (880 rules) and Mode B (276 filtered rules) with interactive slider tuning (/association-rules).")
    add_bullet_point(rtf, "Step 6 — Live Specimen Analysis:", "Upload authentic leaf image; demonstrate 32-feature extraction, cluster assignment, and nearest neighbor retrieval (/image-analysis).")


# ==============================================================================
# MAIN GENERATOR FUNCTION
# ==============================================================================

def main():
    print("Initializing AgroVision-Mine Final Presentation Builder...")
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    builders = [
        build_slide_1,
        build_slide_2,
        build_slide_3,
        build_slide_4,
        build_slide_5,
        build_slide_6,
        build_slide_7,
        build_slide_8,
        build_slide_9,
        build_slide_10,
        build_slide_11,
        build_slide_12,
        build_slide_13,
        build_slide_14,
        build_slide_15,
        build_slide_16,
        build_slide_17,
        build_slide_18,
        build_slide_19,
        build_slide_20,
        build_slide_21,
        build_slide_22,
        build_slide_23,
        build_slide_24,
    ]

    for idx, builder in enumerate(builders):
        print(f"Building Slide {idx + 1}...")
        builder(prs)

    output_path = "AgroVision-Mine_Complete_Final_Project_Review.pptx"
    prs.save(output_path)
    print(f"\nPresentation successfully created and saved to: {output_path}")
    print(f"Total Slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()
