from pathlib import Path
import pytest
import numpy as np
from PIL import Image

from src.feature_extraction.color_features import extract_color_features
from src.feature_extraction.texture_features import extract_texture_features
from src.feature_extraction.shape_features import extract_shape_features
from src.feature_extraction.pipeline import ClassicalFeatureExtractor, FeatureExtractionPipeline, FEATURE_DICTIONARY


def test_color_feature_ranges_and_normalization():
    # Green foliar image
    img = Image.new("RGB", (64, 64), color=(30, 180, 45))
    feats = extract_color_features(img)

    # Check bounds
    assert 0.0 <= feats["rgb_r_norm"] <= 1.0
    assert 0.0 <= feats["rgb_g_norm"] <= 1.0
    assert 0.0 <= feats["rgb_b_norm"] <= 1.0
    assert 0.0 <= feats["hsv_h_norm"] <= 1.0
    assert 0.0 <= feats["hsv_s_norm"] <= 1.0
    assert 0.0 <= feats["hsv_v_norm"] <= 1.0

    # Chlorophyll index verification
    assert feats["exg_index_mean"] > 0
    assert feats["dominant_color_tone"] == "Foliar_Green"


def test_glcm_texture_normalization_and_properties():
    # Uniform image: contrast should be 0, homogeneity 1
    arr_uniform = np.ones((64, 64), dtype=np.uint8) * 128
    img_uniform = Image.fromarray(arr_uniform, mode="L")
    feats_uniform = extract_texture_features(img_uniform)

    assert feats_uniform["glcm_contrast"] == 0.0
    assert feats_uniform["glcm_contrast_norm"] == 0.0
    assert feats_uniform["glcm_homogeneity"] == 1.0

    # High contrast checkered pattern
    arr_checkered = np.zeros((64, 64), dtype=np.uint8)
    arr_checkered[::2, ::2] = 255
    arr_checkered[1::2, 1::2] = 255
    img_checkered = Image.fromarray(arr_checkered, mode="L")
    feats_checkered = extract_texture_features(img_checkered)

    assert feats_checkered["glcm_contrast"] > 0.0
    assert 0.0 <= feats_checkered["glcm_contrast_norm"] <= 1.0
    assert 0.0 <= feats_checkered["glcm_energy"] <= 1.0
    assert -1.0 <= feats_checkered["glcm_correlation"] <= 1.0


def test_shape_descriptors_with_circular_lesion():
    arr = np.ones((128, 128), dtype=np.uint8) * 220
    y, x = np.ogrid[:128, :128]
    # Circular spot in center
    mask = ((x - 64) ** 2 + (y - 64) ** 2) <= 16 ** 2
    arr[mask] = 30
    img = Image.fromarray(arr, mode="L")

    feats = extract_shape_features(img)
    assert feats["has_valid_contour"] is True
    assert feats["contour_area"] > 0
    assert 0.0 < feats["contour_circularity"] <= 1.0
    assert 0.0 < feats["contour_solidity"] <= 1.0
    assert 0.0 < feats["lesion_coverage_ratio"] < 1.0


def test_feature_pipeline_traceability(tmp_path):
    proc_dir = tmp_path / "processed"
    features_dir = tmp_path / "features"
    proc_dir.mkdir(parents=True)
    features_dir.mkdir(parents=True)

    img_path = proc_dir / "proc_leaf.png"
    Image.new("RGB", (64, 64), color=(40, 140, 30)).save(img_path)

    pipeline = FeatureExtractionPipeline()
    pipeline.features_dir = features_dir

    records = [{
        "raw_id": "RAW_TEST_001",
        "filename": "leaf.jpg",
        "raw_path": "/data/raw/leaf.jpg",
        "processed_path": str(img_path),
        "crop_label": "rice",
        "condition_label": "blast",
        "disease_label": "blast",
        "pest_label": "none",
        "is_pest": False,
        "md5_hash": "test_md5_hash_123"
    }]

    results = pipeline.run_pipeline(records)

    assert len(results) == 1
    row = results[0]
    # Verify strict traceability back to Image_ID and source metadata
    assert row["image_id"] == "RAW_TEST_001"
    assert row["filename"] == "leaf.jpg"
    assert row["raw_path"] == "/data/raw/leaf.jpg"
    assert row["md5_hash"] == "test_md5_hash_123"
    assert "glcm_contrast_norm" in row
    assert "rgb_r_norm" in row

    # Verify CSV and dictionary outputs
    assert (features_dir / "image_features.csv").exists()
    assert (features_dir / "feature_dictionary.json").exists()


def test_feature_dictionary_completeness():
    assert "rgb_r_mean" in FEATURE_DICTIONARY
    assert "glcm_contrast" in FEATURE_DICTIONARY
    assert "glcm_homogeneity" in FEATURE_DICTIONARY
    assert "contour_circularity" in FEATURE_DICTIONARY
    assert "image_id" in FEATURE_DICTIONARY
    for k, meta in FEATURE_DICTIONARY.items():
        assert "category" in meta
        assert "description" in meta
