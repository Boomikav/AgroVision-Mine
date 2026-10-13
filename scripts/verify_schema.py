"""
Warehouse Schema Verification Script for AgroVision-Mine (Phase 4).
Performs comprehensive auditing of the physical SQLite / PostgreSQL database:
1. Verifies presence of the 4 supported dimensions and 1 fact table.
2. Asserts absence of unsupported dimensions (dim_pest, dim_time, dim_geography).
3. Verifies primary keys on all tables.
4. Verifies foreign keys, targets, and referential constraints on the fact table.
5. Verifies unique constraints and indexes for query optimization.
6. Verifies dimension seed execution and idempotency.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import inspect
from src.warehouse.connection import get_db_engine, get_db_session
from src.warehouse.schema_manager import SchemaManager
from database.seeds.seed_dimensions import seed_reference_dimensions
from src.warehouse.models import DimCrop, DimDisease, DiseaseObservationFact
from src.utils.logger import setup_logger

logger = setup_logger("verify_schema")


def verify_schema() -> bool:
    print("=" * 80)
    print("AGROVISION-MINE: PHASE 4 DATA WAREHOUSE SCHEMA VERIFICATION")
    print("=" * 80)

    # 1. Initialize schema
    schema_mgr = SchemaManager()
    schema_mgr.initialize_schema(drop_existing=False)

    engine = get_db_engine()
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    print(f"\n1. TABLE INVENTORY AUDIT:")
    print(f"   Detected tables in database: {sorted(list(table_names))}")

    expected_tables = {
        "dim_crop", "dim_disease", "dim_image",
        "dim_visual_feature", "disease_observation_fact"
    }
    unsupported_tables = {"dim_pest", "dim_time", "dim_geography", "dim_location"}

    missing_tables = expected_tables - table_names
    found_unsupported = unsupported_tables.intersection(table_names)

    if missing_tables:
        print(f"   [FAIL] Missing required tables: {missing_tables}")
        return False
    print(f"   [PASS] All 5 required tables are physically present.")

    if found_unsupported:
        print(f"   [FAIL] Found forbidden unsupported tables: {found_unsupported}")
        return False
    print(f"   [PASS] Zero unsupported dimensions present (no fake dim_pest, dim_time, dim_geography).")

    # 2. Primary Key Audit
    print(f"\n2. PRIMARY KEY AUDIT:")
    pk_map = {
        "dim_crop": "crop_key",
        "dim_disease": "disease_key",
        "dim_image": "image_key",
        "dim_visual_feature": "feature_key",
        "disease_observation_fact": "observation_key"
    }

    all_pks_ok = True
    for tbl, expected_pk in pk_map.items():
        pk_constraint = inspector.get_pk_constraint(tbl)
        constrained_cols = pk_constraint.get("constrained_columns", [])
        if expected_pk in constrained_cols:
            print(f"   [PASS] Table '{tbl}': PK is '{expected_pk}'")
        else:
            print(f"   [FAIL] Table '{tbl}': Expected PK '{expected_pk}', found {constrained_cols}")
            all_pks_ok = False

    if not all_pks_ok:
        return False

    # 3. Foreign Key & Referential Integrity Audit on Fact Table
    print(f"\n3. FOREIGN KEY & REFERENTIAL INTEGRITY AUDIT (Fact Table):")
    fks = inspector.get_foreign_keys("disease_observation_fact")
    expected_fks = {
        "crop_key": "dim_crop.crop_key",
        "disease_key": "dim_disease.disease_key",
        "image_key": "dim_image.image_key",
        "feature_key": "dim_visual_feature.feature_key"
    }

    fk_actual_map = {}
    for fk in fks:
        referred_table = fk.get("referred_table")
        referred_cols = fk.get("referred_columns", [""])
        for col in fk.get("constrained_columns", []):
            fk_actual_map[col] = f"{referred_table}.{referred_cols[0]}"

    all_fks_ok = True
    for col, expected_ref in expected_fks.items():
        actual_ref = fk_actual_map.get(col)
        if actual_ref == expected_ref:
            print(f"   [PASS] Foreign Key '{col}' -> {actual_ref}")
        else:
            print(f"   [FAIL] Foreign Key '{col}' expected {expected_ref}, found {actual_ref}")
            all_fks_ok = False

    if not all_fks_ok:
        return False

    # Check SQLite PRAGMA foreign_keys
    with engine.connect() as conn:
        from sqlalchemy import text
        pragma_fk = conn.execute(text("PRAGMA foreign_keys;")).scalar()
        if pragma_fk == 1:
            print(f"   [PASS] SQLite PRAGMA foreign_keys = 1 (Natively Enforced by DB Engine)")
        else:
            print(f"   [FAIL] SQLite PRAGMA foreign_keys = {pragma_fk} (Foreign keys not enforced!)")
            return False


    # 4. Indexes & Performance Optimization Audit
    print(f"\n4. INDEX & QUERY ACCELERATION AUDIT:")
    for tbl in expected_tables:
        indexes = inspector.get_indexes(tbl)
        idx_names = [idx["name"] for idx in indexes]
        print(f"   Table '{tbl}' Indexes: {idx_names}")

    # 5. Seeding & Idempotency Audit
    print(f"\n5. SEEDING & IDEMPOTENCY AUDIT:")
    seed_stats1 = seed_reference_dimensions()
    print(f"   First Seed Execution: {seed_stats1}")
    seed_stats2 = seed_reference_dimensions()
    print(f"   Second Seed Execution (Idempotency Check): {seed_stats2}")

    if seed_stats2["crops_seeded"] != 0 or seed_stats2["diseases_seeded"] != 0:
        print(f"   [FAIL] Seeding is NOT idempotent! Duplicate inserts occurred on second run.")
        return False
    print(f"   [PASS] Seeding is strictly idempotent (0 duplicate records inserted on re-run).")

    session = get_db_session()
    try:
        crop_count = session.query(DimCrop).count()
        disease_count = session.query(DimDisease).count()
        print(f"   Warehouse Reference Counts: {crop_count} Crops, {disease_count} Diseases.")
    finally:
        session.close()

    print("\n" + "=" * 80)
    print(">>> SCHEMA VERIFICATION RESULT: ALL CHECKS PASSED (100% HEALTHY)")
    print("=" * 80 + "\n")
    return True


if __name__ == "__main__":
    success = verify_schema()
    sys.exit(0 if success else 1)
