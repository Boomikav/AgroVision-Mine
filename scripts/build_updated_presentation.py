"""AgroVision-Mine: Master Slide Generator Script.
Builds the complete 28-slide presentation matching TermiteSense visual standards.
"""
import os
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Colors
COLOR_DARK_GREEN = RGBColor(0x17, 0x5D, 0x44)   # Primary brand / headers
COLOR_FOREST     = RGBColor(0x2D, 0x6A, 0x4F)   # Secondary accent / kicker
COLOR_NAVY       = RGBColor(0x1F, 0x4E, 0x79)   # Deep Slate Blue (TermiteSense match)
COLOR_AMBER      = RGBColor(0xB4, 0x53, 0x09)   # Warning / accent
COLOR_RED        = RGBColor(0x93, 0x00, 0x0A)   # Negative / alert
COLOR_DARK_TEXT  = RGBColor(0x1C, 0x1C, 0x1C)   # Charcoal primary text
COLOR_MUTED_TEXT = RGBColor(0x4B, 0x55, 0x63)   # Secondary slate text
COLOR_FOOTER     = RGBColor(0x6B, 0x72, 0x80)   # Footers & page numbers
COLOR_CARD_BG    = RGBColor(0xF7, 0xF6, 0xEF)   # Warm botanical off-white
COLOR_CARD_BORDER= RGBColor(0xD1, 0xD5, 0xDB)   # Clean subtle border
COLOR_GREEN_BG   = RGBColor(0xE0, 0xF2, 0xE8)   # Light green card fill
COLOR_AMBER_BG   = RGBColor(0xFF, 0xF8, 0xE1)   # Light amber card fill
COLOR_AMBER_BORDER = RGBColor(0xFF, 0xE0, 0x82) # Amber card border
COLOR_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)   # Pure white

FONT_TITLE = "Book Antiqua"
FONT_BODY = "Book Antiqua"
FONT_CODE = "Consolas"
TOTAL_SLIDES = 28

ROOT_DIR = Path(__file__).resolve().parent.parent
INSPECT_DIR = ROOT_DIR / "data" / "reports" / "presentation_inspection"
SCREENSHOT_DIR = ROOT_DIR / "data" / "reports" / "browser_screenshots"


def init_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    return prs


def add_header(slide, title, kicker="CSI3010: DATA WAREHOUSING & DATA MINING"):
    tb_kicker = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.73), Inches(0.25))
    tf_kicker = tb_kicker.text_frame
    tf_kicker.word_wrap = True
    tf_kicker.margin_left = tf_kicker.margin_top = tf_kicker.margin_right = tf_kicker.margin_bottom = 0
    p_k = tf_kicker.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = FONT_TITLE
    p_k.font.size = Pt(10.5)
    p_k.font.bold = True
    p_k.font.color.rgb = COLOR_FOREST

    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.73), Inches(0.55))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_t = tf_title.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_DARK_GREEN


def add_footer(slide, current_slide, total_slides=TOTAL_SLIDES):
    tb_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.5), Inches(0.25))
    tf_left = tb_left.text_frame
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_l = tf_left.paragraphs[0]
    p_l.text = "AgroVision-Mine: Multimodal Data Warehouse & Supervised Foliar Intelligence — Faculty Review"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = COLOR_FOOTER

    tb_right = slide.shapes.add_textbox(Inches(10.5), Inches(7.08), Inches(2.03), Inches(0.25))
    tf_right = tb_right.text_frame
    tf_right.margin_left = tf_right.margin_top = tf_right.margin_right = tf_right.margin_bottom = 0
    p_r = tf_right.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"Slide {current_slide} of {total_slides}"
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(9.5)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_FOREST


def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, border_width=1):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()
    return shape


def add_card_content(slide, left, top, width, height, title, bullets, title_color=COLOR_DARK_GREEN, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    create_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(Inches(left + 0.28), Inches(top + 0.26), Inches(width - 0.56), Inches(height - 0.48))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if title:
        p0 = tf.paragraphs[0]
        p0.text = title.upper()
        p0.font.name = FONT_TITLE
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(8)

    for item in bullets:
        p = tf.add_paragraph() if title or tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(4)
        if isinstance(item, tuple):
            headline, detail = item
            run_h = p.add_run()
            run_h.text = f"•  {headline}: "
            run_h.font.name = FONT_BODY
            run_h.font.size = Pt(11.5)
            run_h.font.bold = True
            run_h.font.color.rgb = COLOR_DARK_TEXT

            run_d = p.add_run()
            run_d.text = detail
            run_d.font.name = FONT_BODY
            run_d.font.size = Pt(11)
            run_d.font.bold = False
            run_d.font.color.rgb = COLOR_DARK_TEXT
        else:
            run = p.add_run()
            run.text = f"•  {item}"
            run.font.name = FONT_BODY
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_DARK_TEXT
    return tb


def format_table(table, col_widths, headers, data, header_bg=COLOR_DARK_GREEN):
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = Inches(width)

    for c_idx, head_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.08)
        p = cell.text_frame.paragraphs[0]
        p.text = head_text
        p.font.name = FONT_TITLE
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.LEFT

    for r_idx, row_values in enumerate(data):
        row_num = r_idx + 1
        bg = COLOR_WHITE if r_idx % 2 == 0 else COLOR_CARD_BG
        for c_idx, val in enumerate(row_values):
            cell = table.cell(row_num, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.margin_left = cell.margin_right = cell.margin_top = cell.margin_bottom = Inches(0.08)
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_DARK_TEXT
            p.alignment = PP_ALIGN.LEFT


def add_kpi_card(slide, left, top, width, height, value, label, sublabel=None, accent_color=COLOR_DARK_GREEN, bg_color=COLOR_CARD_BG):
    create_card(slide, left, top, width, height, bg_color=bg_color, border_color=COLOR_CARD_BORDER)
    tb = slide.shapes.add_textbox(Inches(left + 0.1), Inches(top + 0.12), Inches(width - 0.2), Inches(height - 0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_v = tf.paragraphs[0]
    p_v.alignment = PP_ALIGN.CENTER
    p_v.text = value
    p_v.font.name = FONT_TITLE
    p_v.font.size = Pt(20)
    p_v.font.bold = True
    p_v.font.color.rgb = accent_color

    p_l = tf.add_paragraph()
    p_l.alignment = PP_ALIGN.CENTER
    p_l.text = label.upper()
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9.5)
    p_l.font.bold = True
    p_l.font.color.rgb = COLOR_DARK_TEXT

    if sublabel:
        p_s = tf.add_paragraph()
        p_s.alignment = PP_ALIGN.CENTER
        p_s.text = sublabel
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = COLOR_MUTED_TEXT


# -----------------------------------------------------------------------------
# SLIDE BUILDERS (1 TO 28)
# -----------------------------------------------------------------------------

def build_slide_01(prs):
    """Slide 1: Title and Academic Review Cover."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Outer Framing Card
    create_card(slide, 0.8, 0.6, 11.73, 6.3, bg_color=COLOR_WHITE, border_color=COLOR_DARK_GREEN, border_width=2)
    
    # VIT Logo if available
    vit_logo_path = INSPECT_DIR / "vit_logo.png"
    if vit_logo_path.exists():
        slide.shapes.add_picture(str(vit_logo_path), Inches(1.2), Inches(0.9), Inches(1.8), Inches(1.74))

    # Title & Subtitle block
    tb_title = slide.shapes.add_textbox(Inches(3.2), Inches(1.0), Inches(8.8), Inches(1.8))
    tf = tb_title.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "AgroVision-Mine"
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(34)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_DARK_GREEN

    p1 = tf.add_paragraph()
    p1.text = "A Multimodal Data Warehouse, Visual Pattern Mining Framework, and Supervised Foliar Intelligence System for Crop Disease Management"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15.5)
    p1.font.color.rgb = COLOR_FOREST
    p1.space_before = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = "CSI3010: DATA WAREHOUSING & DATA MINING — FINAL LAB PROJECT REVIEW"
    p2.font.name = FONT_TITLE
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_AMBER
    p2.space_before = Pt(6)

    # Metadata & Team Details Card
    meta_box = slide.shapes.add_textbox(Inches(1.2), Inches(3.3), Inches(10.9), Inches(3.2))
    tf_m = meta_box.text_frame
    tf_m.word_wrap = True

    pm0 = tf_m.paragraphs[0]
    pm0.text = "PROJECT TEAM DETAILS & ACADEMIC SUPERVISION"
    pm0.font.name = FONT_TITLE
    pm0.font.size = Pt(14)
    pm0.font.bold = True
    pm0.font.color.rgb = COLOR_DARK_GREEN
    pm0.space_after = Pt(8)

    pm1 = tf_m.add_paragraph()
    pm1.text = "•  Team Members:  BOOMIKA V (23MID0326)   |   AJAY M (23MID0020)"
    pm1.font.name = FONT_BODY
    pm1.font.size = Pt(14)
    pm1.font.bold = True
    pm1.font.color.rgb = COLOR_DARK_TEXT
    pm1.space_after = Pt(6)

    pm2 = tf_m.add_paragraph()
    pm2.text = "•  Faculty Guide:  Dr. DEVIPRIYA A, Associate Professor"
    pm2.font.name = FONT_BODY
    pm2.font.size = Pt(13.5)
    pm2.font.bold = True
    pm2.font.color.rgb = COLOR_NAVY
    pm2.space_after = Pt(4)

    pm3 = tf_m.add_paragraph()
    pm3.text = "•  Laboratory Slot:  L41 + L42      •  Academic Term:  Fall Semester 2026–27"
    pm3.font.name = FONT_BODY
    pm3.font.size = Pt(12.5)
    pm3.font.color.rgb = COLOR_MUTED_TEXT
    pm3.space_after = Pt(4)

    pm4 = tf_m.add_paragraph()
    pm4.text = "•  Department:  School of Computer Science and Engineering (SCOPE), VIT University, Chennai"
    pm4.font.name = FONT_BODY
    pm4.font.size = Pt(12.5)
    pm4.font.color.rgb = COLOR_MUTED_TEXT
    pm4.space_after = Pt(4)

    pm5 = tf_m.add_paragraph()
    pm5.text = "•  Verified Deliverables:  SQLite Star Schema (2,596 facts) • 32D Feature Store • SQL OLAP • Dual K-Means / PCA • Mode A/B Association Rules • 25-Class EfficientNet-B0 Classifier (61.84% Test Acc) • 117/117 Automated Tests"
    pm5.font.name = FONT_BODY
    pm5.font.size = Pt(11)
    pm5.font.bold = True
    pm5.font.color.rgb = COLOR_FOREST


def build_slide_02(prs):
    """Slide 2: Executive Summary & Multimodal Analytical Architecture."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Executive Summary: The Multimodal Analytical Bridge")
    add_footer(slide, 2)

    # Left Column (5.65"): Core Challenge & Implemented Warehouse
    bullets_left = [
        ("Agricultural Data Fragmentation", "Foliar imagery traditionally resides in isolated raw directories without relational metadata, multi-dimensional queryability, or data quality gates."),
        ("Kimball Star Schema Warehouse", "Engineered a formal dimensional warehouse in SQLite (PRAGMA foreign_keys = ON) with 1 Fact table (2,596 rows) and 4 Dimensions (dim_crop, dim_disease, dim_image, dim_visual_feature)."),
        ("Explainable Visual Feature Store", "Extracted 32 continuous descriptors (19 Color Moments, 7 Haralick GLCM Texture, 6 Morphometric Shape) into an audited 44-column feature matrix."),
        ("SQL OLAP Analytical Engine", "Implemented parameterized SQL operations (Roll-up, Drill-down, Slice, Dice, Pivot) with sub-15ms execution latency across all 2,596 observations."),
        ("Unsupervised Visual Mining", "Fitted K-Means clustering (K=2 metric-supported vs K=4 exploratory) and 2D PCA projection (52.11% variance), plus Apriori/FP-Growth association rule mining.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Core Challenge & Implemented Warehouse", bullets_left)

    # Right Column Top (5.7", h=3.1"): Supervised Classification Module
    bullets_right_top = [
        ("Current 25-Class Supervised Module", "Implemented bounded multi-class foliar disease classification using fine-tuned EfficientNet-B0 (transfer learning from ImageNet-1K)."),
        ("Primary Evaluated Benchmark", "Trained and evaluated across 2,447 PlantDoc images covering 25 crop-condition classes across 12 host crops."),
        ("Rigorous Split Partitioning", "1,468 train, 489 validation, and 490 held-out test specimens grouped strictly by perceptual dHash to eliminate cross-partition data leakage."),
        ("Verified Test Performance", "Achieved 61.84% Top-1 Test Accuracy, 61.43% Balanced Accuracy, and 60.84% Macro-F1 on the 490 held-out images (Wilson 95% CI: [57.46%, 66.03%]).")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 3.1, "Implemented Supervised Classification Module", bullets_right_top, bg_color=COLOR_GREEN_BG, border_color=COLOR_FOREST)

    # Right Column Bottom (5.7", h=2.25"): Scientific Boundaries
    bullets_right_bottom = [
        ("Rejection of Generic Binary Task", "An unconditioned all-crop Healthy/Diseased binary classifier was rejected due to severe taxonomic shortcut confounding (e.g. 7 crops were 100% healthy-only)."),
        ("Bounded Multi-Class Scope", "The current model classifies within its 25 supported PlantDoc classes. It is NOT a universal plant diagnostic system."),
        ("Domain Shift Safeguard", "ICAR rice scanner images (N=36) were deliberately excluded from training and trigger an automated 'unsupported_domain' cross-modal rejection alert.")
    ]
    add_card_content(slide, 6.83, 4.60, 5.7, 2.25, "Scientific Boundaries & Academic Integrity", bullets_right_bottom, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER_BORDER)


def build_slide_03(prs):
    """Slide 3: Research Motivation: The Agricultural Data Gap."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Research Motivation: The Agricultural Data Gap")
    add_footer(slide, 3)

    bullets_left = [
        ("Isolated Black-Box Classifiers", "Conventional computer vision models treat plant pathology as an isolated single-image classification problem, lacking historical, taxonomic, or environmental context."),
        ("Metadata Fragmentation", "Raw agricultural datasets strip away critical dimensions (botanical taxonomy, capture equipment, pathogen taxonomy, and spatial lesion properties)."),
        ("Absence of Ingestion Quality Audits", "Public web-scraped corpora frequently suffer from truncated byte streams, corrupted image headers, duplicate frames, and unstandardized orientations."),
        ("Inability to Slice & Drill", "Agronomists and extension officers cannot execute multi-attribute relational queries (e.g., comparing fungal vs bacterial lesion severity across host plant families).")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 4.4, "Limitations of Conventional Approaches", bullets_left)

    bullets_right = [
        ("Relational Star Schema Integration", "Couples image pixel data with Kimball-style dimensional modeling, linking image files to botanical taxonomy, pathology hierarchies, and extracted features."),
        ("5 Automated Quality Gates", "Enforces pre-ingestion checks for file headers, geometry, payload limits, MD5 deduplication, and EXIF transposition, guaranteeing zero corrupt records."),
        ("32 Transparent Visual Descriptors", "Engineers explainable color moments, Haralick GLCM textures, and morphometric shape metrics that remain inspectable alongside deep neural embeddings."),
        ("Dual-Track Analytical Intelligence", "Harmonizes SQL OLAP multi-dimensional slicing, unsupervised visual clustering, and bounded supervised transfer learning under one unified platform.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 4.4, "The AgroVision-Mine Multimodal Solution", bullets_right)

    # Core Research Question Banner
    create_card(slide, 0.8, 5.95, 11.73, 0.95, bg_color=COLOR_DARK_GREEN, border_color=None)
    tb_q = slide.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.33), Inches(0.75))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True
    p = tf_q.paragraphs[0]
    p.text = "CORE RESEARCH QUESTION:"
    p.font.name = FONT_TITLE
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p2 = tf_q.add_paragraph()
    p2.text = "How can multimodal foliar observations and explainable visual features be integrated into an auditable relational data warehouse to support real-time OLAP slicing, visual pattern mining, and a scientifically defensible supervised classification system?"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE


def build_slide_04(prs):
    """Slide 4: Project Objectives & Implemented Deliverables."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Project Objectives & Implemented Deliverables")
    add_footer(slide, 4)

    headers = ["#", "Objective & Scope", "Implemented Component / Logic", "Verified System Deliverable"]
    col_widths = [0.6, 2.8, 4.3, 4.03]
    data = [
        ["1", "Data Governance & Ingestion", "Ingest 2,596 observations across 14 crops with SHA-256 cryptographic immutability", "canonical_dataset_v2.csv\n(SHA-256: c7fd16dc...1cb8 verified)"],
        ["2", "Automated Quality Gates", "5-gate pipeline: magic bytes, geometry, 15MB ceiling, MD5 deduplication, EXIF transpose", "5 quality gates verified;\nZero corrupt images admitted to warehouse"],
        ["3", "Explainable Feature Store", "Extract 32 continuous descriptors (19 Color, 7 GLCM Texture, 6 Morphometry)", "image_features_v2.csv\n(44 columns, 2,596 rows; SHA-256 invariant)"],
        ["4", "Dimensional Data Warehouse", "Kimball Star Schema in SQLite with native PRAGMA foreign_keys = ON via SQLAlchemy", "agrovision_warehouse.db (2,596 fact rows;\n14 crops, 19 conditions, 4 dimensions)"],
        ["5", "SQL-Backed OLAP Engine", "Real ANSI SQL queries: Roll-up, Drill-down, Slice by Crop, Dice Sub-Cube, Pivot Matrix", "Interactive OLAP Console;\nLatency 1.5ms – 14.1ms across 2,596 rows"],
        ["6", "Unsupervised Visual Mining", "Dual-K K-Means (K=2 primary, K=4 exploratory), 2D PCA, Apriori / FP-Growth rule parity", "K=2 Silhouette = 0.4060; PCA 52.1% var;\n880 Mode A rules (exact parity Δ = 0.0)"],
        ["7", "Supervised Foliar Classifier", "25-class transfer learning via EfficientNet-B0; grouped dHash train/val/test splits", "490 held-out test images; 61.84% Test Acc;\n60.84% Macro-F1 (Wilson CI: [57.5%, 66.0%])"]
    ]

    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(1.4), Inches(11.73), Inches(5.4))
    format_table(t_shape.table, col_widths, headers, data)


def build_slide_05(prs):
    """Slide 5: Dataset Provenance & Canonical Composition."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Dataset Provenance & Canonical Composition")
    add_footer(slide, 5)

    bullets_left = [
        ("Canonical Agricultural Corpus", "Unified dataset of 2,596 authentic leaf observations across 14 crop species and 19 pathological condition categories."),
        ("Multi-Source Provenance", "2,560 open-field images sourced from the PlantDoc benchmark (98.6%) plus 36 authenticated flatbed scanner images from ICAR / Open Government Data India (1.4%)."),
        ("Balanced Condition Split", "1,750 Diseased observations (67.4%) and 846 Healthy baseline observations (32.6%) providing verified ground truth."),
        ("Reconciliation of Tomato Count", "The canonical manifest contains exactly 743 Tomato specimens, correcting prior preliminary draft counts."),
        ("Cryptographic Immutability", "Manifest SHA-256 (c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8) and Feature Store SHA-256 (f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1) remain strictly invariant.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Dataset Architecture & Lineage", bullets_left)

    # Right: Taxonomic distribution table
    headers = ["Crop Species", "Record Count", "Percentage", "Pathological Scope"]
    col_widths = [1.8, 1.1, 1.1, 1.7]
    data = [
        ["Tomato", "743", "28.62%", "Early/Late Blight, Mold, Curl"],
        ["Corn", "372", "14.33%", "Rust, Gray Spot, Blight, Healthy"],
        ["Apple", "272", "10.48%", "Scab, Rust, Black Rot, Healthy"],
        ["Potato", "216", "8.32%", "Early Blight, Late Blight, Healthy"],
        ["Grape & Bell Pepper", "265", "10.20%", "Black Rot, Bacterial Spot, Healthy"],
        ["Squash & Raspberry", "249", "9.59%", "Powdery Mildew, Healthy"],
        ["Blueberry, Peach, Strawb.", "321", "12.36%", "Healthy baseline reference"],
        ["Soybean, Cherry, Rice", "158", "6.09%", "Healthy (Soybean/Cherry) + Rice (ICAR)"],
        ["TOTAL CORPUS", "2,596", "100.0%", "14 Crops / 19 Conditions"]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(6.83), Inches(1.35), Inches(5.7), Inches(4.3))
    format_table(t_shape.table, col_widths, headers, data)

    # Note below table
    note_bullets = [
        ("Source Domain Separation", "The 36 ICAR rice observations are captured via flatbed desktop scanner with pure white backgrounds, while PlantDoc imagery is captured in unstructured outdoor fields.")
    ]
    add_card_content(slide, 6.83, 5.80, 5.7, 1.05, "Modality Separation Note", note_bullets, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER_BORDER)


def build_slide_06(prs):
    """Slide 6: Complete End-to-End System Architecture Diagram."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "System Architecture: End-to-End 5-Layer Pipeline")
    add_footer(slide, 6)

    # We build a native landscape 5-layer diagram with distinct visual boxes and connectors
    layers = [
        ("1. INGESTION & GATES", 0.80, 1.35, 2.15, 5.5, COLOR_CARD_BG, COLOR_DARK_GREEN, [
            ("Heterogeneous Ingestion", "PlantDoc (2,560) + ICAR Rice (36)"),
            ("Gate 1: Format", "Magic Bytes header check"),
            ("Gate 2: Geometry", "Min 100x100 resolution"),
            ("Gate 3: Payload", "15 MB ceiling limit"),
            ("Gate 4: Deduplication", "MD5 content hashing"),
            ("Gate 5: Normalization", "EXIF transpose & RGB canvas")
        ]),
        ("2. PREPROCESSING & STORE", 3.20, 1.35, 2.15, 5.5, COLOR_CARD_BG, COLOR_FOREST, [
            ("Image Standardization", "Uniform 256x256 bilinear resize"),
            ("Color Moments (19)", "RGB/HSV mean, std, ExG index"),
            ("GLCM Texture (7)", "Contrast, dissimilarity, ASM, energy"),
            ("Morphometry (6)", "Area, circularity, perimeter, solidity"),
            ("Feature Store", "44 columns, 2,596 rows (image_features_v2.csv)")
        ]),
        ("3. WAREHOUSE & ETL", 5.60, 1.35, 2.15, 5.5, COLOR_CARD_BG, COLOR_NAVY, [
            ("Kimball Star Schema", "SQLite 3 relational warehouse"),
            ("Fact Table", "disease_observation_fact (2,596 rows)"),
            ("Dimension 1", "dim_crop (14 taxa)"),
            ("Dimension 2", "dim_disease (19 conditions)"),
            ("Dimension 3 & 4", "dim_image & dim_visual_feature"),
            ("Integrity", "PRAGMA foreign_keys = ON; 100% idempotent ETL")
        ]),
        ("4. ANALYTICAL ENGINES", 8.00, 1.35, 2.30, 5.5, COLOR_GREEN_BG, COLOR_DARK_GREEN, [
            ("SQL OLAP Engine", "Roll-up, Drill-down, Slice, Dice, Pivot (<15ms)"),
            ("Dual K-Means", "K=2 primary (Silh 0.406) vs K=4 exploratory"),
            ("2D PCA Projection", "52.11% variance (PC1 luminance, PC2 texture)"),
            ("Association Rules", "Mode A (880 visual) & Mode B (285 labeled)"),
            ("Nearest References", "32D Euclidean similarity in descriptor space"),
            ("Supervised CNN", "Fine-tuned EfficientNet-B0 (25 classes, 61.8% acc)")
        ]),
        ("5. PRESENTATION TIER", 10.55, 1.35, 1.98, 5.5, COLOR_CARD_BG, COLOR_FOREST, [
            ("FastAPI Backend", "Asynchronous REST API (:8000)"),
            ("React 18 Frontend", "TypeScript SPA with 9 analytical pages"),
            ("Workbench GUI", "Live upload, 32D extraction, prediction"),
            ("Domain Safeguard", "Out-of-domain rejection alert banner"),
            ("Quality Assurance", "117/117 automated tests passing")
        ])
    ]

    for title, left, top, width, height, bg, border, bullets in layers:
        add_card_content(slide, left, top, width, height, title, bullets, title_color=border, bg_color=bg, border_color=border)

    # Connector right arrows between layers
    arrow_x = [2.98, 5.38, 7.78, 10.33]
    for x in arrow_x:
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(4.0), Inches(0.18), Inches(0.24))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = COLOR_FOREST
        arrow.line.fill.background()


def build_slide_07(prs):
    """Slide 7: Technology Stack & Architectural Rationale."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Technology Stack & Architectural Rationale")
    add_footer(slide, 7)

    headers = ["Technology", "System Layer", "Verified Implementation Role", "Architectural Rationale"]
    col_widths = [2.0, 1.8, 4.4, 3.53]
    data = [
        ["Python 3.11", "Core Runtime", "ETL pipeline, feature extraction, mining engines, and API services", "Robust scientific ecosystem, high performance, strict typing support"],
        ["NumPy & Pandas", "Data Processing", "Vectorized linear algebra, 44-col analytical feature store matrix", "High-speed tabular manipulation and memory-efficient matrix operations"],
        ["Pillow & OpenCV", "Image Engineering", "EXIF auto-transposition, color space conversions, contour morphometry", "Production-grade multi-format image decoding and geometry extraction"],
        ["scikit-image & sklearn", "Machine Learning", "GLCM texture extraction, StandardScaler, K-Means clustering, PCA", "Gold-standard reproducible mathematical formulations for classical ML"],
        ["PyTorch / torchvision", "Deep Learning", "EfficientNet-B0 transfer learning, CrossEntropyLoss, AdamW optimizer", "State-of-the-art CNN modeling with pre-trained ImageNet-1K visual priors"],
        ["mlxtend", "Association Mining", "Apriori level-wise search and FP-Growth frequent pattern tree mining", "Enables exact mathematical parity verification between mining algorithms"],
        ["SQLite & SQLAlchemy", "Data Warehouse", "Kimball Star Schema storage with native PRAGMA foreign_keys = ON", "Zero-configuration ACID relational storage with foreign key enforcement"],
        ["FastAPI & React 18", "Application Delivery", "Asynchronous REST backend (:8000) + TypeScript 9-page responsive GUI", "Low-latency JSON serialization coupled with type-safe modern presentation"],
        ["pytest & Playwright", "Quality Assurance", "107 automated unit/integration tests + 10 browser functional tests", "Guarantees complete regression prevention and verified browser health"]
    ]

    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(1.35), Inches(11.73), Inches(5.5))
    format_table(t_shape.table, col_widths, headers, data)


def build_slide_08(prs):
    """Slide 8: Data Quality Assurance: 5 Automated Gates."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Data Quality Assurance: 5 Automated Gates")
    add_footer(slide, 8)

    bullets_left = [
        ("Gate 1: Byte Header & Format", "Validates binary Magic Bytes for authentic JPEG/PNG signatures. Rejects truncated streams, disguised scripts, and invalid image formats."),
        ("Gate 2: Dimension & Aspect Ratio", "Enforces minimum resolution threshold (100x100 px) and rejects extreme aspect ratios (>10:1) to prevent severe spatial distortion during normalization."),
        ("Gate 3: File Payload Limit", "Enforces a strict 15 MB payload ceiling, preventing memory exhaustion and denial-of-service vulnerabilities during real-time extraction."),
        ("Gate 4: Cryptographic Deduplication", "Calculates MD5 content digests to detect and eliminate exact duplicate images across disparate subdirectories and source datasets."),
        ("Gate 5: Normalization & EXIF", "Applies PIL exif_transpose to correct camera orientation flags and normalizes RGBA/palette modes onto a standardized RGB canvas.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "The 5 Automated Pre-Ingestion Gates", bullets_left)

    # Right: Embedded plot and edge harness text
    plot_path = INSPECT_DIR / "quality_gates_plot.png"
    if plot_path.exists():
        slide.shapes.add_picture(str(plot_path), Inches(6.83), Inches(1.35), Inches(5.7), Inches(2.3))

    bullets_right = [
        ("Controlled Diagnostic Edge Harness", "Evaluated against 10 synthetic adversarial fixtures: truncated JPEG byte stream, 0-byte empty file, 50x50 px sub-threshold, 15:1 distorted aspect ratio, and 25 MB oversized payload."),
        ("100% Rejection Rate", "All 10 corrupt fixtures were rejected at the gate boundary with explicit validation exceptions, confirming zero corrupt admissions into the warehouse."),
        ("Laplacian Variance Sharpness Audit", "Audited all 2,596 images using Laplacian kernel variance to assess blur distribution without discarding authentic field observations.")
    ]
    add_card_content(slide, 6.83, 3.80, 5.7, 3.05, "Edge Harness Verification & Blur Audit", bullets_right)


def build_slide_09(prs):
    """Slide 9: Feature Engineering: 32 Continuous Descriptors."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Feature Engineering: 32 Explainable Visual Descriptors")
    add_footer(slide, 9)

    col1 = [
        ("RGB Channel Statistics (6)", "Mean and standard deviation across Red, Green, and Blue channels capturing overall leaf illumination."),
        ("Normalized RGB Ratios (3)", "Normalized chromaticity r, g, b ratios (channel / sum) providing chromatic invariance under lighting changes."),
        ("HSV Color Space (6)", "Mean and standard deviation across Hue, Saturation, and Value channels separating color tone from brightness."),
        ("Excess Green Index (ExG) (1)", "Mean 2G - R - B vegetation index isolating chlorophyll-rich leaf foliage from necrotic lesions."),
        ("Color Moment Summary", "19 total color descriptors capturing global foliar pigmentation and chlorosis.")
    ]
    add_card_content(slide, 0.8, 1.35, 3.75, 4.4, "Color Moments (19 Features)", col1)

    col2 = [
        ("GLCM Contrast (1)", "Measures local intensity variations and sharpness of lesion boundaries."),
        ("GLCM Dissimilarity (1)", "Linear variation of gray-level pairs across leaf texture."),
        ("GLCM Homogeneity (1)", "Measures smoothness of uniform leaf blade surfaces."),
        ("GLCM Energy & ASM (2)", "Angular Second Moment and Energy measuring textural uniformity."),
        ("GLCM Correlation (1)", "Linear dependency of gray-level values in the neighborhood."),
        ("GLCM Contrast Norm (1)", "Normalized contrast metric across angles 0°, 45°, 90°, 135°."),
        ("Texture Summary", "7 Haralick descriptors capturing tactile foliar roughness.")
    ]
    add_card_content(slide, 4.79, 1.35, 3.75, 4.4, "GLCM Textures (7 Features)", col2)

    col3 = [
        ("Contour Area (1)", "Total pixel area of detected leaf boundary."),
        ("Contour Perimeter (1)", "Boundary perimeter measuring edge complexity."),
        ("Contour Circularity (1)", "Isoperimetric quotient (4π·Area / Perimeter²)."),
        ("Aspect Ratio (1)", "Ratio of bounding box width to height."),
        ("Solidity (1)", "Ratio of contour area to convex hull area."),
        ("Lesion Coverage Ratio (1)", "Proportion of leaf surface affected by necrotic spots."),
        ("Shape Summary", "6 morphometric metrics describing leaf geometry.")
    ]
    add_card_content(slide, 8.78, 1.35, 3.75, 4.4, "Contour & Shape (6 Features)", col3)

    # Bottom summary card
    bottom_bullets = [
        ("Analytical Feature Store Specification", "Persisted in data/features/image_features_v2.csv containing exactly 44 columns: image_id, 4 taxonomic metadata fields, 32 continuous visual descriptors, and 7 technical validation fields across all 2,596 canonical observations.")
    ]
    add_card_content(slide, 0.8, 5.90, 11.73, 1.0, "Canonical Feature Store Architecture", bottom_bullets, bg_color=COLOR_GREEN_BG, border_color=COLOR_FOREST)


def build_slide_10(prs):
    """Slide 10: Algorithm Selection: Technical Rationale Matrix."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Algorithm Selection: Technical Rationale Matrix")
    add_footer(slide, 10)

    headers = ["Algorithm / Technique", "Input Vector", "Why Selected (Selection Rationale)", "Output Representation", "Limitations Disclosed"]
    col_widths = [2.0, 1.8, 3.2, 2.4, 2.33]
    data = [
        ["StandardScaler", "32 continuous features", "Normalizes diverse feature scales to zero mean, unit variance: z = (x - μ) / σ", "Standardized 32D matrix (μ=0, σ=1)", "Assumes approximately Gaussian-like distributions"],
        ["K-Means Clustering", "32 standardized features", "Discovers unsupervised structural groupings of foliar morphology; tested K=2 to 8", "Cluster assignments (K=2 primary, K=4 exploratory)", "Partitions visual appearance, NOT biological etiology"],
        ["PCA Projection", "32 standardized features", "Reduces 32D space to 2 principal components explaining 52.11% total visual variance", "2D orthogonal scatter coordinates (PC1, PC2)", "Linear projection discards 47.89% residual variance"],
        ["Apriori & FP-Growth", "12 discretized features", "Exhaustive level-wise vs compressed FP-Tree mining of frequent visual itemsets", "880 Mode A rules with exact parity (Δ = 0.00000000)", "Identifies statistical co-occurrences, not causality"],
        ["Nearest Neighbors", "32D Euclidean metric", "Ranks authentic warehouse exemplars by standardized visual descriptor distance", "Top-k reference matches with distance metrics", "Geometric proximity does NOT establish disease diagnosis"],
        ["EfficientNet-B0 CNN", "224x224 RGB image", "Pretrained ImageNet-1K CNN transfer learning for 25-class supervised prediction", "Calibrated 25-class probability distribution", "Bounded to 25 classes; out-of-domain input rejected"]
    ]

    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(1.35), Inches(11.73), Inches(5.5))
    format_table(t_shape.table, col_widths, headers, data)


def build_slide_11(prs):
    """Slide 11: Data Warehouse Design: Kimball Star Schema."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Data Warehouse Design: Kimball Star Schema")
    add_footer(slide, 11)

    # Left: Star schema diagram picture
    diag_path = INSPECT_DIR / "star_schema_diagram.png"
    if diag_path.exists():
        slide.shapes.add_picture(str(diag_path), Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.5))
    else:
        # Fallback card
        add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Star Schema Architecture", [("Diagram", "Star Schema diagram placeholder")])

    # Right: Physical table specifications
    bullets_right = [
        ("Central Fact Table", "disease_observation_fact: Grain is exactly one row per validated leaf specimen (2,596 fact rows). Contains foreign keys: crop_key, disease_key, image_key, feature_key."),
        ("Additive & Semi-Additive Measures", "observation_count (additive, integer 1 for SQL COUNT aggregation) and lesion_severity_score (semi-additive, continuous 0.00 to 1.00 for AVG analysis)."),
        ("Dimension 1: dim_crop", "Botanical Host hierarchy (14 rows: crop_key, crop_name, botanical_name, crop_category). Slices queries by agricultural crop groups."),
        ("Dimension 2: dim_disease", "Pathology taxonomy (19 rows: disease_key, disease_name, pathogen_type, condition_status). Distinguishes Fungal, Bacterial, Viral, and Healthy baselines."),
        ("Dimension 3: dim_image", "Acquisition technical metadata (2,596 rows: image_key, raw_id, file_format, dimensions, dataset_source, md5_hash, blur_score, license)."),
        ("Dimension 4: dim_visual_feature", "32 continuous descriptors (2,596 rows: feature_key, 19 color moments, 7 GLCM texture metrics, 6 morphometric shape measurements).")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Physical Star Schema Specification", bullets_right)


def build_slide_12(prs):
    """Slide 12: Production ETL Pipeline & Referential Integrity."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Production ETL Pipeline & Referential Integrity")
    add_footer(slide, 12)

    # Left: Code block card
    bullets_code = [
        ("ETL Architecture", "Engineered in Python using SQLAlchemy 2.0 with atomic transaction management."),
        ("1. Native FK Pragma", "conn.execute(text('PRAGMA foreign_keys = ON;')) enforces relational integrity at database engine level."),
        ("2. Dimension-First Loading", "Populates all 4 dimension tables first (dim_crop, dim_disease, dim_image, dim_visual_feature) using idempotent surrogate key resolution."),
        ("3. Fact Ingestion & Dedup", "Inserts fact rows via INSERT OR IGNORE, preventing duplicate observation injection on pipeline reruns."),
        ("4. Atomic Commit", "Wraps entire ETL in a single transaction; rolls back completely on any validation or constraint violation.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "ETL Pipeline Implementation Protocol", bullets_code)

    bullets_right = [
        ("Complete Ingestion Migration", "Successfully extracted, transformed, and committed all 2,596 canonical observations and 32D feature rows into agrovision_warehouse.db."),
        ("Strict 100% Idempotency", "Subsequent execution of the ETL pipeline against the populated warehouse inserts exactly 0 duplicate rows, cleanly skipping all 2,596 existing records."),
        ("Zero Referential Drift", "100% of fact foreign keys resolve to valid dimension primary keys. Automated tests prove invalid foreign key insertions are rejected by SQLite."),
        ("Surrogate vs Natural Keys", "Employs synthetic integer primary keys (crop_key, disease_key, etc.) for high-performance join indexes, while indexing natural keys (crop_name, md5_hash) for idempotent upserts.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Verified ETL Execution & Invariance Audit", bullets_right)


def build_slide_13(prs):
    """Slide 13: Data Governance & Integrity Verification."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Data Governance & Integrity Verification")
    add_footer(slide, 13)

    # 4 Top KPI Cards
    add_kpi_card(slide, 0.8, 1.35, 2.7, 1.3, "0.00%", "Missing Values", "Zero nulls across all 44 columns", COLOR_DARK_GREEN)
    add_kpi_card(slide, 3.8, 1.35, 2.7, 1.3, "0 Duplicates", "Content Duplication", "MD5 & dHash deduplicated", COLOR_FOREST)
    add_kpi_card(slide, 6.83, 1.35, 2.7, 1.3, "100%", "Foreign Key Integrity", "PRAGMA foreign_keys = ON", COLOR_NAVY)
    add_kpi_card(slide, 9.83, 1.35, 2.7, 1.3, "Invariant", "Cryptographic Hashes", "Exact SHA-256 manifest match", COLOR_DARK_GREEN)

    # Bottom Table: 4 Integrity Checks
    headers = ["Audit Check", "Expected Threshold", "Measured Result", "Status & Academic Evidence"]
    col_widths = [2.5, 2.2, 2.8, 4.23]
    data = [
        ["SQLite Foreign Key Constraints", "100% Enforced (PRAGMA=1)", "0 Violations (PRAGMA foreign_keys = ON)", "PASS: All 2,596 fact rows resolve to valid dimension PKs; orphan inserts fail."],
        ["Fact Table PK Uniqueness", "100% Unique observation_key", "2,596 Unique PKs (1 to 2,596)", "PASS: Zero duplicate, missing, or colliding primary keys across the warehouse."],
        ["Feature Store Completeness", "44 Required Columns Present", "44 Columns Present (100% non-null)", "PASS: 32 continuous descriptors + 12 metadata fields fully verified."],
        ["Cryptographic Manifest Hash", "c7fd16dc...1cb8", "c7fd16dcd6c1f8623f3e25a48b572387...", "PASS: Exact SHA-256 match confirms zero post-freeze file mutations."],
        ["Feature Store Hash", "f6caf70b...093c1", "f6caf70bd07eeda335e471705e3763d3...", "PASS: Exact SHA-256 match proves feature matrix numerical immutability."]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(2.9), Inches(11.73), Inches(3.95))
    format_table(t_shape.table, col_widths, headers, data)


def build_slide_14(prs):
    """Slide 14: SQL-Backed OLAP Operations Engine."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "SQL-Backed OLAP Operations Engine")
    add_footer(slide, 14)

    # 4 Structured cards (2x2 grid)
    c1 = [
        ("Hierarchical Aggregation", "Ascends the botanical hierarchy: Leaf Observation -> Host Crop -> Crop Category."),
        ("SQL Execution", "SELECT c.crop_category, COUNT(f.observation_key) AS total, AVG(f.lesion_severity_score) AS avg_sev FROM disease_observation_fact f JOIN dim_crop c ON f.crop_key = c.crop_key GROUP BY c.crop_category;"),
        ("Benchmark", "Executed in 14.1 ms across all 2,596 warehouse fact rows.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 2.65, "1. Roll-Up Operation", c1)

    c2 = [
        ("Hierarchical Decomposition", "Descends the pathology taxonomy: Crop Category -> Pathology Diagnosis -> Specific Pathogen."),
        ("SQL Execution", "SELECT d.disease_name, d.pathogen_type, COUNT(f.observation_key) AS obs_count FROM disease_observation_fact f JOIN dim_disease d ON f.disease_key = d.disease_key WHERE f.crop_key = ? GROUP BY d.disease_name;"),
        ("Benchmark", "Executed in 2.2 ms for fine-grained disease breakdown.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 2.65, "2. Drill-Down Operation", c2)

    c3 = [
        ("Single & Multi-Dimension Filtering", "Slice: Filters on 1 dimension (WHERE c.crop_name = 'Rice'). Dice: Filters sub-cube across 2+ dimensions (WHERE c.crop_name IN ('Tomato','Corn') AND d.pathogen_type = 'Fungal')."),
        ("SQL Execution", "Parameterized SELECT with WHERE filters applied to dimension keys."),
        ("Benchmark", "Slice latency: 1.56 ms | Dice latency: 1.54 ms.")
    ]
    add_card_content(slide, 0.8, 4.20, 5.7, 2.65, "3. Slice & Dice Sub-Cube Operations", c3)

    c4 = [
        ("Cross-Tabulation Matrix", "Rotates dimensional axes: Host Crop Species (rows) vs Severity Tiers (columns)."),
        ("SQL Execution", "CASE WHEN f.lesion_severity_score < 0.30 THEN 'Low' WHEN f.lesion_severity_score <= 0.60 THEN 'Moderate' ELSE 'Severe' END crosstab."),
        ("Benchmark", "Executed in 2.15 ms producing clean 14x3 matrix.")
    ]
    add_card_content(slide, 6.83, 4.20, 5.7, 2.65, "4. Pivot Matrix Operation", c4)


def build_slide_15(prs):
    """Slide 15: Physical Warehouse: Actual OLAP Query Outputs."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Physical Warehouse: Actual OLAP Query Outputs")
    add_footer(slide, 15)

    # Left: Picture of OLAP output
    pic_path = INSPECT_DIR / "olap_output_plot.png"
    if pic_path.exists():
        slide.shapes.add_picture(str(pic_path), Inches(0.8), Inches(1.35), Inches(5.7), Inches(3.2))

    # Left Bottom Note
    note_bullets = [
        ("Low-Latency SQL Engine", "All OLAP queries execute live via SQLAlchemy 2.0 connected to agrovision_warehouse.db. Sub-15ms response times enable interactive frontend slicing without caching artifacts.")
    ]
    add_card_content(slide, 0.8, 4.75, 5.7, 2.1, "Real-Time Query Telemetry", note_bullets)

    # Right: Table of Actual Sub-Cube Query Outputs
    headers = ["Crop Category / Sub-Cube", "Taxonomic Scope", "Obs Count", "Avg Severity"]
    col_widths = [2.2, 1.8, 0.9, 0.8]
    data = [
        ["Horticultural Crops", "12 Crops (Tomato, Apple, etc.)", "2,123", "0.354"],
        ["Cereal Crops (Corn + Rice)", "Corn (372) + Rice (36)", "408", "0.378"],
        ["Legume Crops", "Soybean (Healthy baseline)", "65", "0.000"],
        ["Authenticated Rice Subset", "ICAR Pathology Benchmark", "36", "0.342"],
        ["Solanaceae Fungal Dice", "Tomato & Potato (Fungal)", "682", "0.412"],
        ["TOTAL UNIFIED WAREHOUSE", "14 Crops / 19 Conditions", "2,596", "0.351"]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(6.83), Inches(1.35), Inches(5.7), Inches(3.8))
    format_table(t_shape.table, col_widths, headers, data)

    bullets_note2 = [
        ("Cross-Category Agronomic Insights", "Legume baseline exhibits 0.00 severity (all healthy). Fungal Solanaceae sub-cube displays the highest average lesion coverage (0.412), reflecting aggressive late blight necrosis.")
    ]
    add_card_content(slide, 6.83, 5.35, 5.7, 1.5, "Agronomic Sub-Cube Interpretation", bullets_note2, bg_color=COLOR_GREEN_BG, border_color=COLOR_FOREST)


def build_slide_16(prs):
    """Slide 16: Visual Pattern Mining: Dual-K Clustering Evaluation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Visual Pattern Mining: Dual-K Clustering Evaluation")
    add_footer(slide, 16)

    # Left: Multi-K Evaluation Table
    headers = ["K Value", "Silhouette (↑)", "Davies-Bouldin (↓)", "Calinski-Harabasz (↑)"]
    col_widths = [1.3, 1.4, 1.5, 1.5]
    data = [
        ["K = 2 (Best)", "0.4060", "1.0990", "1,154.38"],
        ["K = 3", "0.1821", "1.7629", "820.65"],
        ["K = 4 (Subpart)", "0.1651", "1.8339", "674.33"],
        ["K = 5", "0.1623", "1.7326", "589.29"],
        ["K = 6", "0.1648", "1.6312", "529.40"]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(1.35), Inches(5.7), Inches(2.6))
    format_table(t_shape.table, col_widths, headers, data)

    # Left Bottom Card
    c_left = [
        ("K=2 Primary Metric Solution", "Cluster 0 (2,150 images, 82.8%) vs Cluster 1 (446 images, 17.2%). Distinguishes dense green foliage from high-contrast textured lesions."),
        ("K=4 Exploratory Sub-Partition", "Subdivides visual space into 4 exploratory morphology groups for agronomic discovery (Davies-Bouldin = 1.8339)."),
        ("Multi-Seed Algorithmic Stability", "Pairwise Adjusted Rand Index ARI = 1.0000 across seeds [0, 1, 42, 100, 999], proving zero random cluster instability.")
    ]
    add_card_content(slide, 0.8, 4.15, 5.7, 2.7, "Dual-K Metric Optimality & Stability", c_left)

    # Right: Embedded plot
    pic_path = INSPECT_DIR / "kmeans_plot.png"
    if pic_path.exists():
        slide.shapes.add_picture(str(pic_path), Inches(6.83), Inches(1.35), Inches(5.7), Inches(3.2))

    c_right = [
        ("Critical Epistemological Boundary", "Clustering groups foliar specimens strictly by mathematical visual descriptor proximity in standardized 32D space. It does NOT cluster by biological etiology (pathogen species)."),
        ("Warehouse Schema Integration", "Precomputed cluster labels (k2_cluster, k4_cluster) and PCA coordinates are persisted in data/features/clustering_assignments_v2.csv.")
    ]
    add_card_content(slide, 6.83, 4.75, 5.7, 2.1, "Scientific Caveat on Unsupervised Clustering", c_right, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER_BORDER)


def build_slide_17(prs):
    """Slide 17: Dimensionality Reduction: 2D PCA Loadings Analysis."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Dimensionality Reduction: 2D PCA Loadings Analysis")
    add_footer(slide, 17)

    bullets_left = [
        ("Cumulative Explained Variance", "52.11% total variance captured across 2 principal components (PC1 = 38.56%, PC2 = 13.55%), reducing 32 dimensions by 93.7% while preserving majority information."),
        ("Physical Interpretation of PC1 (38.56%)", "Dominant positive loadings on foliar luminance (rgb_r_mean +0.252, rgb_g_mean +0.248, glcm_asm +0.248); negative loadings on perimeter (-0.231) and saturation (-0.219). Captures surface brightness vs dark canopy borders."),
        ("Physical Interpretation of PC2 (13.55%)", "Dominant positive loadings on textural roughness (glcm_contrast +0.384, dissimilarity +0.379); negative loadings on homogeneity (-0.362) and energy (-0.315). Separates smooth healthy blades from mottled necrotic lesions."),
        ("Orthogonal Visual Space", "Demonstrates that color luminance and textural contrast represent two mathematically orthogonal axes of variation across agricultural leaf observations.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "2D PCA Projection Loadings & Variance", bullets_left)

    headers = ["Component", "Variance", "Top Positive Loading", "Top Negative Loading"]
    col_widths = [1.2, 1.0, 1.8, 1.7]
    data = [
        ["PC1", "38.56%", "rgb_r_mean (+0.252)\nglcm_asm (+0.248)", "perimeter (-0.231)\nhsv_s_mean (-0.219)"],
        ["PC2", "13.55%", "glcm_contrast (+0.384)\ndissimilarity (+0.379)", "homogeneity (-0.362)\nglcm_energy (-0.315)"],
        ["Total 2D", "52.11%", "Covers 16.6x of single feature", "Orthogonal 2D Space"]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(6.83), Inches(1.35), Inches(5.7), Inches(2.2))
    format_table(t_shape.table, col_widths, headers, data)

    bullets_right = [
        ("Cluster 0 Distribution (N=2,150)", "Centered around negative PC1 and moderate PC2; corresponds to natural foliage with moderate textural variation."),
        ("Cluster 1 Distribution (N=446)", "Occupies high positive PC1 and high PC2 quadrants; corresponds to high-luminance, high-contrast chlorotic and diseased leaf specimens."),
        ("ICAR Rice Domain Shift", "All 36 ICAR rice images cluster in positive PC1 due to the intense white scanner background, validating why scanner images must be treated separately.")
    ]
    add_card_content(slide, 6.83, 3.75, 5.7, 3.1, "Cluster Distributions & Scanner Domain Shift", bullets_right)


def build_slide_18(prs):
    """Slide 18: Association Rule Mining: Mode A vs Mode B."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Association Rule Mining: Mode A vs Mode B")
    add_footer(slide, 18)

    bullets_left = [
        ("Input Discretization", "Equal-frequency tertile binning (Low, Medium, High) across 12 explainable visual descriptors, strictly excluding condition and pathogen labels."),
        ("Baseline Thresholds", "Minimum Support = 0.15 (15.0%), Minimum Confidence = 0.60 (60.0%), Minimum Lift = 1.0."),
        ("Exact Algorithmic Parity", "Apriori and FP-Growth generate exactly 223 frequent itemsets and 880 association rules with identical support, confidence, and lift values (Δ = 0.00000000)."),
        ("Representative Rule 1", "glcm_contrast_High AND contour_perimeter_High -> glcm_energy_Low (Support = 0.214, Confidence = 0.942, Lift = 2.81)"),
        ("Representative Rule 2", "hsv_s_mean_Low AND rgb_r_mean_High -> exg_index_Low (Support = 0.188, Confidence = 0.891, Lift = 2.45)")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Mode A: Visual-Only Mining (880 Rules)", bullets_left)

    bullets_right = [
        ("Purpose & Formulation", "Appends categorical labels (condition_status, pathogen_type) to the 12 discretized visual descriptors for exploratory cross-modal discovery."),
        ("Rule Count Breakdown", "Generates 285 total association rules at min_support=0.15, min_confidence=0.60; exactly 276 rules exhibit positive correlation (Lift >= 1.0)."),
        ("Representative Rule", "condition_Healthy AND contour_perimeter_Low -> contour_circularity_High AND perimeter_Low (Support = 0.182, Confidence = 0.824, Lift = 1.68)"),
        ("Strict Causality Disclaimer", "Association rules capture statistical co-occurrences in the current corpus; they do NOT prove biological causality or disease pathogenesis."),
        ("Strict Transaction Separation", "Mode A transaction matrix is strictly quarantined from condition labels, preventing data leakage into unsupervised mining.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Mode B: Label-Conditioned Mining (285 Rules)", bullets_right)


def build_slide_19(prs):
    """Slide 19: Supervised Foliar Classification: Problem Formulation & Dataset."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Supervised Classification: Problem Formulation & Dataset")
    add_footer(slide, 19)

    bullets_left = [
        ("Task Formulation", "A bounded 25-class multi-class classification problem predicting composite [Crop]___[Condition] labels from 224x224 RGB foliar images."),
        ("Why Generic Binary Classifier Failed", "A naive all-crop Healthy vs Diseased classifier was formally rejected because the dataset exhibits severe taxonomic confounding: 7 crops (Blueberry, Peach, Raspberry, Strawberry, Soybean, Cherry) were 100% healthy-only."),
        ("Shortcut Learning Danger", "A binary classifier easily learns host crop morphology (e.g. leaf shape or vein structure) instead of foliar pathology."),
        ("The Bounded Multiclass Solution", "Formulating the task across 25 specific crop-condition classes forces the neural network to differentiate pathologies within host taxa (e.g. Tomato Late Blight vs Tomato Early Blight vs Tomato Healthy).")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Problem Formulation & Confounding Avoidance", bullets_left)

    bullets_right = [
        ("Primary Training Benchmark", "2,447 authentic PlantDoc field images spanning 25 classes across 12 host agricultural crops."),
        ("Class Pruning Protocol", "5 underrepresented classes with fewer than 20 total specimens (e.g. Tomato Spider Mites with N=2) were excluded from supervised training to prevent severe class collapse."),
        ("ICAR Rice Scanner Separation", "The 36 ICAR rice images were deliberately isolated from the supervised training split due to extreme flatbed scanner domain shift."),
        ("Supported Agricultural Crops", "Apple (3 classes), Bell Pepper (2 classes), Blueberry (1), Corn (3), Grape (2), Peach (1), Potato (2), Raspberry (1), Soybean (1), Squash (1), Strawberry (1), Tomato (7 classes).")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Dataset Scope & Taxonomic Boundary", bullets_right)


def build_slide_20(prs):
    """Slide 20: Model Architecture & Selection Rationale: EfficientNet-B0 vs Baselines."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Model Architecture & Selection Rationale")
    add_footer(slide, 20)

    bullets_left = [
        ("Convolutional Neural Backbone", "EfficientNet-B0 employs compound scaling to balance network depth, width, and image resolution using mobile inverted bottleneck convolutions (MBConv)."),
        ("Transfer Learning Priors", "Initialized with ImageNet-1K pretrained weights (torchvision EfficientNet_B0_Weights.DEFAULT), transferring rich generic low-level edge, corner, and texture filters."),
        ("Compact Runtime Footprint", "Contains 5.3 million parameters, making it computationally practical for CPU runtime inference (<150 ms) without requiring enterprise GPU infrastructure."),
        ("Spatial Feature Learning", "Unlike classical ML, EfficientNet-B0 learns localized spatial lesion patterns and necrotic borders directly from raw RGB pixel tensors.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "EfficientNet-B0 Architectural Principles", bullets_left)

    bullets_right = [
        ("Validation Macro-F1 Tournament", "Candidate models were benchmarked strictly on the 489-image validation split to make a principled, un-leaked architectural selection."),
        ("Majority Class Baseline", "Validation Macro-F1 = 0.58% (Validation Accuracy = 7.77%). Represents prior-probability chance guessing."),
        ("Classical Random Forest (32D Descriptors)", "Validation Macro-F1 = 17.02% (Validation Accuracy = 17.38%). Handcrafted global descriptors lack spatial awareness."),
        ("Classical RBF-SVM (32D Descriptors)", "Validation Macro-F1 = 15.12% (Validation Accuracy = 16.36%). Non-linear kernel fails to resolve overlapping lesion distributions."),
        ("Winning Selection: EfficientNet-B0", "Validation Macro-F1 = 63.26% (Validation Accuracy = 63.60%). Decisively outperformed handcrafted feature baselines by +46.24% Macro-F1, justifying deep transfer learning.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Validation Tournament & Selection Rationale", bullets_right, bg_color=COLOR_GREEN_BG, border_color=COLOR_FOREST)


def build_slide_21(prs):
    """Slide 21: Offline Training Pipeline & Loss Optimization."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Offline Training Pipeline & Loss Optimization")
    add_footer(slide, 21)

    bullets_left = [
        ("Training Ingestion Pipeline", "Images resized to 224x224 RGB and normalized with ImageNet statistics (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])."),
        ("Data Augmentation", "RandomHorizontalFlip(p=0.5), RandomRotation(degrees=15), and ColorJitter(brightness=0.15, contrast=0.15) applied to training folds to prevent memorization."),
        ("Class-Weighted Loss Function", "CrossEntropyLoss with inverse-frequency class weights w_c = N / (C * N_c) to counteract class imbalance across the 25 classes."),
        ("AdamW Differential Learning Rates", "Backbone top layers (features[5:]): lr = 1e-4, weight_decay = 1e-4. Custom classifier linear head (1280 -> 25): lr = 1e-3, weight_decay = 1e-4. Low-level features (0 to 4) frozen."),
        ("Learning Rate Schedule", "ReduceLROnPlateau(mode='max', factor=0.5, patience=2) tracking validation macro-F1.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Optimization Protocols & Hyperparameters", bullets_left)

    bullets_right = [
        ("8-Epoch Training Trajectory", "Trained for 8 epochs. Epoch 1: Val Acc 44.4%, Macro-F1 40.7% -> Epoch 4: Val Acc 60.7%, Macro-F1 59.5% -> Epoch 8: Peak Val Acc 63.6%, Macro-F1 63.26%."),
        ("Validation-Based Early Checkpointing", "Model checkpoint was locked strictly based on peak validation macro-F1 (Epoch 8 state dict saved to efficientnet_b0_foliar.pt)."),
        ("Strict Offline Boundary", "Training occurs strictly offline via scripts/train_and_evaluate_models.py (1,200.5 seconds). Runtime inference NEVER triggers retraining."),
        ("Sub-150ms Runtime Loading", "FastAPI loads the serialized 16.5 MB model checkpoint once at startup and performs instant CPU inference on uploaded leaf specimens.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Training Dynamics & Checkpoint Serialization", bullets_right)


def build_slide_22(prs):
    """Slide 22: Training, Validation & Testing Partitioning."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Training, Validation & Testing Partitioning")
    add_footer(slide, 22)

    # 3 Column Cards
    col1 = [
        ("Sample Size", "1,468 observations (60.0% of benchmark)."),
        ("Role & Purpose", "Model parameter optimization via backpropagation and AdamW gradient updates."),
        ("Class Coverage", "Stratified across all 25 supported crop-disease classes."),
        ("Data Augmentations", "Active horizontal flip, rotation, and color jitter.")
    ]
    add_card_content(slide, 0.8, 1.35, 3.75, 3.6, "Training Partition (60%)", col1)

    col2 = [
        ("Sample Size", "489 observations (20.0% of benchmark)."),
        ("Role & Purpose", "Candidate model comparison, learning rate decay scheduling, and best-checkpoint selection."),
        ("Class Coverage", "Balanced representation of all 25 classes."),
        ("Integrity Rule", "Zero gradient updates; evaluated purely in eval() mode.")
    ]
    add_card_content(slide, 4.79, 1.35, 3.75, 3.6, "Validation Partition (20%)", col2)

    col3 = [
        ("Sample Size", "490 observations (20.0% of benchmark)."),
        ("Role & Purpose", "Final unbiased held-out performance evaluation."),
        ("Reconciliation", "Exactly matches the sum of all 25 per-class test supports (reconciled from prior 491 typo)."),
        ("Lockbox Rule", "Unlocked strictly ONCE after model selection was finalized.")
    ]
    add_card_content(slide, 8.78, 1.35, 3.75, 3.6, "Held-Out Test Partition (20%)", col3)

    # Bottom Banner: Zero-Leakage Grouped Partitioning
    bullets_bottom = [
        ("Perceptual dHash Grouped Stratification", "Standard random splitting causes severe data leakage when near-duplicate frames from the same video or burst sequence land in both train and test splits."),
        ("Strict Group Isolation", "Grouped images by difference hash (dHash hamming distance <= 10). StratifiedGroupKFold ensured that all near-duplicate frames from a burst belong exclusively to one partition."),
        ("Zero Cross-Partition Leakage", "Automated cryptographic audit verified exactly 0 dHash cluster overlap across Train, Validation, and Test partitions.")
    ]
    add_card_content(slide, 0.8, 5.10, 11.73, 1.8, "Zero-Leakage Grouped Stratification Protocol", bullets_bottom, bg_color=COLOR_GREEN_BG, border_color=COLOR_FOREST)


def build_slide_23(prs):
    """Slide 23: Model Evaluation: Candidate Benchmark Comparison."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Model Evaluation: Candidate Benchmark Comparison")
    add_footer(slide, 23)

    headers = ["Model Candidate", "Input Vector", "Val Macro-F1", "Val Accuracy", "Test Accuracy", "Test Balanced Acc", "Test Macro-F1"]
    col_widths = [2.2, 1.8, 1.3, 1.3, 1.3, 1.6, 1.3]
    data = [
        ["Majority Baseline", "Prior class mode", "0.58%", "7.77%", "7.76%", "4.00%", "0.58%"],
        ["Random Forest (32D)", "32 Handcrafted Features", "17.02%", "17.38%", "19.80%", "19.78%", "19.19%"],
        ["RBF-SVM (32D)", "32 Handcrafted Features", "15.12%", "16.36%", "19.80%", "20.13%", "19.01%"],
        ["EfficientNet-B0 (DEPLOYED)", "224x224 RGB Image Pixels", "63.26%", "63.60%", "61.84%", "61.43%", "60.84%"]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(1.35), Inches(11.73), Inches(2.8))
    format_table(t_shape.table, col_widths, headers, data)

    bullets_notes = [
        ("Strict Validation Selection", "Model selection was determined solely by Validation Macro-F1 (63.26%), ensuring the held-out test split remained an uncorrupted lockbox."),
        ("Representation Comparison", "The comparison highlights input representations: 32 handcrafted global descriptors (RF & SVM) lack the spatial resolution needed for 25 fine-grained foliar classes, whereas convolutional filters learn spatial lesion borders."),
        ("Statistical Significance", "EfficientNet-B0 outperformed the best classical baseline by +41.65% Test Macro-F1 and +42.04% Test Accuracy, with non-overlapping confidence intervals.")
    ]
    add_card_content(slide, 0.8, 4.35, 11.73, 2.55, "Architectural Tournament Analysis", bullets_notes)


def build_slide_24(prs):
    """Slide 24: Final Held-Out Test Performance & Statistical Verification."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Final Held-Out Test Evaluation (N=490 Test Specimens)")
    add_footer(slide, 24)

    # 4 KPI Cards
    add_kpi_card(slide, 0.8, 1.35, 2.7, 1.3, "490 Images", "Held-Out Test Size", "Reconciled across 25 classes", COLOR_DARK_GREEN)
    add_kpi_card(slide, 3.8, 1.35, 2.7, 1.3, "61.84%", "Top-1 Test Accuracy", "+50.82% over Majority (11.02%)", COLOR_FOREST)
    add_kpi_card(slide, 6.83, 1.35, 2.7, 1.3, "61.43%", "Balanced Accuracy", "+57.43% over Chance (4.00%)", COLOR_NAVY)
    add_kpi_card(slide, 9.83, 1.35, 2.7, 1.3, "60.84%", "Macro-Averaged F1", "+60.04% over Baseline (0.80%)", COLOR_DARK_GREEN)

    # Left Column: Statistical Intervals
    b_left = [
        ("Wilson 95% Confidence Interval", "Estimated true accuracy bounds: [57.46%, 66.03%] (z = 1.96). Proves statistically significant generalization beyond baseline chance."),
        ("Zero Data Leakage Verification", "Verified that no perceptual duplicate cluster crossed between training, validation, and test splits."),
        ("No Test-Set Retuning", "The model weights were frozen prior to test set ingestion; metrics stem directly from a single evaluation pass.")
    ]
    add_card_content(slide, 0.8, 2.85, 5.7, 4.05, "Statistical Confidence & Rigor", b_left)

    # Right Column: Per-Class Highlights
    b_right = [
        ("High-Fidelity Classes (F1 > 80%)", "Bell Pepper Healthy (F1 = 95.2%), Potato Early Blight (F1 = 92.3%), Corn Gray Leaf Spot (F1 = 89.5%), Tomato Septoria (F1 = 85.7%), Grape Black Rot (F1 = 83.3%), Apple Scab (F1 = 81.2%)."),
        ("Moderate Classes (F1 = 50–75%)", "Apple Cedar Rust (F1 = 76.9%), Corn Common Rust (F1 = 71.4%), Tomato Yellow Leaf Curl (F1 = 65.3%), Tomato Late Blight (F1 = 54.5%)."),
        ("Confused Classes (F1 < 50%)", "Tomato Early Blight (F1 = 44.4%) vs Tomato Late Blight: Lesions exhibit identical circular brown necrosis in early infection stages."),
        ("Wild-Condition Complexity", "Reflects real PlantDoc field challenges: cluttered soil backgrounds, harsh sunlight, and overlapping leaves.")
    ]
    add_card_content(slide, 6.83, 2.85, 5.7, 4.05, "Per-Class Performance Highlights", b_right)


def build_slide_25(prs):
    """Slide 25: Runtime Inference Workflow & Application Demonstration."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Runtime Inference Workflow & Application Demonstration")
    add_footer(slide, 25)

    bullets_left = [
        ("Inference Execution Pipeline", "Uploaded specimen (JPG/PNG) -> Ingestion validation -> Preprocessing (224x224 RGB) -> PyTorch EfficientNet-B0 forward pass -> 25 class logits -> Softmax distribution -> Ranked candidates."),
        ("Parallel Multimodal Execution", "The 32D classical feature pipeline executes concurrently in <150 ms, providing explainable color/texture metrics alongside deep classification."),
        ("Confidence & Distribution Display", "Displays top predicted class, calibrated probability progress bar, and top-3 candidate alternatives."),
        ("Apple Healthy Test Verification", "Tested authentic PlantDoc Apple Healthy image (proc_AGRO_V2_00037.png): Predicted Apple - Healthy with 97.6% confidence."),
        ("Potato Late Blight Test Verification", "Tested authentic Potato Late Blight image (proc_AGRO_V2_00167.png): Predicted Potato - Late Blight with 96.2% confidence (Tomato Late Blight runner-up 3.1%).")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Inference Pipeline & Case Studies", bullets_left)

    # Right: Embedded screenshot of Image Analysis Workbench
    img_path = INSPECT_DIR / "crop_apple_healthy.png"
    if not img_path.exists():
        img_path = SCREENSHOT_DIR / "10_image_analysis_apple_healthy.png"
    if img_path.exists():
        slide.shapes.add_picture(str(img_path), Inches(6.83), Inches(1.50), Inches(5.7), Inches(5.07))


def build_slide_26(prs):
    """Slide 26: Cross-Modal Out-of-Domain Safeguard & Botanical Rejection."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Cross-Modal Out-of-Domain Safeguard & Rejection")
    add_footer(slide, 26)

    bullets_left = [
        ("Investigation of Rice -> Corn Prediction", "When an out-of-domain ICAR rice scanner image was uploaded, a naive closed-world CNN predicted Corn Common Rust with high probability."),
        ("Botanical Root Cause Identified", "Among the 12 training crops, Corn is the SOLE graminoid monocot (all other 11 crops are broad-leaved dicots). Rice is also a linear, parallel-veined monocot leaf."),
        ("Linear Convolutional Filters", "Linear blade edge and texture filters fired heavily on Corn features, forcing the closed-world softmax to pick Corn."),
        ("Defensible Rejection Mechanism", "Rather than fitting an unvalidated softmax heuristic on test data (which causes leakage), AgroVision-Mine implements Cross-Modal Domain Verification using the 32D descriptor store."),
        ("Automated Rejection Trigger", "Unsupervised warehouse retrieval identifies that the top reference belongs to Rice (icar_ogd), flagging status: 'unsupported_domain' and is_uncertain: true.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Botanical Root Cause & Safeguard Design", bullets_left)

    # Right: Screenshot of rice rejection
    rice_shot = INSPECT_DIR / "crop_rice_rejection.png"
    if not rice_shot.exists():
        rice_shot = SCREENSHOT_DIR / "12_image_analysis_rice_unsupported_domain.png"
    if rice_shot.exists():
        slide.shapes.add_picture(str(rice_shot), Inches(6.83), Inches(1.35), Inches(5.7), Inches(3.55))

    bullets_right = [
        ("UI Rejection Notice", "Displays prominent amber banner explaining that the leaf was matched geometrically to Corn based on monocot morphology rather than a biological diagnosis."),
        ("Academic Honesty", "Discloses that the model supports 25 benchmark classes, preventing false clinical claims on unseen species.")
    ]
    add_card_content(slide, 6.83, 5.05, 5.7, 1.80, "User Interface Behavior & Integrity", bullets_right, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER_BORDER)


def build_slide_27(prs):
    """Slide 27: Multi-Tier Software Testing & Verification Framework."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Multi-Tier Software Testing & Verification Framework")
    add_footer(slide, 27)

    # 4 KPI Cards
    add_kpi_card(slide, 0.8, 1.35, 2.7, 1.3, "117 Passed", "Total Automated Tests", "100% test success rate", COLOR_DARK_GREEN)
    add_kpi_card(slide, 3.8, 1.35, 2.7, 1.3, "0 Failures", "Zero Regressions", "Verified across all modules", COLOR_FOREST)
    add_kpi_card(slide, 6.83, 1.35, 2.7, 1.3, "10 / 10", "Browser Playwright", "Drove Chrome across 9 pages", COLOR_NAVY)
    add_kpi_card(slide, 9.83, 1.35, 2.7, 1.3, "267 ms", "Frontend Build", "React 19 + TypeScript build", COLOR_DARK_GREEN)

    headers = ["Verification Tier", "Test Scope & Tool", "Key Behaviors Tested", "Observed Outcome & Evidence"]
    col_widths = [2.2, 2.2, 4.3, 3.03]
    data = [
        ["Automated Unit & Integration", "107 Tests (pytest in 20.3s)", "ETL idempotency, GLCM textures, SQLite FK constraints, clustering reproducibility, predictor", "107 / 107 Passed in 20.30s (0 failures, 1 Starlette warning)"],
        ["Real Browser E2E Tests", "10 Tests (Playwright in 43.3s)", "Drove local Google Chrome across all 9 pages: crop filtering, specimen modal, image upload/analyze", "10 / 10 Passed in 43.32s; Zero fatal browser console exceptions"],
        ["API Smoke & Contract Tests", "11 Endpoints (FastAPI)", "Health, overview, dataset (Tomato=743), schema, OLAP SQL, clustering, rules, analyze, predict", "11 / 11 Live Endpoints 200 OK; Zero HTTP 500 exceptions"],
        ["Production Build Compilation", "Vite + TypeScript", "Full production bundle compilation (tsc -b && vite build) of 1,923 modules", "Built in 267ms (0 errors); Assets: CSS (39.9 kB), JS (379.4 kB)"]
    ]
    t_shape = slide.shapes.add_table(len(data) + 1, len(headers), Inches(0.8), Inches(2.9), Inches(11.73), Inches(3.95))
    format_table(t_shape.table, col_widths, headers, data)


def build_slide_28(prs):
    """Slide 28: Scientific Limitations, Viva Roadmap & Conclusion."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide, "Conclusion, Limitations & Viva Demonstration Plan")
    add_footer(slide, 28)

    bullets_left = [
        ("Closed-World Taxonomic Scope", "The supervised model evaluates exactly 25 classes from 12 host crops. Images outside this boundary trigger the cross-modal domain rejection safeguard."),
        ("Flatbed Scanner vs Field Domain Shift", "The 36 ICAR rice images exhibit pure white scanner backgrounds, whereas PlantDoc field images have natural soil and leaf clutter."),
        ("Non-Diagnostic Similarity Metric", "Nearest references in 32D space represent geometric descriptor proximity, not biological infection confirmation."),
        ("Laboratory vs Field Environment", "Evaluated on open benchmark test sets; does not guarantee performance across arbitrary farmer phone cameras or extreme weather conditions.")
    ]
    add_card_content(slide, 0.8, 1.35, 5.7, 5.5, "Known Scientific Limitations", bullets_left)

    bullets_right = [
        ("Step 1 — Overview & KPIs (/#/)", "Review 2,596 canonical specimens, 14 taxa, and star schema integration."),
        ("Step 2 — Dataset Explorer (/#/dataset)", "Filter by Tomato (743 records), inspect grid/table, and open specimen detail modal."),
        ("Step 3 — Specimen Analysis (/#/image-analysis)", "Upload Apple Healthy (97.6% confidence), then upload Rice to demonstrate the cross-modal out-of-domain rejection alert."),
        ("Step 4 — Star Schema & OLAP (/#/olap)", "Execute live parameterized Roll-up and Pivot queries in SQLite."),
        ("Step 5 — Visual Mining & PCA (/#/mining)", "Inspect K=2 metric-supported clusters and 2D PCA variance loadings."),
        ("Step 6 — Association Rules (/#/rules)", "Toggle Mode A (880 visual rules) vs Mode B (285 labeled rules), demonstrating exact Apriori/FP-Growth parity.")
    ]
    add_card_content(slide, 6.83, 1.35, 5.7, 5.5, "Faculty Live Demonstration Roadmap (Viva)", bullets_right, bg_color=COLOR_GREEN_BG, border_color=COLOR_FOREST)


# -----------------------------------------------------------------------------
# MAIN GENERATOR PIPELINE
# -----------------------------------------------------------------------------

def main():
    print("======================================================================")
    print("BUILDING AGROVISION-MINE UPDATED FACULTY PRESENTATION")
    print("======================================================================")

    prs = init_presentation()

    builders = [
        (1, build_slide_01),
        (2, build_slide_02),
        (3, build_slide_03),
        (4, build_slide_04),
        (5, build_slide_05),
        (6, build_slide_06),
        (7, build_slide_07),
        (8, build_slide_08),
        (9, build_slide_09),
        (10, build_slide_10),
        (11, build_slide_11),
        (12, build_slide_12),
        (13, build_slide_13),
        (14, build_slide_14),
        (15, build_slide_15),
        (16, build_slide_16),
        (17, build_slide_17),
        (18, build_slide_18),
        (19, build_slide_19),
        (20, build_slide_20),
        (21, build_slide_21),
        (22, build_slide_22),
        (23, build_slide_23),
        (24, build_slide_24),
        (25, build_slide_25),
        (26, build_slide_26),
        (27, build_slide_27),
        (28, build_slide_28),
    ]

    for s_num, builder in builders:
        print(f"Generating Slide {s_num:02d} of {TOTAL_SLIDES}...")
        builder(prs)

    output_path = ROOT_DIR / "AgroVision-Mine_Final_Review_Updated.pptx"
    prs.save(str(output_path))
    print(f"\n[SUCCESS] Successfully generated presentation at:")
    print(f"  {output_path} ({os.path.getsize(output_path):,} bytes, {len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
