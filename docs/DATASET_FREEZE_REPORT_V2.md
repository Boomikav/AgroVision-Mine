# AgroVision-Mine — Dataset Acceptance Gate & Freeze Report (v2)

**Document ID:** `AGRO-FREEZE-V2-20261012`  
**Evaluation Date:** October 12, 2026  
**Auditor:** Lead Data Engineer & Research-Quality Auditor  
**Course:** Data Warehousing & Data Mining (CSI3010)  
**Project:** AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence  
**Overall Verdict:** **PASS** (Ready for Phase 6: Review 2 Pattern Mining)

---

## 1. Executive Summary

This report establishes the formal audit and freezing of the expanded, multi-crop canonical research dataset (`canonical_v2`) for the AgroVision-Mine project. The previous Review 1 proof-of-concept baseline was restricted to 36 rice leaf images across three disease classes. In accordance with Phase 1–5 directives, the dataset has been systematically expanded, audited, deduplicated, standardized, and featurized without fabricating data or breaking Review 1 artifacts.

| Metric | Review 1 Baseline | Phase 1 Target | Canonical v2 Frozen | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Unique Images** | 36 | $\ge 2,000$ | **2,596** | **Target Exceeded** |
| **Crop Species** | 1 (Rice) | $\ge 5$ | **14** | **Target Exceeded** |
| **Disease Classes** | 3 | $\ge 10$ | **19 pathologies + 1 healthy** | **Target Exceeded** |
| **Image Resolution** | $256 \times 256 \times 3$ | $256 \times 256 \times 3$ | **$256 \times 256 \times 3$ RGB** | **100% Compliant** |
| **Feature Dimensionality** | 34 visual + 10 meta (44) | 44 columns | **44 columns (0 missing values)** | **100% Compliant** |
| **Source Provenance** | 100% (ICAR/OGD) | 100% Traceable | **100% Traceable** | **Fully Audited** |
| **Licensing** | GODL-India | Documented Open Access | **GODL-India & CC BY 4.0** | **Fully Verified** |

---

## 2. Dataset Distribution & Composition

### 2.1 Source Registry
The canonical dataset integrates two authentic, empirical image repositories:
1. **ICAR/OGD India Crop Pathology Subset (`icar_ogd`)**:
   - Count: 36 images (1.39%)
   - Provenance: Government of India Open Government Data Platform (`https://data.gov.in/catalogs`) / ICAR-CRIDA / ICAR-IIRR
   - License: Government Open Data License - India (GODL-India)
   - Imaging Domain: Macro in-field pathology survey photography.
2. **PlantDoc In-Field Agricultural Benchmark (`plantdoc`)**:
   - Count: 2,560 images (98.61%)
   - Provenance: Indian Institute of Technology (IIT) Kharagpur & ACM CoDS-COMAD 2020 (`https://github.com/pratikkayal/PlantDoc-Dataset`)
   - License: Creative Commons Attribution 4.0 International (CC BY 4.0)
   - Imaging Domain: Real-world in-field smartphone and handheld camera photographs with natural complex backgrounds.

### 2.2 Crop Species Representation (14 Crops)
| Crop | Retained Images | Percentage | Role / Commodity Group |
| :--- | :--- | :--- | :--- |
| **Tomato** (*Solanum lycopersicum*) | 743 | 28.62% | Solanaceous Vegetable |
| **Corn / Maize** (*Zea mays*) | 372 | 14.33% | Cereal Staple |
| **Apple** (*Malus domestica*) | 272 | 10.48% | Temperate Fruit |
| **Potato** (*Solanum tuberosum*) | 216 | 8.32% | Tuber Staple |
| **Grape** (*Vitis vinifera*) | 133 | 5.12% | Vine Horticultural |
| **Bell Pepper** (*Capsicum annuum*) | 132 | 5.08% | Solanaceous Vegetable |
| **Squash** (*Cucurbita*) | 130 | 5.01% | Cucurbitaceous Crop |
| **Raspberry** (*Rubus idaeus*) | 119 | 4.58% | Berry / Cane Fruit |
| **Blueberry** (*Vaccinium corymbosum*) | 114 | 4.39% | Berry / Ericaceous Fruit |
| **Peach** (*Prunus persica*) | 111 | 4.28% | Stone Fruit |
| **Strawberry** (*Fragaria ananassa*) | 96 | 3.70% | Berry Fruit |
| **Soybean** (*Glycine max*) | 65 | 2.50% | Legume / Oilseed |
| **Cherry** (*Prunus avium*) | 57 | 2.20% | Stone Fruit |
| **Rice** (*Oryza sativa*) | 36 | 1.39% | Cereal Staple (Baseline) |
| **Total** | **2,596** | **100.0%** | **14 Distinct Species** |

### 2.3 Health Status & Pathogen Taxonomy
- **Health Status:**
  - **Diseased:** 1,750 images (67.41%)
  - **Healthy:** 846 images (32.59%)
- **Pathogen Breakdown:**
  - **Fungal Pathologies:** 1,426 images (54.93%) — 11 distinct classes
  - **Healthy Baseline (None):** 846 images (32.59%) — 13 crops
  - **Bacterial Pathologies:** 193 images (7.43%) — Bacterial Spot & Bacterial Leaf Blight
  - **Viral Pathologies:** 129 images (4.97%) — Tomato Yellow Leaf Curl Virus & Mosaic Virus
  - **Pest Damage:** 2 images (0.08%) — Two-Spotted Spider Mite

### 2.4 Disease Pathology Breakdown (20 Classes)
| Canonical Disease Name | Images | Pathogen Type | Crops Affected |
| :--- | :--- | :--- | :--- |
| **Healthy** | 846 | None | Apple, Blueberry, Cherry, Corn, Grape, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato |
| **Late Blight** | 214 | Fungal (*Phytophthora*) | Potato, Tomato |
| **Early Blight** | 201 | Fungal (*Alternaria*) | Potato, Tomato |
| **Northern Leaf Blight** | 190 | Fungal (*Exserohilum*) | Corn |
| **Bacterial Spot** | 181 | Bacterial (*Xanthomonas*) | Bell Pepper, Tomato |
| **Septoria Leaf Spot** | 149 | Fungal (*Septoria*) | Tomato |
| **Powdery Mildew** | 130 | Fungal (*Podosphaera*) | Squash, Cherry |
| **Common Rust** | 116 | Fungal (*Puccinia*) | Corn |
| **Apple Scab** | 93 | Fungal (*Venturia*) | Apple |
| **Leaf Mold** | 91 | Fungal (*Passalora*) | Tomato |
| **Cedar Apple Rust** | 88 | Fungal (*Gymnosporangium*) | Apple |
| **Yellow Leaf Curl Virus** | 75 | Viral (*Begomovirus*) | Tomato |
| **Gray Leaf Spot** | 66 | Fungal (*Cercospora*) | Corn |
| **Black Rot** | 64 | Fungal (*Guignardia / Botryosphaeria*) | Apple, Grape |
| **Mosaic Virus** | 54 | Viral (*Tobamovirus*) | Tomato |
| **Bacterial Leaf Blight** | 12 | Bacterial (*Xanthomonas oryzae*) | Rice |
| **Brown Spot** | 12 | Fungal (*Bipolaris oryzae*) | Rice |
| **Leaf Smut** | 12 | Fungal (*Entyloma oryzae*) | Rice |
| **Two-Spotted Spider Mite**| 2 | Pest (*Tetranychus urticae*) | Tomato |
| **Total** | **2,596** | | |

---

## 3. Data Quality, Deduplication & Validation Audit

### 3.1 Raw Image Integrity
- Raw images evaluated: **2,608 candidate files**
- Corrupt/unreadable files: **0**
- Mean raw resolution: $1086.2 \times 908.0$ pixels (spanning from $300 \times 200$ up to $4000 \times 3000$)
- Color format: All raw images successfully decoded and converted to standard 3-channel RGB.

### 3.2 Deduplication Audit
- Exact MD5 duplicates identified: **12 duplicate files**
- Rejection policy: Every exact MD5 collision was recorded in `data/reports/dataset_exclusion_audit_v2.json` and excluded from the canonical dataset. Only the primary unique instance was retained.
- Perceptual Hash (dHash) Audit: 2,564 unique perceptual hashes detected across 2,596 images. Near-duplicate groups represent minor variations or different crops of identical in-field specimens; these are tracked with lineage keys to prevent test/validation leakage.

### 3.3 Standardization Pipeline
- Target Resolution: **$256 \times 256 \times 3$ RGB**
- Resampling Filter: High-quality Lanczos interpolation (`PIL.Image.Resampling.LANCZOS`).
- Destination: `data/processed_v2/` with deterministic surrogate identifiers (`AGRO_V2_00001` through `AGRO_V2_02596`).
- Review 1 Isolation: The original `data/processed/` directory (36 Rice images) remains strictly untouched.

---

## 4. Feature Extraction & Feature Store Verification

### 4.1 Feature Extraction Pipeline
- Module: `src.feature_extraction.pipeline.ClassicalFeatureExtractor`
- Consistency: Exact mathematical equivalence with Review 1 methodology.
- Dimensionality: **44 columns** total:
  - 10 Identification & Metadata attributes (`image_id`, `filename`, `crop`, `disease`, `pathogen_type`, `health_status`, `severity`, `source_dataset`, `original_width`, `original_height`).
  - 14 Color Moments & Histogram Descriptors (RGB/HSV channel means, standard deviations, skewness, color variance).
  - 14 Gray-Level Co-occurrence Matrix (GLCM) Texture Descriptors (Energy, Contrast, Homogeneity, Correlation across 4 orientations + mean/std).
  - 6 Morphological & Edge Shape Descriptors (Canny edge density, contour count, average perimeter, area ratio, eccentricity, solidity).

### 4.2 Quality Audit of Feature Store (`image_features_v2.csv`)
- Row count: **2,596**
- Column count: **44**
- Missing / Null values: **0**
- Infinite / NaN values: **0**
- Degenerate features (zero variance): **None**; all 34 numeric visual features exhibit non-zero variance.
- One-to-one record alignment: 100% matching join between `canonical_dataset_v2.csv` and `image_features_v2.csv` on `image_id`.

---

## 5. File Inventory & Cryptographic Checksums

All frozen artifacts are recorded with SHA-256 hashes for immutability:

| Frozen File Path | Description | SHA-256 Hash |
| :--- | :--- | :--- |
| `data/manifests/canonical_dataset_v2.csv` | Canonical image manifest (2,596 rows) | `c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8` |
| `data/features/image_features_v2.csv` | Extracted visual features (2,596 rows × 44 cols) | `f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1` |
| `data/manifests/class_mapping_v2.csv` | Source label to canonical taxonomy mapping | `c8be03922d68c02b2c932991539fc984baeeaa5bd493d4e3782e200336a09db3` |
| `data/manifests/source_registry_v2.csv` | Official source lineage, licenses, citations | `d2d44fe50f76ef1dbcdae96b4bc8f8cb7690dec7fc49925eb9adb12874254108` |
| `data/reports/dataset_acquisition_v2.json` | Acquisition report | System-generated JSON |
| `data/reports/dataset_quality_v2.json` | Quality & resolution audit report | System-generated JSON |
| `data/reports/dataset_class_distribution_v2.json` | Crop, disease, pathogen distribution report | System-generated JSON |
| `data/reports/dataset_duplicate_audit_v2.json` | Hash collision & duplicate report | System-generated JSON |
| `data/reports/dataset_exclusion_audit_v2.json` | Machine-readable exclusion ledger (12 rows) | System-generated JSON |
| `docs/dataset_documentation_v2.md` | Detailed research dataset documentation | Complete Markdown documentation |

---

## 6. Analytical Limitations & Known Caveats

1. **Class Imbalance:** Tomato represents 28.6% of the dataset, while Rice represents 1.4% and Two-Spotted Spider Mite contains only 2 images. Data mining algorithms (clustering and association rules) must be analyzed with awareness of majority-class bias.
2. **Domain Background Variations:** PlantDoc images were captured in outdoor agricultural settings with natural soils, weed undergrowth, and hand holders, whereas ICAR images were captured in dedicated field pathology surveys. Unsupervised clustering may cluster background lighting/color distributions as well as lesion features.
3. **Pest Underrepresentation:** Only 2 images correspond to insect pests; pest-specific pattern mining is unfeasible and will be handled within general pathology groupings.

---

## 7. Dataset Acceptance Gate Decision

### Verification Matrix
- [x] **Traceability:** Every image maps to an official public repository and license.
- [x] **Authenticity:** Zero synthetic, augmented, or manufactured images.
- [x] **Volume Target:** 2,596 verified images $\ge 2,000$ target ($\mathbf{+29.8\%}$).
- [x] **Taxonomy Breadth:** 14 crops $\ge 5$ target; 19 disease classes $\ge 10$ target.
- [x] **Integrity:** Zero unreadable images; 12 exact duplicates excluded and logged.
- [x] **Feature Store Completeness:** Zero nulls or NaNs across 2,596 rows × 44 columns.
- [x] **Baseline Preservation:** Review 1 baseline (36 rice images, database, reports, 56 tests) fully intact.

### Final Gate Verdict: **PASS**

The dataset gate has passed all requirements. The dataset is officially **FROZEN**. We are cleared to proceed immediately to **Review 2: Phases 6–9**.
