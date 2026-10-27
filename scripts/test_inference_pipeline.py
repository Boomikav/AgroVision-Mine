import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, ".")
from src.mining.image_analyzer import ImageAnalysisEngine

df = pd.read_csv("data/manifests/canonical_dataset_v2.csv")
engine = ImageAnalysisEngine()

# Test healthy specimen
h_idx = df[df["image_id"] == "AGRO_V2_00037"].index[0]
h_vec = engine.X_scaled[h_idx]
dists = np.linalg.norm(engine.X_scaled - h_vec, axis=1)
top_10 = np.argsort(dists)[:10]

print("Top 10 overall nearest specimens to AGRO_V2_00037:")
for rank, idx in enumerate(top_10, start=1):
    ref = engine.reference_metadata[idx]
    d = dists[idx]
    s = 1.0 / (1.0 + d)
    print(f"  #{rank} ID: {ref['image_id']} | Crop: {ref['crop_name']} | Disease: {ref['disease_name']} | Status: {ref['condition_status']} | Dist: {d:.4f} | Score: {s:.4f}")

top_ids = [engine.reference_metadata[i]["image_id"] for i in top_10[:6]]
sub_feats = ["exg_index_mean", "rgb_g_norm", "hsv_h_mean", "glcm_contrast", "contour_perimeter", "lesion_coverage_ratio"]
feat_df = pd.DataFrame(engine.X_scaled[top_10[:6]], index=top_ids, columns=engine.feature_names)
print("\nFeature comparison (Standardized Z-scores):")
print(feat_df[sub_feats].to_string())

raw_feats_df = pd.DataFrame([engine.df_raw.loc[i, sub_feats].to_dict() for i in top_10[:6]], index=top_ids)
print("\nFeature comparison (Raw values):")
print(raw_feats_df.to_string())

# Check nearest HEALTHY specimens
healthy_indices = [i for i, ref in enumerate(engine.reference_metadata) if ref["condition_status"] == "Healthy"]
h_dists = [(i, dists[i]) for i in healthy_indices]
h_dists.sort(key=lambda x: x[1])
print("\nTop 5 nearest HEALTHY specimens:")
for rank, (i, d) in enumerate(h_dists[:5], start=1):
    ref = engine.reference_metadata[i]
    print(f"  #{rank} ID: {ref['image_id']} | Crop: {ref['crop_name']} | Disease: {ref['disease_name']} | Dist: {d:.4f}")
