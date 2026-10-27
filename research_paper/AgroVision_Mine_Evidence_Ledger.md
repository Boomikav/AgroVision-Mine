# AgroVision-Mine — Research Evidence Ledger

This document establishes the verified empirical evidence supporting all quantitative claims, architectural specifications, and experimental results presented in the IEEE conference paper:

**"AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence"**

---

## 1. Comprehensive Evidence Ledger Table

| # | Claim / Proposed Statement | Supporting File / Experiment | Verification Method | Verified Value | Status | Publication Suitability |
|---|---|---|---|---|:---:|:---:|
| **1** | Total canonical image corpus contains 2,596 observations across 14 crops | `data/manifests/canonical_dataset_v2.csv` | File row count & SHA-256 computation via hashlib | 2,596 rows, 14 unique crops; SHA-256: `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8` | **Verified** | **Suitable** |
| **2** | Canonical corpus provenance comprises 2,560 PlantDoc in-the-wild images and 36 ICAR flatbed scanner images | `data/manifests/canonical_dataset_v2.csv` | Value counts on `dataset_source` | PlantDoc: 2,560 (98.61%); ICAR/OGD: 36 (1.39%) | **Verified** | **Suitable** |
| **3** | Pathological status distribution: 1,750 diseased and 846 healthy specimens | `data/manifests/canonical_dataset_v2.csv` | Value counts on `condition_status` | Diseased: 1,750 (67.41%); Healthy: 846 (32.59%) | **Verified** | **Suitable** |
| **4** | Feature store contains 44 columns with 32 continuous handcrafted descriptors | `data/features/image_features_v2.csv` | Column inspection & SHA-256 calculation | 44 total columns, 32 continuous descriptors (19 Color Moments, 7 Haralick GLCM, 6 Morphometric); SHA-256: `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1` | **Verified** | **Suitable** |
| **5** | Ingestion pipeline enforces 5 automated quality validation gates | `src/preprocessing/preprocessor.py` | Code inspection & unit test execution | Gate 1: Magic bytes format; Gate 2: Dimension $\ge 100\times 100$; Gate 3: Payload $\le 15$ MB; Gate 4: MD5 deduplication; Gate 5: EXIF transposition & RGB normalization | **Verified** | **Suitable** |
| **6** | Kimball-style star schema warehouse persists in SQLite with 0 foreign-key violations | `database/agrovision_warehouse.db` | SQLite `PRAGMA foreign_key_check` and table row counts | `disease_observation_fact`: 2,596 rows; `dim_crop`: 14 rows; `dim_disease`: 20 rows; `dim_image`: 2,596 rows; `dim_visual_feature`: 2,596 rows; Violations: 0 | **Verified** | **Suitable** |
| **7** | Dimensional OLAP queries execute with sub-35ms latency | `src/olap/engine.py` / `scripts/audit_for_paper.py` | `time.perf_counter()` benchmark on real SQLite instance | Roll-up: 33.26 ms; Drill-down: 31.27 ms; Slice (Tomato): 14.99 ms; Dice: 14.42 ms; Pivot: 12.57 ms | **Verified** | **Suitable** |
| **8** | K-Means clustering achieves mathematical optimum at K=2 in standardized 32D space | `data/reports/clustering_report_v2.json` | Evaluation of Silhouette, Davies-Bouldin, and Calinski-Harabasz across $K \in [2, 8]$ | $K=2$: Silhouette = 0.4060, DB = 1.0990, CH = 1,154.38; $K=4$: Silhouette = 0.1651, DB = 1.8339, CH = 674.33 | **Verified** | **Suitable** |
| **9** | 2D PCA captures 52.11% cumulative variance across 32 continuous descriptors | `data/reports/clustering_report_v2.json` | Scikit-learn PCA projection matrix inspection | PC1: 38.56% (Foliar Luminance); PC2: 13.55% (Textural Contrast); Total: 52.11% | **Verified** | **Suitable** |
| **10** | Apriori and FP-Growth association rule mining yield exact mathematical parity ($\Delta = 0.0$) | `data/reports/association_rules_report_v2.json` | Metric comparison of generated itemsets and rules | Mode A (visual-only): 223 frequent itemsets, 880 rules; Parity: 100.0% ($\Delta = 0.0$ on support, confidence, lift) | **Verified** | **Suitable** |
| **11** | Mode B label-conditioned association mining generates 285 exploratory rules | `data/reports/association_rules_report_v2.json` | Inspection of extracted rules at min_support=0.15, min_confidence=0.60 | 285 total rules; 276 positive lift ($\ge 1.0$); top rule lift = 6.0132 | **Verified** | **Suitable** |
| **12** | Supervised learning benchmark evaluates 25 composite classes across 12 host crops | `data/models/prediction/model_metadata.json` | Inspection of `supported_classes` array | 25 classes (14 diseased, 11 healthy); 12 host crops (Tomato, Corn, Apple, Potato, Grape, Bell Pepper, Squash, Raspberry, Blueberry, Peach, Strawberry, Soybean) | **Verified** | **Suitable** |
| **13** | Primary classification dataset partitions 2,447 PlantDoc images into train/val/test using grouped dHash | `data/models/prediction/split_manifest.csv` | Value counts of `evaluation_partition` and perceptual hash group boundary check | Train: 1,468 (60.0%); Val: 489 (20.0%); Test: 490 (20.0%); Excluded rare: 113; Scanner OOD: 36; Total: 2,596 | **Verified** | **Suitable** |
| **14** | Zero cross-partition data leakage across perceptual hash clusters | `data/models/prediction/split_manifest.csv` | Cross-tabulation of dHash cluster IDs against partitions | Overlap: 0 groups, 0 images across train/val/test | **Verified** | **Suitable** |
| **15** | Model selection tournament on validation partition selects EfficientNet-B0 | `data/reports/prediction/prediction_evaluation_report.json` | Validation Macro-F1 comparison | Majority baseline: 0.58%; RBF-SVM (32D): 15.12%; Random Forest (32D): 17.02%; EfficientNet-B0: 63.26% | **Verified** | **Suitable** |
| **16** | Fine-tuned EfficientNet-B0 achieves 61.84% Top-1 Accuracy on 490 held-out test images | `data/reports/prediction/prediction_evaluation_report.json` | Direct evaluation of test predictions against ground truth | 303 / 490 correct predictions; Top-1 Accuracy: 61.84% | **Verified** | **Suitable** |
| **17** | Held-out test Balanced Accuracy is 61.43% and Macro-F1 is 60.84% | `data/reports/prediction/prediction_evaluation_report.json` | Scikit-learn classification report verification | Balanced Accuracy: 61.43%; Macro-F1: 60.84% | **Verified** | **Suitable** |
| **18** | Wilson 95% confidence interval for test accuracy is [57.46%, 66.03%] | `data/reports/prediction/prediction_evaluation_report.json` | Wilson score interval formula on $n=490, p=0.6184$ | Interval: [0.5746, 0.6603] | **Verified** | **Suitable** |
| **19** | EfficientNet-B0 training configuration uses AdamW with differential learning rate and ReduceLROnPlateau | `scripts/train_and_evaluate_models.py` | Code inspection of training loop | Epochs: 8; Batch size: 32; Optimizer: AdamW; Backbone LR: $10^{-4}$; Head LR: $10^{-3}$; Weight decay: $10^{-4}$; Loss: CrossEntropyLoss; ReduceLROnPlateau (factor=0.5, patience=2) | **Verified** | **Suitable** |
| **20** | Out-of-domain ICAR rice scanner images trigger automated `unsupported_domain` rejection alert | `src/mining/image_analyzer.py` / `src/api/app.py` | Integration test and live API verification | Rice scanner images trigger cross-modal 32D nearest-reference check, setting `status: 'unsupported_domain'` and `is_uncertain: true` | **Verified** | **Suitable** |
| **21** | Total automated software test suite contains 117 tests with 100% pass rate | `tests/` / pytest / Playwright logs | Execution of pytest and Playwright test runners | 107 pytest unit/integration tests + 10 Playwright browser E2E tests = 117/117 passed (0 failures) | **Verified** | **Suitable** |
| **22** | Unconstrained binary healthy/diseased classifier is superior to multiclass modeling | N/A (Methodological anti-pattern) | Contingency analysis of raw PlantDoc | **Rejected**: 7 of 14 crops have 0 healthy specimens in PlantDoc; binary classifier learns crop species shortcut rather than pathology | **Unsupported** | **Unsuitable (Must be refuted in text)** |
| **23** | System functions as an autonomous, certified clinical agricultural diagnostic tool | N/A (Overclaim) | Epistemological review | **Rejected**: Geometric proximity in 32D feature space is not biological pathogenesis; deep model is bounded to 25 classes | **Unsupported** | **Unsuitable (Explicit limitation)** |

---

## 2. Integrity Summary
- Total Claims Audited: **23**
- Claims Verified: **21**
- Overclaims Refuted & Controlled: **2** (Unconstrained binary shortcut confounding; Clinical diagnostic claim)
- Cryptographic Immutability: **Confirmed** (Manifest SHA-256 `c7fd16dc...`, Feature Store SHA-256 `f6caf70b...`)
- Data Leakage Audit: **0 Leaks Detected** (Strict grouped dHash split partitioning)
