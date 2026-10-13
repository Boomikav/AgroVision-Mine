# AgroVision-Mine — Review 2 Pattern Mining Methodology

**Document ID:** `AGRO-REV2-METH-20261012`  
**Project:** AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence  
**Course:** Data Warehousing & Data Mining (CSI3010)  
**Scope:** Review 2 Unsupervised Clustering & Association Rule Mining  

---

## 1. Overview & Research Objectives

Review 2 advances the AgroVision-Mine platform from data warehousing and OLAP multidimensional summarization into advanced unsupervised pattern mining. Using the audited, frozen multi-crop research dataset (`canonical_v2`, 2,596 images, 14 crops, 19 disease classes), this phase explores visual pathology signatures across crops without label-guided supervision.

### Formal Research Questions (Hypotheses)
1. **RQ1 (Visual Feature Cohesion):** Do interpretable color, texture, and shape descriptors form mathematically coherent, non-random clusters across multi-crop agricultural field imagery?
2. **RQ2 (Clustering Drivers & Domain Bias):** Are discovered visual clusters driven primarily by disease pathology (lesion severity), botanical crop morphology, or image acquisition context (source dataset bias)?
3. **RQ3 (Textural & Color Itemset Co-occurrence):** Which discretized visual feature combinations co-occur frequently within the transactional feature space?
4. **RQ4 (Cross-Source & Cross-Crop Transferability):** Do discovered visual associations hold true across distinct agricultural datasets (ICAR/OGD vs. PlantDoc)?

---

## 2. Unsupervised K-Means Clustering Methodology

### 2.1 Feature Space Definition
To preserve scientific explainability and prevent label leakage, all identification metadata, filenames, hashes, and target labels are strictly excluded from model inputs:
- **Excluded Attributes:** `image_id`, `filename`, `raw_path`, `processed_path`, `crop_label`, `condition_label`, `disease_label`, `pest_label`, `is_pest`, `md5_hash`, `dominant_color_tone`, `crop_name`, `dataset_source`, `pathogen_type`.
- **Retained Descriptors (32 numeric continuous features):**
  - **Color Descriptors (18 features):** Channel means, standard deviations, and normalized channel ratios for RGB and HSV spaces, along with the Excess Green Index (`exg_index_mean`).
  - **Texture Descriptors (7 features):** Gray-Level Co-occurrence Matrix (GLCM) contrast, dissimilarity, homogeneity, energy, correlation, angular second moment (ASM), and normalized contrast.
  - **Shape & Morphology Descriptors (7 features):** Lesion coverage ratio, contour perimeter, circularity, solidity, aspect ratio, and area.
  - *Note on Degenerate Feature Handling:* Feature `has_valid_contour` exhibited zero variance ($1.0$ across all standardized images) and was algorithmically detected and excluded.

### 2.2 Feature Standardization
Continuous descriptors span diverse physical units (e.g., pixel perimeters vs normalized color ratios). We apply $z$-score feature standardization:
$$z = \frac{x - \mu}{\sigma}$$
using `sklearn.preprocessing.StandardScaler` fitted on the full frozen dataset.

### 2.3 Cluster Number ($K$) Selection & Validation Indices
We evaluate $K \in [2, 10]$ using fixed pseudo-random initialization (`random_state=42`, `n_init=10`) across four complementary internal validity metrics:
1. **Silhouette Score:** Evaluates cluster cohesion versus separation:
   $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
2. **Davies-Bouldin Index:** Measures average similarity between clusters (lower is superior):
   $$DB = \frac{1}{k}\sum_{i=1}^{k} \max_{j \neq i} \left(\frac{s_i + s_j}{d(c_i, c_j)}\right)$$
3. **Calinski-Harabasz Index:** Variance ratio criterion (higher indicates denser, well-separated clusters):
   $$CH = \frac{\text{Tr}(B_k)}{\text{Tr}(W_k)} \times \frac{n - k}{k - 1}$$
4. **Inertia (Within-Cluster Sum of Squares):** Elbow method metric.

### 2.4 Dimensionality Reduction & Visualization
To visualize multi-dimensional clusters in human-interpretable 2D space, Principal Component Analysis (PCA) is applied to projected coordinates (`pca_x`, `pca_y`), retaining and documenting the explained variance ratios.

### 2.5 Post-Hoc Contingency Analysis (RQ2 Investigation)
Cluster assignments are evaluated against categorical ground-truth metadata (`condition_status`, `crop_name`, `pathogen_type`, `dataset_source`) using the Pearson Chi-Square test of independence ($\chi^2$) and Cramér's $V$:
$$V = \sqrt{\frac{\chi^2}{n \cdot \min(r - 1, c - 1)}}$$
where $V \in [0, 1]$ quantifies the true associative strength between cluster assignments and metadata attributes.

---

## 3. Association Rule Mining Methodology (FP-Growth & Apriori)

### 3.1 Feature Discretization Strategy
Association rule algorithms (FP-Growth and Apriori) operate on discrete transactional itemsets. Directly applying these algorithms to continuous floating-point descriptors is mathematically invalid.

We implement **Quantile-Based Tertile Discretization**:
- Continuous values are partitioned into empirical tertiles: `Low` ($[0, 33.3\%]$), `Medium` ($[33.3\%, 66.7\%]$), and `High` ($[66.7\%, 100\%]$).
- Exact numeric bin edges are preserved in metadata (`data/reports/association_rules_report_v2.json`).
- Selected 12 core descriptors span all visual domains:
  - Color: `hsv_h_mean`, `hsv_s_mean`, `hsv_v_mean`, `exg_index_mean`.
  - Texture: `glcm_contrast`, `glcm_homogeneity`, `glcm_energy`, `glcm_correlation`.
  - Shape: `contour_perimeter`, `contour_circularity`, `contour_solidity`, `lesion_coverage_ratio`.

### 3.2 Transaction Encodings
1. **Visual-Feature-Only Matrix:** Contains only discretized visual descriptors (36 binary dummy items across the 12 features).
2. **Label-Conditioned Matrix:** Extends the visual items with categorical metadata items (`condition_status`, `crop_name`, `pathogen_type`) for exploratory cross-domain analysis.

### 3.3 Rule Mining Metrics & Thresholds
- **Support:** Proportion of transactions containing itemset $X$:
  $$\text{Support}(X) = \frac{\text{count}(X)}{N}$$
- **Confidence:** Conditional probability of consequent $Y$ given antecedent $X$:
  $$\text{Confidence}(X \Rightarrow Y) = \frac{\text{Support}(X \cup Y)}{\text{Support}(X)}$$
- **Lift:** Measure of dependence between antecedent and consequent:
  $$\text{Lift}(X \Rightarrow Y) = \frac{\text{Confidence}(X \Rightarrow Y)}{\text{Support}(Y)}$$
  ($\text{Lift} > 1$ denotes positive statistical dependence; $\text{Lift} = 1$ denotes statistical independence).

- **Operational Baseline Settings:** $\text{min\_support} = 0.15$, $\text{min\_confidence} = 0.60$.
- **Sensitivity Analysis:** Systematically evaluates nine threshold combinations ($\text{min\_support} \in \{0.10, 0.15, 0.20\} \times \text{min\_confidence} \in \{0.50, 0.60, 0.70\}$).

### 3.4 Algorithmic Comparison (FP-Growth vs Apriori)
Both algorithms are executed on identical transactional matrices to rigorously compare:
1. Candidate generation overhead vs. compact FP-tree construction runtime.
2. Rule output equivalence (ensuring zero discrepancies between discovered itemsets).

---

## 4. Software Architecture & Module Organization

- `src/mining/clustering.py`: Class `CropVisualClusterer` encapsulates scaling, multi-K evaluation, centroid profiling, contingency testing, PCA projection, and report generation.
- `src/mining/association_rules.py`: Class `VisualAssociationMiner` handles tertile quantile discretization, one-hot transaction encoding, FP-Growth/Apriori execution, and sensitivity analysis.
- `src/mining/evaluation.py`: Class `Review2Evaluator` synthesizes experimental results, evaluates research questions, and outputs consolidated benchmarks.
- `dashboard/app.py`: Integrated Streamlit interface featuring an interactive Review 2 Pattern Mining module.
