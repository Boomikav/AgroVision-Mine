import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, ".")
from src.mining.image_analyzer import ImageAnalysisEngine

df = pd.read_csv("data/manifests/canonical_dataset_v2.csv")
engine = ImageAnalysisEngine()

row = df[df["image_id"] == "AGRO_V2_00538"].iloc[0]
p_path = Path(row["processed_relative_path"])
with open(p_path, "rb") as f:
    bytes_data = f.read()
res = engine.analyze(bytes_data, p_path.name, top_k_neighbors=8)
print("AGRO_V2_00538 Top 6 (with self):")
for s in res["nearest_specimens"][:6]:
    print(f"  #{s['rank']} {s['image_id']} {s['crop_name']} {s['disease_name']} ({s['condition_status']}) d={s['euclidean_distance']}")

non_self = [s for s in res["nearest_specimens"] if s["image_id"] != "AGRO_V2_00538"][:6]
print("AGRO_V2_00538 Top 6 (excluding self):")
for s in non_self:
    print(f"  {s['image_id']} {s['crop_name']} {s['disease_name']} ({s['condition_status']}) d={s['euclidean_distance']}")
