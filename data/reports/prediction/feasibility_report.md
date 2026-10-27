# AgroVision-Mine — Supervised Model Feasibility and Class Support Audit

**Audit Date:** 2026-10-19  
**Status:** Canonical Integrity Verified • Splits Frozen Without Leakage  

---

## 1. Canonical Verification & Checksums
- `canonical_dataset_v2.csv` SHA-256: `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8` (**Verified Immutable**)
- `image_features_v2.csv` SHA-256: `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1` (**Verified Immutable**)
- Total Observations: **2,596** (2,560 PlantDoc in-the-wild images, 36 ICAR/OGD flatbed scanner images)

---

## 2. Confounding Analysis: Binary Healthy vs. Diseased
A diagnostic classifier was evaluated to test whether host crop identity alone could predict disease status:
- **Accuracy using only crop dummy variables:** **89.3%** (`accuracy = 0.8925`)
- **Finding:** 10 of the 14 crop species in the repository are 100% single-condition:
  - **100% Healthy Crops (6):** Blueberry (114), Cherry (57), Peach (111), Raspberry (119), Soybean (65), Strawberry (96). Total = 562 specimens without a single diseased counterpart.
  - **100% Diseased Crops (4):** Corn (372), Potato (216), Rice (36), Squash (130). Total = 754 specimens without a single healthy counterpart.
  - **Mixed Crops (4):** Apple (181 diseased / 91 healthy), Bell Pepper (71 / 61), Grape (64 / 69), Tomato (680 / 63).
- **Scientific Conclusion:** Evaluating a generic binary Healthy vs. Diseased classifier across all 14 crops is scientifically indefensible. The model would learn crop morphology (leaf contours, margins, color tones) as an empirical shortcut rather than foliar disease lesions.
- **Selected Supervised Target:** **Multi-class Crop-Condition Classification** over well-supported PlantDoc classes ($N \ge 60$), supplemented by out-of-domain and rare-class uncertainty detection.

---

## 3. Predeclared Class Support Threshold ($N \ge 60$)
To guarantee statistically sound training and evaluation with at least 12–15 independent test specimens per class:
- **Primary Benchmark:** **25 well-supported classes** across 12 crops, comprising **2,447 images**.
- **Excluded Rare Classes ($N < 60$):**
  - `Tomato - Two-Spotted Spider Mite`: $N=2$ (statistically intractable for multi-fold splitting).
  - `Tomato - Mosaic Virus`: $N=54$ (sub-threshold support).
  - `Cherry - Healthy`: $N=57$ (sub-threshold support).
- **Out-of-Domain Scanner Classes (ICAR/OGD):**
  - `Rice - Bacterial Leaf Blight`: $N=12$
  - `Rice - Brown Spot`: $N=12$
  - `Rice - Leaf Smut`: $N=12$  
  *(Flatbed scanner acquisition with white studio background is separated from field evaluation to avoid cross-domain shortcut bias).*

---

## 4. Grouped Splitting & Deduplication Guarantee
- **Identified Near-Duplicate Groups (dHash):** 31 groups encompassing 63 images.
- **Split Scheme:** Grouped Stratified Partitioning (`StratifiedGroupKFold`) keyed on `dhash` clusters:
  - **Train:** **1468 images** (60.0%)
  - **Validation:** **489 images** (20.0%)
  - **Held-Out Test:** **490 images** (20.0%)
- **Group Overlap:** **0 records** cross split boundaries (zero data leakage).

---

## 5. Class Support Breakdown Table

| Composite Class | Crop | Condition | Source | Support ($N$) | Near Dupes | Unique Units | Primary Benchmark Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `Corn___Northern Leaf Blight` | Corn | Diseased | plantdoc | 190 | 4 | 188 | **Included (Supported)** |
| `Tomato___Septoria Leaf Spot` | Tomato | Diseased | plantdoc | 149 | 8 | 147 | **Included (Supported)** |
| `Squash___Powdery Mildew` | Squash | Diseased | plantdoc | 130 | 2 | 129 | **Included (Supported)** |
| `Raspberry___Healthy` | Raspberry | Healthy | plantdoc | 119 | 2 | 118 | **Included (Supported)** |
| `Corn___Common Rust` | Corn | Diseased | plantdoc | 116 | 0 | 116 | **Included (Supported)** |
| `Blueberry___Healthy` | Blueberry | Healthy | plantdoc | 114 | 0 | 114 | **Included (Supported)** |
| `Potato___Early Blight` | Potato | Diseased | plantdoc | 113 | 7 | 113 | **Included (Supported)** |
| `Tomato___Late Blight` | Tomato | Diseased | plantdoc | 111 | 13 | 107 | **Included (Supported)** |
| `Peach___Healthy` | Peach | Healthy | plantdoc | 111 | 0 | 111 | **Included (Supported)** |
| `Tomato___Bacterial Spot` | Tomato | Diseased | plantdoc | 110 | 3 | 109 | **Included (Supported)** |
| `Potato___Late Blight` | Potato | Diseased | plantdoc | 103 | 8 | 101 | **Included (Supported)** |
| `Strawberry___Healthy` | Strawberry | Healthy | plantdoc | 96 | 0 | 96 | **Included (Supported)** |
| `Apple___Apple Scab` | Apple | Diseased | plantdoc | 93 | 2 | 92 | **Included (Supported)** |
| `Apple___Healthy` | Apple | Healthy | plantdoc | 91 | 0 | 91 | **Included (Supported)** |
| `Tomato___Leaf Mold` | Tomato | Diseased | plantdoc | 91 | 1 | 91 | **Included (Supported)** |
| `Apple___Cedar Apple Rust` | Apple | Diseased | plantdoc | 88 | 0 | 88 | **Included (Supported)** |
| `Tomato___Early Blight` | Tomato | Diseased | plantdoc | 88 | 8 | 87 | **Included (Supported)** |
| `Tomato___Yellow Leaf Curl Virus` | Tomato | Diseased | plantdoc | 75 | 1 | 75 | **Included (Supported)** |
| `Bell Pepper___Bacterial Spot` | Bell Pepper | Diseased | plantdoc | 71 | 4 | 69 | **Included (Supported)** |
| `Grape___Healthy` | Grape | Healthy | plantdoc | 69 | 0 | 69 | **Included (Supported)** |
| `Corn___Gray Leaf Spot` | Corn | Diseased | plantdoc | 66 | 0 | 66 | **Included (Supported)** |
| `Soybean___Healthy` | Soybean | Healthy | plantdoc | 65 | 0 | 65 | **Included (Supported)** |
| `Grape___Black Rot` | Grape | Diseased | plantdoc | 64 | 0 | 64 | **Included (Supported)** |
| `Tomato___Healthy` | Tomato | Healthy | plantdoc | 63 | 0 | 63 | **Included (Supported)** |
| `Bell Pepper___Healthy` | Bell Pepper | Healthy | plantdoc | 61 | 0 | 61 | **Included (Supported)** |
| `Cherry___Healthy` | Cherry | Healthy | plantdoc | 57 | 0 | 57 | **Excluded (Rare Class)** |
| `Tomato___Mosaic Virus` | Tomato | Diseased | plantdoc | 54 | 0 | 54 | **Excluded (Rare Class)** |
| `Rice___Brown Spot` | Rice | Diseased | icar_ogd | 12 | 0 | 12 | **Separated (OOD Scanner)** |
| `Rice___Bacterial Leaf Blight` | Rice | Diseased | icar_ogd | 12 | 0 | 12 | **Separated (OOD Scanner)** |
| `Rice___Leaf Smut` | Rice | Diseased | icar_ogd | 12 | 0 | 12 | **Separated (OOD Scanner)** |
| `Tomato___Two-Spotted Spider Mite` | Tomato | Diseased | plantdoc | 2 | 0 | 2 | **Excluded (Rare Class)** |
