import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, ".")
from src.mining.image_analyzer import ImageAnalysisEngine

df = pd.read_csv("data/manifests/canonical_dataset_v2.csv")
engine = ImageAnalysisEngine()

test_ids = [
    ("AGRO_V2_00037", "Healthy"),
    ("AGRO_V2_00538", "Healthy"),
    ("AGRO_V2_00180", "Healthy"),
    ("AGRO_V2_00001", "Diseased"),
    ("AGRO_V2_00169", "Diseased"),
    ("AGRO_V2_00019", "Diseased"),
]

for img_id, expected_status in test_ids:
    row = df[df["image_id"] == img_id].iloc[0]
    p_path = Path(row["processed_relative_path"])
    if not p_path.exists():
        p_path = Path(row["raw_relative_path"])

    with open(p_path, "rb") as f:
        img_bytes = f.read()

    res = engine.analyze(img_bytes, p_path.name, top_k_neighbors=12)

    print(f"\n=======================================================")
    print(f"TEST SPECIMEN: {img_id} [{row['crop_name']} - {row['disease_name']}] ({expected_status})")
    print(f"File: {p_path}")
    print(f"K=2 Cluster: {res['clustering']['k2']['cluster_id']} | K=4 Cluster: {res['clustering']['k4']['cluster_id']}")
    print(f"PCA 2D: PC1={res['pca_projection']['x']}, PC2={res['pca_projection']['y']}")
    
    # Feature summary
    raw_feats = res["features_raw"]
    std_feats = res["features_standardized"]
    print(f"Sample Features (Raw -> Std):")
    for k in ["exg_index_mean", "rgb_g_norm", "hsv_h_mean", "glcm_contrast", "contour_perimeter", "lesion_coverage_ratio"]:
        print(f"  {k:22s}: Raw={raw_feats[k]:10.4f} | Std(z)={std_feats[k]:+8.4f}")

    # Top 6 WITH self-matching
    print("\n--- TOP 6 NEAREST (WITH SELF-MATCHING) ---")
    for s in res["nearest_specimens"][:6]:
        print(f"  #{s['rank']} {s['image_id']} | {s['crop_name']:12s} | {s['disease_name']:25s} | Status: {s['condition_status']:8s} | d={s['euclidean_distance']:.4f} | Score={s['visual_similarity_score']*100:.1f}%")

    # Top 6 EXCLUDING exact source record
    non_self = [s for s in res["nearest_specimens"] if s["image_id"] != img_id][:6]
    print("\n--- TOP 6 NEAREST (EXCLUDING EXACT SOURCE RECORD) ---")
    healthy_count = sum(1 for s in non_self if s["condition_status"] == "Healthy")
    diseased_count = sum(1 for s in non_self if s["condition_status"] == "Diseased")
    print(f"  Distribution: {healthy_count} Healthy, {diseased_count} Diseased")
    for r_idx, s in enumerate(non_self, start=1):
        print(f"  #{r_idx} {s['image_id']} | {s['crop_name']:12s} | {s['disease_name']:25s} | Status: {s['condition_status']:8s} | d={s['euclidean_distance']:.4f} | Score={s['visual_similarity_score']*100:.1f}%")
