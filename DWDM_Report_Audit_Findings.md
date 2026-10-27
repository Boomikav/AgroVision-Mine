# AgroVision-Mine — Comprehensive Technical Audit & Evidence Reconciliation Findings

**Document Target:** Data Warehousing and Data Mining (DWDM) Laboratory Project Report (CSI3010)  
**Audit Date:** October 25, 2026  
**Audited Artifacts Produced:**
- **Word Document:** [`DWDM_Project_Report_Final_Audited.docx`](file:///c:/Users/ajaya/Desktop/Agro/DWDM_Project_Report_Final_Audited.docx) (2,593,088 bytes | SHA-256: `13c04627f7471056fa9454f11fe9ff72732cc28cc936f4d3c696404b355fd7ad`)
- **PDF Document:** [`DWDM_Project_Report_Final_Audited.pdf`](file:///c:/Users/ajaya/Desktop/Agro/DWDM_Project_Report_Final_Audited.pdf) (36 pages, 966,943 bytes | SHA-256: `afb1e35a0eb6e54c2ffe9b0d87196b1726f3f1d302e76b063ab58637406066f7`)

---

## 1. Executive Summary of Audit

An exhaustive technical audit and reconciliation was conducted across the source codebase, model registries, empirical evaluation JSON records, database schemas, and report drafts of the **AgroVision-Mine** project. The primary objective was to enforce strict academic and scientific truth:
1. **Zero Fabrication:** Eliminate all synthetic, unverified, or inferred performance claims, particularly around regression, classification baselines, and longitudinal forecasting.
2. **Algorithmic Classification:** Explicitly categorize every machine learning algorithm into one of three verifiable operational tiers:
   - **Tier 1 — Implemented and Evaluated:** Code executed, artifacts saved, metrics audited.
   - **Tier 2 — Implemented Reference Baseline (Not Benchmarked in Tournament):** Code implemented as structural baseline, but not evaluated across the 25-class tournament on the held-out test split.
   - **Tier 3 — Conceptual / Future Work Only:** Included for institutional template compliance or future architectural scoping; no continuous ground truth target exists in the dataset.
3. **Feature Space Harmonization:** Resolve conflicting historical notations (9/16/7, 18/7/7, 19/7/6) into the verified canonical database vector of exactly **32 continuous visual descriptors** (19 Colour & Vegetation moments/indices, 7 GLCM Haralick texture statistics, and 6 morphometric contour and lesion coverage parameters).
4. **Architectural Disambiguation:** Distinguish the **4 Image Quality Assurance Gates** from the **5 End-to-End Analytical Workflow Phases**.
5. **Uncertainty & Out-of-Domain Boundaries:** Separate mathematically grounded softmax confidence (<0.35 / 0.40) and normalized Shannon entropy (>0.85) from metadata policy gating for ICAR macro-scanned specimens.
6. **Tone & Superlative Elimination:** Replace all engineering hype ("production-grade", "robust separation", "state-of-the-art", "flawless") with objective, reproducible academic prose.

---

## 2. Comprehensive Claims vs. Evidence Audit Matrix

The following matrix documents each technical topic audited, the claim in earlier drafts, the exact source evidence inspected, the audit verdict, the correction applied in [`DWDM_Project_Report_Final_Audited.docx`](file:///c:/Users/ajaya/Desktop/Agro/DWDM_Project_Report_Final_Audited.docx), and the associated scientific limitation or safeguard.

| # | Topic / Section | Prior Draft Text / Claim | Source Evidence Inspected | Audit Verdict / Tier | Exact Correction Applied | Scientific Safeguard / Unresolved Limitation |
|---|---|---|---|---|---|---|
| **1** | **Chapter 4.1: K-Means Clustering** | Unsupervised clustering over 32D features; claims optimal $K=2$ and $K=4$. Did not state initialization restarts, seed, or exact preprocessing. | `src/mining/clustering.py`, `data/reports/clustering_evaluation.json`, `data/reports/paper_evidence_audit.json` | **Tier 1: Implemented & Evaluated** | Documented Lloyd's algorithm, `StandardScaler` on 32D continuous features, `k-means++` initialization, `n_init=10` random restarts, `random_state=42`, $K \in [2, 8]$ sweep. Confirmed $K=2$ mathematically optimal (Silhouette: 0.4060, DB: 1.0990, CH: 1154.38). Labeled $K=4$ strictly as an exploratory sub-partition (Silhouette: 0.1651). | Internal clustering criteria measure geometric compactness in standardized feature space, not phytopathological diagnosis. |
| **2** | **Chapter 4.2: Agglomerative Hierarchical Clustering** | Described as an "exploratory baseline" with taxonomic dendrograms. | Codebase search: No active HAC execution or dendrogram serialization in `src/mining/` or pipeline. | **Tier 3: Conceptual Alternative Only (Not Executed)** | Explicitly labeled as "Conceptual Alternative Only (Not Executed in Active Pipeline)". Removed claims of execution. Documented computational complexity of $O(N^2 \log N)$ time and $O(N^2)$ memory for pairwise distance matrix over $N=2,596$ observations. Explained why it is unsuited for high-throughput interactive OLAP workloads. | Pairwise distance matrix requires storing $2,596 \times 2,596$ floating-point values in memory, which scales poorly to interactive queries. |
| **3** | **Chapter 4.3: Principal Component Analysis (PCA)** | 2D PCA captures 52.11% variance; used for visualization. | `src/mining/clustering.py` (lines 85–130), `data/reports/paper_evidence_audit.json` (`olap` & `clustering` blocks). | **Tier 1: Implemented & Evaluated** | Retained formulation: sample covariance matrix $\Sigma = \frac{1}{N}X^T X$, eigendecomposition $\Sigma v_i = \lambda_i v_i$. Preprocessing: `StandardScaler` fitted on 32D descriptors. Confirmed PC1 = 38.56% (surface texture & contour perimeter), PC2 = 13.55% (vegetative chromaticity), Cumulative 2D = 52.11%. | Linear projection captures global variance but may compress non-linear manifolds. |
| **4** | **Chapter 4.4: Decision Tree Classifier (CART)** | Described as trained over 32 continuous descriptors to extract human-auditable rules, with decision boundary plots implied. | `src/mining/decision_tree.py` exists as reference class, but `data/reports/paper_evidence_audit.json` and tournament records contain no CART test metrics for 25 classes. | **Tier 2: Implemented Reference Baseline (Not Benchmarked in Tournament)** | Explicitly labeled as "Implemented Reference Baseline (Not Benchmarked in Tournament)". Documented recursive binary splitting and Gini impurity formulation $I_G(t) = 1 - \sum p(c\|t)^2$. Disclosed that CART was not benchmarked in the final 25-class tournament on the held-out test split, and zero fabricated metrics were reported. | Single decision trees exhibit high variance, orthogonal partitioning bias, and severe instability under class imbalance. |
| **5** | **Chapter 4.5: Random Forest Classifier** | Titled "Random Forest Classifier and Regressor". Claimed "robust multi-class separation" and "superior baseline performance". | `data/reports/paper_evidence_audit.json` (`random_forest_32d` entry), `data/models/prediction/random_forest_32d.joblib`. | **Tier 1: Implemented & Evaluated (Classifier Only)** | Renamed section to **4.5 Random Forest Classifier** (removed "and Regressor"). Reported audited metrics: `n_estimators=100`, `class_weight='balanced'`, feature subspace sampling $\sqrt{D} \approx 5.66$, training time 1.15s; Validation Macro-F1 = 17.02%, Held-out Test Accuracy = 19.80%, Test Balanced Accuracy = 19.78%, Test Macro-F1 = 19.19%. Removed all claims of "robust separation" or "superiority"; acknowledged poor performance of handcrafted features. | Handcrafted 32D global visual descriptors lack fine-grained discriminative power for 25-class in-the-wild foliar pathology. |
| **6** | **Chapter 4.6: Linear, Ridge, and Lasso Regression** | Documented OLS, Ridge, and Lasso regression models as if potentially trained or evaluated for continuous severity scoring. | Dataset manifests (`data/manifests/canonical_manifest_v2.json`, `data/warehouse/agrovision_warehouse.db`). Target variables are strictly categorical (`crop_name`, `disease_name`, `condition_status`). | **Tier 3: Conceptual / Future Work Only** | Explicitly labeled as "Conceptual / Future Work Only". Disclosed that the canonical 2,596-image dataset contains categorical pathology labels rather than continuous physical targets (percentage leaf area destroyed, chlorophyll concentration, or metric yield loss in tonnes/ha). Confirmed NO regression models were trained or evaluated on fabricated data. Documented mathematical formulations strictly as an architectural specification for future yield-loss modules. | Training regression on synthetic or non-existent continuous targets would violate scientific integrity. |
| **7** | **Chapter 4.7 & 7.2.1: EfficientNet-B0 (Transfer Learning)** | Mentioned as supplementary classifier; lacked dedicated methodology section in Chapter 4; missing complete tournament baseline table in Chapter 7. | `src/mining/predictor.py`, `data/models/prediction/model_metadata.json`, `data/models/prediction/efficientnet_b0_foliar.pt` (16.4 MB), `data/reports/paper_evidence_audit.json`. | **Tier 1: Implemented & Evaluated** | Added dedicated Section 4.7 covering: ImageNet-1K pretrained backbone (`EfficientNet_B0_Weights.DEFAULT`), modified output head `Dropout(p=0.3) -> Linear(1280, 25)`, 224x224 RGB input resolution, ImageNet normalization, 8 training epochs, Adam optimizer, StratifiedGroupKFold on perceptual dHash (1,468 train / 489 val / 490 test). Audited held-out test metrics: Accuracy = 61.84%, Balanced Accuracy = 61.43%, Macro-F1 = 60.84%, 95% Bootstrap CI: [57.46%, 66.03%], Training latency: 1,200.48s. Added Table 10 tournament comparing EfficientNet-B0 against RF (19.19%), RBF-SVM (19.01%), and Majority Baseline (0.58%). | Explains that deep convolutional representations substantially outperform classical handcrafted features on complex in-the-wild foliage. |
| **8** | **Continuous Feature Count Reconciliation** | Conflicting counts across chapters: Abstract stated "9/16/7", Chapter 3 Table 4 stated "9/16/7", Chapter 5 stated "18/7/7", and some sections implied "19/7/6". | `src/warehouse/models.py` (`DimVisualFeature` and `to_feature_vector()`), `data/features/image_features_v2.csv`. | **Verified Canonical Breakdown** | Reconciled all chapters (Abstract, Ch 1, Ch 3, Ch 5, Ch 6, Ch 7, Sample Code/Output) to state the verified **19 / 7 / 6 = 32** breakdown: **19 Colour & Vegetation** (9 RGB moments + 9 HSV moments + 1 Excess Green Index ExG = 2G - R - B), **7 GLCM Haralick Textures** (contrast, normalized contrast, dissimilarity, homogeneity, energy, correlation, ASM), **6 Morphometrics & Lesion Coverage** (contour area, perimeter, aspect ratio, circularity, solidity, lesion coverage ratio; `has_valid_contour` is a boolean flag). | Explains why historical drafts cited differing groupings due to channel aggregations, standardizing the terminology across the entire report. |
| **9** | **QA Gates vs. Workflow Phases** | Four QA stages sometimes conflated with the overall five pipeline phases. | `src/etl/preprocessing.py`, `src/etl/pipeline.py`, Figure 1, Figure 2. | **Delineated Hierarchy** | Clearly distinguished the **4 Image QA Gates** (Gate 1: PIL decode/integrity; Gate 2: Laplacian blur scoring $\ge 100$; Gate 3: MD5 deduplication & dHash grouping; Gate 4: 256x256 standardization) as sub-components of **Phase 1** within the **5 End-to-End Workflow Phases** (Phase 1: Ingestion & QA; Phase 2: 32D Feature Extraction; Phase 3: Transactional ETL & Star Schema; Phase 4: Multidimensional OLAP Engine; Phase 5: Pattern Mining & Prediction). | Preserves clear architectural separation between data ingestion validation and downstream analytical processing. |
| **10** | **Uncertainty & Out-of-Domain Boundaries** | Termed "Out-of-Domain Detection" generically, risking interpretation as an autonomous neural density estimator. | `src/mining/predictor.py` (lines 40–95), `data/models/prediction/model_metadata.json`. | **Policy & Metric Clarified** | Clarified that uncertainty handling comprises: (1) Softmax confidence thresholding (<0.35 / 0.40 flags uncertain), (2) Normalized Shannon entropy (>0.85 flags high ambiguity), and (3) Out-of-domain detection for ICAR flatbed scanner images (36 specimens) is executed via a source manifest metadata / domain policy gate, NOT an autonomous neural density estimator. | Avoids misleading claims of unsupervised neural OOD density estimation while documenting operational safety gating. |
| **11** | **Automated Test Suite Verification** | Previous text stated "81/81 automated test suite". | Executed `pytest --ignore=tests/test_browser_functional.py` across workspace test directory. | **Audited Test Count** | Updated text, Abstract, Chapter 6, and Output 6 to document **107 passing automated test cases across 16 test modules** (100% pass rate in 18.99s). Documented that 10 additional end-to-end browser tests in `test_browser_functional.py` validate the interactive frontend when the FastAPI server is running. | Complete transparency on unit/integration vs live browser test suites. |
| **12** | **Section 7.3.3: Template Heading Clarification** | Institutional template contained heading: "National Longitudinal Crime Trajectory and 2025 Forecasting". | Template `DWDM_Report_Titles_Only.docx`. | **Template Clarification Provided** | Retained template heading to preserve structural compliance, but provided explicit clarification: The heading originated from a generic institutional lab template referencing municipal crime data. In AgroVision-Mine, this module corresponds to Agricultural Pathogen Longitudinal Surveillance. Because PlantDoc and ICAR datasets do not contain multi-year epidemiological time series, empirical 2025 forecasting was not fabricated on fake data. Scoping for future ICAR-CRIDA / OGD India integration was documented in Section 9.2. | Adheres strictly to scientific truth while honoring institutional submission structure. |

---

## 3. Algorithm Implementation and Evaluation Status

Every algorithm discussed in Chapter 4 and Chapter 7 of the report is formally classified below:

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                  AGROVISION-MINE MACHINE LEARNING ALGORITHM TAXONOMY                                    |
+------------------------------------------+------------------------------------------+-----------------------------------+
| TIER 1: IMPLEMENTED & EVALUATED          | TIER 2: IMPLEMENTED REFERENCE BASELINE   | TIER 3: CONCEPTUAL / FUTURE WORK  |
+------------------------------------------+------------------------------------------+-----------------------------------+
| 1. K-Means Clustering (Section 4.1)      | 1. Decision Tree / CART (Section 4.4)    | 1. Agglomerative Hierarchical     |
|    - Lloyd's algorithm, k-means++ init   |    - Implemented white-box module        |    Clustering / HAC (Section 4.2) |
|    - n_init=10, random_state=42          |    - Gini impurity recursive splitting   |    - Ward's minimum variance      |
|    - Optimal K=2 (Silh: 0.4060)          |    - Not benchmarked in 25-class         |    - O(N^2 log N) time, O(N^2)    |
|    - Exploratory K=4 (Silh: 0.1651)      |      tournament on held-out test split   |      memory unsuited for OLAP     |
|                                          |    - Zero fabricated metrics reported    |                                   |
| 2. Principal Component Analysis / PCA    |                                          | 2. Linear, Ridge, and Lasso       |
|    (Section 4.3)                         |                                          |    Regression (Section 4.6)       |
|    - Eigendecomposition over 32D features|                                          |    - OLS, L2 Ridge, L1 Lasso      |
|    - StandardScaler fitted               |                                          |    - No continuous ground truth   |
|    - PC1: 38.56%, PC2: 13.55%            |                                          |      target in dataset            |
|    - Cumulative 2D variance: 52.11%      |                                          |    - No models trained/evaluated  |
|                                          |                                          |                                   |
| 3. Random Forest Classifier              |                                          | 3. Longitudinal 2025 Epidemiol-   |
|    (Section 4.5)                         |                                          |    ogical Forecasting             |
|    - B=100 trees, sqrt(D) sampling       |                                          |    (Section 7.3.3)                |
|    - Balanced class weighting            |                                          |    - Template heading inherited   |
|    - Val Macro-F1: 17.02%                |                                          |    - Static image corpus lacks    |
|    - Test Accuracy: 19.80%               |                                          |      multi-year time series       |
|    - Test Macro-F1: 19.19%               |                                          |    - Zero synthetic data produced |
|                                          |                                          |                                   |
| 4. Support Vector Machine / RBF-SVM      |                                          |                                   |
|    (Section 4.7 / 7.2.1)                 |                                          |                                   |
|    - Radial Basis Function kernel        |                                          |                                   |
|    - Val Macro-F1: 15.12%                |                                          |                                   |
|    - Test Accuracy: 19.80%               |                                          |                                   |
|    - Test Macro-F1: 19.01%               |                                          |                                   |
|                                          |                                          |                                   |
| 5. EfficientNet-B0 Transfer Learning     |                                          |                                   |
|    (Section 4.7 & 7.2.1)                 |                                          |                                   |
|    - Pretrained ImageNet-1K backbone     |                                          |                                   |
|    - Dropout(0.3) -> Linear(1280, 25)    |                                          |                                   |
|    - StratifiedGroupKFold on dHash       |                                          |                                   |
|    - 8 epochs, Adam, Cross-Entropy       |                                          |                                   |
|    - Val Macro-F1: 63.26%                |                                          |                                   |
|    - Test Accuracy: 61.84%               |                                          |                                   |
|    - Test Balanced Accuracy: 61.43%      |                                          |                                   |
|    - Test Macro-F1: 60.84%               |                                          |                                   |
|    - 95% Bootstrap CI: [57.46%, 66.03%]  |                                          |                                   |
|    - Best-performing evaluated model     |                                          |                                   |
+------------------------------------------+------------------------------------------+-----------------------------------+
```

---

## 4. Supervised Benchmark Tournament Results

The empirical results from the canonical benchmarking tournament across the strictly held-out test split ($N = 490$ specimens) are verified from `data/reports/paper_evidence_audit.json`:

| Model Architecture | Feature Representation | Training Latency | Validation Macro-F1 | Held-out Test Accuracy | Test Balanced Accuracy | Held-out Test Macro-F1 | Evaluation Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| **EfficientNet-B0 (Transfer Learning)** | $224 \times 224$ RGB Normalized Tensors | 1,200.48 s (~20 min) | **63.26%** | **61.84%** | **61.43%** | **60.84%** (95% CI: `[57.46%, 66.03%]`) | **Best Evaluated Model (Optimal)** |
| **Random Forest Classifier** | Standardized 32D Continuous Feature Store | 1.15 s | 17.02% | 19.80% | 19.78% | 19.19% | Handcrafted Baseline (Substantial Underperformance) |
| **Support Vector Machine (RBF-SVM)** | Standardized 32D Continuous Feature Store | 1.43 s | 15.12% | 19.80% | 20.13% | 19.01% | Kernel Baseline (Substantial Underperformance) |
| **Majority Class Baseline** | Zero-Rule Empirical Frequency Prior | < 0.01 s | 0.58% | 7.76% | 4.00% | 0.58% | Naive Trivial Predictor (Theoretical Lower Bound) |
| **Decision Tree Classifier (CART)** | Standardized 32D Continuous Feature Store | N/A | N/A | N/A | N/A | N/A | Reference Implementation (Not Benchmarked in Tournament) |

### Key Scientific Insights:
1. **Transfer Learning Superiority:** EfficientNet-B0 dramatically outperforms the classical handcrafted baselines (60.84% Macro-F1 vs 19.19% for Random Forest and 19.01% for RBF-SVM).
2. **Handcrafted Feature Insufficiency:** While the 32 continuous descriptors provide biological explainability and power the OLAP warehouse and K-Means clustering, global colour, GLCM texture, and morphometric contours lack the spatial hierarchy required to resolve 25 fine-grained foliar disease classes under in-the-wild illumination.
3. **Generalization Stability:** The 95% non-parametric bootstrap confidence interval `[57.46%, 66.03%]` confirms that test accuracy (61.84%) aligns closely with validation accuracy (63.60%), confirming that `StratifiedGroupKFold` on perceptual dHash successfully eliminated near-duplicate leaf leakage.

---

## 5. Feature Vector Formulation Breakdown (Canonical 32 Descriptors)

The 32 continuous visual descriptors extracted per specimen and loaded into `dim_visual_feature` are grouped as follows:

### A. Colour Moments & Vegetation Indices (19 Continuous Descriptors)
- **RGB First & Second Moments (6 descriptors):** `rgb_r_mean`, `rgb_g_mean`, `rgb_b_mean`, `rgb_r_std`, `rgb_g_std`, `rgb_b_std`
- **RGB Normalized Chromatic Intensities (3 descriptors):** `rgb_r_norm`, `rgb_g_norm`, `rgb_b_norm` ($r = R / (R + G + B)$, etc.)
- **HSV First & Second Moments (6 descriptors):** `hsv_h_mean`, `hsv_s_mean`, `hsv_v_mean`, `hsv_h_std`, `hsv_s_std`, `hsv_v_std`
- **HSV Normalized Chromatic Intensities (3 descriptors):** `hsv_h_norm`, `hsv_s_norm`, `hsv_v_norm`
- **Foliar Vegetation Vitality Index (1 descriptor):** `exg_index_mean` (Excess Green Index: $ExG = 2G - R - B$)

### B. Gray-Level Co-occurrence Matrix (GLCM) Haralick Texture Metrics (7 Continuous Descriptors)
Computed at pixel offset distance $d = 1$ and angle $\theta = 0^\circ$ across 256 quantization levels:
- `glcm_contrast` (surface irregularity)
- `glcm_contrast_norm` (range-normalized surface irregularity)
- `glcm_dissimilarity` (mean linear difference in gray-level pairs)
- `glcm_homogeneity` (local surface smoothness)
- `glcm_energy` (uniformity of texture distribution)
- `glcm_correlation` (linear gray-tone dependencies)
- `glcm_asm` (Angular Second Moment, energy squared)

### C. Morphometric Shape & Lesion Coverage Metrics (6 Continuous Descriptors)
Extracted via Otsu binary thresholding of foliar contours:
- `contour_area` (pixel area of primary foliar contour)
- `contour_perimeter` (boundary perimeter length)
- `contour_aspect_ratio` (bounding box width / height)
- `contour_circularity` ($4 \pi \times \text{Area} / \text{Perimeter}^2$)
- `contour_solidity` ($\text{Area} / \text{Convex Hull Area}$)
- `lesion_coverage_ratio` ($\text{Lesion Area} / \text{Total Foliar Area}$)
*(Note: `has_valid_contour` is recorded as a boolean flag indicating whether a valid closed contour was detected).*

**Total Continuous Descriptors:** $19 + 7 + 6 = 32$.

---

## 6. Visual Presentation and Styling Compliance

Both generated documents strictly adhere to the visual and aesthetic requirements extracted from `Smart_Automation_System_Review2_Presentation(1).pptx`:
- **Font Family:** `Book Antiqua` applied consistently across all chapter headings, subsection titles, body paragraphs, table text, headers, and footers.
- **Heading Colors:** Deep Presentation Blue (`#1F4E79`) applied to Project Title, Heading 1 (18 pt bold), Heading 2 (13.5 pt bold), Heading 3 (11.5 pt bold italic), and Heading 4 (10.5 pt bold).
- **Body Text:** Dark Charcoal (`#1C1C1C`), 10.5 pt, justified alignment, line multiplier 1.15.
- **Accent Typography:**
  - Student names and registration numbers: Presentation Crimson Red (`#C00000`, bold 12 pt).
  - Faculty Guide designation: Presentation Forest Green (`#00B050`, bold 12 pt).
  - Figure and table captions: Muted Slate Gray (`#595959`, 9 pt italic).
- **Table Design (Clean Academic Style):**
  - **Zero Blue Fill:** All table cells feature pure white backgrounds (`#FFFFFF`).
  - **Borders:** Thin black borders (`0.5 pt`) on all interior and exterior cells.
  - **Headers:** Bold black text (`#000000`), 10 pt Book Antiqua, repeated across pages (`tblHeader`).
  - **Row Splitting:** Prohibited (`cantSplit`) to prevent orphaned rows across page boundaries.
- **Page Layout & Pagination:**
  - Standard A4 dimensions with 1-inch (2.54 cm) margins.
  - Cover page uses `different_first_page_header_footer = True` with zero headers or footers.
  - Abstract is formatted compactly to fit **entirely on Page 2**.
  - Chapter 1 begins cleanly on **Page 3**.
  - Document spans exactly **36 pages** with zero blank pages.

---

## 7. Deliverable Verification and Artifact Checksums

The following authoritative files have been generated, verified, and saved in the active project workspace:

1. **Final Audited Word Report:**
   - **Path:** [`c:\Users\ajaya\Desktop\Agro\DWDM_Project_Report_Final_Audited.docx`](file:///c:/Users/ajaya/Desktop/Agro/DWDM_Project_Report_Final_Audited.docx)
   - **File Size:** 2,593,088 bytes (2,532.3 KB)
   - **SHA-256:** `13c04627f7471056fa9454f11fe9ff72732cc28cc936f4d3c696404b355fd7ad`

2. **Final Audited PDF Document (Rendered via Microsoft Word COM Automation):**
   - **Path:** [`c:\Users\ajaya\Desktop\Agro\DWDM_Project_Report_Final_Audited.pdf`](file:///c:/Users/ajaya/Desktop/Agro/DWDM_Project_Report_Final_Audited.pdf)
   - **File Size:** 966,943 bytes (944.3 KB)
   - **Total Pages:** 36 pages
   - **SHA-256:** `afb1e35a0eb6e54c2ffe9b0d87196b1726f3f1d302e76b063ab58637406066f7`

3. **Audit Findings & Evidence Reconciliation Report (This Document):**
   - **Path:** [`c:\Users\ajaya\Desktop\Agro\DWDM_Report_Audit_Findings.md`](file:///c:/Users/ajaya/Desktop/Agro/DWDM_Report_Audit_Findings.md)
