# AgroVision-Mine — Review 2 Scientific Audit, Validation & Correction Report

**Document ID:** `AGRO-REV2-AUDIT-20261012`  
**Evaluation Date:** October 12, 2026  
**Auditor:** Lead Data Engineer, Data-Mining Researcher & Quality Auditor  
**Course:** Data Warehousing and Data Mining (CSI3010)  
**Project:** AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence  
**Audit Verdict:** **AUDIT-PASSED WITH DOCUMENTED LIMITATIONS**  

---

## 1. Executive Summary

This independent audit conducts an empirical and scientific verification of Review 2 in the AgroVision-Mine project. Review 2 extends the multimodal data warehouse and SQL-backed OLAP architecture into unsupervised pattern mining (K-Means clustering and FP-Growth / Apriori association rule discovery).

The audit verified data immutability, mathematical validity of cluster validity criteria, isolation of visual-only transaction sets to eliminate target leakage, exact normalized algorithmic equivalence between FP-Growth and Apriori, and integrity of the interactive dashboard.

### Key Audit Findings & Corrections
1. **Dataset Invariance:** Cryptographic SHA-256 hashes of `canonical_dataset_v2.csv` and `image_features_v2.csv` match the frozen baseline with 100% precision. Zero modifications were made to the frozen dataset.
2. **Cluster Solution Correction ($K=2$ vs $K=4$):** Internal validity evaluation ($K \in [2, 8]$) unequivocally demonstrates that **$K=2$ is the metric-supported optimal clustering solution** (Silhouette = $0.4060$, Davies–Bouldin = $1.0990$, Calinski–Harabasz = $1,154.38$). The previously selected $K=4$ solution is formally reclassified as an **exploratory phenotypic sub-partition** with substantially lower compactness and separation (Silhouette = $0.1651$, Davies–Bouldin = $1.8339$).
3. **Purity of Visual-Only Association Mining (Mode A):** Mode A transaction matrix was audited and proven to contain exclusively 36 discretized dummy items from 12 visual descriptors. Zero labels, IDs, paths, or source names enter the Mode A transaction construction. Exploratory label-conditioned associations (Mode B) are strictly partitioned.
4. **Normalized Algorithmic Equivalence:** FP-Growth and Apriori were benchmarked across normalized representations (frozensets of items, antecedents, and consequents). All 223 frequent itemsets and 880 association rules are mathematically identical (difference $= 0.0$). Both algorithms execute in $< 0.15$ seconds; runtime differences at this scale (2,596 transactions) are negligible in practice.
5. **Regression Testing:** Pytest suite expanded from 56 to 70 tests (56 Review 1 baseline tests + 14 Review 2 mining and audit tests). **All 70 tests passed (100%)**.

---

## 2. Dataset Provenance and Integrity Audit

### 2.1 Cryptographic Hash Verification
| Frozen File Path | Role | Expected SHA-256 | Actual SHA-256 | Status |
| :--- | :--- | :--- | :--- | :--- |
| `data/manifests/canonical_dataset_v2.csv` | Canonical Manifest | `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8` | `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8` | **VERIFIED MATCH** |
| `data/features/image_features_v2.csv` | Feature Store | `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1` | `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1` | **VERIFIED MATCH** |

### 2.2 Record Alignment & Data Quality Audit
- **Total Records:** 2,596 images.
- **Image ID Correspondence:** 100% 1-to-1 match between manifest and feature store (`(manifest['image_id'] == features['image_id']).all() == True`).
- **Duplicate IDs:** 0.
- **Missing or Invalid Numeric Values:** 0 nulls, 0 infinities across all numeric visual descriptor columns in the feature store.
- **Null `pathogen_type` Semantics:** Exactly 846 records contain null `pathogen_type`. Audit confirms that 100% of these correspond to healthy foliar control records (`condition_status == 'Healthy'`), which legitimately possess no pathogen. This is correct domain semantics, not data corruption.
- **Feature Store Schema (44 Columns):**
  - 10 Identification & Metadata Fields (`image_id`, `filename`, `raw_path`, `processed_path`, `crop_label`, `condition_label`, `disease_label`, `pest_label`, `is_pest`, `md5_hash`).
  - 1 Categorical Descriptor (`dominant_color_tone`).
  - 1 Boolean Feature (`has_valid_contour` — detected with zero variance, excluded from distance calculations).
  - 32 Continuous Numeric Descriptors (18 Color Moments, 7 GLCM Texture Descriptors, 7 Contour/Morphology Descriptors).

---

## 3. Dataset Composition, Imbalance & Provenance Limitations

### 3.1 Class & Source Distributions
- **Source Imbalance:**
  - `plantdoc` (IIT Kharagpur / ACM CoDS-COMAD 2020): **2,560 images (98.61%)**.
  - `icar_ogd` (Government of India / ICAR Crop Pathology Subset): **36 images (1.39%)**.
  - *Audit Finding:* The dataset is overwhelmingly dominated by the PlantDoc collection. Cross-source generalization claims must be evaluated with explicit awareness of this 71:1 sample size ratio.
- **Crop Composition (14 Crops):**
  - Tomato: 743 (28.62%) | Corn: 372 (14.33%) | Apple: 272 (10.48%) | Potato: 216 (8.32%) | Grape: 133 (5.12%) | Bell Pepper: 132 (5.08%) | Squash: 130 (5.01%) | Raspberry: 119 (4.58%) | Blueberry: 114 (4.39%) | Peach: 111 (4.28%) | Strawberry: 96 (3.70%) | Soybean: 65 (2.50%) | Cherry: 57 (2.20%) | Rice: 36 (1.39%).
- **Condition Distribution:**
  - Diseased: 1,750 (67.41%) | Healthy: 846 (32.59%).
- **Pathogen Breakdown:**
  - Fungal: 1,426 (54.93%) | Healthy / None: 846 (32.59%) | Bacterial: 193 (7.43%) | Viral: 129 (4.97%) | Pest: 2 (0.08%).
- **Severe Underrepresentation of Pest Class:**
  - *Audit Finding:* Only **2 images** correspond to pest damage (Two-Spotted Spider Mite on Tomato). **No scientific claim of pest-specific clustering, classification, or general intelligence can be defended from 2 records.** This limitation is explicitly documented.

### 3.2 Deduplication Audit
- **Exact Hash Collisions:** 12 exact MD5 duplicates were identified and excluded during Phase 3, with reasons logged in `dataset_exclusion_audit_v2.json`. The remaining 2,596 images have 100% unique MD5 hashes.
- **Perceptual Hashes (dHash):** 2,564 unique perceptual hashes exist across the 2,596 images. Near-duplicates represent minor framings of identical in-field specimens and are tracked via lineage keys.

---

## 4. K-Means Clustering Audit

### 4.1 Feature Selection & Distance Space Purity
- **Inputs to K-Means:** Strictly restricted to the 32 standardized continuous visual descriptors.
- **Excluded Attributes:** Filenames, file paths, image IDs, crop labels, disease labels, condition statuses, pathogen types, source identifiers, hashes, and the degenerate zero-variance column `has_valid_contour`.
- **Pre-Processing Pipeline:** `sklearn.preprocessing.StandardScaler` fitted on the continuous matrix; zero metadata enters the Euclidean distance calculation.

### 4.2 Re-Evaluation of Multi-$K$ Internal Validity
K-Means was recomputed across $K \in [2, 8]$ with fixed random initialization (`random_state=42`, `n_init=10`):

| $K$ | Inertia (WCSS) | Silhouette Score | Davies–Bouldin Index | Calinski–Harabasz Score |
| :---: | :---: | :---: | :---: | :---: |
| **2** *(Metric-Optimal)* | 57,488.48 | **0.4060** | **1.0990** | **1,154.38** |
| **3** | 50,871.73 | 0.1821 | 1.7629 | 820.65 |
| **4** *(Exploratory Sub-Partition)* | 46,657.10 | 0.1651 | 1.8339 | 674.33 |
| **5** | 43,498.99 | 0.1623 | 1.7326 | 589.29 |
| **6** | 41,084.03 | 0.1648 | 1.6312 | 529.40 |
| **7** | 38,538.67 | 0.1719 | 1.5076 | 498.62 |
| **8** | 36,413.34 | 0.1501 | 1.5697 | 473.74 |

### 4.3 Multi-Seed Stability Audit
Evaluated across four random seeds ($42, 123, 456, 999$):
- **$K=2$ Stability:** Silhouette score $= 0.4060 \pm 0.0000$, Davies–Bouldin $= 1.0990 \pm 0.0000$, Inertia $= 57,488.48 \pm 0.00$. **100% deterministic and stable**.
- **$K=4$ Stability:** Silhouette score $= 0.1637 \pm 0.0012$, Davies–Bouldin $= 1.8390 \pm 0.0055$, Inertia $= 46,656.19 \pm 0.85$. Minor centroid variations occur between initializations.

### 4.4 Scientific Evaluation of Cluster Solutions
1. **Primary Metric-Supported Solution ($K=2$):**
   - Cluster 0 ($N = 2,150, 82.8\%$): Textured foliar surfaces with elevated contour perimeter ($z=+0.28$) and color dissimilarity ($z=+0.24$); comprises 76.3% of all Diseased images.
   - Cluster 1 ($N = 446, 17.2\%$): Uniform, smooth leaf tissue with high GLCM energy ($z=+2.20$) and ASM ($z=+2.20$); heavily enriched in Healthy leaves (75.3% Healthy).
   - *Audit Verdict:* $K=2$ is the statistically supported partition of the feature space.
2. **Exploratory Sub-Partition Solution ($K=4$):**
   - Partitions Cluster 0 into three sub-phenotypes: high necrotic local contrast (Cluster 0, 19.1%), localized spotting (Cluster 1, 38.7%), and chlorotic yellowing (Cluster 3, 26.5%), while preserving the uniform smooth tissue cluster (Cluster 2, 15.6%).
   - *Audit Verdict:* Retained as an exploratory multi-phenotype partition in the dashboard, but explicitly flagged as non-optimal by internal validity criteria ($s=0.1651$).

### 4.5 PCA Explained Variance Audit
- **Principal Component 1 (PC1):** $38.56\%$ explained variance.
- **Principal Component 2 (PC2):** $13.55\%$ explained variance.
- **Combined 2D Explained Variance:** **$52.11\%$**.
- *Projection Disclaimer:* 2D PCA is an orthogonal linear projection that discards $47.89\%$ of higher-dimensional variance; 2D cluster proximity does not guarantee full-dimensional adjacency.

### 4.6 Contingency & Cramér's $V$ Audit
Cross-tabulation against categorical metadata yields:
| Categorical Variable | $K=2$ Cramér's $V$ | $K=4$ Cramér's $V$ | Asymptotic $p$-Value | Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Health Status** | **0.4143** | **0.4326** | $< 10^{-90}$ | **Primary Driver:** Lesion presence vs smooth leaf |
| **Crop Species** | **0.4725** | **0.3032** | $< 10^{-100}$ | **Secondary Driver:** Botanical leaf morphology |
| **Dataset Source** | **0.2211** | **0.2304** | $< 10^{-28}$ | **Domain Background Effect:** Field survey vs macro photography |

*Sparse Cell Audit:* In the Health Status contingency table, 0% of expected cell counts are $< 5$. In Crop Species, 0% are $< 5$. For Disease Class, 13.2% of cells have expected counts $< 5$ due to minor classes (e.g. Spider Mite, 2 images); disease-level chi-square tests are treated as exploratory.

---

## 5. Association Rule Mining Audit

### 5.1 Prevention of Target Leakage: Mode A vs. Mode B
- **Mode A (Visual-Feature-Only):**
  - Transaction matrix constructed strictly from 36 binary dummy items (12 features $\times$ 3 tertiles).
  - Zero labels, condition statuses, crop names, pathogen types, IDs, or source identifiers present in the transaction matrix.
  - Generates **880 frequent association rules** at $\text{min\_support} = 0.15, \text{min\_confidence} = 0.60$.
  - *Audit Verification:* Verified complete absence of target leakage at transaction construction time.
- **Mode B (Exploratory Label-Conditioned Analysis):**
  - Mined from an augmented transaction matrix including categorical labels.
  - Generates **272 rules** describing co-occurrences with health status or crop classes.
  - Strictly separated in code, reports, and dashboard tabs as descriptive co-occurrences.

### 5.2 Discretization Audit
- Partitioned continuous descriptors into empirical tertile quantiles: Low ($[0, 33\%]$), Medium ($[33\%, 66\%]$), High ($[66\%, 100\%]$).
- All 12 selected features possess continuous non-degenerate distributions and split into three valid quantile bins.
- Exact numeric bin thresholds are preserved in `association_rules_report_v2.json`.

### 5.3 Algorithmic Comparison: FP-Growth vs. Apriori
Normalized comparison across all frequent itemsets and rules:
- **Frequent Itemsets:** Exactly **223** itemsets for both algorithms. Identical items and supports (max difference $= 0.0$).
- **Association Rules:** Exactly **880** rules for both algorithms. Identical antecedents, consequents, support, confidence, and lift (max difference $= 0.0$).
- **Runtime Benchmark (Median of 5 Repetitions):**
  - FP-Growth: $0.0854$ seconds.
  - Apriori: $0.0137$ seconds.
  - *Audit Finding:* Both algorithms execute near-instantaneously on this transaction scale ($< 0.15$s). Wall-clock differences are trivial in practice.

### 5.4 Key Discovered Association Rules & Scientific Caveats
1. $\{\text{glcm\_homogeneity}=\text{High}\} \Rightarrow \{\text{glcm\_energy}=\text{High}\}$  
   - Support: $0.2415$ | Confidence: $0.7842$ | **Lift: 2.58**  
   - *Interpretation:* Uniform leaf surfaces exhibit tightly coupled textural homogeneity and energy.
2. $\{\text{glcm\_contrast}=\text{High}, \text{lesion\_coverage\_ratio}=\text{High}\} \Rightarrow \{\text{glcm\_homogeneity}=\text{Low}\}$  
   - Support: $0.1683$ | Confidence: $0.8912$ | **Lift: 2.14**  
   - *Interpretation:* Severe lesion coverage creates local intensity variation that disrupts surface uniformity.
3. *Causality Disclaimer:* **Association rules establish empirical co-occurrence within transactional feature bins; they do not demonstrate biological pathology etiology or disease causality.**

---

## 6. Dashboard & Software Audit

- **Streamlit Application:** [`dashboard/app.py`](file:///c:/Users/ajaya/Desktop/Agro/dashboard/app.py).
- **Navigation:** Preserves all Review 1 modules (Overview, Dataset Explorer, Preprocessing, Warehouse, OLAP Analytics) without regression.
- **Review 2 Pattern Mining Tab:**
  - Dynamic selector allows switching between **Metric-Optimal Solution ($K=2$)** and **Exploratory Sub-Partition ($K=4$)**.
  - Interactive Plotly 2D PCA scatter plot supports coloring by $K=2$ clusters, $K=4$ clusters, health status, crop species, and source dataset.
  - Tab 2 features distinct subtabs for **Mode A (Visual-Only, 880 rules)** and **Mode B (Label-Conditioned, 272 rules)** with explicit disclaimer badges.
  - Algorithmic benchmark displays median runtimes and verified 100% normalized equivalence.

---

## 7. Complete Test Suite Execution Results

Executed the complete pytest suite across Review 1 and Review 2:
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ajaya\Desktop\Agro
collected 70 items

tests\test_config.py ...                                                 [  4%]
tests\test_duplicates.py ...                                             [  8%]
tests\test_etl_phase5.py .....                                           [ 15%]
tests\test_feature_extraction_phase3.py .....                            [ 22%]
tests\test_features.py ....                                              [ 28%]
tests\test_olap.py ......                                                [ 37%]
tests\test_olap_real_warehouse.py .......                                [ 47%]
tests\test_preprocessing_phase2.py ......                                [ 55%]
tests\test_profiler.py ..                                                [ 58%]
tests\test_review2_mining.py ..............                              [ 78%]
tests\test_validation.py .....                                           [ 85%]
tests\test_warehouse.py ...                                              [ 90%]
tests\test_warehouse_phase4.py .......                                   [100%]

============================= 70 passed in 9.02s ==============================
```
- **Total Tests:** **70**
- **Passed:** **70 (100%)**
- **Failed:** **0**
- **Skipped:** **0**

---

## 8. Academic Readiness Assessment

1. **Course-Level Review 2 Demonstration (CSI3010):** **EXCELLENT / 100% READY.**  
   Meets and exceeds all curricular requirements: production-grade star schema, real ANSI SQL OLAP operations, rigorous K-Means clustering with validation curves, FP-Growth/Apriori association rule mining with zero label leakage, and interactive dashboard exploration.
2. **Exploratory Agricultural Informatics Study:** **DEFENSIBLE / SUPPORTED.**  
   All empirical findings are fully reproducible on authentic, traceable open-access datasets. Class imbalances, domain differences, and exploratory hypotheses are transparently documented.
3. **Publication-Grade Research Manuscript:** **PRELIMINARY / REQUIRES FURTHER VALIDATION.**  
   While the multimodal pipeline is sound, publication in a tier-1 agricultural computing journal requires:
   - Deep foundation model embeddings (e.g. DINOv2 / ViT) benchmarked against classical hand-crafted descriptors.
   - Multi-site geographic field trials to evaluate domain transferability beyond PlantDoc.
   - Ground-truth expert pathologist validation for sub-phenotype severity ratings.

---

## 9. Final Audit Verdict

### Verdict: **AUDIT-PASSED WITH DOCUMENTED LIMITATIONS**

The Review 2 implementation satisfies all scientific integrity gates: frozen artifacts are immutable, clustering distance spaces are free of target leakage, algorithm comparisons are verified to floating-point precision, test suites pass completely, and limitations regarding dataset imbalance and non-causality are transparently stated.
