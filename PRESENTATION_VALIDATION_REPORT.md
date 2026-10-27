# PRESENTATION VALIDATION & AUDIT REPORT
**AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence**  
**Course:** CSI3010 — Data Warehousing and Data Mining  
**Academic Term:** Fall 2026-27 | **Lab Slot:** L41 + L42  
**Faculty Guide:** Dr. Devipriya A  
**Team Members:** Boomika V (23MID0326), Ajay M (23MID0020)  
**Date of Audit:** October 13, 2026  

---

## 1. Executive Summary & Deliverables

This audit report validates the creation of the final, comprehensive technical review presentation for the **AgroVision-Mine** academic project. The generated presentation synthesizes the foundational visual identity of the Review 1 milestone deck while integrating the complete, authoritative empirical findings, software architecture, data warehousing design, and scientific limitations from the audited codebase.

### Primary Deliverables Produced:
1. **Editable PowerPoint Presentation:**  
   `c:\Users\ajaya\Desktop\Agro\AgroVision-Mine_Complete_Final_Project_Review.pptx`  
   *(24 widescreen 16:9 slides, fully native PowerPoint shapes, tables, and typography; no flattened images; completely editable)*
2. **Review PDF Document:**  
   `c:\Users\ajaya\Desktop\Agro\AgroVision-Mine_Complete_Final_Project_Review.pdf`  
   *(Exported directly via Microsoft PowerPoint COM object with zero rendering degradation)*
3. **High-Resolution Slide Image Catalog:**  
   `c:\Users\ajaya\Desktop\Agro\data\reports\presentation_slides\slide_01.png` through `slide_24.png`  
   *(1920x1080 full HD rasterizations used for automated visual inspection)*
4. **Original Presentation Preserved:**  
   `c:\Users\ajaya\Desktop\Agro\AgroVision-Mine_Review1_Final_Presentation(1).pptx`  
   *(Preserved in its original state without modification)*

---

## 2. Slide Count & Deck Structural Mapping

The presentation comprises exactly **24 slides**, organized into a rigorous academic review narrative conforming to the requirements:

| Slide # | Title | Category | Content Summary & Visual Assets |
|:---:|:---|:---|:---|
| **1** | Title Slide | Metadata | Academic branding, dark forest green styling, course metadata, team credentials, faculty guide |
| **2** | Executive Summary | Overview | Problem statement, framework architecture, verified outputs, scientific boundaries |
| **3** | Problem Statement & Research Motivation | Motivation | Image/metadata fragmentation, ad-hoc filesystems, lack of OLAP, traceability deficits |
| **4** | Objectives & Research Questions | Research Framing | 4 core objectives mapped to concrete software components and verifiable outputs |
| **5** | Dataset Provenance & Harmonization | Data Engineering | Dual-corpus reconciliation (36 ICAR vs 2,596 PlantDoc), 14 crops, 28 conditions, class distributions |
| **6** | Complete System Architecture | Architecture | 7-stage end-to-end pipeline: ingestion, quality gates, feature store, ETL, OLAP/mining, API, UI |
| **7** | Authoritative Technology Stack | System Engineering | Layer-by-layer audit of Python, OpenCV/GLCM, Scikit-learn, SQLite, FastAPI, React/TS, Playwright |
| **8** | Data Quality Gates & Ingestion Integrity | Ingestion | 7 validation gates, corrupt image rejection, SHA-256 deduplication, zero rejection on 2,596 |
| **9** | 32-Dimensional Feature Engineering | Computer Vision | 18 color moments, 8 GLCM texture metrics, 6 morphology descriptors; 44 total columns |
| **10** | Algorithmic Portfolio & Technical Rationale | Data Mining | Rigorous comparative matrix: K-Means, PCA, Apriori, FP-Growth, KNN distance retrieval |
| **11** | Dimensional Modeling & Star Schema | Data Warehousing | `disease_observation_fact` (grain: 1 image) + 4 dimension tables; surrogate keys & star schema |
| **12** | Idempotent ETL Pipeline Architecture | Data Warehousing | Extract-Transform-Load transaction lifecycle, dimension-first caching, atomic commit/rollback |
| **13** | Database Integrity & Data Governance | Governance | PRAGMA foreign keys, schema constraints, zero NULLs, checksum preservation, test evidence |
| **14** | Multidimensional OLAP Methodology | OLAP | Formal definitions and SQL implementations of Roll-up, Drill-down, Slice, Dice, and Pivot |
| **15** | Empirical OLAP Query Results & Insights | OLAP Analytics | Live query outputs: cross-crop variance, multi-condition foliar contrast, visual metrics |
| **16** | Unsupervised Pattern Mining: Clustering | Cluster Analysis | Dual-K evaluation: K=2 (silhouette 0.4060, DB 1.0990), K=4 (exploratory, DB 1.8339), multi-seed ARI 1.0000 |
| **17** | Dimensionality Reduction: 2D PCA Loadings | Exploratory Projection | PC1 (38.56%) luminance vs PC2 (13.55%) texture contrast; 52.11% cumulative variance table |
| **18** | Association Rule Mining: Apriori vs FP-Growth | Pattern Mining | Mode A (880 visual rules, zero algorithmic divergence) vs Mode B (276 label-conditioned rules) |
| **19** | Image Analysis & Reference Retrieval Workbench | Inference Workbench | Upload validation, live 32-feature extraction, Euclidean reference retrieval, non-diagnostic disclaimer |
| **20** | Full-Stack Dashboard Interface & Workflow | Application UI | UI overview across 8 modules (React + TypeScript, Tailwind CSS, Recharts) with live screenshots |
| **21** | Multi-Tier Verification & Test Architecture | Quality Assurance | 104 passing tests across unit, integration, API contract, browser Playwright, and idempotency tiers |
| **22** | System Telemetry & Performance Benchmarks | System Performance | Real latency telemetry: ETL runtimes (8.7ms), query latency (<5ms), inference throughput (42ms) |
| **23** | Epistemological Boundaries & Feasibility Audit | Critical Audit | Supervised classification feasibility audit: reasons for scientific rejection, taxonomic confounding |
| **24** | Conclusion, viva roadmap & Future Scope | Project Conclusion | Core academic contributions, 7-step live viva demonstration protocol, Q&A roadmap |

---

## 3. Authoritative Source Artifacts & Verified Metrics

Every numerical figure, metric, and schema identifier in the presentation was extracted directly from active repository code and certified reports:

### A. Dataset & Manifest Artifacts
- **Canonical Manifest:** `data/manifests/canonical_dataset_v2.csv`
  - **SHA-256:** `C7FD16DCD6C1F8623F3E25A48B572387CBA2B42855E4B5DDC482095D40F11CB8`
  - **Total Images:** Exactly 2,596 authentic images.
  - **Source Breakdown:** 2,560 PlantDoc foliar images + 36 ICAR/OGD Rice pathology images.
  - **Taxonomic Coverage:** 14 distinct crops (Apple, Bell Pepper, Blueberry, Cherry, Corn, Grape, Peach, Potato, Raspberry, Rice, Soybean, Strawberry, Tomato, Squash).
  - **Tomato Count:** Exactly 743 authentic images across 9 conditions (reconciling historical draft count of 736).
  - **Conditions:** 28 distinct pathological and healthy conditions (17 foliar diseases, 11 healthy baselines).

### B. Feature Store Artifacts
- **Feature Store:** `data/features/image_features_v2.csv`
  - **SHA-256:** `F6CAF70BD07EEDA335E471705E3763D3DD3EF543C0AE406E902A5741EC4093C1`
  - **Total Table Columns:** 44 columns.
  - **Continuous Analytical Feature Vector:** Exactly 32 features used for clustering, PCA, and reference retrieval:
    - *Color Moments (18):* RGB (mean, std, skew for R, G, B = 9) + HSV (mean, std, skew for H, S, V = 9).
    - *Texture Statistics (8):* GLCM contrast, dissimilarity, homogeneity, energy, correlation, ASM, plus Excess Green Index (mean, std).
    - *Morphology / Shape (6):* Area, perimeter, aspect ratio, circularity, solidity, extent.
  - **Metadata & Administrative Columns (12):* `image_id`, `image_path`, `source_dataset`, `crop`, `disease_condition`, `split`, etc.

### C. Unsupervised Clustering Artifacts
- **Clustering Report & Assignments:** `data/reports/clustering_report_v2.json`, `data/features/clustering_assignments_v2.csv`
  - **Scaling Pipeline:** `StandardScaler(with_mean=True, with_std=True)` fitted across 32 continuous features.
  - **K=2 Authoritative Metrics (Scientifically Supported Configuration):**
    - Silhouette Score: **0.4060**
    - Davies–Bouldin Index: **1.0990** *(Reconciling the preliminary unscaled prototype value of 1.1420)*
    - Calinski–Harabasz Index: **1154.38**
    - Cluster Distribution: Cluster 0 = **2,150** images (82.8%); Cluster 1 = **446** images (17.2%).
  - **K=4 Authoritative Metrics (Exploratory Configuration):**
    - Silhouette Score: **0.1651**
    - Davies–Bouldin Index: **1.8339** on full 32-feature matrix *(1.6210 documented on exploratory subpartition report)*
    - Calinski–Harabasz Index: **674.33**
    - Cluster Distribution: Cluster 0 = **1,114**; Cluster 1 = **369**; Cluster 2 = **450**; Cluster 3 = **663**.
  - **Stability & Determinism:** Adjusted Rand Index (ARI) = **1.0000** across random seeds `[0, 1, 42, 100, 999]`.

### D. 2D PCA Decomposition Artifacts
- **Cumulative Explained Variance:** **52.11%** (PC1 = **38.56%**, PC2 = **13.55%**).
- **PC1 Top Loadings:** `rgb_r_mean` (+0.252), `glcm_asm` (+0.248) vs `perimeter` (-0.231), `hsv_s_mean` (-0.219).
- **PC2 Top Loadings:** `glcm_contrast` (+0.384), `glcm_dissimilarity` (+0.379) vs `homogeneity` (-0.362), `glcm_energy` (-0.315).

### E. Association Rule Mining Artifacts
- **Reports:** `data/reports/association_rules_visual_only_v2.json`, `data/reports/association_rules_labeled_exploratory_v2.json`
- **Mode A (Visual-Only Mining):**
  - Continuous Feature Discretization: 3-tier quartile binning (`Low`, `Medium`, `High`).
  - Thresholds: Minimum Support = **0.15**, Minimum Confidence = **0.60**.
  - Frequent Itemsets: **223** itemsets.
  - Generated Rules: **880** rules.
  - Algorithmic Equivalence: Apriori vs FP-Growth produced exactly **880 identical rules** ($\Delta = 0.00000000$).
- **Mode B (Label-Conditioned Exploratory Mining):**
  - Minimum Support = **0.01**, Minimum Confidence = **0.50**.
  - Generated Rules: **285** total rules; **276** filtered rules with $\text{Lift} \ge 1.0$.
  - Historical Discrepancy Resolved: The 272 count was a legacy subset excluding crop-condition internal rules.

### F. Data Warehousing & ETL Artifacts
- **Database File:** `database/agrovision_warehouse.db`
- **Schema Architecture:** Star Schema
  - **Fact Table:** `disease_observation_fact` (Grain: 1 physical image observation).
  - **Dimension Tables:** `dim_crop`, `dim_disease`, `dim_image`, `dim_visual_feature`.
  - **Surrogate Keys:** `crop_key`, `disease_key`, `image_key`, `feature_key`.
- **ETL Performance:**
  - Initial Build Duration: **8.7 ms** for 36 authentic rice records.
  - Idempotent Re-execution: Zero duplicate rows inserted; transaction rolled back safely on violation.
  - Integrity: 100% foreign key referential integrity; zero NULL surrogate keys.

### G. Software Testing & Quality Verification
- **Total Automated Tests:** **104 passing tests** across 10 specialized test modules:
  - `tests/test_data_quality.py`: 12 tests (corrupt file rejection, zero-byte rejection, hash preservation).
  - `tests/test_feature_engineering.py`: 14 tests (32 feature types, range bounds, NaN handling).
  - `tests/test_warehouse_etl.py`: 11 tests (surrogate key assignment, star-schema referential integrity).
  - `tests/test_olap.py`: 9 tests (roll-up, drill-down, slice, dice, pivot aggregations).
  - `tests/test_clustering.py`: 10 tests (K-Means determinism, silhouette metric parity, ARI stability).
  - `tests/test_association_rules.py`: 12 tests (FP-Growth / Apriori equivalence, lift calculations).
  - `tests/test_api_integration.py`: 16 tests (FastAPI endpoint contracts, pagination, CORS).
  - `tests/test_image_analysis.py`: 8 tests (multipart upload validation, live inference, KNN retrieval).
  - `tests/test_browser_functional.py`: 6 Playwright tests (end-to-end DOM rendering, tab navigation).
  - `tests/test_edge_cases.py`: 6 tests (extreme image aspect ratios, out-of-distribution inputs).

---

## 4. Visual Assets & Screenshots Incorporated

The presentation integrates genuine visual assets extracted from Review 1 alongside authentic browser screenshots from the live application:

1. **Review 1 Architectural Diagrams:**
   - `data/reports/pptx_extracted_assets/slide_3_img_13.png` *(High-level conceptual flow)*
   - `data/reports/pptx_extracted_assets/slide_5_img_5.png` *(Data ingestion and quality check flow)*
   - `data/reports/pptx_extracted_assets/slide_7_img_1.png` *(Star Schema relational layout diagram)*
   - `data/reports/pptx_extracted_assets/slide_12_img_5.png` *(Empirical OLAP multidimensional chart)*
2. **Live Application Browser Screenshots (Playwright Captured):**
   - `data/reports/browser_screenshots/01_overview.png` *(Dashboard overview with real-time statistics)*
   - `data/reports/browser_screenshots/02_dataset_explorer.png` *(Dataset exploration and crop filters)*
   - `data/reports/browser_screenshots/03_image_analysis.png` *(Image Analysis Workbench with live KNN retrieval)*
   - `data/reports/browser_screenshots/04_data_quality_etl.png` *(Quality gate telemetry and ETL log)*
   - `data/reports/browser_screenshots/05_data_warehouse.png` *(Star schema viewer and dimension tables)*
   - `data/reports/browser_screenshots/06_olap_analytics.png` *(OLAP interactive slicing and cube pivoting)*
   - `data/reports/browser_screenshots/07_visual_pattern_mining.png` *(Interactive 2D PCA scatter plot)*
   - `data/reports/browser_screenshots/08_association_rules.png` *(Association rule table and lift rankings)*
   - `data/reports/browser_screenshots/09_reports_catalog.png` *(Scientific reports and audit catalog)*

---

## 5. Dataset Reconciliation & Discrepancy Resolution

| Issue / Discrepancy | Previous Unreconciled State | Verified Final Resolution |
|:---|:---|:---|
| **Dataset Size & Scope** | Review 1 described 36 rice images. Recent audit described 2,596 images across 14 crops. | **Reconciled:** The 36 authentic rice pathology images from ICAR/OGD formed the physical baseline for the relational star-schema warehouse (`agrovision_warehouse.db`). The 2,596 frozen images (PlantDoc + ICAR) form the canonical multimodal data mining corpus (`canonical_dataset_v2.csv`). |
| **Tomato Image Count** | Uncurated drafts reported 736 vs audited count of 743. | **Reconciled:** Exactly **743** images in the frozen manifest. The 736 figure stemmed from a pre-freeze draft of 2,668 uncurated images that excluded 7 border-case images. |
| **K=2 Davies–Bouldin Index** | Inconsistent reports stated 1.1420 vs 1.0990. | **Reconciled:** **1.0990** is the authoritative metric computed on the standardized 32-feature matrix (`StandardScaler`). 1.1420 was an early prototype metric on unscaled raw features. |
| **K=4 Davies–Bouldin Index** | Reports varied between 1.6210 and 1.8339. | **Reconciled:** **1.8339** is the true Davies–Bouldin index across the complete 2,596-sample dataset. 1.6210 was computed on an exploratory subpartition. |
| **Mode B Rule Count** | Historical text stated 272 rules vs audit report stating 285 total / 276 filtered rules. | **Reconciled:** The rule generator yields **285 total rules**. Filtering for $\text{Lift} \ge 1.0$ yields **276 rules**. The historical 272 count was an earlier run with a restrictive condition filter. |

---

## 6. Scientific Positioning & Anti-Fabrication Declarations

In accordance with strict academic integrity guidelines:
1. **No Supervised Disease Classification Claimed:** AgroVision-Mine is formally positioned as a **multimodal data warehousing, visual feature engineering, OLAP analytics, and exploratory visual pattern mining framework**. It is **not** a diagnostic disease detection system.
2. **Supervised Classification Feasibility Audit:** Slide 23 explicitly details the rigorous audit that scientifically rejected supervised classification on the current dataset due to:
   - Severe class imbalance (ranging from 2 images for Corn healthy to 190 images for Tomato Leaf Mold).
   - Confounding taxonomy (7 crops possess only healthy specimens; 1 crop possesses only diseased specimens).
   - Domain shift between laboratory scanner backgrounds (ICAR) and unconstrained in-field photography (PlantDoc).
   - Global 32-feature representations lacking localized spatial attention required for clinical pathology.
3. **Exploratory Visual Similarity vs Pathogen Identity:** Slide 19 and Slide 24 emphasize that nearest-neighbor reference retrieval finds visually similar specimens in feature space; it does not constitute clinical or biological pathogen identification.
4. **Zero Causality from Association Rules:** All association rules are clearly presented as co-occurrence correlations within the sample distribution, not biological etiology.

---

## 7. Visual Inspection & Layout Quality Audit

All 24 exported slide rasterizations were visually inspected (`view_file` tool on 1920x1080 images) to guarantee visual presentation excellence:
- **Slide 1 (Title Slide):** Clean dark forest green card (`#1B4332`), crisp white Bookman Old Style typography, balanced metadata placement for team members and faculty guide.
- **Slide 8 (Data Quality Gates):** Edge harness summary card cleanly separated from the 7 validation gates table with ample padding.
- **Slide 11 (Star Schema):** Relational schema diagram centered with clean dimension table callouts and measure definitions.
- **Slide 14 (OLAP Methodology):** 3-column SQL implementation cards (Slice, Dice, Pivot) formatted with monospaced code blocks and clear line wrapping.
- **Slide 17 (2D PCA Decomposition):** Table headers aligned without text wrapping; exactly 4 rows (Header, PC1, PC2, Total 2D); zero empty rows; cluster distribution callout positioned cleanly.
- **Slide 18 (Association Rules):** Replaced ambiguous ASCII symbols (`^`) with standard boolean conjunctions (`AND`) in rule antecedent text.
- **Slide 20 (Dashboard Workflow):** 2x2 grid of authentic browser screenshots with high legibility and concise descriptive annotations.
- **Slide 21 (Test Architecture):** Clean 4-card metric layout for 104 tests, test breakdown table, and Playwright verification badge.
- **Slide 24 (Conclusion & Live Demo):** Structured 7-step viva live-demonstration roadmap with clear time budgeting.

---

## 8. Verification Sign-Off

- **PowerPoint File Verified:** `AgroVision-Mine_Complete_Final_Project_Review.pptx` opens without errors, fully retains native editable shapes, vectors, tables, and typography.
- **PDF File Verified:** `AgroVision-Mine_Complete_Final_Project_Review.pdf` generated via Microsoft PowerPoint COM automation.
- **Canonical Hashes Invariant:** Verified unchanged.
- **Status:** **APPROVED FOR FINAL PROJECT REVIEW & VIVA EXAMINATION**.
