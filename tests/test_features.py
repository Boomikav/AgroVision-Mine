import numpy as np
import pytest
from PIL import Image
from src.feature_extraction.color_features import extract_color_features
from src.feature_extraction.texture_features import extract_texture_features
from src.feature_extraction.shape_features import extract_shape_features
from src.feature_extraction.pipeline import ClassicalFeatureExtractor

def test_extract_color_features():
    # Green image
    img = Image.new("RGB", (64, 64), color=(0, 200, 0))
    feats = extract_color_features(img)

    assert "rgb_r_mean" in feats
    assert "rgb_g_mean" in feats
    assert "hsv_h_mean" in feats
    assert feats["rgb_g_mean"] > feats["rgb_r_mean"]
    assert feats["dominant_color_tone"] == "Foliar_Green"

def test_extract_texture_features():
    # Checkered pattern for non-zero contrast
    arr = np.zeros((64, 64), dtype=np.uint8)
    arr[::2, ::2] = 255
    arr[1::2, 1::2] = 255
    img = Image.fromarray(arr, mode="L")

    feats = extract_texture_features(img)
    assert "glcm_contrast" in feats
    assert "glcm_homogeneity" in feats
    assert "glcm_energy" in feats
    assert feats["glcm_contrast"] >= 0.0

def test_extract_shape_features():
    # Image with distinct dark circle in center
    arr = np.ones((100, 100), dtype=np.uint8) * 200
    y, x = np.ogrid[:100, :100]
    mask = ((x - 50) ** 2 + (y - 50) ** 2) <= 20 ** 2
    arr[mask] = 20
    img = Image.fromarray(arr, mode="L")

    feats = extract_shape_features(img)
    assert feats["has_valid_contour"] is True
    assert feats["contour_area"] > 0
    assert 0.0 <= feats["contour_circularity"] <= 1.0

def test_classical_feature_pipeline_combined():
    img = Image.new("RGB", (64, 64), color=(40, 140, 40))
    extractor = ClassicalFeatureExtractor()
    combined = extractor.extract(img)

    expected_keys = [
        "rgb_r_mean", "rgb_g_mean", "glcm_contrast",
        "glcm_homogeneity", "has_valid_contour"
    ]
    for key in expected_keys:
        assert key in combined
