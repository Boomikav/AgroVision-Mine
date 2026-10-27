# AgroVision-Mine: Star Schema Data Dictionary
## Unified Physical Data Warehouse (2,596 Canonical Multimodal Observations)

**Database System:** SQLite 3 (WAL mode enabled, `PRAGMA foreign_keys = ON`)  
**Physical Storage:** `database/agrovision_warehouse.db`  
**Dataset Population:** Exactly 2,596 authentic observations (2,560 PlantDoc + 36 ICAR/OGD Rice)  
**Dimensional Architecture:** Star Schema (4 Dimension Tables, 1 Central Fact Table)

---

### 1. `dim_crop` (Crop Dimension)
Stores normalized botanical and agronomic taxonomy for host crops.
- **Table Type:** Dimension
- **Primary Key:** `crop_key` (INTEGER, Autoincrement)
- **Natural / Business Key:** `crop_code` (VARCHAR(50), Unique, Indexed)
- **Total Unique Records:** 14

| Column Name | Data Type | Nullable | Description / Business Meaning | Valid Range / Example Values |
|:---|:---|:---:|:---|:---|
| `crop_key` | INTEGER | No | Surrogate dimension primary key | 1 .. 14 |
| `crop_code` | VARCHAR(50) | No | Normalized uppercase natural code (Unique) | `RICE`, `TOMATO`, `APPLE`, `CORN`, etc. |
| `crop_name` | VARCHAR(100) | No | Common agronomic name | "Rice", "Tomato", "Apple", "Corn" |
| `botanical_name` | VARCHAR(150) | No | Scientific binomial nomenclature | "Oryza sativa", "Solanum lycopersicum", "Malus domestica" |
| `crop_category` | VARCHAR(50) | No | Broad agricultural grouping for OLAP roll-up | "Cereal", "Horticultural", "Legume" |
| `economic_significance` | VARCHAR(255) | Yes | Macroeconomic significance note | "Primary Global Staple Cereal", "Major Commercial Vegetable" |

---

### 2. `dim_disease` (Disease & Condition Dimension)
Stores authentic plant pathology taxonomy, classifying conditions into causal pathogens.
- **Table Type:** Dimension
- **Primary Key:** `disease_key` (INTEGER, Autoincrement)
- **Natural / Business Key:** `disease_code` (VARCHAR(100), Unique, Indexed)
- **Total Unique Records:** 19

| Column Name | Data Type | Nullable | Description / Business Meaning | Valid Range / Example Values |
|:---|:---|:---:|:---|:---|
| `disease_key` | INTEGER | No | Surrogate dimension primary key | 1 .. 19 |
| `disease_code` | VARCHAR(100) | No | Standardized condition natural key (Unique) | `HEALTHY`, `BACTERIAL_LEAF_BLIGHT`, `BROWN_SPOT` |
| `disease_name` | VARCHAR(150) | No | Standardized pathological condition label | "Healthy", "Bacterial Leaf Blight", "Brown Spot", "Apple Scab" |
| `pathogen_type` | VARCHAR(50) | No | Etiological classification (Drill-Down / Slice) | `Fungal`, `Bacterial`, `Viral`, `Pest`, `None` |
| `causal_agent` | VARCHAR(150) | Yes | Specific microorganism or pest species | "Magnaporthe oryzae", "Xanthomonas oryzae", "Tetranychus urticae" |
| `primary_symptom` | TEXT | Yes | Characteristic macroscopic macroscopic symptom | "Uniform green foliar tissue", "Water-soaked marginal lesions" |

---

### 3. `dim_image` (Physical Image & Provenance Dimension)
Stores physical image characteristics, acquisition provenance, and cryptographic hashes.
- **Table Type:** Dimension
- **Primary Key:** `image_key` (INTEGER, Autoincrement)
- **Natural Keys:** `image_id` (VARCHAR(50), Unique, Indexed), `raw_id` (VARCHAR(50), Unique, Indexed)
- **Total Records:** 2,596

| Column Name | Data Type | Nullable | Description / Business Meaning | Valid Range / Example Values |
|:---|:---|:---:|:---|:---|
| `image_key` | INTEGER | No | Surrogate dimension primary key | 1 .. 2596 |
| `image_id` | VARCHAR(50) | No | Canonical surrogate identifier (Unique, Indexed) | `AGRO_V2_00001` .. `AGRO_V2_02596` |
| `raw_id` | VARCHAR(50) | No | Original source specimen identifier (Unique) | `AGRO_V2_00001`, `RAW_DSC_0365` |
| `dataset_source` | VARCHAR(50) | No | Acquisition source repository | `plantdoc` (2,560) or `icar_ogd` (36) |
| `filename` | VARCHAR(255) | No | Raster filename on disk | "DSC_0365.png", "001.jpg" |
| `file_format` | VARCHAR(20) | No | Image compression format | "JPEG", "PNG" |
| `raw_width` | INTEGER | No | Original raster pixel width | >= 32 |
| `raw_height` | INTEGER | No | Original raster pixel height | >= 32 |
| `raw_channels` | INTEGER | No | Optical channels | 3 (RGB) |
| `raw_size_kb` | FLOAT | No | Storage footprint of raw raster | Kilobytes |
| `processed_width`| INTEGER | No | Standardized normalized width | 256 |
| `processed_height`| INTEGER | No | Standardized normalized height | 256 |
| `processed_size_kb`| FLOAT | No | Standardized raster footprint | Kilobytes |
| `md5_hash` | VARCHAR(64) | No | 128-bit MD5 cryptographic checksum (Lineage) | 32-character hexadecimal string |
| `phash` | VARCHAR(64) | Yes | Perceptual dHash for near-duplicate audit | 16-character hexadecimal string |
| `blur_score` | FLOAT | No | Laplacian variance sharpness metric | Higher indicates sharper edge gradients |
| `is_blurry` | BOOLEAN | No | Quality gate flag (blur threshold < 100.0) | `True` / `False` |
| `original_path` | TEXT | No | Relative path to raw archived image | `data/raw/...` |
| `processed_path`| TEXT | No | Relative path to standardized raster | `data/processed/...` |
| `license` | VARCHAR(100) | No | Dataset governance license | `CC BY 4.0`, `Research/Educational` |

---

### 4. `dim_visual_feature` (Continuous Descriptors Dimension)
Stores all 32 continuous explainable visual descriptors computed for each observation.
- **Table Type:** Dimension
- **Primary Key:** `feature_key` (INTEGER, Autoincrement)
- **Foreign / Lineage Key:** `image_id` (VARCHAR(50), Unique, Indexed)
- **Total Records:** 2,596
- **Feature Groups:**
  1. **Color Moments & Foliar Index (19 continuous features):**
     - First-order RGB means: `rgb_r_mean`, `rgb_g_mean`, `rgb_b_mean` (Range: [0, 255])
     - RGB standard deviations: `rgb_r_std`, `rgb_g_std`, `rgb_b_std` (Range: >= 0)
     - Unit-normalized RGB: `rgb_r_norm`, `rgb_g_norm`, `rgb_b_norm` (Range: [0, 1])
     - HSV means: `hsv_h_mean` (Range: [0, 360)), `hsv_s_mean`, `hsv_v_mean` (Range: [0, 1])
     - HSV standard deviations: `hsv_h_std`, `hsv_s_std`, `hsv_v_std` (Range: >= 0)
     - Unit-normalized HSV: `hsv_h_norm`, `hsv_s_norm`, `hsv_v_norm` (Range: [0, 1])
     - Foliar Vegetative Index: `exg_index_mean` (Excess Green Index = 2G - R - B, Range: [-255, 510])
  2. **GLCM Haralick Textures (7 continuous features):**
     - Haralick contrast: `glcm_contrast` (Range: >= 0)
     - Normalized contrast: `glcm_contrast_norm` (Range: [0, 1])
     - Dissimilarity: `glcm_dissimilarity` (Range: >= 0)
     - Homogeneity / Inverse Difference Moment: `glcm_homogeneity` (Range: [0, 1])
     - Energy / Angular Second Moment: `glcm_energy` (Range: [0, 1])
     - Textural correlation: `glcm_correlation` (Range: [-1, 1])
     - Angular Second Moment: `glcm_asm` (Range: [0, 1])
  3. **Lesion Morphometry & Coverage (6 continuous features):**
     - Lesion area: `contour_area` (Range: >= 0 px²)
     - Lesion perimeter: `contour_perimeter` (Range: >= 0 px)
     - Contour aspect ratio: `contour_aspect_ratio` (Range: > 0)
     - Contour circularity: `contour_circularity` (Range: [0, 1])
     - Contour solidity: `contour_solidity` (Range: [0, 1])
     - Lesion coverage ratio: `lesion_coverage_ratio` (Fraction of total foliar area affected, Range: [0, 1])

---

### 5. `disease_observation_fact` (Central Observation Fact Table)
Represents the central fact table of the data warehouse.
- **Table Type:** Central Fact Table
- **Grain:** Exactly ONE row per validated multimodal image observation.
- **Primary Key:** `observation_key` (INTEGER, Autoincrement)
- **Natural / Observation Key:** `image_id` (VARCHAR(50), Unique, Indexed)
- **Total Records:** Exactly 2,596

| Column Name | Data Type | Nullable | Foreign Key Reference | Description / Analytical Role |
|:---|:---|:---:|:---|:---|
| `observation_key` | INTEGER | No | None (PK) | Surrogate primary key for fact row |
| `image_id` | VARCHAR(50) | No | None (Indexed, Unique) | Observation natural identifier (`AGRO_V2_...`) |
| `crop_key` | INTEGER | No | `dim_crop.crop_key` | FK to host crop dimension |
| `disease_key` | INTEGER | No | `dim_disease.disease_key` | FK to pathological condition dimension |
| `image_key` | INTEGER | No | `dim_image.image_key` | FK to physical image dimension |
| `feature_key` | INTEGER | No | `dim_visual_feature.feature_key` | FK to 32 continuous visual descriptors |
| `dataset_source` | VARCHAR(50) | No | None | Observation provenance (`plantdoc` or `icar_ogd`) |
| `condition_status` | VARCHAR(50) | No | None | Degenerate dimension: `Diseased` or `Healthy` |
| `is_pest` | BOOLEAN | No | None | Binary pest indicator (`True` if pest infestation) |
| `observation_count` | INTEGER | No | None | Additive OLAP Measure: Constant 1 per observation |
| `lesion_severity_score` | FLOAT | No | None | Semi-additive OLAP Measure: 0.0 for Healthy, up to 10.0 for severe |
| `image_sharpness_score` | FLOAT | No | None | Non-additive Measure: Optical Laplacian variance score |
| `lesion_coverage_ratio` | FLOAT | No | None | Non-additive Measure: Surface lesion coverage fraction |
| `texture_contrast_norm` | FLOAT | No | None | Non-additive Measure: Normalized GLCM texture contrast |
| `processing_latency_ms` | FLOAT | No | None | Pipeline telemetry: Feature extraction latency |
| `etl_batch_id` | VARCHAR(50) | No | None | Batch provenance identifier for ETL audit |
| `created_at` | DATETIME | No | None | Warehouse load timestamp (UTC) |

---

### Referential Integrity & Database Constraints
1. **Foreign Key Enforcement:** SQLite `PRAGMA foreign_keys = ON` is actively enforced.
2. **Dimension-First Loading:** Dimensions (`dim_crop`, `dim_disease`, `dim_image`, `dim_visual_feature`) are inserted and flushed prior to fact table loading.
3. **Transactional Guarantees:** ETL load executes inside an atomic SQLite transaction with immediate rollback upon referential violation.
4. **Zero Orphan Invariant:** SQL checks verify 0 orphaned foreign keys across all 2,596 fact rows.
