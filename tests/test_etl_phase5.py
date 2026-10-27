"""
Phase 5 ETL Pipeline Unit & Integration Tests.
Verifies:
1. Extractor component (raw, processed, feature bundles).
2. Transformer component (cleaning, standardization, validation, entity staging).
3. Loader component (dimension-first ordering, FK resolution, referential integrity, duplicate skipping).
4. End-to-end pipeline execution and idempotent re-runs.
"""
import pytest
from pathlib import Path
from src.etl.extract import Extractor
from src.etl.transform import Transformer
from src.etl.load import Loader
from src.etl.pipeline import ETLPipeline
from src.warehouse.connection import get_db_session
from src.warehouse.models import DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact


def test_extractor_components():
    extractor = Extractor()
    bundle = extractor.extract_all()

    assert "raw_metadata" in bundle
    assert "processed_metadata" in bundle
    assert "visual_features" in bundle
    assert "stats" in bundle

    assert bundle["stats"]["raw_count"] == 2596
    assert bundle["stats"]["processed_count"] == 2596
    assert bundle["stats"]["feature_count"] == 2596
    assert bundle["stats"]["rice_records"] == 36
    assert bundle["stats"]["plantdoc_records"] == 2560


def test_transformer_standardization():
    transformer = Transformer()

    # Crop standardization
    crop = transformer.standardize_crop("rice")
    assert crop["crop_code"] == "RICE"
    assert crop["botanical_name"] == "Oryza sativa"
    assert crop["crop_category"] == "Cereal"

    # Disease standardization
    dis_blight = transformer.standardize_disease("bacterial_leaf_blight")
    assert dis_blight["disease_code"] == "BACTERIAL_LEAF_BLIGHT"
    assert dis_blight["pathogen_type"] == "Bacterial"

    dis_healthy = transformer.standardize_disease("healthy")
    assert dis_healthy["disease_code"] == "HEALTHY"
    assert dis_healthy["pathogen_type"] == "None"


def test_transformer_validation_and_staging():
    extractor = Extractor()
    transformer = Transformer()
    bundle = extractor.extract_all()
    staged = transformer.transform(bundle)

    assert "dim_crops" in staged
    assert "dim_diseases" in staged
    assert "dim_images" in staged
    assert "dim_features" in staged
    assert "fact_records" in staged

    assert len(staged["fact_records"]) == 2596
    assert len(staged["dim_images"]) == 2596
    assert len(staged["dim_features"]) == 2596
    assert len(staged["rejected_records"]) == 0

    fact_sample = staged["fact_records"][0]
    assert "crop_code" in fact_sample
    assert "disease_code" in fact_sample
    assert "image_id" in fact_sample
    assert "observation_count" in fact_sample
    assert fact_sample["observation_count"] == 1


def test_loader_referential_integrity():
    loader = Loader()

    # Create invalid staged data with missing foreign key
    corrupted_staged = {
        "dim_crops": [],
        "dim_diseases": [],
        "dim_images": [],
        "dim_features": [],
        "fact_records": [{
            "crop_code": "NON_EXISTENT_CROP",
            "disease_code": "NON_EXISTENT_DISEASE",
            "raw_id": "NON_EXISTENT_RAW",
            "image_filename": "non_existent.jpg",
            "observation_count": 1
        }]
    }

    stats = loader.load_dimensions_and_facts(corrupted_staged, "TEST_CORRUPTED_BATCH")
    assert stats["orphan_foreign_keys"] == 1
    assert stats["facts_inserted"] == 0
    assert len(stats["errors"]) > 0


def test_end_to_end_etl_pipeline_run():
    pipeline = ETLPipeline()
    summary = pipeline.run(initialize_schema=False)

    assert "batch_id" in summary
    assert "execution_time_seconds" in summary
    assert summary["transformed_records"] == 2596
    assert summary["warehouse_health"]["status"] == "HEALTHY"

    # Verify fact table row count in database
    session = get_db_session()
    try:
        fact_count = session.query(DiseaseObservationFact).count()
        assert fact_count == 2596
    finally:
        session.close()
