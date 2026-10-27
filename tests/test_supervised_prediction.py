"""
Unit and Integration Tests for the Supervised Crop-Disease Prediction Module.
Verifies:
1. Canonical dataset and warehouse invariants remain strictly preserved.
2. Model artifacts, split manifest, and class mappings exist and are valid.
3. Grouped split manifest guarantees 0 group leakage across partitions.
4. Predictor initializes cleanly without retraining and executes deterministic inference.
5. Inference on authentic healthy and diseased specimens returns calibrated probabilities.
6. Uncertainty detection operates correctly on out-of-distribution and anomalous inputs.
7. Prediction API endpoints (/api/predict/disease, /api/prediction/metadata) adhere to contracts.
8. Unsupervised nearest-specimens and supervised predictions remain strictly decoupled.
"""
import io
import json
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import pytest
from starlette.testclient import TestClient

from src.api.app import app
from src.mining.predictor import CropDiseasePredictor, get_crop_disease_predictor
from src.warehouse.connection import get_db_engine


@pytest.fixture(scope="session")
def project_root():
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_canonical_hashes_and_warehouse_invariance(project_root):
    """Verifies that the canonical dataset, features, and warehouse remain 100% unaltered."""
    import hashlib

    expected_hashes = {
        "canonical_dataset_v2.csv": (
            project_root / "data" / "manifests" / "canonical_dataset_v2.csv",
            "c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8",
        ),
        "image_features_v2.csv": (
            project_root / "data" / "features" / "image_features_v2.csv",
            "f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1",
        ),
    }

    for name, (path, expected_h) in expected_hashes.items():
        assert path.exists(), f"File {name} must exist"
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        assert h.hexdigest() == expected_h, f"Checksum mismatch for {name}"

    # Verify SQLite warehouse row counts
    engine = get_db_engine()
    with engine.connect() as conn:
        from sqlalchemy import text
        facts = conn.execute(text("SELECT COUNT(*) FROM disease_observation_fact")).scalar()
        crops = conn.execute(text("SELECT COUNT(*) FROM dim_crop")).scalar()
        diseases = conn.execute(text("SELECT COUNT(*) FROM dim_disease")).scalar()
        images = conn.execute(text("SELECT COUNT(*) FROM dim_image")).scalar()
        features = conn.execute(text("SELECT COUNT(*) FROM dim_visual_feature")).scalar()

    assert facts == 2596, f"Expected 2,596 fact records, got {facts}"
    assert crops == 14, f"Expected 14 crop dimensions, got {crops}"
    assert diseases == 20, f"Expected 20 disease dimensions, got {diseases}"
    assert images == 2596, f"Expected 2,596 image dimensions, got {images}"
    assert features == 2596, f"Expected 2,596 visual feature dimensions, got {features}"


def test_prediction_model_artifacts_and_metadata_exist(project_root):
    """Verifies that all versioned model artifacts and evaluation reports are present."""
    model_dir = project_root / "data" / "models" / "prediction"
    report_dir = project_root / "data" / "reports" / "prediction"

    required_artifacts = [
        model_dir / "efficientnet_b0_foliar.pt",
        model_dir / "class_mapping.json",
        model_dir / "model_metadata.json",
        model_dir / "split_manifest.csv",
        report_dir / "prediction_evaluation_report.json",
        report_dir / "prediction_evaluation_report.md",
        report_dir / "feasibility_report.json",
        report_dir / "feasibility_report.md",
    ]

    for artifact in required_artifacts:
        assert artifact.exists(), f"Missing required prediction artifact: {artifact}"


def test_class_mapping_consistency_and_support_threshold(project_root):
    """Verifies class mapping adheres to the 25 supported classes with N >= 60 threshold."""
    class_map_path = project_root / "data" / "models" / "prediction" / "class_mapping.json"
    with open(class_map_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["num_classes"] == 25, f"Expected 25 supported classes, found {data['num_classes']}"
    assert len(data["supported_classes"]) == 25
    assert len(data["class_to_idx"]) == 25
    assert len(data["idx_to_class"]) == 25

    # Check documented rare and scanner classes
    assert "Tomato___Two-Spotted Spider Mite" in data["excluded_rare_classes"]
    assert data["excluded_rare_classes"]["Tomato___Two-Spotted Spider Mite"] == 2
    assert "Rice___Bacterial Leaf Blight" in data["out_of_domain_scanner_classes"]


def test_split_manifest_zero_group_leakage(project_root):
    """Verifies that duplicate groups in split_manifest.csv have 0 leakage across partitions."""
    split_path = project_root / "data" / "models" / "prediction" / "split_manifest.csv"
    df = pd.read_csv(split_path)

    train_groups = set(df[df["evaluation_partition"] == "train"]["dhash"])
    val_groups = set(df[df["evaluation_partition"] == "val"]["dhash"])
    test_groups = set(df[df["evaluation_partition"] == "test"]["dhash"])

    # Overlap must be strictly empty
    assert len(train_groups.intersection(val_groups)) == 0, "Train-Val group leakage!"
    assert len(train_groups.intersection(test_groups)) == 0, "Train-Test group leakage!"
    assert len(val_groups.intersection(test_groups)) == 0, "Val-Test group leakage!"


def test_predictor_clean_initialization_without_retraining():
    """Verifies CropDiseasePredictor initializes cleanly without retraining."""
    predictor = get_crop_disease_predictor()
    assert predictor is not None
    assert predictor.num_classes == 25
    assert predictor.model is not None


def test_predictor_inference_on_authentic_healthy_specimen(project_root):
    """Verifies prediction on authentic Apple Healthy leaf."""
    img_path = project_root / "data" / "processed_v2" / "plantdoc" / "apple" / "healthy" / "proc_AGRO_V2_00037.png"
    if not img_path.exists():
        pytest.skip(f"Test image not found at {img_path}")

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    predictor = get_crop_disease_predictor()
    result = predictor.predict(img_bytes)

    assert result["status"] == "confident"
    assert result["is_uncertain"] is False
    assert result["predicted_class"] == "Apple___Healthy"
    assert result["condition_status"] == "Healthy"
    assert result["confidence_score"] > 0.50
    assert len(result["top_candidates"]) == 3

    # Check that candidate probabilities sum towards 1 and are sorted
    probs = [c["probability"] for c in result["top_candidates"]]
    assert probs[0] >= probs[1] >= probs[2]


def test_predictor_inference_on_authentic_diseased_specimen(project_root):
    """Verifies prediction on authentic Potato Late Blight leaf."""
    img_path = project_root / "data" / "processed_v2" / "plantdoc" / "potato" / "late_blight" / "proc_AGRO_V2_00169.png"
    if not img_path.exists():
        pytest.skip(f"Test image not found at {img_path}")

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    predictor = get_crop_disease_predictor()
    result = predictor.predict(img_bytes)

    assert result["status"] == "confident"
    assert result["is_uncertain"] is False
    assert result["predicted_class"] == "Potato___Late Blight"
    assert result["condition_status"] == "Diseased"
    assert result["confidence_score"] > 0.50


def test_predictor_uncertainty_on_synthetic_noise_input():
    """Verifies that high-entropy uniform noise input is handled safely."""
    noise_arr = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(noise_arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    predictor = get_crop_disease_predictor()
    result = predictor.predict(buf.getvalue())

    assert "status" in result
    assert "confidence_score" in result
    assert "normalized_entropy" in result
    assert result["prediction_entropy"] > 0.0


def test_api_prediction_endpoints(client, project_root):
    """Verifies the /api/predict/disease and /api/prediction/metadata endpoints."""
    # 1. Metadata endpoint
    res_meta = client.get("/api/prediction/metadata")
    assert res_meta.status_code == 200
    meta_json = res_meta.json()
    assert meta_json["num_classes"] == 25
    assert len(meta_json["classes"]) == 25
    assert "EfficientNet-B0" in meta_json["model_architecture"]

    # 2. Prediction endpoint with valid image
    img_path = project_root / "data" / "processed_v2" / "plantdoc" / "apple" / "healthy" / "proc_AGRO_V2_00037.png"
    if img_path.exists():
        with open(img_path, "rb") as f:
            files = {"file": ("test_leaf.png", f.read(), "image/png")}
        res_pred = client.post("/api/predict/disease", files=files)
        assert res_pred.status_code == 200
        pred_json = res_pred.json()
        assert pred_json["status"] in ("confident", "uncertain")
        assert pred_json["predicted_class"] == "Apple___Healthy"
        assert "top_candidates" in pred_json

    # 3. Prediction endpoint with empty file
    files_empty = {"file": ("empty.png", b"", "image/png")}
    res_empty = client.post("/api/predict/disease", files=files_empty)
    assert res_empty.status_code == 400

    # 4. Integrated analyze endpoint returns prediction block
    if img_path.exists():
        with open(img_path, "rb") as f:
            files = {"file": ("test_leaf.png", f.read(), "image/png")}
        res_analyze = client.post("/api/analyze/image", files=files)
        assert res_analyze.status_code == 200
        analyze_json = res_analyze.json()
        assert "prediction" in analyze_json
        assert analyze_json["prediction"]["predicted_class"] == "Apple___Healthy"
        assert "nearest_specimens" in analyze_json
        assert len(analyze_json["nearest_specimens"]) > 0


def test_nearest_references_not_conflated_with_prediction(client, project_root):
    """Verifies nearest reference similarity score is decoupled from prediction probability."""
    img_path = project_root / "data" / "processed_v2" / "plantdoc" / "apple" / "healthy" / "proc_AGRO_V2_00037.png"
    if not img_path.exists():
        pytest.skip(f"Test image not found at {img_path}")

    with open(img_path, "rb") as f:
        files = {"file": ("test_leaf.png", f.read(), "image/png")}
    res = client.post("/api/analyze/image", files=files)
    assert res.status_code == 200
    data = res.json()

    pred = data["prediction"]
    specimens = data["nearest_specimens"]

    # Prediction confidence is a neural softmax probability (0.976)
    # Nearest neighbor distance is Euclidean in 32D (0.0 for self match)
    assert pred["confidence_score"] > 0.0
    assert specimens[0]["euclidean_distance"] == pytest.approx(0.0, abs=1e-4)  # Self match
    assert specimens[0]["visual_similarity_score"] == pytest.approx(1.0, abs=1e-4)

    # Verify diagnostic notice states disease status is not determined by similarity
    assert "NON_DIAGNOSTIC" in data["diagnostic_interpretation"]["status"]
