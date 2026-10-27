# AgroVision-Mine: Unified Production ETL Pipeline Execution Report

**Batch Identifier:** `BATCH_20261027_130728`  
**Execution Timestamp:** `2026-10-27T13:07:31.882640`  
**Total Pipeline Duration:** `3.82s`  
**Overall Pipeline Status:** `SUCCESS`  

---

## 1. Executive Summary & Flow

```
CANONICAL DATASET MANIFEST (2,596 records) + FEATURE STORE (2,596 rows, 32 continuous features)
       ↓
EXTRACTION & SHA-256 INTEGRITY VALIDATION (PlantDoc: 2,560 | ICAR/OGD Rice: 36)
       ↓
TRANSFORMATION & TAXONOMIC HARMONIZATION (14 Crops, 19 Diseases/Conditions)
       ↓
TRANSACTIONAL LOAD (Dimensions First → Observation Facts Second)
       ↓
UNIFIED PHYSICAL DATA WAREHOUSE (disease_observation_fact: 2596 loaded facts)
```

---

## 2. Extraction Statistics
- **Total Discovered Records:** 2596
- **PlantDoc Field Observations:** 2560
- **ICAR/OGD Rice Observations:** 36
- **Canonical Manifest SHA-256 Validated:** `True`
- **Canonical Feature Store SHA-256 Validated:** `True`

---

## 3. Transformation & Quality Gates
- **Successfully Staged Facts:** 2596
- **Unique Crops Identified:** 14
- **Unique Diseases/Conditions Identified:** 19
- **Rejected Records:** 0

*Zero records rejected during transformation quality gates.*

---

## 4. Transactional Load Statistics
- **DimCrop:** 14 total crops in database
- **DimDisease:** 20 total disease categories in database
- **DimImage:** 2596 physical images in database
- **DimVisualFeature:** 2596 complete 32-feature vectors in database
- **DiseaseObservationFact:** 2596 loaded observation facts
- **Facts Skipped Duplicates (Idempotency):** 2596
- **Orphan Foreign Keys:** 0
- **Load Execution Duration:** 3559.79 ms

---

## 5. Warehouse Table Counts & Post-Load Integrity
- **Total Facts in Database:** `2596`
- **Host Crops in Database:** `14`
- **Diseases in Database:** `20`
- **Physical Images in Database:** `2596`
- **Visual Feature Vectors in Database:** `2596`
- **Referential Integrity Violations:** `0`
- **Warehouse Status:** `HEALTHY`

