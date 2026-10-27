"""AgroVision-Mine: IEEE Conference Paper Word (.docx) & PDF Generator.
Builds an authentic two-column IEEE conference paper matching IEEE formatting standards:
- 24pt bold title
- 3-column author block
- Bold italic abstract and index terms
- Two-column body layout (3.4" width, 0.25" gap)
- Roman numeral headings
- Formatted tables with IEEE captions
- Embedded high-resolution figures
- Numbered IEEE citations matching references.bib
- Direct Word COM PDF export (SaveAs2 format=17)
"""
import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = ROOT / "research_paper"
FIG_DIR = PAPER_DIR / "figures"
DOCX_OUT = PAPER_DIR / "AgroVision_Mine_IEEE_Conference_Paper.docx"
PDF_OUT = PAPER_DIR / "AgroVision_Mine_IEEE_Conference_Paper.pdf"

FONT_NAME = "Times New Roman"

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/><w:insideV w:val="none"/><w:left w:val="none"/><w:right w:val="none"/></w:tblBorders>')
    tblPr.append(borders)

def make_callout_box(doc, text_content):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text_content)
    run.font.name = FONT_NAME
    run.font.size = Pt(8.5)
    run.font.italic = True

def add_ieee_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text.upper())
    run.font.name = FONT_NAME
    run.font.size = Pt(10)
    run.font.bold = True

def add_ieee_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(9.5)
    run.font.italic = True
    run.font.bold = True

def add_ieee_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(9.0)
    run.font.italic = True

def add_body_p(doc, text, bold_prefix=None, indent=0.18):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.02
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.5)
    if indent > 0:
        p.paragraph_format.first_line_indent = Inches(indent)

    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = FONT_NAME
        r_b.font.size = Pt(9.0)
        r_b.font.bold = True

    r = p.add_run(text)
    r.font.name = FONT_NAME
    r.font.size = Pt(9.0)
    return p

def add_equation_p(doc, eq_text, eq_num):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    # Equation text (tabbed)
    r_eq = p.add_run(f"\t{eq_text}")
    r_eq.font.name = FONT_NAME
    r_eq.font.size = Pt(9.0)
    r_eq.font.italic = True

    # Tab to right margin for equation number
    r_num = p.add_run(f"\t({eq_num})")
    r_num.font.name = FONT_NAME
    r_num.font.size = Pt(9.0)

def add_figure(doc, img_filename, caption_text, width_inches=3.2):
    img_path = FIG_DIR / img_filename
    if img_path.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(str(img_path), width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(4)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = FONT_NAME
        run_cap.font.size = Pt(8.0)
    else:
        print(f"Warning: Figure {img_path} not found.")

def set_section_two_columns(section):
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        col = cols[0]
        col.set(qn('w:num'), '2')
        col.set(qn('w:space'), '360') # 0.25 in dxa
    else:
        new_cols = parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="360"/>')
        sectPr.append(new_cols)

def build_paper_docx():
    print("Building IEEE Conference Paper DOCX...")
    doc = docx.Document()

    # Page Margins: Standard IEEE (Top: 0.75", Bottom: 1.0", Left: 0.625", Right: 0.625")
    section1 = doc.sections[0]
    section1.top_margin = Inches(0.75)
    section1.bottom_margin = Inches(1.0)
    section1.left_margin = Inches(0.625)
    section1.right_margin = Inches(0.625)
    section1.page_width = Inches(8.5)
    section1.page_height = Inches(11.0)

    # 1. Title (Single column)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence")
    r_title.font.name = FONT_NAME
    r_title.font.size = Pt(22)
    r_title.font.bold = True

    # 2. Author Block Table (3 columns, borderless)
    table_auth = doc.add_table(rows=1, cols=3)
    table_auth.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_auth.autofit = False

    authors = [
        ("Boomika V", "School of Computer Science & Eng. (SCOPE)\nVellore Institute of Technology (VIT)\nChennai, Tamil Nadu, India\nboomika.v2023@vitstudent.ac.in"),
        ("Ajay M", "School of Computer Science & Eng. (SCOPE)\nVellore Institute of Technology (VIT)\nChennai, Tamil Nadu, India\najay.m2023@vitstudent.ac.in"),
        ("Dr. Devipriya A", "Associate Professor, SCOPE\nVellore Institute of Technology (VIT)\nChennai, Tamil Nadu, India\ndevipriya.a@vit.ac.in")
    ]

    for idx, (name, affil) in enumerate(authors):
        cell = table_auth.cell(0, idx)
        cell.width = Inches(2.4)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r_n = p.add_run(name + "\n")
        r_n.font.name = FONT_NAME
        r_n.font.size = Pt(10.5)
        r_n.font.bold = True

        r_a = p.add_run(affil)
        r_a.font.name = FONT_NAME
        r_a.font.size = Pt(8.5)
        r_a.font.italic = True

    # Spacing before Abstract
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(10)
    p_sp.paragraph_format.space_after = Pt(0)

    # 3. Abstract Paragraph
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.line_spacing = 1.05
    p_abs.paragraph_format.space_after = Pt(4)
    r_ab_hdr = p_abs.add_run("Abstract—")
    r_ab_hdr.font.name = FONT_NAME
    r_ab_hdr.font.size = Pt(9.0)
    r_ab_hdr.font.bold = True
    r_ab_hdr.font.italic = True

    abs_text = (
        "Contemporary agricultural computer vision models predominantly formulate plant pathology as an isolated, "
        "single-image classification task, decoupling high-dimensional pixel data from botanical taxonomy, capture metadata, "
        "and relational analytical workflows. Consequently, agronomists and decision-support systems cannot perform multidimensional "
        "slicing across pathogen families or audit visual quality across heterogeneous acquisitions. In this paper, we propose "
        "AgroVision-Mine, a unified, reproducible multimodal data warehousing and visual pattern mining framework for foliar disease intelligence. "
        "The framework integrates an automated five-stage quality gate pipeline, a 32-dimensional explainable visual descriptor engine "
        "(19 color moments, 7 Haralick textures, and 6 morphometric metrics), and a Kimball-style dimensional data warehouse in SQLite with verified "
        "referential integrity across 2,596 canonical observations spanning 14 host crops. On top of this relational substrate, we implement sub-35 ms "
        "ANSI SQL OLAP operations (Roll-up, Drill-down, Slice, Dice, and Pivot), metric-supported visual clustering (K=2 primary Silhouette score of 0.4060), "
        "2D PCA projection (52.11% cumulative explained variance), and association rule mining exhibiting 100% algorithmic parity between Apriori and "
        "FP-Growth (Delta = 0.0). To deliver bounded diagnostic support, we develop a supervised deep learning module using transfer learning with "
        "EfficientNet-B0 across 25 composite crop-condition classes (2,447 PlantDoc images). Under strict perceptual difference-hash (dHash) grouped partitioning "
        "that eliminates near-duplicate leakage, EfficientNet-B0 achieves 63.26% validation Macro-F1 (substantially outperforming handcrafted Random Forest at 17.02% "
        "and RBF-SVM at 15.12%) and achieves 61.84% Top-1 Accuracy (61.43% Balanced Accuracy, 60.84% Macro-F1, Wilson 95% CI: [57.46%, 66.03%]) on 490 held-out test images. "
        "Finally, we formulate a cross-modal domain verification safeguard that detects out-of-distribution acquisitions—such as flatbed scanner rice leaf images (N=36)—"
        "preventing false diagnostic attributions on unsupported botanical domains. The complete framework is verified through 117 automated unit, integration, and browser end-to-end tests."
    )
    r_ab_txt = p_abs.add_run(abs_text)
    r_ab_txt.font.name = FONT_NAME
    r_ab_txt.font.size = Pt(9.0)
    r_ab_txt.font.bold = True

    # 4. Index Terms Paragraph
    p_idx = doc.add_paragraph()
    p_idx.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_idx.paragraph_format.line_spacing = 1.05
    p_idx.paragraph_format.space_after = Pt(14)
    r_idx_hdr = p_idx.add_run("Index Terms—")
    r_idx_hdr.font.name = FONT_NAME
    r_idx_hdr.font.size = Pt(9.0)
    r_idx_hdr.font.bold = True
    r_idx_hdr.font.italic = True

    r_idx_txt = p_idx.add_run("Agricultural Computer Vision, Multimodal Data Warehouse, OLAP Analytics, Feature Engineering, Transfer Learning, EfficientNet-B0, Association Rule Mining, Out-of-Distribution Detection.")
    r_idx_txt.font.name = FONT_NAME
    r_idx_txt.font.size = Pt(9.0)
    r_idx_txt.font.italic = True

    # 5. Continuous Section Break for Two-Column Layout
    section2 = doc.add_section(docx.enum.section.WD_SECTION.CONTINUOUS)
    section2.top_margin = Inches(0.75)
    section2.bottom_margin = Inches(1.0)
    section2.left_margin = Inches(0.625)
    section2.right_margin = Inches(0.625)
    set_section_two_columns(section2)

    # -------------------------------------------------------------------------
    # I. INTRODUCTION
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "I. Introduction")
    add_body_p(doc, "Global food security is profoundly threatened by agricultural plant pathogens and foliar pests, which cause estimated global harvest yield losses ranging from 20% to 40% annually [1]. Timely, accurate pathological identification is vital to containment; however, manual expert agronomist scouting is labor-intensive, logistically constrained, and inaccessible to smallholder farming communities [2]. While deep convolutional neural networks (CNNs) have shown exceptional perceptual capability in controlled laboratory benchmarks such as PlantVillage [3], [4], practical deployments in natural, unconstrained farm environments face severe performance degradation [5], [6].")
    
    add_body_p(doc, "Crucially, existing agricultural deep learning systems treat foliar pathology as an isolated black-box classification exercise. Three fundamental structural deficiencies characterize conventional paradigms:")
    add_body_p(doc, "High-dimensional foliar imagery is divorced from relational botanical taxonomy (crop family, genus, order), capture equipment parameters (sensor resolution, lighting, aspect ratio), and epidemiological hierarchies (fungal, bacterial, viral, abiotic) [7]. Agronomists cannot perform relational slicing (e.g., comparing necrotic lesion expansion across Solanaceae crops versus Fabaceae crops).", bold_prefix="1) Metadata and Relational Decoupling: ")
    add_body_p(doc, "Public agricultural corpora scraped from web sources frequently suffer from truncated byte streams, corrupted image headers, duplicate frames, and unstandardized orientations [5]. Conventional deep learning pipelines silently consume these anomalies, leading to latent bias and unverified dataset provenance [8].", bold_prefix="2) Lack of Pre-Ingestion Data Governance: ")
    add_body_p(doc, "As demonstrated by Geirhos et al. [9], deep networks frequently latch onto spurious background shortcuts (e.g., flatbed scanner backgrounds, soil textures, or acquisition framing) rather than genuine pathological lesions. An unconditioned binary classifier (Healthy vs. Diseased) trained across heterogeneous crops is fundamentally confounded when certain host species in the training corpus possess only healthy or only diseased specimens.", bold_prefix="3) Confounding and Shortcut Learning: ")

    add_body_p(doc, "To resolve these practical and methodological challenges, we introduce AgroVision-Mine, an open, reproducible, and verifiable multimodal data warehousing and visual pattern mining platform. AgroVision-Mine integrates relational dimensional modeling with explainable classical computer vision descriptors and bounded deep transfer learning. Rather than proposing an ungrounded black-box architecture, our framework enforces strict data governance, cryptographic dataset immutability, sub-35 ms relational Online Analytical Processing (OLAP) queries, and rigorous statistical hypothesis validation.")

    add_ieee_heading_2(doc, "A. Principal Contributions")
    add_body_p(doc, "The primary scientific and technical contributions of this investigation are:")
    add_body_p(doc, "We design and implement an automated five-stage quality gate enforcing header magic-byte verification, minimum spatial geometry, payload limits, MD5 hash deduplication, and EXIF transposition, guaranteeing zero corrupted or duplicate records enter the canonical warehouse.", bold_prefix="• End-to-End Data Governance: ")
    add_body_p(doc, "We architect a formal relational star schema in SQLite with native foreign-key constraints (PRAGMA foreign_keys = ON), linking a central fact table of 2,596 validated specimen observations to four normalized dimensions (dim_crop, dim_disease, dim_image, and dim_visual_feature).", bold_prefix="• Multimodal Kimball Star Schema: ")
    add_body_p(doc, "We implement real SQL-backed Roll-up, Drill-down, Slice, Dice, and Pivot operations, providing agronomists with multi-dimensional analytical views across botanical families and pathogen classes with query execution latencies below 35 ms.", bold_prefix="• ANSI SQL-Backed OLAP Engine: ")
    add_body_p(doc, "We engineer an explainable descriptor vector space combining 19 Color Moments, 7 Haralick Gray-Level Co-occurrence Matrix (GLCM) textural metrics, and 6 Morphometric contours, providing transparent physical features alongside deep neural embeddings.", bold_prefix="• Explainable 32D Visual Feature Store: ")
    add_body_p(doc, "We demonstrate optimal unsupervised visual clustering (K=2 Silhouette score 0.4060) and 2D Principal Component Analysis (52.11% explained variance), coupled with association rule mining demonstrating 100% algorithmic parity between Apriori and FP-Growth (Delta = 0.0000 across support, confidence, and lift).", bold_prefix="• Dual-Track Pattern Mining: ")
    add_body_p(doc, "We evaluate an EfficientNet-B0 transfer learning module on a 25-class composite foliar benchmark (2,447 PlantDoc images) partitioned via grouped perceptual difference-hashing (dHash). The model achieves 63.26% validation Macro-F1 (vs. 17.02% for Random Forest) and 61.84% Top-1 Accuracy (60.84% Macro-F1, Wilson 95% CI: [57.46%, 66.03%]) on 490 held-out test images.", bold_prefix="• Bounded Supervised Classification: ")
    add_body_p(doc, "We formulate an automated rejection mechanism utilizing 32D descriptor nearest-reference retrieval to flag out-of-distribution acquisitions (e.g., flatbed scanner rice leaf observations, N=36), preventing false clinical claims on unseen botanical domains.", bold_prefix="• Cross-Modal Out-of-Domain Safeguard: ")

    # -------------------------------------------------------------------------
    # II. RELATED WORK
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "II. Related Work and Research Gap")
    add_body_p(doc, "The application of deep convolutional neural networks to foliar disease identification accelerated with the release of the PlantVillage benchmark [3]. Mohanty et al. [2] evaluated AlexNet and GoogLeNet architectures across 54,306 laboratory images, reporting classification accuracies exceeding 99.3%. Similarly, Ferentinos [4] benchmarked VGG, ResNet, and DenseNet architectures, achieving 99.5% accuracy. However, subsequent critical evaluations by Barbedo [1] and Singh et al. [5] revealed that these laboratory-trained models fail catastrophically when exposed to in-the-wild field conditions. Background homogeneity, uniform lighting, and lack of occlusions in laboratory settings act as spurious non-pathological shortcuts [9].")

    add_body_p(doc, "To bridge this gap, Singh et al. [5] introduced the PlantDoc dataset, comprising 2,560 authentic field images captured across natural lighting, varied camera sensors, and complex foliage clutter. Standard vision models benchmarked on PlantDoc achieved significantly lower accuracies (30%–40%), underscoring the intrinsic difficulty of real-world foliar pathology. Too et al. [6] demonstrated that modern compact convolutional architectures, particularly DenseNets and MobileNets, offer favorable parameter efficiency over older VGG networks. Tan and Le [10] proposed EfficientNet, utilizing compound scaling across network depth, width, and input resolution. In our work, we leverage ImageNet-1K pretrained EfficientNet-B0 as a compact, high-capacity feature extractor for bounded foliar classification.")

    add_body_p(doc, "Prior to deep learning dominance, agricultural image processing relied on handcrafted color, texture, and morphological features [11]. Haralick's GLCM descriptors (contrast, dissimilarity, homogeneity, energy, and correlation) capture spatial gray-level dependencies that reflect leaf necrosis and tissue mottling. While classical feature vectors rarely match deep networks on high-capacity multiclass benchmarks, they possess significant advantages in interpretability, low computational overhead, and zero data-hungry training requirements [12]. In AgroVision-Mine, we do not discard handcrafted descriptors; instead, we engineer a standardized 32-dimensional continuous feature store that operates in parallel with deep embeddings, powering unsupervised K-Means clustering, PCA ordination, and association rule discovery via Apriori [13] and FP-Growth [14].")

    add_body_p(doc, "Dimensional modeling, formulated by Kimball and Ross [7], represents the industry standard for organizing operational enterprise data for Online Analytical Processing (OLAP) [15]. While widely adopted in finance, retail, and supply chain domains, dimensional modeling has rarely been integrated into computer vision pipelines. Vision datasets are typically stored as unstructured flat folders, stripping away relational taxonomy and precluding complex analytical queries. AgroVision-Mine bridges this divide by formalizing image observations as relational facts linked to botanical, pathological, and technical dimensions within a zero-configuration SQLite warehouse [16].")

    # Table I: Literature Comparison
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(8)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.keep_with_next = True
    r_t1 = p_t1.add_run("TABLE I\nSYSTEMATIC COMPARATIVE ANALYSIS OF SURVEYED AGRICULTURAL VISION SYSTEMS")
    r_t1.font.name = FONT_NAME
    r_t1.font.size = Pt(8.5)
    r_t1.font.bold = True

    t_lit = doc.add_table(rows=7, cols=5)
    t_lit.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_lit.autofit = False
    set_table_borders(t_lit)

    lit_headers = ["Study & Dataset", "Core Architecture", "Warehouse Star Schema", "Handcrafted 32D Features", "Out-of-Domain Safeguard"]
    col_w = [1.2, 0.9, 0.5, 0.45, 0.35]
    for c_i, h_txt in enumerate(lit_headers):
        cell = t_lit.cell(0, c_i)
        cell.width = Inches(col_w[c_i])
        set_cell_shading(cell, "EAEAEA")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = FONT_NAME
        run.font.size = Pt(7.5)
        run.font.bold = True

    lit_data = [
        ["Mohanty et al. [2] (PlantVillage)", "AlexNet, GoogLeNet", "No", "No", "No"],
        ["Ferentinos [4] (PlantVillage)", "VGG, ResNet-50", "No", "No", "No"],
        ["Barbedo [1] (Proprietary Lab)", "Transfer Learning", "No", "No", "No"],
        ["Too et al. [6] (PlantVillage)", "DenseNet-121, VGG-16", "No", "No", "No"],
        ["Singh et al. [5] (PlantDoc)", "Faster R-CNN, MobileNet", "No", "No", "No"],
        ["AgroVision-Mine (Ours)\n(PlantDoc + ICAR, N=2,596)", "Kimball Star Schema +\nEfficientNet-B0 + OLAP", "Yes (SQLite\nForeign Keys)", "Yes (19 Color,\n7 GLCM, 6 Morph)", "Yes (Cross-Modal\n32D Retrieval)"]
    ]

    for r_i, row in enumerate(lit_data):
        row_num = r_i + 1
        for c_i, val in enumerate(row):
            cell = t_lit.cell(row_num, c_i)
            cell.width = Inches(col_w[c_i])
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            if r_i == len(lit_data) - 1:
                set_cell_shading(cell, "F0F7F4")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i > 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = FONT_NAME
            run.font.size = Pt(7.5)
            if r_i == len(lit_data) - 1:
                run.font.bold = True

    # -------------------------------------------------------------------------
    # III. SYSTEM ARCHITECTURE
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "III. System Architecture and Data Flow")
    add_body_p(doc, "AgroVision-Mine is structured as a five-layer end-to-end analytical pipeline, depicted in Fig. 1. The architecture decouples data ingestion, feature store extraction, dimensional relational persistence, analytical mining engines, and presentation delivery.")

    add_figure(doc, "fig1_system_architecture.png", "Fig. 1. End-to-End Five-Layer System Architecture of AgroVision-Mine, illustrating data ingestion quality gates, feature store extraction, Kimball relational warehouse, dual analytical branches (SQL OLAP / visual mining vs. deep transfer learning), and presentation delivery.", width_inches=3.4)

    add_body_p(doc, "The ingestion tier accepts heterogeneous agricultural imagery from web-scraped field repositories (PlantDoc) and flatbed scanner archives (ICAR/OGD). To prevent data corruption, every candidate file must sequentially pass five automated quality gates: Gate 1 verifies JPEG/PNG magic bytes; Gate 2 enforces spatial geometry (H >= 100, W >= 100); Gate 3 sets a 15 MB payload ceiling; Gate 4 applies MD5 bitstream deduplication; and Gate 5 performs EXIF loss-free transposition and RGB channel standardization.", bold_prefix="A. Layer 1: Ingestion & Quality Control—")

    add_body_p(doc, "Validated images are preprocessed through bilinear interpolation to a standardized 256x256 RGB representation for canonical feature extraction. Thirty-two continuous descriptors are extracted across color, texture, and morphometry, producing the frozen analytical feature matrix X in R^(2596 x 32). The dataset manifest and feature store are cryptographically validated via SHA-256 checksums to ensure experimental immutability.", bold_prefix="B. Layer 2: Preprocessing & Feature Store—")

    add_body_p(doc, "The relational persistence layer implements a Kimball star schema in SQLite [7]. The central fact table, disease_observation_fact, links 2,596 specimen records to four normalized dimensions through integer surrogate keys: dim_crop, dim_disease, dim_image, and dim_visual_feature. Referential integrity is enforced at the database engine level via PRAGMA foreign_keys = ON.", bold_prefix="C. Layer 3: Relational Data Warehouse & ETL—")

    add_body_p(doc, "The system bifurcates into two independent, complementary analytical branches: (1) Descriptor-Based Relational & Unsupervised Branch: Operates on the standardized 32D handcrafted feature matrix and the relational star schema, powering ANSI SQL OLAP operations, K-Means clustering, 2D PCA ordination, Apriori/FP-Growth association rule mining, and nearest-reference Euclidean similarity retrieval. (2) Deep Supervised Transfer Learning Branch: Operates directly on standardized 224x224 RGB image tensors. An EfficientNet-B0 CNN fine-tuned on 25 composite classes outputs class logits, softmax probability distributions, and domain uncertainty indicators. Crucially, the deep neural network does not consume the 32 handcrafted descriptors as input; both pipelines remain mathematically and architecturally distinct.", bold_prefix="D. Layer 4: Dual-Track Analytical Engines—")

    add_body_p(doc, "The application tier couples an asynchronous FastAPI backend (:8001) [17] with a responsive React 19 and TypeScript single-page application (SPA). Nine specialized views provide agronomists with interactive dataset exploration, live SQL execution, multidimensional charts, and a real-time Visual Specimen Workbench.", bold_prefix="E. Layer 5: Presentation & Delivery Tier—")

    # -------------------------------------------------------------------------
    # IV. METHODOLOGY & MATHEMATICAL FORMULATION
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "IV. Methodology and Mathematical Formulation")

    add_ieee_heading_2(doc, "A. Multimodal Star Schema Design")
    add_body_p(doc, "The relational star schema (Fig. 2) models agricultural foliar observations at the grain of one validated specimen per fact row. The central fact table, disease_observation_fact, records observation measures (lesion_severity_score, image_sharpness_score) linked to four foreign dimensions:")
    add_body_p(doc, "dim_crop stores botanical taxonomy (crop_name, botanical_name, crop_category); dim_disease records pathology hierarchies (disease_name, pathogen_type, causal_agent); dim_image holds technical file metadata (filename, raw_path, processed_path, md5_hash); and dim_visual_feature persists all 32 normalized descriptors alongside cluster assignments.", bold_prefix="• Dimensional Relations: ")

    add_figure(doc, "fig2_star_schema.png", "Fig. 2. AgroVision-Mine Kimball Star Schema: Central fact table (disease_observation_fact) surrounded by four normalized dimensions with enforced foreign key integrity.", width_inches=3.4)

    add_ieee_heading_2(doc, "B. Explainable Visual Feature Extraction")
    add_body_p(doc, "The 32 continuous descriptors are mathematically formulated across three distinct visual domains:")

    add_ieee_heading_3(doc, "1) Color Moments (19 Descriptors):")
    add_body_p(doc, "Let I_c(x, y) denote the intensity of color channel c in {R, G, B} at coordinate (x, y) over an M x N image. The first two statistical color moments are computed as:")
    add_equation_p(doc, "mu_c = (1 / MN) * sum_{x=1}^M sum_{y=1}^N I_c(x, y)", "1")
    add_equation_p(doc, "sigma_c = sqrt( (1 / MN) * sum_{x=1}^M sum_{y=1}^N (I_c(x, y) - mu_c)^2 )", "2")
    add_body_p(doc, "Normalized chromaticities r, g, b = I_c / (R + G + B) and HSV moments (mu_H, sigma_H, mu_S, sigma_S, mu_V, sigma_V) are appended. To isolate vegetative chlorophyll content from soil backgrounds, the Excess Green Index (ExG) is computed pixel-wise:")
    add_equation_p(doc, "ExG(x, y) = 2G(x, y) - R(x, y) - B(x, y)", "3")

    add_ieee_heading_3(doc, "2) Haralick GLCM Textures (7 Descriptors):")
    add_body_p(doc, "Texture statistics are computed from the Gray-Level Co-occurrence Matrix P(i, j | d=1, theta) averaged over orientations theta in {0, 45, 90, 135 deg} [11]:")
    add_equation_p(doc, "Contrast = sum_{i,j} |i - j|^2 P(i, j)", "4")
    add_equation_p(doc, "Homogeneity = sum_{i,j} P(i, j) / (1 + |i - j|^2)", "5")
    add_equation_p(doc, "ASM = sum_{i,j} P(i, j)^2,   Energy = sqrt(ASM)", "6")

    add_ieee_heading_3(doc, "3) Contour Morphometrics (6 Descriptors):")
    add_body_p(doc, "From binary foliar leaf masks, area A, perimeter P, bounding box aspect ratio AR, circularity C_circ, solidity S, and lesion coverage ratio LCR are extracted:")
    add_equation_p(doc, "C_circ = (4 * pi * A) / P^2,   S = A / A_hull,   LCR = A_lesion / A_leaf", "7")

    add_ieee_heading_3(doc, "4) Feature Standardization:")
    add_body_p(doc, "To eliminate scale sensitivity across disparate units, all 32 continuous descriptors are standardized via z-score normalization:")
    add_equation_p(doc, "z_{ij} = (x_{ij} - mu_j) / sigma_j,   forall j in {1, ..., 32}", "8")

    add_ieee_heading_2(doc, "C. Unsupervised Mining & Ordination")
    add_body_p(doc, "K-Means partitioning minimizes the Within-Cluster Sum of Squares (WCSS):")
    add_equation_p(doc, "J_K = sum_{k=1}^K sum_{z_i in C_k} || z_i - mu_k ||_2^2", "9")
    add_body_p(doc, "Cluster validity is assessed across K in [2, 8] via the Silhouette coefficient s(i) = (b(i) - a(i)) / max(a(i), b(i)). PCA projects the standardized matrix Z onto the principal eigenvectors of covariance matrix Sigma = (1 / (N-1)) Z^T Z.")

    add_body_p(doc, "Association rule mining extracts frequent itemsets from 12 discretized visual descriptors. Rules X => Y are evaluated via confidence and lift:")
    add_equation_p(doc, "conf(X => Y) = supp(X union Y) / supp(X)", "10")
    add_equation_p(doc, "lift(X => Y) = conf(X => Y) / supp(Y)", "11")

    add_ieee_heading_2(doc, "D. Supervised Deep Learning Formulation")
    add_body_p(doc, "For bounded multiclass classification across C=25 composite crop-condition classes, we employ EfficientNet-B0 [10], which applies compound scaling across depth d = alpha^phi, width w = beta^phi, and resolution r = gamma^phi (alpha=1.2, beta=1.1, gamma=1.15). Pretrained on ImageNet-1K [18], the final linear layer is replaced with a custom projection head W_c in R^(25 x 1280):")
    add_equation_p(doc, "z = W_c * GAP(F_backbone(x)) + b_c", "12")
    add_equation_p(doc, "p_k = exp(z_k) / sum_{j=1}^{25} exp(z_j)", "13")
    add_body_p(doc, "Model parameters are optimized by minimizing multi-class Cross-Entropy Loss via AdamW (weight decay lambda = 10^-4) with differential learning rates (backbone: 10^-4, head: 10^-3) and dynamic ReduceLROnPlateau scheduling.")

    add_body_p(doc, "Statistical uncertainty around held-out test accuracy p^ is quantified using the Wilson Score Interval with continuity correction at a 95% confidence level (z=1.96) [19]:")
    add_equation_p(doc, "CI_95 = ( p^ + z^2/(2n) +/- z * sqrt( p^(1-p^)/n + z^2/(4n^2) ) ) / ( 1 + z^2/n )", "14")

    # -------------------------------------------------------------------------
    # V. EXPERIMENTAL SETUP
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "V. Experimental Setup and Evaluation Protocol")
    add_body_p(doc, "The canonical dataset manifest (canonical_dataset_v2.csv) contains exactly 2,596 authentic foliar observations across 14 host crops: 2,560 PlantDoc field images (98.61%) and 36 ICAR/OGD flatbed scanner rice leaf images (1.39%). Annotations comprise 1,750 diseased specimens (67.41%) and 846 healthy specimens (32.59%).")

    add_body_p(doc, "In web-scraped corpora like PlantDoc, identical or burst-captured frames frequently appear under different filenames. Random partitioning introduces severe data leakage. To ensure complete leakage isolation, we compute 64-bit difference hashes (dHash) [20] across all images. Observations with Hamming distance D_H <= 10 are clustered into disjoint equivalence groups. Using StratifiedGroupKFold, these groups are assigned atomically to training, validation, or test partitions. Cross-partition verification confirms that zero perceptual hash groups cross partition boundaries.", bold_prefix="A. Perceptual Hash Leakage Prevention Protocol—")

    add_body_p(doc, "The canonical corpus is partitioned into three distinct operational sets: (1) Primary Benchmark (N=2,447): Encompasses 25 composite classes across 12 host crops, split into 1,468 train (60.0%), 489 validation (20.0%), and 490 test specimens (20.0%). (2) Excluded Rare Classes (N=113): Six rare classes with fewer than 15 total images are excluded from training to prevent extreme class collapse. (3) Out-of-Domain Scanner Subset (N=36): The 36 ICAR rice scanner images are withheld completely from training and evaluation benchmarks, serving as a dedicated distributional shift test set.", bold_prefix="B. Benchmark Partitions—")

    # -------------------------------------------------------------------------
    # VI. RESULTS & DISCUSSION
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "VI. Empirical Results and Discussion")

    add_ieee_heading_2(doc, "A. Model Selection Tournament")
    add_body_p(doc, "To justify the selection of EfficientNet-B0, we conducted a model comparison tournament evaluated strictly on the 489-sample validation partition. We benchmarked three distinct algorithmic paradigms: Zero-Rule Majority Baseline, RBF-SVM (32D), Random Forest (32D), and fine-tuned EfficientNet-B0.")

    add_figure(doc, "fig3_model_tournament.png", "Fig. 3. Model Selection Tournament: Validation Macro-F1 (model selection metric) and Held-Out Test Macro-F1 across handcrafted baselines and fine-tuned EfficientNet-B0.", width_inches=3.4)

    # Table II: Tournament
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.space_before = Pt(6)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.keep_with_next = True
    r_t2 = p_t2.add_run("TABLE II\nMODEL SELECTION TOURNAMENT ON VALIDATION PARTITION")
    r_t2.font.name = FONT_NAME
    r_t2.font.size = Pt(8.5)
    r_t2.font.bold = True

    t_tourn = doc.add_table(rows=5, cols=4)
    t_tourn.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tourn.autofit = False
    set_table_borders(t_tourn)

    t2_headers = ["Model Architecture", "Input Feature Space", "Val Macro-F1", "Test Macro-F1"]
    col_w2 = [1.2, 1.0, 0.6, 0.6]
    for c_i, h_txt in enumerate(t2_headers):
        cell = t_tourn.cell(0, c_i)
        cell.width = Inches(col_w2[c_i])
        set_cell_shading(cell, "EAEAEA")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = FONT_NAME
        run.font.size = Pt(7.5)
        run.font.bold = True

    t2_data = [
        ["Majority Baseline", "Prior Class Only", "0.58%", "0.58%"],
        ["RBF-SVM (C=10)", "Handcrafted 32D", "15.12%", "19.01%"],
        ["Random Forest (200 trees)", "Handcrafted 32D", "17.02%", "19.19%"],
        ["EfficientNet-B0 (Ours)", "224x224 RGB Tensors", "63.26%", "60.84%"]
    ]
    for r_i, row in enumerate(t2_data):
        row_num = r_i + 1
        for c_i, val in enumerate(row):
            cell = t_tourn.cell(row_num, c_i)
            cell.width = Inches(col_w2[c_i])
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            if r_i == 3:
                set_cell_shading(cell, "F0F7F4")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = FONT_NAME
            run.font.size = Pt(7.5)
            if r_i == 3:
                run.font.bold = True

    add_body_p(doc, "As reported in Table II and Fig. 3, classical classifiers trained on handcrafted descriptors achieve validation Macro-F1 scores of only 15.12% (SVM) and 17.02% (Random Forest). While these 32 global color and texture descriptors are sufficient for clustering macro foliage types, they lack the spatial local receptive field capacity necessary to distinguish subtle fungal versus bacterial necrotic lesions. EfficientNet-B0 achieves a validation Macro-F1 of 63.26%—an absolute improvement of +46.24% over Random Forest—justifying its selection as the primary classification architecture.")

    add_ieee_heading_2(doc, "B. Held-Out Test Performance and Metrics")
    add_body_p(doc, "Evaluating the frozen EfficientNet-B0 checkpoint once on the unseen held-out test partition (N=490) yielded a Top-1 Accuracy of 61.84% (303 / 490 correct), Balanced Accuracy of 61.43%, Macro-F1 of 60.84%, and a Wilson 95% Confidence Interval of [57.46%, 66.03%]. Fig. 4 illustrates the normalized confusion matrix, and Fig. 5 shows the ranked per-class F1 distribution.")

    add_figure(doc, "fig4_confusion_matrix.png", "Fig. 4. Normalized 25-Class Confusion Matrix evaluated on the 490 held-out PlantDoc test images, illustrating strong diagonal density alongside Solanaceae lesion confounding.", width_inches=3.4)

    add_figure(doc, "fig6_per_class_f1.png", "Fig. 5. Ranked Per-Class F1-Score Breakdown across all 25 evaluated composite classes on the held-out test partition (N=490).", width_inches=3.4)

    add_body_p(doc, "Inspection of per-class performance reveals marked disparities: Distinctive pathological morphology achieves high fidelity, such as Squash Powdery Mildew (F1 = 90.57%), Raspberry Healthy (F1 = 83.33%), and Corn Northern Leaf Blight (F1 = 75.00%). Conversely, necrotic Solanaceae foliar diseases exhibit severe visual confounding: Tomato Bacterial Spot (F1 = 25.00%), Potato Early Blight (F1 = 32.43%), and Potato Late Blight (F1 = 39.22%). In real-world field conditions, circular dark brown necrotic spots produced by Xanthomonas campestris (Bacterial Spot) and Alternaria solani (Early Blight) exhibit near-identical visual morphology and irregular concentric halos.", bold_prefix="• Biological Confounding Analysis: ")

    add_ieee_heading_2(doc, "C. Relational OLAP Performance")
    add_body_p(doc, "Table III summarizes query execution latencies across the five primary OLAP operations executed against the physical SQLite star schema instance (2,596 fact records). All queries complete within 35 ms, validating the feasibility of relational interactive slicing over multimodal observations.")

    # Table III: OLAP
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.space_before = Pt(6)
    p_t3.paragraph_format.space_after = Pt(2)
    p_t3.paragraph_format.keep_with_next = True
    r_t3 = p_t3.add_run("TABLE III\nRELATIONAL OLAP QUERY EXECUTION BENCHMARKS (N = 2,596 FACTS)")
    r_t3.font.name = FONT_NAME
    r_t3.font.size = Pt(8.5)
    r_t3.font.bold = True

    t_olap = doc.add_table(rows=6, cols=3)
    t_olap.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_olap.autofit = False
    set_table_borders(t_olap)

    t3_headers = ["OLAP Operation", "Analytical Scope & Filtering", "Latency (ms)"]
    col_w3 = [1.1, 1.7, 0.6]
    for c_i, h_txt in enumerate(t3_headers):
        cell = t_olap.cell(0, c_i)
        cell.width = Inches(col_w3[c_i])
        set_cell_shading(cell, "EAEAEA")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_txt)
        run.font.name = FONT_NAME
        run.font.size = Pt(7.5)
        run.font.bold = True

    t3_data = [
        ["Roll-Up", "Crop Species -> Higher Botanical Category", "33.26 ms"],
        ["Drill-Down", "Category -> Crop -> Disease -> Visual Tone", "31.27 ms"],
        ["Slice", "Fixed Dimension (crop_name = 'Tomato')", "14.99 ms"],
        ["Dice", "Sub-cube: Solanaceae/Fabaceae x Fungus/Bacteria", "14.42 ms"],
        ["Pivot", "14 Crops x 4 Pathogen Classes Cross-Tab", "12.57 ms"]
    ]
    for r_i, row in enumerate(t3_data):
        row_num = r_i + 1
        for c_i, val in enumerate(row):
            cell = t_olap.cell(row_num, c_i)
            cell.width = Inches(col_w3[c_i])
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 2 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = FONT_NAME
            run.font.size = Pt(7.5)

    add_ieee_heading_2(doc, "D. Unsupervised Ordination & PCA Separation")
    add_body_p(doc, "K-Means clustering across K in [2, 8] reveals that the 32D standardized descriptor space attains its global mathematical optimum at K=2 (Silhouette = 0.4060, Davies-Bouldin = 1.0990, Calinski-Harabasz = 1,154.38). As depicted in Fig. 6, the first two principal components account for 52.11% of total variance (PC1 = 38.56%, PC2 = 13.55%). Physical factor loading analysis confirms that PC1 is heavily loaded on foliar luminance (RGB_R +0.252, RGB_G +0.248, GLCM_ASM +0.248), separating dense green canopies from bright reflective leaves. PC2 is loaded on textural contrast (GLCM_contrast +0.384, GLCM_dissim +0.379), separating smooth blades from mottled necrotic lesions.")

    add_figure(doc, "fig5_pca_clusters.png", "Fig. 6. 2D PCA projection of standardized 32D visual descriptors (52.11% total variance), demonstrating cluster distributions and severe domain shift of flatbed scanner rice leaf imagery (N=36).", width_inches=3.4)

    add_ieee_heading_2(doc, "E. Cross-Modal Out-of-Domain Safeguard")
    add_body_p(doc, "When the 36 ICAR flatbed scanner rice leaf images were passed through the naive closed-world EfficientNet-B0 classifier, the model predicted Corn Common Rust with over 90% probability. Botanical investigation explains the root cause: among the 12 training crops, Corn is the sole graminoid monocot leaf with parallel venation (all other 11 crops are broad-leaved dicots). Flatbed scanner rice leaves possess linear, parallel-veined margins; hence, convolutional edge filters activated heavily on Corn features, forcing the closed-world softmax to select Corn.")

    add_body_p(doc, "Rather than fitting an unvalidated threshold heuristic on test probabilities, AgroVision-Mine implements a cross-modal verification check utilizing the 32D descriptor store. During runtime inference, the query image's standardized 32D vector is compared against warehouse references. When nearest neighbors identify an acquisition source or crop label outside the 25 supported classes (e.g., dataset_source = 'icar_ogd'), the system flags status: 'unsupported_domain' and triggers a prominent warning banner in the visual workbench (Fig. 7).")

    add_figure(doc, "fig7_inference_workbench.png", "Fig. 7. Runtime Visual Specimen Workbench demonstration: Top: Authentic Apple Healthy prediction (97.6% confidence); Bottom: ICAR Rice scanner specimen triggering the automated cross-modal out-of-domain rejection alert.", width_inches=3.4)

    # -------------------------------------------------------------------------
    # VII. THREATS TO VALIDITY
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "VII. Threats to Validity and Scientific Limitations")
    add_body_p(doc, "To maintain rigorous academic integrity, several fundamental methodological limitations must be stated:")
    add_body_p(doc, "The supervised model is bounded to 25 composite classes across 12 host crops. It cannot diagnose arbitrary unseen agricultural plants or novel exotic pathogens.", bold_prefix="1) Closed-World Taxonomic Scope: ")
    add_body_p(doc, "In the raw PlantDoc corpus, seven crops (Bell Pepper, Blueberry, Peach, Raspberry, Soybean, Squash, Strawberry) contain exclusively healthy or exclusively diseased observations. An unconditioned binary classifier trained across all crops learns to predict crop species rather than pathological state.", bold_prefix="2) Dataset Confounding in Raw PlantDoc: ")
    add_body_p(doc, "As demonstrated by the PCA ordination (Fig. 6), flatbed scanner images exhibit pure white background saturations that shift PC1 markedly, rendering laboratory or scanner imagery non-generalizable to farm field photography without domain adaptation.", bold_prefix="3) Scanner vs. Field Domain Shift: ")
    add_body_p(doc, "Nearest-reference Euclidean proximity in 32D feature space reflects geometric and textural similarity, not certified microbiological or PCR-confirmed pathogen etiology. Softmax output probabilities reflect relative network activations within a closed label space, not calibrated epidemiological likelihoods.", bold_prefix="4) Non-Diagnostic Nature of Geometric Retrieval: ")

    # -------------------------------------------------------------------------
    # VIII. CONCLUSION
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "VIII. Conclusion and Future Work")
    add_body_p(doc, "This paper presented AgroVision-Mine, an integrated agricultural computer vision and multimodal data warehousing framework that bridges the gap between deep visual inference and relational analytical intelligence. By unifying a five-stage quality gate, a 32D explainable feature store, a Kimball star schema warehouse, sub-35 ms relational OLAP slicing, and an EfficientNet-B0 transfer learning module (61.84% test accuracy on 25 classes), the framework enables auditable, multidimensional disease intelligence. Furthermore, the cross-modal out-of-domain safeguard provides a defensible mechanism to prevent false clinical attributions on unsupported acquisition domains.")

    add_body_p(doc, "Future extensions will incorporate multi-spectral drone imagery into the fact schema, implement temperature-scaled probability calibration, expand the benchmark to 50+ classes with few-shot learning for rare crops, and evaluate edge quantization on low-power agricultural IoT hardware.")

    # -------------------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------------------
    add_ieee_heading_1(doc, "References")

    refs = [
        "[1] J. G. A. Barbedo, \"Impact of dataset size and variety on the effectiveness of deep learning and transfer learning for plant pathology and pest identification,\" Biosystems Engineering, vol. 172, pp. 86–101, 2018.",
        "[2] S. P. Mohanty, D. P. Hughes, and M. Salathé, \"Using deep learning for image-based plant disease detection,\" Frontiers in Plant Science, vol. 7, p. 1419, 2016.",
        "[3] D. P. Hughes and M. Salathé, \"An open access repository of images on plant health to enable the development of mobile disease diagnostics,\" arXiv preprint arXiv:1511.08060, 2015.",
        "[4] K. P. Ferentinos, \"Deep learning models for plant disease detection and diagnosis,\" Computers and Electronics in Agriculture, vol. 145, pp. 311–318, 2018.",
        "[5] D. Singh, N. Jain, P. Jain, P. Kayal, S. Kumawat, and N. Batra, \"PlantDoc: A dataset for visual plant disease detection in the wild,\" in Proc. 7th ACM IKDD CoDS and 25th COMAD, 2020, pp. 249–253.",
        "[6] E. C. Too, L. Li, S. Njuki, and Y. Liu, \"A comparative study of fine-tuning deep learning architectures for plant disease identification,\" Computers and Electronics in Agriculture, vol. 161, pp. 272–279, 2019.",
        "[7] R. Kimball and M. Ross, The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling, 3rd ed. John Wiley & Sons, 2013.",
        "[8] A. Torralba and A. A. Efros, \"Unbiased look at dataset bias,\" in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2011, pp. 1521–1528.",
        "[9] R. Geirhos, J.-H. Jacobsen, C. Michaelis, R. Zemel, W. Brendel, M. Bethge, and F. A. Wichmann, \"Shortcut learning in deep neural networks,\" Nature Machine Intelligence, vol. 2, no. 11, pp. 665–673, 2020.",
        "[10] M. Tan and Q. V. Le, \"EfficientNet: Rethinking model scaling for convolutional neural networks,\" in Proc. 36th Int. Conf. Mach. Learn. (ICML), 2019, pp. 6105–6114.",
        "[11] R. M. Haralick, K. Shanmugam, and I. Dinstein, \"Textural features for image classification,\" IEEE Trans. Syst., Man, Cybern., vol. SMC-3, no. 6, pp. 610–621, 1973.",
        "[12] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[13] R. Agrawal and R. Srikant, \"Fast algorithms for mining association rules in large databases,\" in Proc. 20th Int. Conf. Very Large Data Bases (VLDB), 1994, pp. 487–499.",
        "[14] J. Han, J. Pei, and Y. Yin, \"Mining frequent patterns without candidate generation,\" in Proc. ACM SIGMOD Int. Conf. Manage. Data, 2000, pp. 1–12.",
        "[15] E. F. Codd, S. B. Codd, and C. T. Salley, \"Providing OLAP to user-analysts: An IT mandate,\" E. F. Codd and Associates, vol. 32, 1993.",
        "[16] D. R. Hipp, \"SQLite: An in-process relational database management system,\" 2020. [Online]. Available: https://www.sqlite.org/",
        "[17] S. Ramírez, \"FastAPI: Modern, fast (high-performance) web framework for building APIs with Python,\" 2018. [Online]. Available: https://github.com/tiangolo/fastapi",
        "[18] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, \"ImageNet: A large-scale hierarchical image database,\" in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2009, pp. 248–255.",
        "[19] E. B. Wilson, \"Probable inference, the law of succession, and statistical inference,\" Journal of the American Statistical Association, vol. 22, no. 158, pp. 209–212, 1927.",
        "[20] C. Zauner, \"Implementation and benchmarking of perceptual image hash functions,\" Master's thesis, Upper Austria Univ. of Applied Sciences, Hagenberg, 2010."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(2)
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = FONT_NAME
        r_ref.font.size = Pt(8.0)

    # Save DOCX
    doc.save(str(DOCX_OUT))
    print(f"[SUCCESS] Saved IEEE DOCX to: {DOCX_OUT} ({os.path.getsize(DOCX_OUT):,} bytes)")

    # Export PDF via Word COM
    export_docx_to_pdf(DOCX_OUT, PDF_OUT)


def export_docx_to_pdf(docx_path, pdf_path):
    print("Exporting DOCX to PDF via Microsoft Word COM...")
    import win32com.client
    import pythoncom

    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0

        doc = word.Documents.Open(str(docx_path.resolve()))
        # 17 = wdFormatPDF
        doc.SaveAs2(str(pdf_path.resolve()), FileFormat=17)
        doc.Close(False)
        print(f"[SUCCESS] Exported IEEE PDF to: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
    except Exception as e:
        print(f"Error during Word COM export: {e}")
    finally:
        if word:
            try:
                word.Quit()
            except:
                pass
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    build_paper_docx()
