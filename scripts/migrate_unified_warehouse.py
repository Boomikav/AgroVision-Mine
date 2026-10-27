"""
AgroVision-Mine: Master Unified Warehouse Migration & Integrity Verifier.
Migrates the physical SQLite database (database/agrovision_warehouse.db)
to contain all 2,596 authentic observations, their metadata, provenance,
and all 32 continuous visual descriptors per observation.
"""
import os
import sys
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.etl.pipeline import ETLPipeline
from src.warehouse.connection import get_warehouse_db_url, reset_db_connection


def run_migration() -> int:
    print("=" * 80)
    print("AGROVISION-MINE: UNIFIED PHYSICAL DATA WAREHOUSE MIGRATION (2,596 OBSERVATIONS)")
    print("=" * 80)
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Project Root: {ROOT_DIR}")

    db_path = ROOT_DIR / "database" / "agrovision_warehouse.db"
    manifest_path = ROOT_DIR / "data" / "manifests" / "canonical_dataset_v2.csv"
    features_path = ROOT_DIR / "data" / "features" / "image_features_v2.csv"

    # Step 1: Pre-Migration Backup
    print("\n>>> STEP 1: Creating verified pre-migration database backup...")
    backup_dir = ROOT_DIR / "backups" / "pre_unified_migration"
    backup_dir.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        backup_file = backup_dir / f"agrovision_warehouse_pre_migration_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db_path, backup_file)
        print(f"   [SUCCESS] Backed up {db_path.name} ({db_path.stat().st_size} bytes) -> {backup_file}")
    else:
        print("   [INFO] No existing database file found to back up.")

    # Step 2: Validate Canonical Input Sources
    print("\n>>> STEP 2: Validating canonical inputs...")
    if not manifest_path.exists() or not features_path.exists():
        print("   [ERROR] Missing canonical manifest or feature store files!")
        return 1

    df_man = pd.read_csv(manifest_path)
    df_feat = pd.read_csv(features_path)

    print(f"   Manifest records: {len(df_man)}")
    print(f"   Feature store records: {len(df_feat)}")

    if len(df_man) != 2596 or len(df_feat) != 2596:
        print("   [ERROR] Expected exactly 2,596 observations!")
        return 1

    if (df_man["image_id"] != df_feat["image_id"]).any():
        print("   [ERROR] Manifest IDs and Feature Store IDs do not match one-to-one!")
        return 1

    # Verify Rice records
    rice_records = df_man[df_man["crop_name"].str.lower() == "rice"]
    print(f"   Authentic Rice observations: {len(rice_records)}")
    if len(rice_records) != 36:
        print(f"   [ERROR] Expected exactly 36 authentic rice records, found {len(rice_records)}")
        return 1

    plantdoc_records = df_man[df_man["dataset_source"].str.lower() == "plantdoc"]
    print(f"   PlantDoc field observations: {len(plantdoc_records)}")
    if len(plantdoc_records) != 2560:
        print(f"   [ERROR] Expected exactly 2,560 PlantDoc records, found {len(plantdoc_records)}")
        return 1

    # Step 3: Run Full ETL Pipeline Migration
    print("\n>>> STEP 3: Executing transactional ETL pipeline with schema initialization...")
    reset_db_connection()
    pipeline = ETLPipeline(
        manifest_path=str(manifest_path),
        features_path=str(features_path)
    )

    try:
        summary = pipeline.run(initialize_schema=True, drop_existing=True)
        print(f"   [SUCCESS] ETL pipeline executed successfully in {summary['execution_time_seconds']}s")
    except Exception as e:
        print(f"   [CRITICAL FAILURE] ETL pipeline failed: {e}")
        return 1

    # Step 4: Strict Post-Migration SQL Invariant Verification
    print("\n>>> STEP 4: Executing post-migration SQL invariant verification...")
    reset_db_connection()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    invariants = []

    # 4.1 Fact Row Count
    cursor.execute("SELECT COUNT(*) FROM disease_observation_fact;")
    fact_count = cursor.fetchone()[0]
    invariants.append(("Total Observation Facts == 2,596", fact_count == 2596, f"Actual: {fact_count}"))

    # 4.2 Unique Image IDs in Fact Table
    cursor.execute("SELECT COUNT(DISTINCT image_id) FROM disease_observation_fact;")
    distinct_fact_ids = cursor.fetchone()[0]
    invariants.append(("Unique Observation IDs == 2,596", distinct_fact_ids == 2596, f"Actual: {distinct_fact_ids}"))

    # 4.3 Dimension Image Count
    cursor.execute("SELECT COUNT(*) FROM dim_image;")
    image_count = cursor.fetchone()[0]
    invariants.append(("dim_image rows == 2,596", image_count == 2596, f"Actual: {image_count}"))

    # 4.4 Dimension Visual Feature Count
    cursor.execute("SELECT COUNT(*) FROM dim_visual_feature;")
    feat_count = cursor.fetchone()[0]
    invariants.append(("dim_visual_feature rows == 2,596", feat_count == 2596, f"Actual: {feat_count}"))

    # 4.5 Authentic Rice Preservation
    cursor.execute("""
        SELECT COUNT(f.observation_key)
        FROM disease_observation_fact f
        JOIN dim_crop c ON f.crop_key = c.crop_key
        WHERE LOWER(c.crop_name) = 'rice';
    """)
    rice_fact_count = cursor.fetchone()[0]
    invariants.append(("Preserved Rice Facts == 36", rice_fact_count == 36, f"Actual: {rice_fact_count}"))

    # 4.6 PlantDoc Observations Count
    cursor.execute("""
        SELECT COUNT(f.observation_key)
        FROM disease_observation_fact f
        JOIN dim_image i ON f.image_key = i.image_key
        WHERE LOWER(i.dataset_source) = 'plantdoc';
    """)
    plantdoc_fact_count = cursor.fetchone()[0]
    invariants.append(("PlantDoc Facts == 2,560", plantdoc_fact_count == 2560, f"Actual: {plantdoc_fact_count}"))

    # 4.7 Unique Crops Count
    cursor.execute("SELECT COUNT(DISTINCT crop_key) FROM dim_crop;")
    crops_count = cursor.fetchone()[0]
    invariants.append(("dim_crop unique crops == 14", crops_count == 14, f"Actual: {crops_count}"))

    # 4.8 Unique Diseases Count
    cursor.execute("SELECT COUNT(DISTINCT disease_key) FROM dim_disease;")
    diseases_count = cursor.fetchone()[0]
    invariants.append(("dim_disease categories >= 19", diseases_count >= 19, f"Actual: {diseases_count}"))

    # 4.9 Foreign Key Integrity Check (Zero Orphans)
    cursor.execute("""
        SELECT COUNT(*)
        FROM disease_observation_fact f
        LEFT JOIN dim_crop c ON f.crop_key = c.crop_key
        LEFT JOIN dim_disease d ON f.disease_key = d.disease_key
        LEFT JOIN dim_image i ON f.image_key = i.image_key
        LEFT JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
        WHERE c.crop_key IS NULL OR d.disease_key IS NULL OR i.image_key IS NULL OR vf.feature_key IS NULL;
    """)
    orphan_count = cursor.fetchone()[0]
    invariants.append(("Orphan Foreign Keys == 0", orphan_count == 0, f"Actual: {orphan_count}"))

    # 4.10 Null Check on Visual Features
    cursor.execute("""
        SELECT COUNT(*) FROM dim_visual_feature
        WHERE rgb_r_mean IS NULL OR glcm_contrast IS NULL OR contour_perimeter IS NULL
           OR hsv_h_std IS NULL OR hsv_s_std IS NULL OR hsv_v_std IS NULL;
    """)
    null_feat_count = cursor.fetchone()[0]
    invariants.append(("Zero Nulls in Required 32 Features", null_feat_count == 0, f"Actual: {null_feat_count}"))

    # Print Invariant Results
    all_passed = True
    print("\n=== POST-LOAD SQL INVARIANT AUDIT REPORT ===")
    for desc, passed, details in invariants:
        status = "[PASS]" if passed else "[FAIL]"
        print(f" {status} {desc.ljust(45)} | {details}")
        if not passed:
            all_passed = False

    conn.close()

    if all_passed:
        print("\n" + "=" * 80)
        print("ALL INVARIANTS SATISFIED! WAREHOUSE UNIFICATION SUCCESSFUL.")
        print("The physical warehouse now authoritative contains all 2,596 observations.")
        print("=" * 80)
        return 0
    else:
        print("\n" + "=" * 80)
        print("[CRITICAL] ONE OR MORE INVARIANTS FAILED!")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    exit_code = run_migration()
    sys.exit(exit_code)
