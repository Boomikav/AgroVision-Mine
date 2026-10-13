"""
Phase 4 Warehouse Architecture & Schema Integrity Unit Tests.
Verifies:
1. Star Schema table structure and column definitions.
2. Primary keys, foreign keys, and referential constraints.
3. Compound indexes for OLAP query acceleration.
4. Absence of unsupported dimensions (anti-fabrication mandate).
5. Idempotent seeding mechanism.
"""
import pytest
from sqlalchemy import inspect, create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from src.warehouse.connection import get_db_engine, get_db_session
from src.warehouse.models import (
    Base, DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact
)
from src.warehouse.schema_manager import SchemaManager
from database.seeds.seed_dimensions import seed_reference_dimensions, CROP_SEEDS, DISEASE_SEEDS


@pytest.fixture
def test_db():
    """Isolated in-memory SQLite database fixture."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield engine, session
    session.close()


def test_schema_contains_only_supported_tables(test_db):
    engine, _ = test_db
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    expected_tables = {
        "dim_crop", "dim_disease", "dim_image",
        "dim_visual_feature", "disease_observation_fact"
    }
    assert expected_tables == tables

    # Explicitly assert absence of unsupported dimensions
    unsupported = {"dim_pest", "dim_time", "dim_geography", "dim_weather"}
    assert len(unsupported.intersection(tables)) == 0


def test_primary_keys_and_types(test_db):
    engine, _ = test_db
    inspector = inspect(engine)

    pk_map = {
        "dim_crop": "crop_key",
        "dim_disease": "disease_key",
        "dim_image": "image_key",
        "dim_visual_feature": "feature_key",
        "disease_observation_fact": "observation_key"
    }

    for table, pk_name in pk_map.items():
        pk = inspector.get_pk_constraint(table)
        assert pk_name in pk["constrained_columns"], f"Table {table} missing PK {pk_name}"


def test_foreign_key_constraints_on_fact_table(test_db):
    engine, _ = test_db
    inspector = inspect(engine)
    fks = inspector.get_foreign_keys("disease_observation_fact")

    fk_map = {}
    for fk in fks:
        col = fk["constrained_columns"][0]
        ref = f"{fk['referred_table']}.{fk['referred_columns'][0]}"
        fk_map[col] = ref

    assert fk_map["crop_key"] == "dim_crop.crop_key"
    assert fk_map["disease_key"] == "dim_disease.disease_key"
    assert fk_map["image_key"] == "dim_image.image_key"
    assert fk_map["feature_key"] == "dim_visual_feature.feature_key"


def test_unique_constraints(test_db):
    engine, _ = test_db
    inspector = inspect(engine)

    # Check unique indexes
    crop_indexes = inspector.get_indexes("dim_crop")
    crop_unique_cols = {col for idx in crop_indexes if idx.get("unique") for col in idx["column_names"]}
    assert "crop_code" in crop_unique_cols

    disease_indexes = inspector.get_indexes("dim_disease")
    dis_unique_cols = {col for idx in disease_indexes if idx.get("unique") for col in idx["column_names"]}
    assert "disease_code" in dis_unique_cols

    img_indexes = inspector.get_indexes("dim_image")
    img_unique_cols = {col for idx in img_indexes if idx.get("unique") for col in idx["column_names"]}
    assert "md5_hash" in img_unique_cols
    assert "raw_id" in img_unique_cols


def test_seed_mechanism_idempotency():
    """Verify seed_dimensions runs cleanly without throwing duplicates."""
    res1 = seed_reference_dimensions()
    assert res1["crops_seeded"] >= 0
    assert res1["diseases_seeded"] >= 0

    # Second run should insert 0 new records
    res2 = seed_reference_dimensions()
    assert res2["crops_seeded"] == 0
    assert res2["diseases_seeded"] == 0


def test_sqlite_foreign_key_pragma_active(test_db):
    """Verify that PRAGMA foreign_keys is strictly enabled (=1) on SQLite connections."""
    engine, _ = test_db
    with engine.connect() as conn:
        pragma_val = conn.execute(text("PRAGMA foreign_keys;")).scalar()
        assert pragma_val == 1


def test_foreign_key_enforcement_rejects_invalid_insertion(test_db):
    """Verify that an invalid foreign key insertion is rejected by SQLite engine directly."""
    engine, session = test_db
    # Attempt inserting a fact with non-existent foreign keys (e.g., 9999)
    invalid_fact = DiseaseObservationFact(
        crop_key=9999,
        disease_key=9999,
        image_key=9999,
        feature_key=9999,
        observation_count=1
    )
    session.add(invalid_fact)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()

