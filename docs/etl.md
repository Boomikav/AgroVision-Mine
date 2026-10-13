# Extract, Transform, Load (ETL) Architecture & Operations

## 1. Overview & Pipeline Architecture

The **AgroVision-Mine Production ETL Pipeline** orchestrates the transformation of heterogeneous raw agricultural imagery and taxonomy metadata into an integrated, analytics-ready Star Schema data warehouse.

```text
[ EXTRACT ]
  │
  ├── 1. Extract Raw Metadata: Recursive directory scanning of data/raw/ via DatasetInspector
  ├── 2. Extract Processed Metadata: Ingests validated records from data/processed/cleaned_metadata.csv
  └── 3. Extract Visual Features: Ingests 44 classical descriptors from data/features/image_features.csv
  │
  ▼
[ TRANSFORM ]
  │
  ├── 1. Cleaning & Sanitization: Whitespace trimming, casing normalization, null filtering
  ├── 2. Standardization: Botanical classification (Oryza sativa) & pathology taxonomy (Xanthomonas, Bipolaris, Entyloma)
  ├── 3. Quality Validation: Verifies physical file presence, MD5 hashes, numerical feature bounds
  ├── 4. Dimension Assembly: Structures records for dim_crop, dim_disease, dim_image, dim_visual_feature
  └── 5. Fact Staging: Computes severity scores [0.0 - 10.0], sharpness scores, coverage ratios, latency
  │
  ▼
[ LOAD ]
  │
  ├── STEP 1: Dimension Tables First (Transactional Resolution)
  │     ├── DimCrop (resolves/assigns crop_key by crop_code)
  │     ├── DimDisease (resolves/assigns disease_key by disease_code)
  │     ├── DimImage (resolves/assigns image_key by raw_id / md5_hash)
  │     └── DimVisualFeature (resolves/assigns feature_key by image_filename)
  │
  └── STEP 2: Fact Table Second (Referential Integrity & Idempotency)
        ├── Resolves surrogate foreign keys (crop_key, disease_key, image_key, feature_key)
        ├── Rejects any orphan foreign keys (strict referential integrity)
        ├── Enforces unique image_key constraint (prevents duplicate observation facts)
        ├── Wraps operations in ACID transaction (atomic commit or automatic rollback)
        └── Emits execution reports to data/reports/etl_report.json & data/reports/etl_report.md
```

---

## 2. Idempotency & Repeatability Guarantees

The pipeline is engineered for strict production-grade repeatability:

1. **Natural Key Resolution (Dimension Deduplication):**
   - `dim_crop` is queried by `crop_code` (`RICE`). Existing surrogate keys are preserved.
   - `dim_disease` is queried by `disease_code` (`BACTERIAL_BLIGHT`, `BROWN_SPOT`, `LEAF_SMUT`, `HEALTHY`).
   - `dim_image` is queried by `raw_id` and `md5_hash`. Existing images are not duplicated.
   - `dim_visual_feature` is queried by `image_filename`. Existing feature vectors are preserved.
2. **Fact Table Duplicate Prevention:**
   - Each fact record corresponds 1:1 with an individual preprocessed image (`image_key`).
   - If an observation with the given `image_key` is already present in `disease_observation_fact`, the record is skipped, incrementing `facts_skipped_duplicate` without throwing constraint violations.
3. **Transaction Safety (ACID):**
   - The entire load stage executes within a single SQLAlchemy transaction session.
   - If an unexpected database exception or referential error occurs, `session.rollback()` is automatically invoked, leaving the warehouse in a pristine, uncorrupted state.

---

## 3. Ground-Truth Data Flow & Verification

Running against the authentic ICAR research dataset yielded the following audited figures:

| Metric | Ground-Truth Count | Audit Status |
|---|---|---|
| **Raw Images Discovered** | 39 | 36 valid field images + 3 diagnostic test files |
| **Processed Images Extracted** | 36 | Successfully standardized to $256 \times 256 \times 3$ RGB |
| **Visual Feature Vectors** | 36 | 44 numerical classical descriptors extracted |
| **Facts Staged for Loading** | 36 | 100% matched to valid image and feature entries |
| **DimCrop Rows Loaded** | 1 | Rice (*Oryza sativa*, Cereal) |
| **DimDisease Rows Loaded** | 4 | Bacterial Blight, Brown Spot, Leaf Smut, Healthy |
| **DimImage Rows Loaded** | 36 | 100% unique cryptographic MD5 hashes |
| **DimVisualFeature Rows Loaded** | 36 | 100% unique image filename mappings |
| **DiseaseObservationFact Rows Loaded** | 36 | Exactly 36 unique observations |
| **Null Values in Fact Keys/Measures** | 0 | 100% clean |
| **Orphan Foreign Keys** | 0 | 100% referential integrity |
| **Duplicate Fact Rows** | 0 | 100% uniqueness |

---

## 4. Execution & Audit Commands

```bash
# Execute production ETL pipeline
python run.py --stage etl

# Execute comprehensive ETL audit and integrity verification
python scripts/verify_etl.py

# Run complete ETL unit and integration test suite
pytest tests/test_etl_phase5.py -v
```
