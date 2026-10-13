# AgroVision-Mine System Architecture Specification

## 1. High-Level Modular Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                              │
│   Streamlit Review 1 Interactive Dashboard (dashboard/app.py)          │
│   - Project Overview    - Dataset Explorer    - Preprocessing Diagnostics│
│   - Star Schema Live    - Interactive OLAP Engine (Roll-up, Drill-down,│
│                           Slice, Dice, Pivot with SQL Query Inspector) │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                       OLAP ANALYTICS ENGINE                            │
│   src/olap/engine.py                                                   │
│   - ANSI SQL dimensional query generator                              │
│   - Hierarchy aggregation (Roll-up / Drill-down)                       │
│   - Predicate sub-cubing (Slice / Dice)                                │
│   - Cross-tabulation matrices (Pivot)                                  │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                    MULTIMODAL DATA WAREHOUSE                           │
│   src/warehouse/ (models.py, connection.py, schema_manager.py)         │
│   - Star Schema DDL (database/schema/star_schema.sql)                  │
│   - Central Fact: DiseaseObservation_Fact                              │
│   - Dimensions: Dim_Crop, Dim_Disease, Dim_Pest, Dim_Image,            │
│                 Dim_VisualFeature                                      │
│   - Multi-dialect engine: SQLite (local default) / PostgreSQL          │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                           ETL PIPELINE                                 │
│   src/etl/ (extract.py, transform.py, load.py, pipeline.py)            │
│   - Idempotent dimension and fact loading                              │
│   - Surrogate key resolution and referential integrity verification    │
│   - Lineage and audit reporting (data/reports/etl_summary.json)        │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                    FEATURE EXTRACTION PIPELINE                         │
│   src/feature_extraction/ (color, texture_glcm, shape_contours)        │
│   - 14 Color Moments (RGB mean/std, HSV mean/std, Excess Green index) │
│   - 6 GLCM Haralick Texture Properties (contrast, homogeneity, energy) │
│   - Morphometric Contours (area, perimeter, circularity, solidity)     │
│   - Extensible BaseFeatureExtractor interface for future deep models   │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                 IMAGE PREPROCESSING & VALIDATION                       │
│   src/preprocessing/ (validator.py, duplicate_detector.py, preproc.py) │
│   - Header and format integrity check; corrupted image rejection       │
│   - Discrete Laplacian variance blur score computation                 │
│   - Exact MD5 and perceptual dHash duplicate elimination               │
│   - Standardized 256×256 RGB normalization without modifying raw files │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                      RAW DATA INGESTION LAYER                          │
│   src/ingestion/ (dataset_loader.py, sample_data.py)                   │
│   - Official ICAR / data.gov.in folder and manifest scanner            │
│   - Zero-fabrication inspection & cryptographic checksum catalog       │
│   - Source inventory emission (data/reports/source_inventory.json)     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Design Decisions

1. **Python-First Practical Architecture:**
   Leverages standard scientific libraries (`numpy`, `pandas`, `pillow`, `scipy`) for numerical processing and `SQLAlchemy 2.0` for dimensional abstraction.

2. **Clean Database Decoupling:**
   Local evaluation uses SQLite with zero infrastructure friction, while maintaining full compatibility with enterprise PostgreSQL without modifying queries or models.

3. **Academic Defensibility:**
   Eliminates black-box opacity by extracting mathematically rigorous classical visual features (first/second-order color statistics, Haralick spatial co-occurrence matrices, and geometric moments) directly linked to pathology.

4. **Extensible Design for Future Reviews:**
   The `BaseFeatureExtractor` abstract interface allows drop-in addition of deep embeddings (e.g., ResNet/Vision Transformer vectors) in Review 2/3 without altering the core warehouse schema or OLAP engine.
