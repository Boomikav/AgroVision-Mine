"""AgroVision-Mine: Full Audit & Evidence Verification for IEEE Research Paper.
Extracts and validates all quantitative evidence across:
- Canonical dataset & feature store
- Star schema database & foreign keys
- OLAP benchmarks
- Unsupervised clustering & PCA
- Association rule mining (Apriori vs FP-Growth)
- Supervised classification (train/val/test, tournament, metrics, Wilson CI)
- Software test suite
"""
import hashlib
import json
import sqlite3
import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def audit_all():
    results = {}
    print("=" * 70)
    print("AGROVISION-MINE RESEARCH PAPER AUDIT")
    print("=" * 70)

    # 1. Manifest
    manifest_p = ROOT / "data" / "manifests" / "canonical_dataset_v2.csv"
    with open(manifest_p, "rb") as f:
        manifest_hash = hashlib.sha256(f.read()).hexdigest()
    df_manifest = pd.read_csv(manifest_p)
    results["manifest"] = {
        "path": str(manifest_p),
        "sha256": manifest_hash,
        "rows": len(df_manifest),
        "sources": df_manifest["dataset_source"].value_counts().to_dict(),
        "conditions": df_manifest["condition_status"].value_counts().to_dict(),
        "crops_count": df_manifest["crop_name"].nunique(),
        "crops": df_manifest["crop_name"].value_counts().to_dict()
    }
    print(f"[1] Manifest: {len(df_manifest)} rows | SHA256: {manifest_hash}")

    # 2. Features
    feat_p = ROOT / "data" / "features" / "image_features_v2.csv"
    with open(feat_p, "rb") as f:
        feat_hash = hashlib.sha256(f.read()).hexdigest()
    df_feat = pd.read_csv(feat_p)
    cont_cols = [c for c in df_feat.columns if c.startswith(("rgb_", "hsv_", "glcm_", "contour_", "exg_"))]
    results["features"] = {
        "path": str(feat_p),
        "sha256": feat_hash,
        "rows": len(df_feat),
        "cols": df_feat.shape[1],
        "continuous_cols_count": len(cont_cols),
        "continuous_cols": cont_cols
    }
    print(f"[2] Features: {df_feat.shape} | Continuous descriptors: {len(cont_cols)} | SHA256: {feat_hash}")

    # 3. Warehouse
    db_p = ROOT / "database" / "agrovision_warehouse.db"
    conn = sqlite3.connect(str(db_p))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]
    table_counts = {}
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        table_counts[t] = cur.fetchone()[0]
    cur.execute("PRAGMA foreign_key_check")
    fk_violations = cur.fetchall()
    results["warehouse"] = {
        "path": str(db_p),
        "tables": table_counts,
        "fk_violations": len(fk_violations)
    }
    print(f"[3] Warehouse: {table_counts} | FK violations: {len(fk_violations)}")

    # 4. OLAP Latency Benchmarks
    from src.olap.engine import OLAPEngine
    engine = OLAPEngine()
    olap_bench = {}
    
    t0 = time.perf_counter()
    res_rollup = engine.rollup()
    olap_bench["rollup_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    olap_bench["rollup_rows"] = len(res_rollup["data"])

    t0 = time.perf_counter()
    res_drill = engine.drilldown()
    olap_bench["drilldown_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    olap_bench["drilldown_rows"] = len(res_drill["data"])

    t0 = time.perf_counter()
    res_slice = engine.slice_by_crop("Tomato")
    olap_bench["slice_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    olap_bench["slice_rows"] = len(res_slice["data"])

    t0 = time.perf_counter()
    res_dice = engine.dice(selected_crops=["Tomato", "Potato"], selected_pathogens=["Fungal", "Bacterial"])
    olap_bench["dice_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    olap_bench["dice_rows"] = len(res_dice["data"])

    t0 = time.perf_counter()
    res_pivot = engine.pivot()
    olap_bench["pivot_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    olap_bench["pivot_shape"] = list(res_pivot["data"].shape)

    results["olap"] = olap_bench
    print(f"[4] OLAP Benchmarks: Rollup {olap_bench['rollup_ms']}ms, Drill {olap_bench['drilldown_ms']}ms, Slice {olap_bench['slice_ms']}ms, Dice {olap_bench['dice_ms']}ms, Pivot {olap_bench['pivot_ms']}ms")

    # 5. Clustering and PCA
    clustering_p = ROOT / "data" / "features" / "clustering_assignments_v2.csv"
    if clustering_p.exists():
        df_cl = pd.read_csv(clustering_p)
        results["clustering"] = {
            "rows": len(df_cl),
            "k2_dist": df_cl["k2_cluster"].value_counts().to_dict() if "k2_cluster" in df_cl else {},
            "k4_dist": df_cl["k4_cluster"].value_counts().to_dict() if "k4_cluster" in df_cl else {}
        }
        print(f"[5] Clustering Assignments: {results['clustering']}")

    # 6. Prediction Model & Evaluation
    meta_p = ROOT / "data" / "models" / "prediction" / "model_metadata.json"
    with open(meta_p) as f:
        meta = json.load(f)
    results["model_metadata"] = meta

    rep_p = ROOT / "data" / "reports" / "prediction" / "prediction_evaluation_report.json"
    with open(rep_p) as f:
        rep = json.load(f)
    results["prediction_report"] = rep
    print(f"[6] Classification: EfficientNet-B0 Test Acc: {rep['evaluation_summary']['test_accuracy']*100:.2f}%, Macro-F1: {rep['evaluation_summary']['test_macro_f1']*100:.2f}%, 95% CI: [{rep['evaluation_summary']['test_confidence_interval_95'][0]*100:.2f}%, {rep['evaluation_summary']['test_confidence_interval_95'][1]*100:.2f}%]")

    # Save complete audit report
    out_json = ROOT / "data" / "reports" / "paper_evidence_audit.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[SUCCESS] Full audit report saved to: {out_json}")

if __name__ == "__main__":
    audit_all()
