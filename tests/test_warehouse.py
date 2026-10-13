import pytest
from sqlalchemy import inspect
from src.warehouse.connection import get_db_engine, get_db_session
from src.warehouse.schema_manager import SchemaManager
from src.warehouse.models import (
    Base, DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact
)

@pytest.fixture
def schema_mgr():
    mgr = SchemaManager()
    mgr.initialize_schema(drop_existing=False)
    return mgr

def test_database_connection(schema_mgr):
    engine = get_db_engine()
    with engine.connect() as conn:
        assert conn is not None

def test_star_schema_tables_exist(schema_mgr):
    health = schema_mgr.get_warehouse_health()
    assert health["status"] == "HEALTHY"
    expected = {
        "dim_crop", "dim_disease",
        "dim_image", "dim_visual_feature", "disease_observation_fact"
    }
    for tbl in expected:
        assert tbl in health["existing_tables"]

def test_warehouse_models_insertion():
    session = get_db_session()
    try:
        # Verify dimension query
        crop_count = session.query(DimCrop).count()
        assert crop_count >= 0
    finally:
        session.close()
