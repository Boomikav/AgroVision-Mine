# AgroVision-Mine Project File Map

## Project Root
`C:\Users\ajaya\Desktop\Agro`

## Dataset
* **Root Directory:** `data/raw/rice/`
* **Sub-directories & Authentic Files (36 Authentic Field Images):**
  * `data/raw/rice/bacterial_leaf_blight/` (12 images):
    * `DSC_0365.JPG`, `DSC_0366.jpg`, `DSC_0367.JPG`, `DSC_0370.jpg`, `DSC_0372.JPG`, `DSC_0373.JPG`, `DSC_0374.JPG`, `DSC_0375.JPG`, `DSC_0376.JPG`, `DSC_0377.JPG`, `DSC_0378.JPG`, `DSC_0379.JPG`
  * `data/raw/rice/brown_spot/` (12 images):
    * `DSC_0100.jpg`, `DSC_0101.jpg`, `DSC_0104.jpg`, `DSC_0105.jpg`, `DSC_0106.jpg`, `DSC_0107.jpg`, `DSC_0108.jpg`, `DSC_0109.jpg`, `DSC_0110.jpg`, `DSC_0111.jpg`, `DSC_0112.jpg`, `DSC_0113.jpg`
  * `data/raw/rice/leaf_smut/` (12 images):
    * `DSC_0293.JPG`, `DSC_0308.JPG`, `DSC_0309.JPG`, `DSC_0310.JPG`, `DSC_0312.JPG`, `DSC_0313.JPG`, `DSC_0314.JPG`, `DSC_0315.jpg`, `DSC_0316.JPG`, `DSC_0317.JPG`, `DSC_0318.JPG`, `DSC_0319.jpg`
* **Host Crop:** Rice (*Oryza sativa*), Category: Cereal.
* **Processed Output Directory:** `data/processed/rice/{disease}/proc_{filename}.png` (36 standardized images, 256×256×3 RGB).
* **Metadata Manifests:** `data/processed/cleaned_metadata.csv`, `data/reports/source_inventory.json`.

## Diagnostic Tests
* **Directory:** `data/diagnostic_tests/` (strictly isolated from research observations)
* **Files:**
  * `corrupted_header_test.jpg` (53 bytes) -> Tests truncated header detection (`CORRUPTED`).
  * `duplicate_exact_test.jpg` (467,109 bytes) -> Tests MD5 duplicate hash collision detection (`EXACT_HASH`).
  * `invalid_dim_tiny.jpg` (632 bytes, 16×16 px) -> Tests sub-threshold dimension rejection (`INVALID_DIM`).
  * `unsupported_extension.txt` (46 bytes) -> Tests MIME/format rejection (`UNSUPPORTED_FORMAT`).

## Preprocessing
* `src/preprocessing/validator.py`:
  * `ImageValidator.validate_file()`: Inspects file existence, MIME extension, uncorrupted header integrity, and dimension boundaries.
* `src/preprocessing/duplicate_detector.py`:
  * `DuplicateDetector.check_duplicate()`: Computes MD5 hash for exact matching and perceptual hash (pHash) with Hamming distance thresholding for near-duplicates.
* `src/preprocessing/preprocessor.py`:
  * `ImagePreprocessor.process_image()`: Standardizes valid images to 256×256×3 RGB via Lanczos interpolation, computes Laplacian blur scores, and saves to `data/processed/`.

## Feature Extraction
* `src/feature_extraction/color_features.py`:
  * `extract_color_features()`: Computes RGB channel means, standard deviations, normalized chromaticities, HSV moments, Excess Green Index (ExG), and dominant color tone.
* `src/feature_extraction/texture_features.py`:
  * `extract_texture_features()`: Computes Gray-Level Co-occurrence Matrix (GLCM) Haralick descriptors (contrast, dissimilarity, homogeneity, energy, correlation, angular second moment).
* `src/feature_extraction/shape_features.py`:
  * `extract_shape_features()`: Otsu thresholding, foliar contour area, perimeter, aspect ratio, circularity, solidity, and lesion coverage ratio.
* `src/feature_extraction/pipeline.py`:
  * `FeatureExtractionPipeline.process_dataset()`: Extracts 34 visual descriptors + 10 metadata fields for each image observation.

## Feature Store
* **File:** `data/features/image_features.csv`
* **Dimensions:** 36 rows × 44 columns.
* **10 Metadata / Lineage Columns:** `condition_label`, `crop_label`, `disease_label`, `filename`, `image_id`, `is_pest`, `md5_hash`, `pest_label`, `processed_path`, `raw_path`.
* **34 Explainable Visual Descriptors:** `rgb_r_mean`, `rgb_g_mean`, `rgb_b_mean`, `rgb_r_std`, `rgb_g_std`, `rgb_b_std`, `rgb_r_norm`, `rgb_g_norm`, `rgb_b_norm`, `hsv_h_mean`, `hsv_s_mean`, `hsv_v_mean`, `hsv_h_std`, `hsv_s_std`, `hsv_v_std`, `hsv_h_norm`, `hsv_s_norm`, `hsv_v_norm`, `exg_index_mean`, `dominant_color_tone`, `glcm_contrast`, `glcm_contrast_norm`, `glcm_dissimilarity`, `glcm_homogeneity`, `glcm_energy`, `glcm_correlation`, `glcm_asm`, `has_valid_contour`, `contour_area`, `contour_perimeter`, `contour_aspect_ratio`, `contour_circularity`, `contour_solidity`, `lesion_coverage_ratio`.

## Database
* **Database Path:** `database/agrovision_warehouse.db`
* **Database Engine:** SQLite 3 (PostgreSQL dialect compatible via SQLAlchemy).
* **Database Name:** `agrovision_dw` / `agrovision_warehouse.db`.
* **Connection Layer:** `src/warehouse/connection.py` (enforces `PRAGMA foreign_keys = ON` on connection).

## Warehouse Schema
* `src/warehouse/models.py`: Declarative SQLAlchemy models:
  * `DimCrop` -> Table `dim_crop` (PK: `crop_key`)
  * `DimDisease` -> Table `dim_disease` (PK: `disease_key`)
  * `DimImage` -> Table `dim_image` (PK: `image_key`)
  * `DimVisualFeature` -> Table `dim_visual_feature` (PK: `feature_key`)
  * `DiseaseObservationFact` -> Table `disease_observation_fact` (PK: `observation_key`, FKs: `crop_key`, `disease_key`, `image_key`, `feature_key`)
* `src/warehouse/schema_manager.py`: `SchemaManager.initialize_schema()`, `get_warehouse_health()`.
* `database/schema/star_schema.sql`: ANSI SQL DDL script defining tables, foreign keys with `ON DELETE RESTRICT`, and compound performance indices.
* `database/seeds/seed_dimensions.py`: `seed_reference_dimensions()` (idempotently populates `dim_crop` and `dim_disease`).

## ETL
* `src/etl/extract.py`: `Extractor.extract_all()`: Ingests raw images, cleaned metadata, and extracted features.
* `src/etl/transform.py`: `Transformer.transform()`: Standardizes botanical crop taxonomy, disease classifications, and generates surrogate keys.
* `src/etl/load.py`: `Loader.load_dimensions_and_facts()`: Loads dimension tables first, fact table second, enforcing referential integrity and duplicate prevention.
* `src/etl/pipeline.py`: `ETLPipeline.run()`: Orchestrates end-to-end execution and compiles audit statistics.
* `scripts/verify_etl.py`: `verify_etl_integrity()`: Audits ETL repeatability and idempotency.

## OLAP
* `src/olap/engine.py`: `OLAPEngine` class implementing:
  * `rollup()`: Observation -> Crop -> Crop Category (`GROUP BY c.crop_category`).
  * `true_drilldown()`: Pathogen Type -> Disease Name (`GROUP BY d.pathogen_type, d.disease_name`).
  * `diagnostic_drilldown()`: Diagnostic Drill-Across (`GROUP BY c.crop_category, c.crop_name, d.disease_name, d.pathogen_type, vf.dominant_color_tone`).
  * `slice_by_crop(crop_name)`: 2D sub-plane slice (`WHERE LOWER(c.crop_name) = LOWER(:crop_name)`).
  * `slice_by_pathogen(pathogen_type)`: Slices by pathogen kingdom.
  * `dice(selected_crops, selected_pathogens, min_contrast)`: Multi-dimensional sub-cube.
  * `pivot(measure)`: Cross-tabulation using ANSI SQL conditional aggregation (`SUM(CASE WHEN...)`).

## Dashboard
* `dashboard/app.py`: Streamlit multi-tab presentation layer.
  * Launch command: `streamlit run dashboard/app.py` or `python run.py --stage dashboard`.
  * Tabs: 1. Overview, 2. Dataset Explorer, 3. Preprocessing, 4. Warehouse, 5. OLAP Analytics.
  * Dynamic KPIs: Directly queries database row counts, `source_inventory.json`, and `image_features.csv`.

## Tests
* `tests/` directory: 12 test files containing 56 automated test cases (100% passing):
  * `test_config.py` (3 tests)
  * `test_duplicates.py` (3 tests)
  * `test_etl_phase5.py` (5 tests)
  * `test_feature_extraction_phase3.py` (5 tests)
  * `test_features.py` (4 tests)
  * `test_olap.py` (6 tests)
  * `test_olap_real_warehouse.py` (7 tests)
  * `test_preprocessing_phase2.py` (6 tests)
  * `test_profiler.py` (2 tests)
  * `test_validation.py` (5 tests)
  * `test_warehouse.py` (3 tests)
  * `test_warehouse_phase4.py` (7 tests)

## Documentation
* `README.md`: Project summary, architecture, pipeline execution guide.
* `DATASET_SETUP.md`: Ground-truth ICAR dataset discovery and setup instructions.
* `docs/architecture.md`: System topology, multimodal warehouse design, and pipeline layers.
* `docs/dataset_documentation.md`: Botanical taxonomy, source provenance, and disease characteristics.
* `docs/preprocessing.md`: Quality gate validation logic and normalization pipeline.
* `docs/feature_extraction.md`: Mathematical descriptions of the 34 visual descriptors.
* `docs/star_schema.md`: Kimball star schema, fact grain, PK/FK constraints, and indices.
* `docs/warehouse_design.md`: Storage architecture, surrogate key mapping, and schema governance.
* `docs/etl.md`: ETL architecture, transaction safety, and idempotency guarantees.
* `docs/olap.md`: Formally verified OLAP operations, hierarchies, queries, and outputs.
* `docs/review1_checklist.md`: 24-point Review 1 audit verification matrix.

## Important Verified Counts
* **Authentic Raw Observations:** 36 images (12 Bacterial Leaf Blight, 12 Brown Spot, 12 Leaf Smut).
* **Controlled Diagnostic Artifacts:** 4 test files in `data/diagnostic_tests/` (100% rejected).
* **Standardized Images:** 36 images (256×256×3 RGB).
* **Feature Store Columns:** 44 columns (34 explainable visual descriptors + 10 metadata fields).
* **Warehouse Table Row Counts:**
  * `dim_crop`: 1 row (Rice / Cereal).
  * `dim_disease`: 4 rows (3 active + `HEALTHY` control baseline).
  * `dim_image`: 36 rows.
  * `dim_visual_feature`: 36 rows.
  * `disease_observation_fact`: 36 rows.
* **ETL Idempotency:** Run 1 = 36 facts inserted; Run 2 = 0 inserted, 36 duplicates skipped.
* **Test Suite Result:** 56 / 56 tests passed (100% pass rate).
