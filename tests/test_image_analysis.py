"""Tests for Image Analysis Inference Endpoint and Pipeline.

Verifies:
- File format validation (JPG, JPEG, PNG allowed; others rejected).
- Corrupted file and empty file rejection.
- Exact 32-feature extraction matching frozen categories.
- Scaling consistency using frozen StandardScaler.
- Cluster assignment for K=2 and K=4.
- Nearest reference specimen retrieval.
- Scientific disclaimers (disease classification UNAVAILABLE).
- Complete invariance of frozen dataset manifests and feature store SHA-256 hashes.
"""
import hashlib
import io
from pathlib import Path
from PIL import Image
import pytest
from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)

ROOT_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT_DIR / "data" / "manifests" / "canonical_dataset_v2.csv"
FEATURES_PATH = ROOT_DIR / "data" / "features" / "image_features_v2.csv"

CANONICAL_EXPECTED_SHA256 = "c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8"
FEATURES_EXPECTED_SHA256 = "f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1"


def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def create_test_image(size=(300, 300), color=(60, 150, 45), format="JPEG") -> bytes:
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def test_valid_jpeg_analysis_workflow():
    """Verify successful analysis of valid JPEG specimen."""
    raw_bytes = create_test_image(size=(320, 240), color=(50, 160, 40), format="JPEG")
    files = {"file": ("test_leaf.jpg", raw_bytes, "image/jpeg")}

    response = client.post("/api/analyze/image", files=files)
    assert response.status_code == 200, response.text
    data = response.json()

    # Preprocessing validation
    assert data["validation"]["is_valid"] is True
    assert data["validation"]["format"] == "JPEG"
    assert data["validation"]["processed_width"] == 256
    assert data["validation"]["processed_height"] == 256

    # Feature counts
    assert data["feature_counts"]["total_continuous_features"] == 32
    assert data["feature_counts"]["color_moments"] == 19
    assert data["feature_counts"]["glcm_texture"] == 7
    assert data["feature_counts"]["contour_morphology"] == 6

    # Cluster assignments
    assert data["clustering"]["k2"]["cluster_id"] in (0, 1)
    assert data["clustering"]["k4"]["cluster_id"] in (0, 1, 2, 3)

    # PCA coordinates
    assert "x" in data["pca_projection"]
    assert "y" in data["pca_projection"]
    assert data["pca_projection"]["total_explained_pct"] == 52.1

    # Nearest reference specimens
    assert len(data["nearest_specimens"]) == 6
    top_specimen = data["nearest_specimens"][0]
    assert "image_id" in top_specimen
    assert top_specimen["image_id"].startswith("AGRO_V2_")
    assert top_specimen["euclidean_distance"] > 0
    assert 0.0 < top_specimen["visual_similarity_score"] <= 1.0
    assert top_specimen["pathogen_type"] != "nan"

    # Scientific caveats
    assert data["scientific_caveats"]["disease_classification"] == "UNAVAILABLE"
    assert "NOT implemented" in data["scientific_caveats"]["classification_disclosure"]


def test_valid_png_analysis():
    """Verify PNG format support."""
    raw_bytes = create_test_image(size=(256, 256), color=(100, 180, 70), format="PNG")
    files = {"file": ("foliage_sample.png", raw_bytes, "image/png")}

    response = client.post("/api/analyze/image", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["validation"]["is_valid"] is True
    assert data["validation"]["format"] == "PNG"


def test_empty_file_rejected():
    """Verify 400 Bad Request on empty file."""
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/api/analyze/image", files=files)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_unsupported_extension_rejected():
    """Verify rejection of disallowed file formats (e.g. .txt, .pdf, .gif)."""
    files = {"file": ("document.txt", b"not an image", "text/plain")}
    response = client.post("/api/analyze/image", files=files)
    assert response.status_code == 400
    assert "unsupported file format" in response.json()["detail"].lower()


def test_corrupted_file_rejected():
    """Verify rejection of corrupted image stream."""
    corrupted_bytes = b"\xff\xd8\xff\xe0" + b"random corrupted garbage data bytes"
    files = {"file": ("corrupt.jpg", corrupted_bytes, "image/jpeg")}
    response = client.post("/api/analyze/image", files=files)
    assert response.status_code == 400
    assert "corrupted" in response.json()["detail"].lower() or "decoding failed" in response.json()["detail"].lower()


def test_frozen_dataset_invariance_after_uploads():
    """Confirm that image upload and analysis does NOT alter frozen CSV files."""
    initial_manifest_hash = get_file_sha256(MANIFEST_PATH)
    initial_features_hash = get_file_sha256(FEATURES_PATH)

    assert initial_manifest_hash == CANONICAL_EXPECTED_SHA256
    assert initial_features_hash == FEATURES_EXPECTED_SHA256

    # Execute multiple analysis requests
    for i in range(3):
        raw_bytes = create_test_image(color=(40 + i * 20, 100 + i * 10, 30))
        res = client.post("/api/analyze/image", files={"file": (f"test_{i}.jpg", raw_bytes, "image/jpeg")})
        assert res.status_code == 200

    # Verify checksums remain perfectly unchanged
    post_manifest_hash = get_file_sha256(MANIFEST_PATH)
    post_features_hash = get_file_sha256(FEATURES_PATH)

    assert post_manifest_hash == CANONICAL_EXPECTED_SHA256, "Manifest was mutated!"
    assert post_features_hash == FEATURES_EXPECTED_SHA256, "Feature store was mutated!"


def test_grayscale_and_rgba_images_handling():
    """Verify that Grayscale ('L') and RGBA images are converted safely without error."""
    # 1. Grayscale image
    gray_img = Image.new("L", (200, 200), color=128)
    buf_gray = io.BytesIO()
    gray_img.save(buf_gray, format="PNG")
    res_gray = client.post("/api/analyze/image", files={"file": ("gray.png", buf_gray.getvalue(), "image/png")})
    assert res_gray.status_code == 200
    data_gray = res_gray.json()
    assert data_gray["validation"]["is_valid"] is True
    assert data_gray["validation"]["original_color_mode"] == "L"
    assert data_gray["validation"]["color_space"] == "RGB"

    # 2. RGBA image with alpha transparency
    rgba_img = Image.new("RGBA", (200, 200), color=(50, 150, 50, 180))
    buf_rgba = io.BytesIO()
    rgba_img.save(buf_rgba, format="PNG")
    res_rgba = client.post("/api/analyze/image", files={"file": ("transparent.png", buf_rgba.getvalue(), "image/png")})
    assert res_rgba.status_code == 200
    data_rgba = res_rgba.json()
    assert data_rgba["validation"]["is_valid"] is True
    assert data_rgba["validation"]["original_color_mode"] == "RGBA"
    assert data_rgba["validation"]["color_space"] == "RGB"


def test_raw_vs_standardized_features_distinction():
    """Verify raw descriptors in natural units vs standardized z-scores."""
    raw_bytes = create_test_image(size=(256, 256), color=(80, 140, 60), format="JPEG")
    res = client.post("/api/analyze/image", files={"file": ("test_features.jpg", raw_bytes, "image/jpeg")})
    assert res.status_code == 200
    data = res.json()

    assert "features_raw" in data
    assert "features_standardized" in data
    assert "feature_definitions" in data

    # Raw features should have natural scale (e.g. RGB red mean around 80)
    raw_r = data["features_raw"]["rgb_r_mean"]
    assert 60 <= raw_r <= 100, f"Unexpected raw_r value: {raw_r}"

    # Standardized features should be z-score (centered around 0, typically -3 to +3)
    std_r = data["features_standardized"]["rgb_r_mean"]
    assert -4.0 <= std_r <= 4.0, f"Unexpected std_r z-score: {std_r}"

    # Check definitions metadata
    assert "rgb_r_mean" in data["feature_definitions"]
    assert data["feature_definitions"]["rgb_r_mean"]["range"] == "[0, 255]"


def test_exact_nearest_neighbor_ranking():
    """Verify that nearest neighbor specimens are strictly ordered by ascending Euclidean distance."""
    raw_bytes = create_test_image(size=(256, 256), color=(70, 120, 50), format="JPEG")
    res = client.post("/api/analyze/image", files={"file": ("test_ranking.jpg", raw_bytes, "image/jpeg")})
    assert res.status_code == 200
    data = res.json()

    neighbors = data["nearest_specimens"]
    assert len(neighbors) == 6

    # Verify monotonic increasing distance
    distances = [n["euclidean_distance"] for n in neighbors]
    assert distances == sorted(distances), f"Distances not sorted ascending: {distances}"

    # Verify heuristic similarity score formula: sim = 1 / (1 + dist)
    for n in neighbors:
        expected_sim = round(1.0 / (1.0 + n["euclidean_distance"]), 4)
        assert abs(n["visual_similarity_score"] - expected_sim) < 1e-3

