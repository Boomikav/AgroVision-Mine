# AgroVision-Mine — Review 2 Final Verification and Freeze Report

**Document ID:** `AGRO-REV2-FREEZE-20261012`  
**Execution Date:** October 12, 2026  
**Auditor:** Independent Quality Auditor & Data Mining Researcher  
**Course:** Data Warehousing and Data Mining (CSI3010)  
**Project:** AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence  
**Final Verdict:** **PASSED WITH LIMITATIONS**  

---

## 1. Executive Summary

This report establishes the final, independent verification and permanent freeze of Review 2 for AgroVision-Mine. All claims regarding dataset volume, cryptographic invariance, clustering stability, target-leakage prevention, normalized algorithmic equivalence, and regression tests were audited against the live codebase and freshly recomputed.

| Verification Dimension | Tested Claim | Independent Re-Evaluation | Status |
| :--- | :--- | :--- | :--- |
| **Dataset Invariance** | Frozen SHA-256 match | SHA-256 verified identical before & after execution | **100% Invariant** |
| **Observation Volume** | 2,596 images, 0 nulls | Exactly 2,596 aligned rows, 0 numeric nulls/Infs | **Verified** |
| **Clustering Stability ($K=2$)** | Metric-supported solution | Pairwise ARI across seeds $[42, 123, 456, 999] = \mathbf{1.0000}$ | **Perfect Stability** |
| **Clustering Stability ($K=4$)** | Exploratory sub-partition | Pairwise ARI across seeds $= 0.8609\text{--}0.9871$ ($\text{Mean} = 0.9044$) | **Exploratory Validated** |
| **Association Mining Purity** | Zero label leakage in Mode A | 36 boolean dummies exclusively from 12 visual descriptors | **Zero Leakage** |
| **FP-Growth vs Apriori** | Normalized equivalence | Max support/confidence/lift discrepancy $= \mathbf{0.0}$ | **100% Equivalence** |
| **Pytest Suite** | Full regression test | **70 collected, 70 passed, 0 failed in 14.71s** | **100% Green** |
| **Review 1 Preservation** | Warehouse & 36 rice images | 56/56 Review 1 baseline tests passed | **100% Preserved** |

---

## 2. Frozen Dataset Checksums & Record Verification

Cryptographic SHA-256 hashes of both canonical dataset files were verified before and after execution:

```text
canonical_dataset_v2.csv:
  Path: data/manifests/canonical_dataset_v2.csv
  Actual SHA-256:   c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8
  Expected SHA-256: c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8
  Match Status:     VERIFIED TRUE

image_features_v2.csv:
  Path: data/features/image_features_v2.csv
  Actual SHA-256:   f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1
  Expected SHA-256: f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1
  Match Status:     VERIFIED TRUE
```

- **Row Count:** Exactly 2,596 rows in both files.
- **ID Alignment:** Exactly 2,596 unique IDs in identical order (`(manifest['image_id'] == features['image_id']).all() == True`).
- **Pathogen Null Semantics:** Exactly 846 null values in `pathogen_type` in the manifest; 100% map to `condition_status == 'Healthy'`.

---

## 3. Independent Clustering Stability Audit (Adjusted Rand Index)

Models for $K=2$ and $K=4$ were independently fitted across four pseudo-random seeds ($42, 123, 456, 999$) on the 32 standardized numeric visual descriptors (`StandardScaler`, `n_init=10`). Pairwise Adjusted Rand Index (ARI) was computed across all 6 seed pairs to evaluate partition stability:

### 3.1 Pairwise ARI Stability Results
| Seed Comparison | $K=2$ (Metric-Supported) ARI | $K=4$ (Exploratory Sub-Partition) ARI |
| :--- | :---: | :---: |
| **Seed 42 vs. Seed 123** | **1.0000** | 0.8609 |
| **Seed 42 vs. Seed 456** | **1.0000** | 0.8630 |
| **Seed 42 vs. Seed 999** | **1.0000** | 0.9871 |
| **Seed 123 vs. Seed 456** | **1.0000** | 0.9835 |
| **Seed 123 vs. Seed 999** | **1.0000** | 0.8648 |
| **Seed 456 vs. Seed 999** | **1.0000** | 0.8669 |
| **Mean Pairwise ARI** | **1.0000** | **0.9044** |
| **Min Pairwise ARI** | **1.0000** | **0.8609** |
| **Max Pairwise ARI** | **1.0000** | **0.9871** |

### 3.2 Cluster Sizes and Metrics Across Seeds
- **For $K=2$:**
  - Cluster Sizes: Exactly $\{2,150, 446\}$ across all seeds (modulo label permutation).
  - Silhouette Score: $0.4060 \pm 0.0000$ (Highest across all evaluated $K$).
  - Davies–Bouldin Index: $1.0990 \pm 0.0000$ (Lowest/best across all evaluated $K$).
  - Calinski–Harabasz Index: $1,154.38 \pm 0.00$ (Highest across all evaluated $K$).
  - Inertia (WCSS): $57,488.48 \pm 0.00$.
- **For $K=4$:**
  - Cluster Sizes: Varies slightly across seeds (e.g., $\{497, 1005, 406, 688\}$ for seed 42 vs. $\{408, 766, 468, 954\}$ for seed 123) due to local sub-partition shifts within the textured data cloud.
  - Silhouette Score: $0.1625\text{--}0.1651$ ($s = 0.1637 \pm 0.0012$).
  - Davies–Bouldin Index: $1.8332\text{--}1.8447$ ($DB = 1.8390 \pm 0.0055$).
  - Calinski–Harabasz Index: $674.33\text{--}674.40$.
  - Inertia (WCSS): $46,655.34\text{--}46,657.10$.

### 3.3 Scientific Stability Interpretation
1. **$K=2$ is the unique metric-supported and partition-stable solution.** It separates smooth, low-perimeter tissue (Cluster 1) from textured, high-perimeter foliar surfaces (Cluster 0) with 100% deterministic reproducibility.
2. **$K=4$ is confirmed to be an exploratory sub-partition.** While it provides interesting descriptive phenotypes (e.g. chlorotic yellowing vs local spotting), its internal validity metrics are more than 50% lower than $K=2$, and cluster boundaries exhibit seed-dependent boundary variance ($ARI \approx 0.90$). It must never be presented as the mathematically optimal solution.

---

## 4. Association Rule Mining Source Purity Audit

### 4.1 Transaction Matrix Verification (Mode A)
- **Source Feature Set:** Strictly 12 continuous visual descriptors:
  - Color: `hsv_h_mean`, `hsv_s_mean`, `hsv_v_mean`, `exg_index_mean`.
  - Texture: `glcm_contrast`, `glcm_homogeneity`, `glcm_energy`, `glcm_correlation`.
  - Shape: `contour_perimeter`, `contour_circularity`, `contour_solidity`, `lesion_coverage_ratio`.
- **Discretization:** Empirical tertiles (Low, Medium, High).
- **Matrix Dimensions:** 2,596 transactions $\times$ 36 boolean columns.
- **Leakage Check:** 0 prohibited terms present. Zero labels, zero IDs, zero filenames, zero paths, zero hashes, and zero source identifiers exist in the transaction matrix.

### 4.2 Separation of Mode A and Mode B
- **Mode A (Visual-Only):** Exactly **880 rules** ($\text{min\_support} = 0.15, \text{min\_confidence} = 0.60$). Zero label items present in any antecedent or consequent.
- **Mode B (Exploratory Label-Conditioned):** Exactly **272 rules** describing descriptive co-occurrences with health status and crop labels. Maintained in separate report keys and dashboard tabs.
- **Algorithmic Equivalence:** Normalized verification confirms that all 223 itemsets and all 880 rules match 100% identically between FP-Growth and Apriori (max discrepancy $= 0.0$).

---

## 5. Artifact Consistency & Dashboard Verification

All generated outputs were traced and validated against fresh calculations:
- `clustering_report_v2.json`: Dual $K=2$ and $K=4$ profiles and contingency statistics match fresh calculations.
- `clustering_assignments_v2.csv`: Contains `cluster_id_k2`, `cluster_id_k4`, `cluster_id` (defaulting to metric-optimal $K=2$), and PCA coordinates (`pca_x`, `pca_y`).
- `association_rules_report_v2.json`: Contains normalized benchmark (median runtimes, tolerance verification, 880 Mode A rules, 272 Mode B rules).
- `review2_evaluation_report.json`: Consolidates research findings with explicit caveats.
- `dashboard/app.py`: Interactive radio selector enables toggling between $K=2$ (Metric-Supported) and $K=4$ (Exploratory), with Mode A/B rule subtabs and scientific disclaimers.

---

## 6. Full Test Suite Execution Summary

Executed from project root (`pytest tests/`):
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ajaya\Desktop\Agro
plugins: anyio-4.14.2, asyncio-1.4.0
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

============================= 70 passed in 14.71s =============================
```
- **Total Tests Collected:** 70
- **Total Tests Passed:** 70 (100%)
- **Failures:** 0
- **Skipped:** 0

---

## 7. Remaining Limitations & Scientific Disclosures

1. **Source Imbalance (PlantDoc vs. ICAR):** PlantDoc comprises 98.61% (2,560 images) of the dataset, whereas ICAR/OGD comprises 1.39% (36 images). While cross-source patterns hold, findings reflect predominantly PlantDoc in-field conditions.
2. **Taxonomic Imbalance:** Solanaceous crops (Tomato, Potato, Pepper) represent 42% of images. Generalization across non-solanaceous crops is preliminary.
3. **Pest Underrepresentation:** The pest damage class contains only **2 images** (Two-Spotted Spider Mite). No reliable claim of automated pest classification or detection can be supported.
4. **Non-Causality of Association Rules:** Rules describe observational co-occurrences in discretized feature transactions; they do not establish biological pathology etiology or disease causality.
5. **Dimensionality Reduction Caveat:** 2D PCA projects 52.11% of variance; 47.89% resides in higher-dimensional space. 2D proximity does not guarantee full-dimensional separation.

---

## 8. Final Freeze Decision

### Verdict: **PASSED WITH LIMITATIONS**

The Review 2 implementation of AgroVision-Mine is fully verified, reproducible, mathematically validated, and permanently frozen. All scientific claims are appropriately scoped and supported by empirical evidence.
