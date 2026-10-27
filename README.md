# AgroVision-Mine: Multimodal Data Warehouse & Visual Pattern Mining Framework for Crop Disease and Pest Intelligence

[![Course](https://img.shields.io/badge/Course-CSI3010%20Data%20Warehousing%20%26%20Data%20Mining-green.svg)]()
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)]()
[![React 19](https://img.shields.io/badge/Frontend-React%2019%20%2B%20TypeScript-61dafb.svg)]()
[![Tailwind CSS](https://img.shields.io/badge/Design-Botanical%20Precision%20Tailwind-38b2ac.svg)]()
[![FastAPI](https://img.shields.io/badge/API-FastAPI%20Adapter-009688.svg)]()
[![Database](https://img.shields.io/badge/Warehouse-SQLite%203%20Star%20Schema-orange.svg)]()
[![Tests](https://img.shields.io/badge/Tests-117%2F117%20Passed-success.svg)]()
[![Dataset Status](https://img.shields.io/badge/Dataset-v2.0%20Frozen%20(2%2C596%20Records)-brightgreen.svg)]()

---

## 📌 Executive Summary & Academic Identity

Unlike conventional computer vision applications that treat crop disease identification as an isolated black-box classification problem, **AgroVision-Mine** establishes an enterprise-grade **Multimodal Data Warehouse and Visual Pattern Mining Architecture** integrating:

1. **Frozen Canonical Agricultural Corpus**: 2,596 verified leaf image records across 14 crops and 17 foliar pathologies, sourced from the **PlantDoc** benchmark (2,560 images) and the **Indian Council of Agricultural Research (ICAR / data.gov.in)** (36 images).
2. **Quality Assurance & Preprocessing Gates**: Laplacian variance blur scoring, MD5 cryptographic deduplication, uniform 256×256 bilinear normalization, and zero image corruptions.
3. **Classical Explainable Visual Feature Store**: 32 continuous descriptors (19 colour & vegetation features [18 RGB/HSV channel moments + 1 Excess Green Index ExG], 7 GLCM Haralick texture statistics, and 6 morphometric contour and lesion coverage parameters) stored in a standardized 44-column analytical feature matrix.
4. **Kimball Star Schema Data Warehouse**: Relational star schema with surrogate keys, native database foreign-key enforcement (`PRAGMA foreign_keys = ON`), referential integrity, and dual-dialect compatibility.
5. **SQL-Backed OLAP Engine**: Real ANSI SQL execution of **Roll-up**, **True Drill-down** (single-dimension hierarchy) & **Diagnostic Drill-Across**, **Slice by Crop/Pathogen**, **Dice Sub-Cube**, and **Pivot Matrix**.
6. **Unsupervised Visual Pattern Mining**: Dual K-Means clustering ($K=2$ optimal metric-supported solution vs $K=4$ exploratory sub-partition) and 2D Principal Component Analysis (PCA) capturing 59.6% total explained variance.
7. **Association Rule Mining**: Unsupervised visual co-occurrence discovery using **Apriori** and **FP-Growth** algorithms over equal-frequency discretized feature itemsets. Mode A (880 visual-only rules) is strictly segregated from Mode B (285 label-conditioned exploratory rules).
8. **Botanical Precision React Dashboard**: Full modern user interface generated from Stitch design specifications (`projects/1107814904366249836`), built with React 19, TypeScript, Tailwind CSS, Space Grotesk, Hanken Grotesk, and JetBrains Mono.

---

## 🏗️ System Architecture

```text
                                HETEROGENEOUS RAW DATASETS
                ┌─────────────────────────────────────────────────────────┐
                │ PlantDoc Benchmark (2,560)  │  ICAR / OGD India (36)    │
                └────────────────────────────┬────────────────────────────┘
                                             │
                                             ▼
                               PREPROCESSING & QUALITY GATES
                ┌─────────────────────────────────────────────────────────┐
                │  - Image Non-Corruption Gate (PIL verification: 0 errors)│
                │  - Laplacian Blur Scoring (Sharpness variance audit)    │
                │  - Standardization (Uniform 256x256 RGB normalization)  │
                │  - Deduplication (Cryptographic MD5 hash matching)      │
                └────────────────────────────┬────────────────────────────┘
                                             │
                                             ▼
                             EXPLAINABLE VISUAL FEATURE STORE
                ┌─────────────────────────────────────────────────────────┐
                │  - Color Moments: RGB/HSV Mean/Std, Excess Green (ExG)  │
                │  - Texture Descriptors: GLCM Contrast, Homogeneity, ASM │
                │  - Morphometrics: Contour Area, Perimeter, Circularity  │
                │  - Standardized z-score transform (zero mean, unit var) │
                └────────────────────────────┬────────────────────────────┘
                                             │
                        ┌────────────────────┴────────────────────┐
                        ▼                                         ▼
            RELATIONAL STAR SCHEMA WAREHOUSE             PATTERN MINING ENGINE
        ┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
        │ Database: SQLite 3 (Foreign Keys ON) │  │ K-Means Dual Clustering:          │
        │ Dimensions:                          │  │   - K=2 Metric-Supported (Silh 0.41)│
        │   - dim_crop                         │  │   - K=4 Exploratory (Silh 0.17)   │
        │   - dim_disease                      │  │ PCA 2D Projection (59.6% var)     │
        │   - dim_image                        │  │ Rule Mining (Apriori & FP-Growth):│
        │   - dim_visual_feature               │  │   - Mode A: Visual-Only (880 rules│
        │ Fact: disease_observation_fact       │  │   - Mode B: Labeled (285 rules)   │
        └──────────────────┬───────────────────┘  └─────────────────┬─────────────────┘
                           │                                        │
                           └────────────────────┬───────────────────┘
                                                │
                                                ▼
                                    FASTAPI ADAPTER SERVICE
                         (REST Endpoints: Overview, Dataset, OLAP, Mining)
                                                │
                                                ▼
                              BOTANICAL PRECISION REACT DASHBOARD
                    (8 Analytical Pages, Interactive Controls, Slicers, Modals)
```

---

## 🔒 Cryptographic Verification & Invariance Guarantee

The underlying dataset and feature stores are frozen and verified via SHA-256 cryptographic hashes:

| Artifact | File Location | Expected SHA-256 Checksum | Status |
| :--- | :--- | :--- | :--- |
| **Canonical Manifest v2** | `data/manifests/canonical_dataset_v2.csv` | `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8` | **VERIFIED INVARIANT** |
| **Visual Feature Store v2** | `data/features/image_features_v2.csv` | `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1` | **VERIFIED INVARIANT** |

---

## 💻 Technology Stack

- **Core Backend**: Python 3.11, FastAPI, Uvicorn, Pydantic
- **Relational Storage & Dimensional OLAP**: SQLite 3, SQLAlchemy 2.0 (PRAGMA foreign_keys = ON)
- **Computer Vision & Pattern Mining**: NumPy, Pandas, Scikit-learn, SciPy, Mlxtend, Pillow (PIL)
- **Frontend Presentation Layer**: React 19, TypeScript, Tailwind CSS, Vite
- **Typography & Aesthetics**: Space Grotesk (Headlines), Hanken Grotesk (Body), JetBrains Mono (Telemetry/Data), Google Material Symbols
- **Testing & Quality Assurance**: Pytest (81/81 passed)

---

## 📂 Repository Structure

```text
Agro/
├── config/                         # System configuration and path settings
├── data/
│   ├── raw/                        # Original archived leaf image rasters
│   ├── processed/                  # Standardized 256x256 normalized images
│   ├── manifests/
│   │   └── canonical_dataset_v2.csv # Frozen canonical dataset (2,596 records)
│   ├── features/
│   │   ├── image_features_v2.csv    # Frozen 44-column feature store (32 visual features)
│   │   └── clustering_assignments_v2.csv # Precomputed K=2, K=4, and PCA coordinates
│   └── reports/                    # Verified JSON evaluation and mining reports
│       ├── clustering_report_v2.json
│       ├── association_rules_report_v2.json
│       ├── association_rules_visual_only_v2.json
│       ├── association_rules_labeled_exploratory_v2.json
│       └── review2_evaluation_report.json
├── database/
│   └── agrovision_warehouse.db     # Populated local SQLite Star Schema warehouse
├── frontend/                       # Stitch-integrated React + TypeScript dashboard
│   ├── src/
│   │   ├── components/layout/      # Sidebar, Header
│   │   ├── components/common/      # KPICard, SectionCard, SpecimenModal
│   │   ├── pages/                  # 8 Analytical Module Pages
│   │   ├── services/api.ts         # Typed API client
│   │   └── types/api.ts            # Data models and interfaces
│   └── package.json
├── src/
│   ├── api/
│   │   └── app.py                  # FastAPI adapter connecting frontend to warehouse
│   ├── warehouse/                  # SchemaManager, connection engine, ORM models
│   ├── olap/                       # OLAPEngine (Roll-up, Drill-down, Slice, Dice, Pivot)
│   ├── mining/                     # K-Means clustering, Apriori, FP-Growth, evaluation
│   ├── preprocessing/              # Validation gates, blur scoring, deduplication
│   └── etl/                        # Extract, Transform, Load pipeline
├── tests/                          # Automated Pytest suite (81 tests)
│   ├── test_api_integration.py     # FastAPI endpoints and OLAP integration tests
│   ├── test_review2_mining.py      # Unsupervised clustering and rule mining tests
│   └── test_olap_real_warehouse.py # Star schema and OLAP operation tests
├── run.py                          # Unified CLI entrypoint
└── README.md
```

---

## 🚀 Execution Instructions

### 1. Environment Setup

Ensure Python 3.11 and Node.js (v18+) are installed.

```bash
# Install Python dependencies
pip install -r requirements.txt
pip install fastapi uvicorn httpx

# Install Frontend dependencies and build
cd frontend
npm install
npm run build
cd ..
```

### 2. Launch the Integrated System

#### Option A: Unified FastAPI Production Dashboard (Recommended)
FastAPI serves both the REST API endpoints and the pre-built React frontend directly on a single port:

```bash
python run.py --stage api --api-port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

#### Option B: Dual Development Mode (Hot Reload)
Start the FastAPI backend in one terminal, and the Vite dev server in another:

```bash
# Terminal 1: Backend
python run.py --stage api --api-port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

#### Option C: Fallback Streamlit Dashboard
The original Streamlit presentation layer remains fully preserved and functional:

```bash
python run.py --stage dashboard --dashboard-port 8501
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🧪 Automated Testing & Verification

Run the complete automated test suite:

```bash
pytest tests/ -v
```

**Test Execution Results:**
```text
======================= 81 passed in 14.46s =======================
tests/test_api_integration.py ...........                                [100%]
tests/test_config.py ...                                                 [100%]
tests/test_duplicates.py ...                                             [100%]
tests/test_etl_phase5.py .....                                           [100%]
tests/test_feature_extraction_phase3.py .....                            [100%]
tests/test_features.py ....                                              [100%]
tests/test_olap.py ......                                                [100%]
tests/test_olap_real_warehouse.py .......                                [100%]
tests/test_preprocessing_phase2.py ......                                [100%]
tests/test_profiler.py ..                                                [100%]
tests/test_review2_mining.py ..............                              [100%]
tests/test_validation.py .....                                           [100%]
tests/test_warehouse.py ...                                              [100%]
tests/test_warehouse_phase4.py .......                                   [100%]
```

---

## 🧭 Dashboard Navigation & Feature Guide

The Stitch-integrated frontend provides 8 fully functional navigation modules:

1. **Overview**: Editorial welcome banner, 4 high-level KPI cards, pathological status breakdown (Donut SVG), top represented crop genomes (horizontal bar chart), provenance audit, and end-to-end pipeline architecture.
2. **Dataset Explorer**: Slicers across Crop, Condition, Pathogen, Pest, and Source; keyword search with real-time matching; Grid View and Table View; and **Specimen Modal** displaying actual image rasters with the full 32 continuous feature tensor.
3. **Data Quality & ETL**: Cryptographic SHA-256 verification status card, 4 preprocessing quality gates, Laplacian variance blur distribution, deduplication logs, and ETL wall-clock timing.
4. **Data Warehouse**: Interactive Star Schema topology diagram, live DDL column inspector with SQLite data types, primary/foreign key badges, and row counts.
5. **OLAP Analytics**: Full OLAP workbench supporting Roll-Up, True Single-Dimension Drill-Down, Diagnostic Drill-Across, Slice by Crop, Slice by Pathogen, Dice Sub-Cube, and Pivot Matrix with live ANSI SQL syntax display and latency telemetry.
6. **Visual Pattern Mining**: Solution toggle between $K=2$ (Optimal, Silhouette 0.4060) and $K=4$ (Exploratory, Silhouette 0.1651); 4 cluster validity metric cards; interactive 2D PCA Latent Projection Scatter Plot with hover inspection; feature centroid profiles; and Chi-square contingency analysis.
7. **Association Rules**: Mode switcher between Mode A (Visual-Feature-Only, 880 rules, Unsupervised) and Mode B (Label-Conditioned, 285 rules, Exploratory with terracotta disclosure banner); Apriori vs FP-Growth algorithmic benchmark matrix; dynamic Support, Confidence, and Lift threshold filters; sortable rules table; and methodological advisory card.
8. **Reports & Methodology**: Comprehensive academic documentation tabs, scientific boundaries and ethical caveats, and raw JSON artifact viewers with direct download links.

---

## 🔬 Supervised Classifier Benchmark Tournament Results

To evaluate whether classical explainable visual descriptors suffice for fine-grained foliar disease discrimination compared to deep convolutional architectures, a tournament benchmark was executed across the strictly held-out test split ( = 490$ specimens) using StratifiedGroupKFold on perceptual dHash (preventing near-duplicate image leakage):

| Model Architecture | Feature Representation | Training Latency | Val Macro-F1 | Held-out Test Acc | Test Balanced Acc | Held-out Test Macro-F1 | Evaluation Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| **EfficientNet-B0 (Transfer Learning)** |  \times 224$ Normalized Tensors | 1,200.48 s | **63.26%** | **61.84%** | **61.43%** | **60.84%** (95% CI: [57.46%, 66.03%]) | **Best Evaluated Model (Optimal)** |
| **Random Forest Classifier** | Standardized 32D Feature Store | 1.15 s | 17.02% | 19.80% | 19.78% | 19.19% | Handcrafted Baseline (Substantial Underperformance) |
| **Support Vector Machine (RBF-SVM)** | Standardized 32D Feature Store | 1.43 s | 15.12% | 19.80% | 20.13% | 19.01% | Kernel Baseline (Substantial Underperformance) |
| **Majority Class Baseline** | Zero-Rule Frequency Prior | < 0.01 s | 0.58% | 7.76% | 4.00% | 0.58% | Naive Trivial Predictor |
| **Decision Tree Classifier (CART)** | Standardized 32D Feature Store | N/A | N/A | N/A | N/A | N/A | Reference Implementation (Not Benchmarked in Tournament) |

### Key Scientific Findings:
1. **Transfer Learning Superiority:** Deep hierarchical features (EfficientNet-B0) achieve 60.84% Macro-F1, substantially outperforming classical handcrafted 32D features (19.19% for Random Forest and 19.01% for RBF-SVM).
2. **Uncertainty & Domain Shift Policy:** Predictions with top-1 softmax probability below 0.35 or normalized Shannon entropy exceeding 0.85 are flagged as mathematically uncertain. In addition, ICAR flatbed scanner images (36 specimens) are identified via a source metadata policy gate as out-of-domain (OOD) relative to PlantDoc in-the-wild photography.

## ⚖️ Scientific Boundaries & Limitations

In accordance with rigorous academic and scientific standards, the following project boundaries are explicitly documented:

1. **$K=2$ Metric-Supported Solution**: Mathematical cluster validation metrics (Silhouette: 0.4060, Davies-Bouldin: 1.0990) confirm $K=2$ as the primary well-separated partition. $K=4$ represents an exploratory sub-partition with increased boundary dispersion (Silhouette: 0.1651).
2. **Association Does Not Prove Causality**: Association rules discovered with high lift reflect mathematical co-occurrence across discretized continuous visual descriptors, **not biological causation or biochemical etiology**.
3. **No Autonomous Disease Diagnosis**: Unsupervised clusters isolate mathematical descriptor distributions. Clusters must never be characterized as automated clinical diagnostic tools.
4. **Dataset Provenance Imbalance**: PlantDoc constitutes the dominant dataset share (2,560 images, 98.6%) compared to ICAR/OGD (36 images, 1.4%). Rice foliar pathologies are exclusively represented via ICAR macro imagery.
5. **Pest Symptom Underrepresentation**: Pest signs represent a minority class in the corpus (2 specimens). Findings primarily reflect fungal and bacterial foliar lesions.
