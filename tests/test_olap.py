import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.olap.engine import OLAPEngine
from src.warehouse.models import (
    Base, DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact
)

@pytest.fixture
def olap_test_engine():
    """
    Creates an isolated in-memory SQLite database populated with minimal test fixtures
    strictly for unit testing OLAP queries, adhering to academic unit test standards.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Dimensions
    c_rice = DimCrop(crop_code="RICE", crop_name="Rice", botanical_name="Oryza sativa", crop_category="Cereal")
    c_wheat = DimCrop(crop_code="WHEAT", crop_name="Wheat", botanical_name="Triticum aestivum", crop_category="Cereal")
    c_cotton = DimCrop(crop_code="COTTON", crop_name="Cotton", botanical_name="Gossypium hirsutum", crop_category="Fiber")
    session.add_all([c_rice, c_wheat, c_cotton])
    session.flush()

    d_blast = DimDisease(disease_code="BLAST", disease_name="Blast", pathogen_type="Fungal", causal_agent="Magnaporthe oryzae")
    d_blight = DimDisease(disease_code="BACTERIAL_BLIGHT", disease_name="Bacterial Blight", pathogen_type="Bacterial", causal_agent="Xanthomonas oryzae")
    d_healthy = DimDisease(disease_code="HEALTHY", disease_name="Healthy", pathogen_type="None", causal_agent="None")
    session.add_all([d_blast, d_blight, d_healthy])
    session.flush()

    img1 = DimImage(
        image_id="RAW_001", raw_id="RAW_001", filename="img1.jpg", file_format="JPG",
        raw_width=512, raw_height=512, raw_channels=3, raw_size_kb=100.0,
        processed_width=256, processed_height=256, processed_size_kb=45.0,
        md5_hash="h1", original_path="/raw/1", processed_path="/proc/1"
    )
    img2 = DimImage(
        image_id="RAW_002", raw_id="RAW_002", filename="img2.jpg", file_format="JPG",
        raw_width=512, raw_height=512, raw_channels=3, raw_size_kb=105.0,
        processed_width=256, processed_height=256, processed_size_kb=48.0,
        md5_hash="h2", original_path="/raw/2", processed_path="/proc/2"
    )
    session.add_all([img1, img2])
    session.flush()

    vf1 = DimVisualFeature(
        image_id="RAW_001",
        image_filename="img1.jpg", rgb_r_mean=50.0, rgb_g_mean=120.0, rgb_b_mean=40.0,
        rgb_r_std=10.0, rgb_g_std=15.0, rgb_b_std=8.0, rgb_r_norm=0.24, rgb_g_norm=0.57, rgb_b_norm=0.19,
        hsv_h_mean=80.0, hsv_s_mean=0.6, hsv_v_mean=0.5, hsv_h_norm=0.22, hsv_s_norm=0.6, hsv_v_norm=0.5,
        exg_index_mean=150.0, dominant_color_tone="Foliar_Green",
        glcm_contrast=0.15, glcm_contrast_norm=0.00067, glcm_dissimilarity=0.1, glcm_homogeneity=0.9, glcm_energy=0.7,
        glcm_correlation=0.8, glcm_asm=0.7, has_valid_contour=True, contour_area=150.0,
        contour_perimeter=45.0, contour_aspect_ratio=1.0, contour_circularity=0.8, contour_solidity=0.9,
        lesion_coverage_ratio=0.08
    )
    vf2 = DimVisualFeature(
        image_id="RAW_002",
        image_filename="img2.jpg", rgb_r_mean=60.0, rgb_g_mean=110.0, rgb_b_mean=35.0,
        rgb_r_std=12.0, rgb_g_std=14.0, rgb_b_std=9.0, rgb_r_norm=0.29, rgb_g_norm=0.54, rgb_b_norm=0.17,
        hsv_h_mean=75.0, hsv_s_mean=0.55, hsv_v_mean=0.48, hsv_h_norm=0.21, hsv_s_norm=0.55, hsv_v_norm=0.48,
        exg_index_mean=125.0, dominant_color_tone="Foliar_Green",
        glcm_contrast=0.22, glcm_contrast_norm=0.00098, glcm_dissimilarity=0.14, glcm_homogeneity=0.85, glcm_energy=0.65,
        glcm_correlation=0.75, glcm_asm=0.65, has_valid_contour=True, contour_area=210.0,
        contour_perimeter=55.0, contour_aspect_ratio=1.1, contour_circularity=0.75, contour_solidity=0.85,
        lesion_coverage_ratio=0.12
    )
    session.add_all([vf1, vf2])
    session.flush()

    # Facts
    f1 = DiseaseObservationFact(
        image_id="RAW_001",
        crop_key=c_rice.crop_key, disease_key=d_blast.disease_key,
        image_key=img1.image_key, feature_key=vf1.feature_key, observation_count=1,
        lesion_severity_score=6.5, image_sharpness_score=150.0, lesion_coverage_ratio=0.08,
        texture_contrast_norm=0.00067, processing_latency_ms=12.0,
        etl_batch_id="TEST_BATCH"
    )
    f2 = DiseaseObservationFact(
        image_id="RAW_002",
        crop_key=c_rice.crop_key, disease_key=d_blight.disease_key,
        image_key=img2.image_key, feature_key=vf2.feature_key, observation_count=1,
        lesion_severity_score=7.0, image_sharpness_score=145.0, lesion_coverage_ratio=0.12,
        texture_contrast_norm=0.00098, processing_latency_ms=14.0,
        etl_batch_id="TEST_BATCH"
    )
    session.add_all([f1, f2])
    session.commit()
    session.close()

    return engine

@pytest.fixture
def olap(olap_test_engine):
    return OLAPEngine(engine=olap_test_engine)

def test_olap_rollup(olap):
    res = olap.rollup()
    assert res["operation"] == "ROLL-UP"
    assert "data" in res
    assert "sql" in res
    assert len(res["data"]) > 0
    assert "crop_category" in res["data"].columns
    assert "total_observations" in res["data"].columns

def test_olap_drilldown(olap):
    res = olap.drilldown()
    assert res["operation"] == "DRILL-DOWN"
    assert "data" in res
    assert len(res["data"]) > 0
    assert "crop_name" in res["data"].columns
    assert "disease_name" in res["data"].columns


def test_olap_true_drilldown(olap):
    res = olap.true_drilldown()
    assert res["operation"] == "TRUE OLAP DRILL-DOWN"
    assert "data" in res
    assert len(res["data"]) > 0
    assert "pathogen_type" in res["data"].columns
    assert "disease_name" in res["data"].columns


def test_olap_slice_by_crop(olap):
    res = olap.slice_by_crop("Rice")
    assert res["operation"] == "SLICE"
    assert "data" in res
    assert len(res["data"]) > 0
    assert "disease_name" in res["data"].columns
    assert "disease_observations" in res["data"].columns

def test_olap_dice(olap):
    res = olap.dice(
        selected_crops=["Rice", "Wheat"],
        selected_pathogens=["Fungal", "Bacterial"],
        min_contrast=0.0
    )
    assert res["operation"] == "DICE"
    assert "data" in res
    assert len(res["data"]) > 0
    assert "crop_name" in res["data"].columns

def test_olap_pivot(olap):
    res = olap.pivot(measure="observation_count")
    assert res["operation"] == "PIVOT"
    assert "data" in res
    assert "Crop" in res["data"].columns
    assert "Fungal" in res["data"].columns
    assert "Bacterial" in res["data"].columns
