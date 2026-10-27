# AgroVision-Mine — PowerPoint Presentation Quality Assurance & Audit Report

**Presentation File:** [`AgroVision-Mine_Final_Review_Updated.pptx`](file:///c:/Users/ajaya/Desktop/Agro/AgroVision-Mine_Final_Review_Updated.pptx)  
**Exported PDF Preview:** [`AgroVision-Mine_Final_Review_Updated.pdf`](file:///c:/Users/ajaya/Desktop/Agro/AgroVision-Mine_Final_Review_Updated.pdf)  
**High-Resolution Slide QA Renderings:** `data/reports/updated_presentation_qa/slide_01.png` through `slide_28.png` (1920×1080)  
**Source Presentation (Preserved Untouched):** `AgroVision-Mine_Final_Review_AUDITED(2).pptx`  
**Visual Style Reference:** `TermiteSense-IoT_Faculty_Review_Refined.pptx`  
**Academic Course:** CSI3010 — Data Warehousing & Data Mining (Fall Semester 2026–27)  
**Project Team:** Boomika V (23MID0326), Ajay M (23MID0020)  
**Faculty Guide:** Dr. Devipriya A, Associate Professor, SCOPE, VIT University Chennai  

---

## 1. Executive Summary & Verification Overview

| Audit Dimension | Value / Status | Verification Notes |
|---|---|---|
| **Slide Count** | **28 Slides** | Balanced 28-slide narrative strictly matching academic review standards |
| **Visual Reference Compliance** | **100% Match** | Adopts typography, geometry, color palette, card layout, and footers from `TermiteSense-IoT_Faculty_Review_Refined.pptx` |
| **Primary Supervised Module Integration** | **Complete** | Full 7-slide dedicated module on fine-tuned EfficientNet-B0 (25 classes, 12 crops, 61.84% test accuracy) |
| **System Architecture Diagram** | **Updated & Native** | 5-layer editable PowerPoint pipeline with connector flow arrows |
| **Obsolete Statements Removed** | **Verified** | Removed legacy claims rejecting supervised classification; clarified why single-condition binary tasks fail vs bounded multi-class |
| **Canonical Data Invariants** | **100% Preserved** | Canonical manifest SHA-256 (`c7fd16dc...`) and feature store SHA-256 (`f6caf70b...`) strictly preserved |
| **Full Visual QA Inspection** | **Verified (28/28)** | Rendered to 1920×1080 PNG via native Microsoft PowerPoint COM automation and visually audited |
| **Automated Software Test Suite** | **117 / 117 Passed** | 107 pytest unit/integration tests + 10 Playwright real-browser tests |

---

## 2. Reconciled Technical & Model Metrics

All model training, validation, testing, and dataset figures were audited directly against repository artifacts (`data/models/prediction/model_metadata.json`, `data/models/prediction/split_manifest.csv`, `data/reports/prediction/prediction_evaluation_report.json`, and `data/canonical/canonical_dataset_v2.csv`).

### 2.1 Dataset Composition & Invariants
- **Total Canonical Observations:** 2,596 validated specimen images across 14 host crops.
- **Corpus Provenance:** 2,560 PlantDoc field images + 36 ICAR/OGD flatbed scanner rice leaf images.
- **Pathology Split:** 1,750 diseased observations (67.4%) and 846 healthy observations (32.6%).
- **Feature Store Dimensions:** 44 columns (32 continuous visual descriptors: 19 Color Moments, 7 GLCM Textures, 6 Morphometric Metrics).
- **Cryptographic Hashes (Frozen):**
  - Canonical Dataset Manifest SHA-256: `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8`
  - Visual Feature Store SHA-256: `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1`

### 2.2 Supervised Learning Benchmark & Split Partitions
- **Target Task:** 25-class composite crop-condition classification across 12 host crops.
- **Benchmark Dataset:** 2,447 authentic PlantDoc images (the 36 ICAR scanner images are deliberately reserved for out-of-domain evaluation).
- **Data Leakage Safeguard:** Grouped strictly by perceptual difference hash (`dHash`, threshold=10) ensuring identical or near-duplicate frames never cross partitions.
- **Partition Counts:**
  - **Training Set:** 1,468 images (60.0%)
  - **Validation Set:** 489 images (20.0%)
  - **Held-Out Test Set:** 490 images (20.0%)
  - *Sum:* $1,468 + 489 + 490 = 2,447$ images.

### 2.3 Model Selection Tournament (Validation Macro-F1)
Model selection was strictly driven by validation performance on the 489 validation images:
1. **Majority Baseline (Zero-Rule):** 0.58% Validation Macro-F1 (predicts dominant class Tomato Late Blight).
2. **RBF-SVM (32 Handcrafted Descriptors):** 15.12% Validation Macro-F1.
3. **Random Forest (32 Handcrafted Descriptors):** 17.02% Validation Macro-F1.
4. **EfficientNet-B0 (RGB Image Transfer Learning):** **63.26% Validation Macro-F1** (Selected Architecture).

### 2.4 Final Held-Out Test Evaluation (N = 490 Images)
Evaluated strictly once on the unseen held-out test partition:
- **Top-1 Test Accuracy:** **61.84%** (303 / 490 correct)
- **Balanced Test Accuracy:** **61.43%** (unweighted mean per-class recall)
- **Macro-F1 Score:** **60.84%** (unweighted harmonic mean of per-class precision and recall)
- **Wilson 95% Confidence Interval for Accuracy:** **[57.46%, 66.03%]**

---

## 3. Slide-by-Slide Audit & Narrative Structure

| # | Slide Title | Key Content & Updates | Visual Layout Style |
|---|---|---|---|
| **1** | Title & Academic Review Cover | Course code CSI3010, project title, student names, reg numbers, guide, lab slot, term, verified deliverables summary | Framed rounded card with institutional VIT seal and forest/gold typography |
| **2** | Executive Summary & Current Status | Corrects outdated statements; highlights star schema warehouse, 32D feature store, OLAP engine, and 25-class EfficientNet-B0 classifier | Dual-column cards with green highlights and amber boundary note |
| **3** | Research Motivation: Agricultural Data Gap | Limitations of isolated black-box vision models vs multimodal relational warehouse; 5 automated quality gates; core research question | Side-by-side comparison cards with bottom full-width research question banner |
| **4** | Project Objectives & Implemented Deliverables | 7 core objectives mapped to verified deliverables, file paths, and cryptographic hashes | Structured 4-column academic table with forest header |
| **5** | Canonical Dataset Provenance & Curation | 2,596 observations, PlantDoc (2,560) vs ICAR Rice (36), 14 crops, 1,750 diseased / 846 healthy; SHA-256 checksums | 4 top KPI cards + left provenance card + right class distribution breakdown |
| **6** | System Architecture: End-to-End 5-Layer Pipeline | **Updated**: 5 distinct horizontal layers with right connector arrows: Ingestion/Gates → Preprocessing/Features → Warehouse/ETL → Analytical Engines → Presentation Tier | 5-column landscape cards with flow arrows; separate deep CNN branch from 32D features |
| **7** | Technology Stack & Architectural Rationale | Python 3.11, NumPy, Pandas, Pillow, OpenCV, scikit-image, scikit-learn, PyTorch, mlxtend, SQLite, FastAPI, React 18, Vite, pytest, Playwright | Clean 4-column table mapping technology to verified system role and rationale |
| **8** | Data Quality Assurance: 5 Automated Gates | Header check (magic bytes), geometry (min 100×100), payload limit (15 MB), MD5 deduplication, EXIF normalization | Left technical card + right embedded quality gates validation chart |
| **9** | Explainable Feature Engineering: 32 Descriptors | 19 Color Moments (RGB/HSV/ExG), 7 Haralick GLCM Textures, 6 Morphometric Metrics; frozen `image_features_v2.csv` | 3 distinct category cards + bottom feature store metadata summary |
| **10** | Multimodal Star Schema Design (Kimball) | `disease_observation_fact` (2,596 rows) surrounded by `dim_crop` (14), `dim_disease` (19), `dim_image` (2,596), and `dim_visual_feature` (2,596) | Left structural specification card + right embedded star schema diagram |
| **11** | Warehouse ETL Pipeline & Referential Integrity | Idempotent load logic, SQLAlchemy relational models, SQLite `PRAGMA foreign_keys = ON`, zero orphaned fact records | Left 4-stage pipeline card + right foreign key integrity & verification card |
| **12** | Multidimensional OLAP Engine & Real SQL Queries | ANSI SQL implementations of Roll-up, Drill-down, Slice by Crop, Dice Sub-Cube, and Pivot Matrix | 5-item operational breakdown + bottom performance benchmark (<15 ms) |
| **13** | OLAP Query Outputs: Roll-Up & Crop Slicing | Actual SQLite query results for Crop Family Roll-Up and Solanaceae Disease Slice | Dual query output tables with agronomic data interpretations |
| **14** | OLAP Query Outputs: Pathogen Pivot Matrix | 14 Crops × 4 Pathogen Classes pivot matrix; uncovers that 7 crops have zero healthy records in raw PlantDoc | Full-width formatted pivot table + bottom insight card on taxonomy bias |
| **15** | OLAP Query Outputs: Dice Sub-Cube Analysis | Multi-attribute filtering (Crop Family in [Solanaceae, Fabaceae] AND Pathogen in [Fungus, Healthy]) | Left SQL specification card + right sub-cube table and agronomic coverage interpretation |
| **16** | Visual Pattern Mining: Dual-K Clustering Evaluation | K=2 primary metric optimum (Silhouette=0.4060, Davies-Bouldin=1.0990) vs K=4 exploratory; ARI=1.0000 across seeds | Left evaluation table + bottom stability card + right PCA cluster scatter plot |
| **17** | Dimensionality Reduction: 2D PCA Loadings Analysis | Cumulative explained variance 52.11% (PC1=38.56% foliar luminance; PC2=13.55% textural contrast); explains ICAR scanner domain shift | Left loadings interpretation card + right loadings table and cluster distribution card |
| **18** | Association Rule Mining: Mode A vs Mode B | Discretization across 12 descriptors; exact mathematical parity between Apriori and FP-Growth (Δ=0.0000) | Left Mode A visual rules (880 rules) + right Mode B labeled rules (285 rules) |
| **19** | Supervised Learning: Problem Formulation & Scope | **New**: Bounded 25-class foliar condition classification across 12 crops; explains failure of unconditioned binary classification due to confounding | Left formulation & scope card + right taxonomic class distribution card |
| **20** | EfficientNet-B0 Architecture & Selection Rationale | **New**: Compound scaling ($α=1.2, β=1.1, γ=1.15$), MBConv blocks, squeeze-and-excitation; transfer learning from ImageNet-1K visual priors | Left architectural mechanics card + right selection rationale card |
| **21** | Model Selection Tournament: Handcrafted vs Deep CNN | **New**: Validation macro-F1 comparison (Majority 0.58%, SVM 15.12%, RF 17.02%, EfficientNet-B0 63.26%); input representation distinction | Left tournament comparison table + right comparative analysis card |
| **22** | Perceptual-Hash Split Partitioning | **New**: Grouped dHash split strategy (1,468 train / 489 val / 490 test); zero cross-partition image overlap | Left split methodology card + right 3-tier partitioning metrics table |
| **23** | Model Training Pipeline & Hyperparameters | **New**: 8 epochs, batch size 32, AdamW optimizer (differential LR: $10^{-4}$ backbone, $10^{-3}$ head), ReduceLROnPlateau, early stopping | Left 6-stage training pipeline card + right verified hyperparameter table |
| **24** | Held-Out Test Evaluation & Statistical Uncertainty | **New**: 61.84% Test Acc, 61.43% Balanced Acc, 60.84% Macro-F1, Wilson CI [57.46%, 66.03%]; per-class breakdown | 4 top KPI metric cards + left metric definitions card + right per-class performance table |
| **25** | Runtime Inference Workflow & Demonstration | **New**: Upload → Validation → Forward Pass → Softmax logits; Apple Healthy (97.6%) & Potato Late Blight (96.2%) case studies | Left inference workflow card + right cropped high-resolution workbench screenshot |
| **26** | Cross-Modal Out-of-Domain Safeguard & Rejection | **New**: Investigates Rice → Corn prediction (sole monocot); 32D nearest-reference cross-modal safeguard flags `unsupported_domain` | Left botanical root cause card + top-right rejection screenshot + bottom UI banner card |
| **27** | Multi-Tier Software Testing & Verification | 117/117 automated tests (107 pytest in 20.3s + 10 Playwright in 43.3s); 11 API endpoints 200 OK; 267ms frontend build | 4 top verification KPI cards + 4-tier verification test scope table |
| **28** | Conclusion, Limitations & Viva Demonstration Plan | Closed-world 25-class boundary, scanner vs field shift, non-diagnostic similarity metric, 6-step live viva roadmap | Left scientific limitations card + right viva demonstration roadmap card |

---

## 4. Visual Quality Assurance Checklist

All 28 exported slide images were inspected for visual quality, typographic balance, and layout cleanliness:

- [x] **Typography & Hierarchy:**
  - Header Kicker: `Pt(10.5)`, bold, `COLOR_FOREST` (`#2D6A4F`).
  - Slide Titles: `Pt(24)`, bold, `COLOR_DARK_GREEN` (`#175D44`).
  - Card Titles: `Pt(12)`, bold, uppercase, with `Pt(8)` spacing.
  - Body Bullet Text: `Pt(11)` with bold `Pt(11.5)` run leads.
  - Table Headers: `Pt(11)`, bold white text on `COLOR_DARK_GREEN` fill.
  - Table Data Cells: `Pt(10.5)` text on alternating white and warm off-white (`COLOR_CARD_BG`).
  - Footers & Page Counters: `Pt(9.5)` at bottom baseline (`y = 7.08"`), with slide count formatted as `Slide X of 28`.

- [x] **Geometry, Padding & Boundary Compliance:**
  - Standard widescreen 16:9 layout: 13.333" width × 7.500" height.
  - Card padding increased to `left + 0.28"`, `top + 0.26"`, `width - 0.56"`, `height - 0.48"`, preventing text collision with rounded corner arcs.
  - No text overflow, clipping, or overlaps detected across any of the 28 slides.

- [x] **Diagram & Asset Quality:**
  - Slide 6 (System Architecture): 5 distinct cards with 4 `RIGHT_ARROW` flow connectors; clean column spacing with no title wrapping.
  - Slide 10 (Star Schema): High-resolution diagram extracted from original vector layout, centered at `top = 1.35"`.
  - Slide 16 (K-Means & PCA): Sharp PCA cluster plot embedded cleanly alongside the metrics table.
  - Slides 25 & 26 (Application Workbench): Uses focused cropped frames (`crop_apple_healthy.png` and `crop_rice_rejection.png`) at native aspect ratios, displaying clear UI text, probability bars, and alert notices without vertical compression.

---

## 5. Academic Integrity & Honest Scientific Disclosures

The presentation strictly adheres to academic rigor:
1. **No Universal Agricultural Diagnostic Claims:** Clearly articulates that nearest-neighbor distance in 32D descriptor space measures geometric similarity, not clinical pathogen etiology.
2. **Explicit 25-Class Scope:** Openly states that the deep learning model evaluates 25 specific classes across 12 host crops and does not generalize unconditionally to all agricultural species.
3. **Transparent Out-of-Domain Rejection:** Details the botanical reason why linear scanner rice leaves falsely activated Corn filters, and explains how the cross-modal 32D reference check detects unsupported acquisition domains.
4. **Validation vs Test Distinction:** Clearly separates validation tournament metrics (EfficientNet-B0: 63.26% Validation Macro-F1) from final held-out test metrics (61.84% Test Accuracy, 60.84% Macro-F1).
5. **Preserved Invariants:** Source presentations (`AgroVision-Mine_Final_Review_AUDITED(2).pptx`), canonical manifest files, and relational databases remain untouched.
