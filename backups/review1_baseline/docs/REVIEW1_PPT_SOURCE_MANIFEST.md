# AgroVision-Mine: Review 1 PPT Source Manifest

This document provides a verifiable 1:1 mapping between each slide in the Review 1 PowerPoint presentation (`AgroVision-Mine_Review1_Final_Presentation.pptx`) and its physical implementation source in the AgroVision-Mine codebase.

---

### Slide 1: Title & Review Scope
* **Presentation Slide:** Slide 1 (`TITLE2` layout)
* **Underlying Implementation Sources:**
  * Project Name & Scope: `config/config.yaml` (`project.name`, `project.review_stage`)
  * Verified Scope Counts:
    * 36 Authentic Field Images: `data/raw/rice/` (12 per pathology)
    * 4 Diagnostic Tests: `data/diagnostic_tests/`
    * 34 Visual Descriptors: `data/features/image_features.csv`
    * 56/56 Tests Passed: `pytest` test suite execution (`tests/`)

---

### Slide 2: Research Motivation & Problem Statement
* **Presentation Slide:** Slide 2 (`CONTENT` layout)
* **Underlying Implementation Sources:**
  * Problem Formulation: `docs/architecture.md` (Section 1: "The Agricultural Data Gap")
  * Design Philosophy: `docs/warehouse_design.md` (Section 1: "Multimodal Agricultural Intelligence")
  * Relational Rigor: `src/warehouse/connection.py` (`set_sqlite_pragma`)
  * Research Question: `README.md` (Section: "Project Motivation")

---

### Slide 3: Project Objectives & Multimodal Pipeline Flow
* **Presentation Slide:** Slide 3 (`CONTENT` layout)
* **Underlying Implementation Sources:**
  * 6 Project Objectives: `docs/architecture.md` (Section 2: "Core Architectural Principles")
  * 7-Stage Pipeline Diagram: `assets/presentation/pipeline_flow.png`
  * Generating Script: `scripts/generate_presentation_assets.py` (`generate_pipeline_flow()`)
  * End-to-End Orchestrator: `run.py` (`main()`)

---

### Slide 4: Dataset Description & Agronomic Taxonomy
* **Presentation Slide:** Slide 4 (`CONTENT` layout — replaces Template Slide 2)
* **Underlying Implementation Sources:**
  * 7x2 Dataset Specification Table: `docs/dataset_documentation.md`
  * Raw Image Paths: `data/raw/rice/`
    * Bacterial Leaf Blight (12): `data/raw/rice/bacterial_leaf_blight/`
    * Brown Spot (12): `data/raw/rice/brown_spot/`
    * Leaf Smut (12): `data/raw/rice/leaf_smut/`
  * Source Inventory Report: `data/reports/source_inventory.json`
  * Control Baseline Policy (`HEALTHY`): `database/seeds/seed_dimensions.py` (`DISEASE_SEEDS`) & `docs/warehouse_design.md` (Section 3.2)

---

### Slide 5: Image Preprocessing & Quality Gate Verification
* **Presentation Slide:** Slide 5 (`CONTENT` layout)
* **Underlying Implementation Sources:**
  * Diagnostic Test Directory: `data/diagnostic_tests/`
    * `corrupted_header_test.jpg` -> `src/preprocessing/validator.py` (`validate_file`)
    * `invalid_dim_tiny.jpg` -> `src/preprocessing/validator.py` (`validate_dimensions`)
    * `duplicate_exact_test.jpg` -> `src/preprocessing/duplicate_detector.py` (`check_duplicate`)
    * `unsupported_extension.txt` -> `src/preprocessing/validator.py` (`validate_file`)
  * Preprocessing Report: `data/reports/preprocessing_report.json`
  * Rejection Audit: `data/reports/rejected_images_report.json`
  * Standardized Output: `data/processed/rice/{disease}/proc_{filename}.png` (36 files, 256×256 RGB)
  * Comparison Visual: `assets/presentation/preprocessing_comparison.png`

---

### Slide 6: Visual Feature Extraction & Attribute Summary
* **Presentation Slide:** Slide 6 (`CONTENT` layout — replaces Template Slide 3)
* **Underlying Implementation Sources:**
  * 8x4 Attribute Summary Table: `docs/feature_extraction.md` & `data/features/image_features.csv`
  * 17 Color Descriptors: `src/feature_extraction/color_features.py` (`extract_color_features`)
  * 7 Haralick GLCM Descriptors: `src/feature_extraction/texture_features.py` (`extract_texture_features`)
  * 7 Morphometric Shape Descriptors: `src/feature_extraction/shape_features.py` (`extract_shape_features`)
  * 10 Metadata / Lineage Fields: `src/feature_extraction/pipeline.py` (`process_dataset`)
  * Feature Store Dataset: `data/features/image_features.csv` (36 rows × 44 columns)

---

### Slide 7: Multimodal Data Warehouse — Star Schema Topology
* **Presentation Slide:** Slide 7 (`CONTENT` layout — replaces Template Slide 4)
* **Underlying Implementation Sources:**
  * Star Schema ERD Diagram: `assets/presentation/star_schema_erd.png`
  * Generating Script: `scripts/generate_presentation_assets.py` (`generate_star_schema_erd()`)
  * Fact Grain Definition: `docs/star_schema.md` (Section 2: "Fact Table Grain")
  * Declarative Models: `src/warehouse/models.py` (`DimCrop`, `DimDisease`, `DimImage`, `DimVisualFeature`, `DiseaseObservationFact`)
  * Database File: `database/agrovision_warehouse.db`
  * Verified Row Counts:
    * `dim_crop`: 1
    * `dim_disease`: 4 (3 active pathologies + `HEALTHY` control)
    * `dim_image`: 36
    * `dim_visual_feature`: 36
    * `disease_observation_fact`: 36

---

### Slide 8: Warehouse Design & Production ETL Architecture
* **Presentation Slide:** Slide 8 (`CONTENT` layout — replaces Template Slide 5)
* **Underlying Implementation Sources:**
  * Fact Measures Specification: `docs/star_schema.md` (Section 3: "Measures")
  * Dimension Hierarchies: `docs/star_schema.md` (Section 4: "Dimension Hierarchies")
  * ETL Idempotency Verification:
    * Implementation: `src/etl/load.py` (`Loader.load_dimensions_and_facts()`)
    * Audit Script: `scripts/verify_etl.py` (`verify_etl_integrity()`)
    * Audit Report: `data/reports/etl_report.json` (`facts_inserted: 0`, `facts_skipped_duplicate: 36`)

---

### Slide 9: Code: Creating the Warehouse (ANSI SQL DDL)
* **Presentation Slide:** Slide 9 (`CONTENT` layout — replaces Template Slide 7)
* **Underlying Implementation Sources:**
  * ANSI SQL Schema DDL: `database/schema/star_schema.sql` (Lines 8-124)
  * Schema Deployment Engine: `src/warehouse/schema_manager.py` (`initialize_schema()`)
  * Database Connection Layer: `src/warehouse/connection.py` (`set_sqlite_pragma`)

---

### Slide 10: Code: Production ETL Pipeline (Python & SQLAlchemy)
* **Presentation Slide:** Slide 10 (`CONTENT` layout — replaces Template Slide 8)
* **Underlying Implementation Sources:**
  * Connection Pragma Listener: `src/warehouse/connection.py` (`set_sqlite_pragma`)
  * Staged Data Transformer: `src/etl/transform.py` (`Transformer.transform()`)
  * Dimension-First Loader: `src/etl/load.py` (`Loader.load_dimensions_and_facts()`)
  * End-to-End Orchestrator: `src/etl/pipeline.py` (`ETLPipeline.run()`)

---

### Slide 11: SQL-Backed OLAP Operations Engine
* **Presentation Slide:** Slide 11 (`CONTENT` layout — replaces Template Slide 6 & 9)
* **Underlying Implementation Sources:**
  * 1. Roll-up: `src/olap/engine.py` (`OLAPEngine.rollup()`)
  * 2. True Drill-down: `src/olap/engine.py` (`OLAPEngine.true_drilldown()`)
  * 3. Slice: `src/olap/engine.py` (`OLAPEngine.slice_by_crop()`, `slice_by_pathogen()`)
  * 4. Dice: `src/olap/engine.py` (`OLAPEngine.dice()`)
  * 5. Pivot: `src/olap/engine.py` (`OLAPEngine.pivot()`)
  * OLAP Architectural Documentation: `docs/olap.md`

---

### Slide 12: Actual OLAP Query Results from Physical Warehouse
* **Presentation Slide:** Slide 12 (`CONTENT` layout)
* **Underlying Implementation Sources:**
  * Roll-up Verified Output (Cereal: 36 Obs, 1 Crop, 3 Diseases, 3.57 Avg Sev, 0.3178 Avg Contrast): `src/olap/engine.py` (`rollup()`)
  * Drill-down Verified Output (Bacterial BLB: 12, Fungal BS: 12, Fungal LS: 12): `src/olap/engine.py` (`true_drilldown()`)
  * Pivot Verified Output (Rice x Fungal: 24, Bacterial: 12, Viral: 0, Healthy: 0): `src/olap/engine.py` (`pivot()`)
  * Diagnostic Drill-Across (6 rows): `src/olap/engine.py` (`diagnostic_drilldown()`)
  * OLAP Visualizations: `assets/presentation/olap_visuals.png`
  * Generating Script: `scripts/generate_presentation_assets.py` (`generate_olap_visuals()`)

---

### Slide 13: Dashboard Demonstration, Quality Audit & Next Phase
* **Presentation Slide:** Slide 13 (`CONTENT` layout)
* **Underlying Implementation Sources:**
  * Streamlit Dashboard Application: `dashboard/app.py`
  * Dashboard Visual Composite: `assets/presentation/dashboard_composite.png`
  * Test Suite Execution (56/56 Passed): `pytest tests/` (12 test modules, 100% pass rate in ~2.87s)
  * Test Verification Modules:
    * `tests/test_validation.py` (5 tests)
    * `tests/test_duplicates.py` (3 tests)
    * `tests/test_preprocessing_phase2.py` (6 tests)
    * `tests/test_feature_extraction_phase3.py` (5 tests)
    * `tests/test_warehouse_phase4.py` (7 tests)
    * `tests/test_etl_phase5.py` (5 tests)
    * `tests/test_olap_real_warehouse.py` (7 tests)
  * Review 2 Roadmap Scope: `docs/architecture.md` (Section: "Phase 2 / Review 2 Roadmap")
