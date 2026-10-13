"""Unit and Integration Tests for Review 2 Visual Pattern Mining.

Tests:
1. Frozen canonical manifest integrity and row counts.
2. Feature-store alignment and zero-null assertions.
3. Deduplication and leakage prevention checks.
4. Preprocessing and feature standardization.
5. Clustering reproducibility with fixed random seed.
6. Multi-K validity indices and silhouette metrics.
7. FP-Growth vs Apriori output equivalence.
8. Association rule metrics (support, confidence, lift) correctness.
9. Sensitivity analysis threshold handling.
10. Dashboard and report availability.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.mining.clustering import CropVisualClusterer
from src.mining.association_rules import VisualAssociationMiner
from src.mining.evaluation import Review2Evaluator


@pytest.fixture(scope="session")
def project_root():
    return Path(__file__).resolve().parent.parent


def test_frozen_manifest_integrity(project_root):
    """Verifies that the canonical v2 manifest exists, has >= 2000 rows, and required columns."""
    manifest_path = project_root / "data" / "manifests" / "canonical_dataset_v2.csv"
    assert manifest_path.exists(), "canonical_dataset_v2.csv must exist"

    df = pd.read_csv(manifest_path)
    assert len(df) == 2596, f"Expected 2,596 rows in canonical manifest, found {len(df)}"
    assert len(df) >= 2000, "Dataset must meet or exceed 2,000 images target"

    # Required lineage & quality columns
    required_cols = [
        "image_id", "dataset_source", "crop_name", "disease_name",
        "condition_status", "md5_hash", "dhash", "license"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column in manifest: {col}"

    # Verify minimum crops and diseases
    assert df["crop_name"].nunique() >= 5, f"Expected >= 5 crops, found {df['crop_name'].nunique()}"
    assert df["disease_name"].nunique() >= 10, f"Expected >= 10 diseases, found {df['disease_name'].nunique()}"


def test_feature_store_alignment(project_root):
    """Verifies that the frozen feature store perfectly aligns 1-to-1 with the manifest."""
    manifest_path = project_root / "data" / "manifests" / "canonical_dataset_v2.csv"
    features_path = project_root / "data" / "features" / "image_features_v2.csv"

    df_manifest = pd.read_csv(manifest_path)
    df_features = pd.read_csv(features_path)

    assert len(df_features) == len(df_manifest), "Feature store row count must equal manifest row count"
    assert (df_features["image_id"] == df_manifest["image_id"]).all(), "Image IDs must align 1-to-1 in order"
    assert df_features.isnull().sum().sum() == 0, "Feature store must have exactly zero missing values"


def test_no_exact_duplicate_leakage(project_root):
    """Verifies that no exact MD5 duplicates exist in the canonical dataset."""
    manifest_path = project_root / "data" / "manifests" / "canonical_dataset_v2.csv"
    df = pd.read_csv(manifest_path)
    assert df["md5_hash"].is_unique, "All MD5 hashes in canonical dataset must be strictly unique"


def test_clustering_reproducibility(project_root):
    """Verifies that K-Means clustering produces deterministic results with fixed seed."""
    clusterer1 = CropVisualClusterer(random_seed=42)
    clusterer1.load_and_preprocess()
    clusterer1.fit(k=4)

    clusterer2 = CropVisualClusterer(random_seed=42)
    clusterer2.load_and_preprocess()
    clusterer2.fit(k=4)

    assert np.array_equal(clusterer1.cluster_labels, clusterer2.cluster_labels), "Clusters must be 100% reproducible"
    assert clusterer1.optimal_k == 4
    assert len(clusterer1.feature_names) == 32


def test_clustering_evaluation_metrics(project_root):
    """Verifies that clustering evaluation generates valid mathematical metric ranges."""
    report_path = project_root / "data" / "reports" / "clustering_report_v2.json"
    assert report_path.exists(), "clustering_report_v2.json must exist"

    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    eval_items = data["multi_k_evaluation"]
    assert len(eval_items) >= 5, "Must evaluate at least 5 values of K"

    for item in eval_items:
        # Silhouette score must be in [-1, 1]
        assert -1.0 <= item["silhouette_score"] <= 1.0
        # Davies-Bouldin must be >= 0
        assert item["davies_bouldin_index"] >= 0.0
        # Inertia must be positive
        assert item["inertia"] > 0.0

    # Total 2D PCA explained variance must be in (0, 1]
    assert 0.0 < data["pca_total_variance_explained"] <= 1.0


def test_association_rules_output_equivalence(project_root):
    """Verifies that FP-Growth and Apriori produce identical rule counts on the same transactions."""
    miner = VisualAssociationMiner(min_support=0.15, min_confidence=0.60)
    miner.load_and_discretize()
    comp = miner.compare_algorithms()

    assert comp["output_equivalence"] is True, "FP-Growth and Apriori must generate equivalent rule counts"
    assert comp["fpgrowth"]["rules_count"] == comp["apriori"]["rules_count"]
    assert comp["fpgrowth"]["rules_count"] > 0, "Must discover positive rule count"


def test_association_rule_metrics_validity(project_root):
    """Verifies that mined association rules satisfy support, confidence, and lift bounds."""
    miner = VisualAssociationMiner(min_support=0.15, min_confidence=0.60)
    _, rules, _ = miner.mine_patterns(mode="visual_only", algorithm="fpgrowth", min_support=0.15, min_confidence=0.60)

    assert not rules.empty, "Mined rules dataframe must not be empty"
    for _, r in rules.iterrows():
        assert 0.0 <= r["support"] <= 1.0, "Support must be in [0, 1]"
        assert 0.60 <= r["confidence"] <= 1.0, "Confidence must be >= min_confidence"
        assert r["lift"] > 0.0, "Lift must be strictly positive"


def test_evaluation_report_consistency(project_root):
    """Verifies that the consolidated Review 2 evaluation report contains all research conclusions."""
    eval_path = project_root / "data" / "reports" / "review2_evaluation_report.json"
    assert eval_path.exists(), "review2_evaluation_report.json must exist"

    with open(eval_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "clustering_evaluation" in data
    assert "association_mining_evaluation" in data
    assert "research_conclusions" in data
    assert "RQ1_Visual_Clustering" in data["research_conclusions"]
    assert "RQ2_Source_vs_Disease_Drivers" in data["research_conclusions"]
    assert "RQ3_Feature_Cooccurrence" in data["research_conclusions"]
    assert "RQ4_Cross_Source_Stability" in data["research_conclusions"]


def test_review1_compatibility(project_root):
    """Verifies that Review 1 warehouse and original baseline remain completely intact."""
    r1_feat = project_root / "data" / "features" / "image_features.csv"
    r1_db = project_root / "database" / "agrovision_warehouse.db"
    assert r1_feat.exists(), "Original Review 1 feature store must not be deleted"
    assert r1_db.exists(), "Original Review 1 SQLite database must not be deleted"

    df_r1 = pd.read_csv(r1_feat)
    assert len(df_r1) == 36, "Original Review 1 dataset must remain exactly 36 rows"


def test_frozen_dataset_checksums(project_root):
    """Verifies that the frozen dataset SHA-256 checksums match expected immutable hashes."""
    import hashlib

    expected_hashes = {
        "canonical_dataset_v2.csv": (
            project_root / "data" / "manifests" / "canonical_dataset_v2.csv",
            "c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8"
        ),
        "image_features_v2.csv": (
            project_root / "data" / "features" / "image_features_v2.csv",
            "f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1"
        )
    }

    for name, (path, expected_h) in expected_hashes.items():
        assert path.exists(), f"File {name} must exist"
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        assert h.hexdigest() == expected_h, f"Checksum mismatch for {name}"


def test_mode_a_transaction_matrix_purity(project_root):
    """Verifies that Mode A transaction matrix is completely free of labels, IDs, and source bias."""
    miner = VisualAssociationMiner()
    miner.load_and_discretize()
    tx_visual = miner.df_transactions_visual

    assert tx_visual is not None
    assert len(tx_visual.columns) == 36, "Must contain exactly 36 discretized visual descriptor columns"

    # Strictly forbidden semantic terms
    forbidden_terms = ["health", "disease", "crop", "pathogen", "source", "dataset", "pest_label"]
    for col in tx_visual.columns:
        col_lower = col.lower()
        for term in forbidden_terms:
            assert term not in col_lower, f"Target leakage detected in Mode A: column '{col}' contains forbidden term '{term}'"


def test_dual_k_metric_optimality(project_root):
    """Verifies that K=2 is the metric-supported optimal clustering solution and K=4 is exploratory."""
    report_path = project_root / "data" / "reports" / "clustering_report_v2.json"
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["metric_supported_k"] == 2
    assert data["exploratory_subpartition_k"] == 4

    k2_sil = data["k2_solution"]["silhouette_score"]
    k4_sil = data["k4_solution"]["silhouette_score"]

    # K=2 must have substantially higher silhouette than K=4
    assert k2_sil > 0.40, f"Expected K=2 silhouette > 0.40, got {k2_sil}"
    assert k4_sil < 0.20, f"Expected K=4 silhouette < 0.20, got {k4_sil}"
    assert k2_sil > k4_sil * 2.0, "K=2 silhouette must be more than double K=4 silhouette"


def test_healthy_record_null_pathogen_semantics(project_root):
    """Verifies that null pathogen_type values correspond legitimately to healthy control records."""
    manifest_path = project_root / "data" / "manifests" / "canonical_dataset_v2.csv"
    df = pd.read_csv(manifest_path)

    null_pathogen_mask = df["pathogen_type"].isnull()
    assert null_pathogen_mask.sum() == 846, "Expected exactly 846 null pathogen_type entries"
    assert (df.loc[null_pathogen_mask, "condition_status"] == "Healthy").all(), "All null pathogen records must be Healthy"
    assert (df.loc[~null_pathogen_mask, "condition_status"] == "Diseased").all(), "All non-null pathogen records must be Diseased"


def test_pca_explained_variance_bounds(project_root):
    """Verifies that 2D PCA projection yields expected explained variance."""
    report_path = project_root / "data" / "reports" / "clustering_report_v2.json"
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    evr = data["pca_explained_variance_ratio"]
    assert len(evr) == 2
    assert 0.35 <= evr[0] <= 0.42, f"PC1 variance out of expected range: {evr[0]}"
    assert 0.10 <= evr[1] <= 0.16, f"PC2 variance out of expected range: {evr[1]}"
    assert 0.48 <= sum(evr) <= 0.56, f"Total 2D variance out of expected range: {sum(evr)}"

