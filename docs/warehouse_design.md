# Multimodal Data Warehouse Architecture & Dimensional Design

## 1. Architectural Philosophy & Academic Justification

Standard computer vision projects typically store images in flat directory structures with loose CSV files or labels. While sufficient for training black-box neural networks, this architecture fails for agricultural decision support, epidemiological surveillance, and scientific pattern discovery due to three fundamental limitations:

1. **Absence of Relational Rigor:** Disconnected image files provide no relational integrity guarantees between botanical taxonomy, pathology diagnoses, cryptographic hashes, and extracted visual descriptors.
2. **Inability to Perform Multidimensional OLAP Analysis:** Flat files cannot answer aggregate analytical questions across hierarchical levels (e.g., *"What is the mean lesion contrast and coverage ratio of bacterial blights compared to fungal diseases in cereal crops?"*).
3. **No Explainable Lineage or Reproducibility:** Without surrogate key mappings and batch audit dimensions, there is no reproducible trace linking an extracted texture feature back to the exact physical image file and preprocessing quality audit.

**AgroVision-Mine** resolves these challenges by formalizing a **Multimodal Data Warehouse** modeled after Ralph Kimball's dimensional modeling methodology. The warehouse implements a **Star Schema** centered on physical agricultural observations, integrating image metadata, classical visual features, and botanical/pathological taxonomies.

---

## 2. Fact Table Specification

### `DiseaseObservation_Fact`

#### 2.1 Grain of the Fact Table
> **Grain Definition:** Exactly **ONE record per validated, preprocessed multimodal agricultural image observation**.

Each row represents an individual physical plant specimen photographed, validated through preprocessing quality gates ($256 \times 256 \times 3$), analyzed through explainable feature extraction (RGB/HSV moments, Haralick textures, morphometric shape descriptors), and mapped to its agronomic classification.

#### 2.2 Primary and Foreign Keys
- **Primary Key:** `observation_key` (INTEGER PRIMARY KEY AUTOINCREMENT) — Surrogate key ensuring physical independence from raw source filenames.
- **Foreign Keys:**
  - `crop_key` $\rightarrow$ `dim_crop.crop_key` (`ON DELETE RESTRICT`)
  - `disease_key` $\rightarrow$ `dim_disease.disease_key` (`ON DELETE RESTRICT`)
  - `image_key` $\rightarrow$ `dim_image.image_key` (`UNIQUE`, `ON DELETE RESTRICT`)
  - `feature_key` $\rightarrow$ `dim_visual_feature.feature_key` (`UNIQUE`, `ON DELETE RESTRICT`)

#### 2.3 Measures Classification
The fact table measures combine physical optical characteristics, disease manifestation metrics, and computational pipeline statistics:

| Measure | SQL Column | Mathematical Type | Formula / Origin |
|---|---|---|---|
| **Observation Count** | `observation_count` | Additive | Constant $1$ per row; serves as unit basis for frequency aggregation |
| **Lesion Severity Score** | `lesion_severity_score` | Semi-Additive | Continuous $[0.0, 10.0]$ estimated from lesion coverage ratio and color deviation |
| **Image Sharpness Score** | `image_sharpness_score` | Semi-Additive | Continuous $\sigma^2_{\Delta}$ (Laplacian variance blur score) |
| **Lesion Coverage Ratio** | `lesion_coverage_ratio` | Semi-Additive | Continuous $[0.0, 1.0]$: $\frac{\text{Lesion Area}}{\text{Total Image Area}}$ |
| **Texture Contrast (Norm)** | `texture_contrast_norm` | Semi-Additive | Continuous $[0.0, 1.0]$: Normalized GLCM contrast $\frac{\sum |i-j|^2 P_{i,j}}{(N_g - 1)^2}$ |
| **Processing Latency** | `processing_latency_ms` | Semi-Additive | Execution duration in milliseconds for image preprocessing and feature extraction |

#### 2.4 Audit & Lineage Attributes
- `etl_batch_id` (VARCHAR(50)): Degenerate identifier tracking the specific ETL execution batch for traceability.
- `created_at` (TIMESTAMP): Physical database insertion timestamp.

---

## 3. Dimension Support Analysis & Ground-Truth Verification

A strict academic guideline of this research is the **Anti-Fabrication Mandate**: every dimension and attribute must be supported by ground-truth evidence discovered during dataset profiling and preprocessing. Unsupported or synthetic attributes are strictly excluded.

### 3.1 Supported Dimensions (Included)

#### 1. `Dim_Crop` (Host Plant Dimension)
- **Academic Purpose:** Captures host plant taxonomy and agronomic classification.
- **Ground-Truth Source:** Ingested ICAR / agricultural research dataset containing Rice specimens.
- **Hierarchy:** Crop Name $\rightarrow$ Crop Category (e.g., Rice $\rightarrow$ Cereal).
- **Attributes:**
  - `crop_key` (PK, INTEGER)
  - `crop_code` (Natural Key, VARCHAR(50), UNIQUE)
  - `crop_name` (VARCHAR(100), e.g., 'Rice')
  - `botanical_name` (VARCHAR(150), e.g., '*Oryza sativa*')
  - `crop_category` (VARCHAR(50), e.g., 'Cereal')
  - `economic_significance` (VARCHAR(100))

#### 2. `Dim_Disease` (Pathology Dimension)
- **Academic Purpose:** Classifies pathological condition, pathogen kingdom/type, and foliar symptoms.
- **Ground-Truth Source:** Authentic diagnoses from research dataset:
  - *Bacterial Leaf Blight* (*Xanthomonas oryzae pv. oryzae*) — Bacterial (12 facts)
  - *Brown Spot* (*Bipolaris oryzae*) — Fungal (12 facts)
  - *Leaf Smut* (*Entyloma oryzae*) — Fungal (12 facts)
  - *Healthy Foliage* — Unpopulated control baseline catalog domain (0 facts)
- **Taxonomy Reference Policy:** The current ICAR research collection contains pathological foliar specimens only; therefore no healthy observations are loaded into the fact table. `HEALTHY` is maintained in `dim_disease` as an unpopulated control reference value / baseline domain.
- **Hierarchy:** Specific Disease $\rightarrow$ Pathogen Type (e.g., Bacterial Leaf Blight $\rightarrow$ Bacterial; Brown Spot $\rightarrow$ Fungal).
- **Attributes:**
  - `disease_key` (PK, INTEGER)
  - `disease_code` (Natural Key, VARCHAR(50), UNIQUE)
  - `disease_name` (VARCHAR(150))
  - `pathogen_type` (VARCHAR(50), 'Bacterial', 'Fungal', 'None')
  - `causal_agent` (VARCHAR(150))
  - `primary_symptom` (VARCHAR(200))

#### 3. `Dim_Image` (Physical & Technical Image Dimension)
- **Academic Purpose:** Preserves optical parameters, standardized geometry, cryptographic integrity, and disk references.
- **Ground-Truth Source:** Image headers, EXIF/PIL metadata, and MD5/pHash digests computed in Phase 2.
- **Attributes:**
  - `image_key` (PK, INTEGER)
  - `raw_id` (VARCHAR(50), UNIQUE, e.g., 'RAW_000002')
  - `filename` (VARCHAR(255))
  - `file_format` (VARCHAR(20), 'JPEG', 'PNG')
  - `raw_width`, `raw_height`, `raw_channels`, `raw_size_kb`
  - `processed_width` ($256$), `processed_height` ($256$), `processed_size_kb`
  - `md5_hash` (VARCHAR(64), UNIQUE)
  - `phash` (VARCHAR(32))
  - `blur_score` (FLOAT), `is_blurry` (BOOLEAN)
  - `original_path` (TEXT), `processed_path` (TEXT)

#### 4. `Dim_VisualFeature` (Visual Pattern Descriptor Dimension)
- **Academic Purpose:** Stores explainable color moments, Haralick texture descriptors, and morphometric shape contours extracted in Phase 3.
- **Ground-Truth Source:** Deterministic computation via NumPy, SciPy, and Pillow on standardized images.
- **Attributes (34 Explainable Descriptors across a 44-Column Feature Dataset):**
  - `feature_key` (PK, INTEGER)
  - `image_filename` (VARCHAR(255), UNIQUE)
  - **Color Descriptors (17):** `rgb_r_mean`, `rgb_g_mean`, `rgb_b_mean`, `rgb_r_std`, `rgb_g_std`, `rgb_b_std`, `rgb_r_norm`, `rgb_g_norm`, `rgb_b_norm`, `hsv_h_mean`, `hsv_s_mean`, `hsv_v_mean`, `hsv_h_norm`, `hsv_s_norm`, `hsv_v_norm`, `exg_index_mean`, `dominant_color_tone`
  - **GLCM Texture Descriptors (7):** `glcm_contrast`, `glcm_contrast_norm`, `glcm_dissimilarity`, `glcm_homogeneity`, `glcm_energy`, `glcm_correlation`, `glcm_asm`
  - **Morphometric Shape Descriptors (7):** `has_valid_contour`, `contour_area`, `contour_perimeter`, `contour_aspect_ratio`, `contour_circularity`, `contour_solidity`, `lesion_coverage_ratio`
  - *(Note: Stored in an analytical dataset with 10 lineage/metadata identifier columns for end-to-end traceability).*


---

### 3.2 Unsupported Dimensions (Explicitly Excluded)

The following candidate dimensions were evaluated and deliberately **excluded** to prevent data fabrication:

1. **`Dim_Pest` (EXCLUDED):**
   - *Rationale:* The ground-truth dataset consists solely of microbial foliar pathologies (bacterial and fungal). There are zero insect or invertebrate pest occurrences. Creating a dummy pest record (e.g., 'None') as a permanent dimension distorts the schema topology and misrepresents the experimental data.
2. **`Dim_Time` (EXCLUDED):**
   - *Rationale:* The raw image EXIF tags do not contain reliable historical field-capture dates or seasonal timestamps. Fabricating harvest years or survey dates would violate scientific research ethics. Temporal auditing is captured strictly via `created_at` and `etl_batch_id` on the fact table.
3. **`Dim_Geography` (EXCLUDED):**
   - *Rationale:* Source files do not provide geocoordinates (GPS latitude/longitude) or validated administrative district tags. Synthesizing geographical boundaries is strictly prohibited.

---

## 4. Physical Schema Implementation & Constraints

### 4.1 Schema DDL & Dialect Compatibility
The complete DDL is maintained in `database/schema/star_schema.sql` and mirrored in SQLAlchemy 2.0 ORM models (`src/warehouse/models.py`). The schema is ANSI SQL-compliant and validated on both:
- **Local Embedded Mode:** SQLite 3 (`database/agrovision_warehouse.db`)
- **Enterprise Server Mode:** PostgreSQL 15+

### 4.2 Constraints & Referential Integrity
- **Surrogate Keys:** All tables utilize surrogate auto-incrementing integer primary keys.
- **Unique Constraints:** Enforced on natural keys (`crop_code`, `disease_code`), cryptographic digests (`md5_hash`), physical identifiers (`raw_id`), and 1:1 fact relationships (`image_key`, `feature_key`).
- **Referential Integrity:** Foreign keys on `disease_observation_fact` use `ON DELETE RESTRICT` to prevent orphan observations.

### 4.3 Query Acceleration Indices
To ensure high OLAP query throughput, indexes are defined on all foreign keys, dimensional hierarchies, and frequent slice/dice predicates:
- `idx_dim_crop_category` on `dim_crop(crop_category)`
- `idx_dim_disease_pathogen` on `dim_disease(pathogen_type)`
- `idx_dim_image_hash` on `dim_image(md5_hash)`
- `idx_dim_feature_tone` on `dim_visual_feature(dominant_color_tone)`
- `idx_dim_feature_contrast` on `dim_visual_feature(glcm_contrast_norm)`
- `idx_fact_crop_disease` compound index on `disease_observation_fact(crop_key, disease_key)`
- `idx_fact_batch` on `disease_observation_fact(etl_batch_id)`

---

## 5. Seeding & Load Mechanisms

### 5.1 Idempotent Reference Seeding (`database/seeds/seed_dimensions.py`)
Pre-populates the reference dimension tables (`dim_crop` and `dim_disease`) with verified botanical and pathological taxonomies. The script queries existing natural keys (`crop_code`, `disease_code`) and only inserts missing records, guaranteeing idempotent re-execution.

### 5.2 Transactional ETL Load (`src/etl/load.py`)
1. Ingests preprocessed metadata and extracted visual feature CSVs.
2. Resolves surrogate foreign keys from natural keys via in-memory dimension key maps.
3. Inserts facts into `disease_observation_fact` within an atomic database transaction.
4. If any foreign key is unresolvable or an anomaly occurs, the transaction rolls back cleanly.
