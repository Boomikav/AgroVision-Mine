"""
Post-ETL Verification and Integrity Audit Script for AgroVision-Mine (Phase 5).
Audits:
1. Exact row counts across all dimensions and fact table.
2. Null values in primary keys, foreign keys, and mandatory measures.
3. Orphan foreign key detection.
4. Duplicate fact record detection.
5. Dimension integrity and range validity.
6. Idempotent re-execution verification.
"""
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from src.warehouse.connection import get_db_engine, get_db_session
from src.warehouse.models import (
    DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact
)
from src.etl.pipeline import ETLPipeline
from src.utils.logger import setup_logger

logger = setup_logger("verify_etl")


def verify_etl_integrity() -> bool:
    print("=" * 80)
    print("AGROVISION-MINE: PHASE 5 ETL INTEGRITY & WAREHOUSE AUDIT")
    print("=" * 80)

    engine = get_db_engine()
    all_passed = True

    with engine.connect() as conn:
        # =====================================================================
        # 1. ROW COUNTS AUDIT
        # =====================================================================
        print("\n1. ROW COUNTS AUDIT:")
        counts = {}
        for table in ["dim_crop", "dim_disease", "dim_image", "dim_visual_feature", "disease_observation_fact"]:
            cnt = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            counts[table] = cnt
            print(f"   Table '{table}': {cnt} rows")

        if counts["disease_observation_fact"] == 0:
            print("   [FAIL] Fact table is empty!")
            all_passed = False
        else:
            print(f"   [PASS] Fact table is populated with {counts['disease_observation_fact']} observations.")

        if counts["dim_image"] != counts["disease_observation_fact"]:
            print(f"   [WARNING] dim_image ({counts['dim_image']}) != fact table ({counts['disease_observation_fact']})")
        else:
            print(f"   [PASS] 1:1 correspondence verified between dim_image and disease_observation_fact.")

        if counts["dim_visual_feature"] != counts["disease_observation_fact"]:
            print(f"   [WARNING] dim_visual_feature ({counts['dim_visual_feature']}) != fact table ({counts['disease_observation_fact']})")
        else:
            print(f"   [PASS] 1:1 correspondence verified between dim_visual_feature and disease_observation_fact.")

        # =====================================================================
        # 2. NULL VALUE DETECTION AUDIT
        # =====================================================================
        print("\n2. NULL VALUES AUDIT (Fact Table):")
        null_query = text("""
        SELECT
            SUM(CASE WHEN observation_key IS NULL THEN 1 ELSE 0 END) AS null_obs_key,
            SUM(CASE WHEN crop_key IS NULL THEN 1 ELSE 0 END) AS null_crop_key,
            SUM(CASE WHEN disease_key IS NULL THEN 1 ELSE 0 END) AS null_disease_key,
            SUM(CASE WHEN image_key IS NULL THEN 1 ELSE 0 END) AS null_image_key,
            SUM(CASE WHEN feature_key IS NULL THEN 1 ELSE 0 END) AS null_feature_key,
            SUM(CASE WHEN observation_count IS NULL THEN 1 ELSE 0 END) AS null_obs_count,
            SUM(CASE WHEN lesion_severity_score IS NULL THEN 1 ELSE 0 END) AS null_severity,
            SUM(CASE WHEN image_sharpness_score IS NULL THEN 1 ELSE 0 END) AS null_sharpness,
            SUM(CASE WHEN etl_batch_id IS NULL THEN 1 ELSE 0 END) AS null_batch_id
        FROM disease_observation_fact;
        """)
        null_row = conn.execute(null_query).fetchone()
        null_dict = dict(null_row._mapping)
        total_nulls = sum(null_dict.values())

        for col, cnt in null_dict.items():
            if cnt > 0:
                print(f"   [FAIL] Found {cnt} null values in column {col}!")
                all_passed = False

        if total_nulls == 0:
            print("   [PASS] Zero nulls found across all critical primary, foreign, and measure fields.")

        # =====================================================================
        # 3. ORPHAN FOREIGN KEY AUDIT
        # =====================================================================
        print("\n3. ORPHAN FOREIGN KEY AUDIT:")
        orphan_checks = [
            ("crop_key", "dim_crop", "crop_key"),
            ("disease_key", "dim_disease", "disease_key"),
            ("image_key", "dim_image", "image_key"),
            ("feature_key", "dim_visual_feature", "feature_key")
        ]

        total_orphans = 0
        for fk_col, ref_table, ref_pk in orphan_checks:
            orphan_query = text(f"""
            SELECT COUNT(*) FROM disease_observation_fact f
            LEFT JOIN {ref_table} d ON f.{fk_col} = d.{ref_pk}
            WHERE d.{ref_pk} IS NULL;
            """)
            orphan_count = conn.execute(orphan_query).scalar()
            if orphan_count > 0:
                print(f"   [FAIL] Found {orphan_count} orphan references in {fk_col} -> {ref_table}.{ref_pk}!")
                total_orphans += orphan_count
                all_passed = False
            else:
                print(f"   [PASS] Zero orphan keys for {fk_col} -> {ref_table}.{ref_pk}")

        # =====================================================================
        # 4. DUPLICATE FACT RECORD AUDIT
        # =====================================================================
        print("\n4. DUPLICATE FACT RECORD AUDIT:")
        dup_img_query = text("""
        SELECT image_key, COUNT(*) AS cnt
        FROM disease_observation_fact
        GROUP BY image_key
        HAVING COUNT(*) > 1;
        """)
        dup_images = conn.execute(dup_img_query).fetchall()

        dup_feat_query = text("""
        SELECT feature_key, COUNT(*) AS cnt
        FROM disease_observation_fact
        GROUP BY feature_key
        HAVING COUNT(*) > 1;
        """)
        dup_feats = conn.execute(dup_feat_query).fetchall()

        if dup_images or dup_feats:
            print(f"   [FAIL] Found duplicate fact records! Duplicate images={len(dup_images)}, duplicate features={len(dup_feats)}")
            all_passed = False
        else:
            print("   [PASS] Zero duplicate fact records detected (100% unique observations).")

        # =====================================================================
        # 5. DIMENSION INTEGRITY & MEASURE RANGE AUDIT
        # =====================================================================
        print("\n5. DIMENSION INTEGRITY & RANGE AUDIT:")
        # Check that severity scores are within [0.0, 10.0]
        range_query = text("""
        SELECT
            MIN(lesion_severity_score) AS min_sev,
            MAX(lesion_severity_score) AS max_sev,
            MIN(image_sharpness_score) AS min_sharp,
            MAX(image_sharpness_score) AS max_sharp,
            MIN(lesion_coverage_ratio) AS min_cov,
            MAX(lesion_coverage_ratio) AS max_cov
        FROM disease_observation_fact;
        """)
        ranges = dict(conn.execute(range_query).fetchone()._mapping)
        print(f"   Severity Range: [{ranges['min_sev']}, {ranges['max_sev']}] (Expected: [0.0, 10.0])")
        print(f"   Sharpness Range: [{ranges['min_sharp']}, {ranges['max_sharp']}]")
        print(f"   Coverage Ratio Range: [{ranges['min_cov']}, {ranges['max_cov']}] (Expected: [0.0, 1.0])")

        if ranges["min_sev"] < 0.0 or ranges["max_sev"] > 10.0:
            print("   [FAIL] Severity score out of [0.0, 10.0] bounds!")
            all_passed = False
        else:
            print("   [PASS] Lesion severity scores strictly bounded.")

        if ranges["min_cov"] < 0.0 or ranges["max_cov"] > 1.0:
            print("   [FAIL] Lesion coverage ratio out of [0.0, 1.0] bounds!")
            all_passed = False
        else:
            print("   [PASS] Lesion coverage ratios strictly bounded.")

        # =====================================================================
        # 6. IDEMPOTENT RE-EXECUTION AUDIT
        # =====================================================================
        print("\n6. REPEATABLE EXECUTION & DUPLICATE PREVENTION AUDIT:")
        pipeline = ETLPipeline()
        re_summary = pipeline.run(initialize_schema=False)
        re_stats = re_summary["load_statistics"]
        print(f"   Re-run load stats: Inserted={re_stats['facts_inserted']}, Skipped Duplicates={re_stats['facts_skipped_duplicate']}")

        if re_stats["facts_inserted"] != 0:
            print("   [FAIL] Pipeline inserted duplicate facts on re-run!")
            all_passed = False
        else:
            print(f"   [PASS] Re-execution is strictly idempotent (0 duplicate facts inserted, {re_stats['facts_skipped_duplicate']} safely skipped).")

    print("\n" + "=" * 80)
    if all_passed:
        print(">>> FINAL ETL VERIFICATION: ALL 6 AUDIT CRITERIA PASSED (100% HEALTHY)")
    else:
        print(">>> FINAL ETL VERIFICATION: ONE OR MORE AUDIT CRITERIA FAILED!")
    print("=" * 80 + "\n")

    return all_passed


if __name__ == "__main__":
    success = verify_etl_integrity()
    sys.exit(0 if success else 1)
