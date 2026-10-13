import os
import sys
import json
import sqlite3
from pathlib import Path
import pandas as pd

root = Path(r"c:\Users\ajaya\Desktop\Agro")
print("=== 1. PROJECT ROOT ===")
print(f"Root: {root.resolve()}")

print("\n=== 2. DATASET VERIFICATION ===")
raw_dir = root / "data" / "raw"
print(f"Raw dir: {raw_dir}")
for disease in ["bacterial_leaf_blight", "brown_spot", "leaf_smut"]:
    folder = raw_dir / "rice" / disease
    if folder.exists():
        files = sorted([f.name for f in folder.glob("*") if f.is_file()])
        print(f"  rice/{disease}: {len(files)} files -> {files}")

total_raw = list(raw_dir.glob("rice/**/*.JPG")) + list(raw_dir.glob("rice/**/*.jpg")) + list(raw_dir.glob("rice/**/*.png"))
print(f"Total authentic raw images: {len(total_raw)}")

print("\n=== 3. DIAGNOSTIC FILES ===")
diag_dir = root / "data" / "diagnostic_tests"
print(f"Diag dir: {diag_dir}")
if diag_dir.exists():
    for f in sorted(diag_dir.glob("*")):
        print(f"  {f.name} ({f.stat().st_size} bytes)")

print("\n=== 4. DATABASE & ROW COUNTS ===")
db_path = root / "database" / "agrovision_warehouse.db"
print(f"DB Path: {db_path} exists: {db_path.exists()}")
if db_path.exists():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables in DB:", tables)
    for t in tables:
        cursor.execute(f"SELECT count(*) FROM {t}")
        cnt = cursor.fetchone()[0]
        print(f"  {t}: {cnt} rows")
    conn.close()

print("\n=== 5. FEATURES STORE ===")
feat_path = root / "data" / "features" / "image_features.csv"
print(f"Features CSV: {feat_path} exists: {feat_path.exists()}")
if feat_path.exists():
    df = pd.read_csv(feat_path)
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    meta_cols = {'image_id', 'filename', 'raw_path', 'processed_path', 'crop_label', 'condition_label', 'disease_label', 'pest_label', 'is_pest', 'md5_hash'}
    vis_cols = [c for c in df.columns if c not in meta_cols]
    print(f"Metadata cols count ({len(meta_cols.intersection(df.columns))}): {sorted(list(meta_cols.intersection(df.columns)))}")
    print(f"Visual descriptor cols count ({len(vis_cols)}): {vis_cols}")

print("\n=== 6. PROCESSED DATA ===")
proc_dir = root / "data" / "processed"
print(f"Processed dir: {proc_dir}")
for disease in ["bacterial_leaf_blight", "brown_spot", "leaf_smut"]:
    folder = proc_dir / "rice" / disease
    if folder.exists():
        files = sorted([f.name for f in folder.glob("*") if f.is_file()])
        print(f"  rice/{disease}: {len(files)} files")

print("\n=== 7. REPORTS ===")
rep_dir = root / "data" / "reports"
for f in sorted(rep_dir.glob("*")):
    print(f"  {f.name} ({f.stat().st_size} bytes)")
