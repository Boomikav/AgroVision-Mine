"""API Integration and Analytical Validation Test Suite for AgroVision-Mine.

Verifies FastAPI adapter endpoints against the real SQLite warehouse,
frozen dataset v2 manifests, feature store, and unsupervised mining models.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from src.api.app import (
    app,
    CANONICAL_EXPECTED_SHA256,
    FEATURES_EXPECTED_SHA256,
    MANIFEST_FILE,
    FEATURES_FILE,
)

client = TestClient(app)


def test_frozen_dataset_checksum_invariance():
    """Verify that canonical manifest and feature store checksums have not been altered."""
    assert MANIFEST_FILE.exists(), f"Missing {MANIFEST_FILE}"
    assert FEATURES_FILE.exists(), f"Missing {FEATURES_FILE}"

    with open(MANIFEST_FILE, "rb") as f:
        manifest_hash = hashlib.sha256(f.read()).hexdigest()
    assert manifest_hash == CANONICAL_EXPECTED_SHA256, (
        f"Manifest checksum mismatch: got {manifest_hash}, expected {CANONICAL_EXPECTED_SHA256}"
    )

    with open(FEATURES_FILE, "rb") as f:
        features_hash = hashlib.sha256(f.read()).hexdigest()
    assert features_hash == FEATURES_EXPECTED_SHA256, (
        f"Features checksum mismatch: got {features_hash}, expected {FEATURES_EXPECTED_SHA256}"
    )


def test_api_health_endpoint():
    """Verify /api/health endpoint returns verified status and 2,596 records."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["records_count"] == 2596
    assert data["manifest_sha256_verified"] is True
    assert data["features_sha256_verified"] is True


def test_overview_endpoint():
    """Verify /api/overview returns authentic dataset and mining telemetry."""
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["corpus_size"] == 2596
    assert data["taxa_count"] == 14
    assert data["pathological_status"]["diseased"] == 1750
    assert data["pathological_status"]["healthy"] == 846
    assert data["sources"]["plantdoc"] == 2560
    assert data["sources"]["icar_ogd"] == 36
    assert data["feature_dimensions"]["continuous_count"] == 32
    assert data["clustering_summary"]["metric_supported_k"] == 2
    assert round(data["clustering_summary"]["k2_silhouette"], 4) == 0.4060
    assert round(data["clustering_summary"]["k4_silhouette"], 4) == 0.1651
    assert data["verification_status"]["verified"] is True


def test_dataset_pagination_and_filtering():
    """Verify pagination and dimensional slicer filtering on /api/dataset."""
    # Test default page
    res_default = client.get("/api/dataset?page=1&page_size=10")
    assert res_default.status_code == 200
    d_default = res_default.json()
    assert d_default["total_records"] == 2596
    assert len(d_default["records"]) == 10
    assert d_default["page"] == 1

    # Filter by Crop = Rice (ICAR source)
    res_rice = client.get("/api/dataset?crop=Rice")
    assert res_rice.status_code == 200
    d_rice = res_rice.json()
    assert d_rice["total_records"] == 36
    assert all(r["crop_name"] == "Rice" for r in d_rice["records"])

    # Filter by Crop = Tomato (PlantDoc source, 743 records)
    res_tomato = client.get("/api/dataset?crop=Tomato")
    assert res_tomato.status_code == 200
    d_tomato = res_tomato.json()
    assert d_tomato["total_records"] == 743
    assert all(r["crop_name"] == "Tomato" for r in d_tomato["records"])

    # Verify case-insensitive filtering for Tomato
    res_tomato_lower = client.get("/api/dataset?crop=tomato")
    assert res_tomato_lower.status_code == 200
    assert res_tomato_lower.json()["total_records"] == 743

    # Filter by Condition = Healthy
    res_healthy = client.get("/api/dataset?condition=Healthy")
    assert res_healthy.status_code == 200
    d_healthy = res_healthy.json()
    assert d_healthy["total_records"] == 846
    assert all(r["condition_status"] == "Healthy" for r in d_healthy["records"])

    # Filter by Search = AGRO_V2_00001
    res_search = client.get("/api/dataset?search=AGRO_V2_00001")
    assert res_search.status_code == 200
    d_search = res_search.json()
    assert d_search["total_records"] == 1
    assert d_search["records"][0]["image_id"] == "AGRO_V2_00001"


def test_specimen_detail_and_features():
    """Verify /api/dataset/{image_id} extracts 32 continuous descriptors and cluster keys."""
    response = client.get("/api/dataset/AGRO_V2_00001")
    assert response.status_code == 200
    data = response.json()
    assert data["image_id"] == "AGRO_V2_00001"
    assert data["crop_label"] == "Rice"
    assert "cluster_id_k2" in data
    assert "cluster_id_k4" in data
    assert "pca_coordinates" in data

    # Check that feature categories exist and sum to 32 continuous features
    total_features = (
        len(data["color_features"])
        + len(data["glcm_features"])
        + len(data["shape_features"])
    )
    assert total_features == 32, f"Expected 32 continuous features, got {total_features}"

    # Non-existent specimen returns 404
    res_404 = client.get("/api/dataset/NON_EXISTENT_ID")
    assert res_404.status_code == 404


def test_data_quality_endpoint():
    """Verify /api/data-quality returns freeze report and zero corruption rate."""
    response = client.get("/api/data-quality")
    assert response.status_code == 200
    data = response.json()
    assert data["dataset_freeze"]["version"] == "v2.0-frozen"
    assert data["dataset_freeze"]["total_records"] == 2596
    assert data["dataset_freeze"]["manifest_verified"] is True
    assert data["dataset_freeze"]["features_verified"] is True


def test_warehouse_schema_access():
    """Verify /api/warehouse/schema connects to real SQLite star schema."""
    response = client.get("/api/warehouse/schema")
    assert response.status_code == 200
    data = response.json()
    table_names = [t["table_name"] for t in data["tables"]]
    expected_tables = [
        "dim_crop",
        "dim_disease",
        "dim_image",
        "dim_visual_feature",
        "disease_observation_fact",
    ]
    for exp in expected_tables:
        assert exp in table_names, f"Expected table {exp} in warehouse schema"

    fact_table = next(t for t in data["tables"] if t["table_name"] == "disease_observation_fact")
    assert fact_table["row_count"] > 0
    assert fact_table["table_type"] == "Fact"


def test_olap_query_operations():
    """Verify all 5 OLAP operations return real SQL and records."""
    # 1. Roll-Up
    res_rollup = client.post("/api/olap/query", json={"operation": "rollup"})
    assert res_rollup.status_code == 200
    d_rollup = res_rollup.json()
    assert d_rollup["operation"] == "ROLL-UP"
    assert "SELECT" in d_rollup["sql"]
    assert d_rollup["row_count"] > 0
    assert d_rollup["latency_ms"] >= 0

    # 2. True Drill-Down
    res_drill = client.post("/api/olap/query", json={"operation": "true_drilldown"})
    assert res_drill.status_code == 200
    d_drill = res_drill.json()
    assert d_drill["operation"] == "TRUE OLAP DRILL-DOWN"
    assert d_drill["row_count"] > 0

    # 3. Slice by Crop
    res_slice = client.post("/api/olap/query", json={"operation": "slice_crop", "crop_name": "Rice"})
    assert res_slice.status_code == 200
    d_slice = res_slice.json()
    assert d_slice["operation"] == "SLICE"
    assert d_slice["row_count"] > 0

    # 4. Dice Sub-cube
    res_dice = client.post(
        "/api/olap/query",
        json={
            "operation": "dice",
            "selected_crops": ["Rice"],
            "selected_pathogens": ["Fungal", "Bacterial"],
            "min_contrast": 0.0,
        },
    )
    assert res_dice.status_code == 200
    d_dice = res_dice.json()
    assert d_dice["operation"] == "DICE"
    assert d_dice["row_count"] > 0

    # 5. Pivot
    res_pivot = client.post("/api/olap/query", json={"operation": "pivot"})
    assert res_pivot.status_code == 200
    d_pivot = res_pivot.json()
    assert d_pivot["operation"] == "PIVOT"
    assert d_pivot["row_count"] > 0


def test_clustering_dual_solution_switching():
    """Verify K=2 optimal vs K=4 exploratory solution metrics."""
    # K=2
    res_k2 = client.get("/api/mining/clustering?selected_k=2")
    assert res_k2.status_code == 200
    d_k2 = res_k2.json()
    assert d_k2["selected_k"] == 2
    assert d_k2["is_metric_optimal"] is True
    assert round(d_k2["solution_metrics"]["silhouette_score"], 4) == 0.4060
    assert len(d_k2["scatter_points"]) > 0

    # K=4
    res_k4 = client.get("/api/mining/clustering?selected_k=4")
    assert res_k4.status_code == 200
    d_k4 = res_k4.json()
    assert d_k4["selected_k"] == 4
    assert d_k4["is_metric_optimal"] is False
    assert round(d_k4["solution_metrics"]["silhouette_score"], 4) == 0.1651


def test_association_rules_mode_separation():
    """Verify Mode A (visual-only, 880 rules) is strictly separated from Mode B (labeled, 285 rules)."""
    # Mode A: Visual-Only
    res_a = client.get("/api/mining/association-rules?mode=visual&page=1&page_size=50")
    assert res_a.status_code == 200
    d_a = res_a.json()
    assert d_a["mode_id"] == "A"
    assert d_a["total_rules"] == 880
    assert d_a["methodological_warning"] is None
    assert d_a["algorithm_benchmark"]["output_verification"]["output_equivalence"] is True
    assert d_a["algorithm_benchmark"]["mode"] == "visual_only"
    assert d_a["algorithm_benchmark"]["unique_items_count"] == 36
    assert d_a["algorithm_benchmark"]["fpgrowth"]["frequent_itemsets_count"] == 223
    assert d_a["algorithm_benchmark"]["fpgrowth"]["rules_count"] == 880

    # Mode B: Label-Conditioned (Exploratory)
    res_b_all = client.get("/api/mining/association-rules?mode=labeled&min_lift=0.0&page=1&page_size=50")
    assert res_b_all.status_code == 200
    d_b_all = res_b_all.json()
    assert d_b_all["mode_id"] == "B"
    assert d_b_all["total_rules"] == 285
    assert d_b_all["methodological_warning"] is not None
    assert "ground-truth labels" in d_b_all["methodological_warning"].lower()
    assert d_b_all["algorithm_benchmark"]["mode"] == "labeled"
    assert d_b_all["algorithm_benchmark"]["unique_items_count"] == 57
    assert d_b_all["algorithm_benchmark"]["fpgrowth"]["frequent_itemsets_count"] == 387
    assert d_b_all["algorithm_benchmark"]["fpgrowth"]["rules_count"] == 1165
    assert d_b_all["algorithm_benchmark"]["fpgrowth"]["label_conditioned_rules_count"] == 285
    assert d_b_all["algorithm_benchmark"]["output_verification"]["output_equivalence"] is True

    # Filtered by lift >= 1.0
    res_b_filt = client.get("/api/mining/association-rules?mode=labeled&page=1&page_size=50")
    assert res_b_filt.status_code == 200
    assert res_b_filt.json()["total_rules"] == 276


def test_reports_catalog_and_content():
    """Verify /api/reports catalog and content endpoints."""
    res_cat = client.get("/api/reports")
    assert res_cat.status_code == 200
    d_cat = res_cat.json()
    report_ids = [r["id"] for r in d_cat["available_reports"]]
    assert "review2_evaluation" in report_ids
    assert "clustering_report" in report_ids
    assert "association_report" in report_ids

    # Fetch specific report
    res_rep = client.get("/api/reports/review2_evaluation")
    assert res_rep.status_code == 200
    assert "evaluation_title" in res_rep.json()
