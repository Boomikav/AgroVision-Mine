import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sqlite3
import pandas as pd
from src.mining.association_rules import VisualAssociationMiner, SELECTED_DISCRETIZATION_FEATURES

print("=== 1. WAREHOUSE & DATASET SCHEMA INSPECTION ===")
conn = sqlite3.connect("database/agrovision_warehouse.db")
cursor = conn.cursor()

print("Fact table columns:")
for row in cursor.execute("PRAGMA table_info(disease_observation_fact)"):
    print(f"  {row[1]} ({row[2]})")

print("\ndim_disease columns:")
for row in cursor.execute("PRAGMA table_info(dim_disease)"):
    print(f"  {row[1]} ({row[2]})")

print("\nDistinct condition values in fact table:")
for r in cursor.execute("SELECT DISTINCT condition_status, COUNT(*) FROM disease_observation_fact GROUP BY condition_status"):
    print(f"  {r}")

print("\nDistinct pathogen_type values in dim_disease:")
for r in cursor.execute("SELECT DISTINCT pathogen_type, COUNT(*) FROM dim_disease GROUP BY pathogen_type"):
    print(f"  {r}")

print("\nDistinct pathogen_type joined with facts:")
for r in cursor.execute("SELECT d.pathogen_type, COUNT(f.observation_key) FROM disease_observation_fact f JOIN dim_disease d USING(disease_key) GROUP BY d.pathogen_type"):
    print(f"  {r}")

print("\nCanonical dataset v2 columns and distinct condition/pathogen:")
df_can = pd.read_csv("data/manifests/canonical_dataset_v2.csv")
print("  Columns:", df_can.columns.tolist())
if "condition_status" in df_can.columns:
    print("  condition_status value counts:\n", df_can["condition_status"].value_counts(dropna=False))
if "pathogen_type" in df_can.columns:
    print("  pathogen_type value counts:\n", df_can["pathogen_type"].value_counts(dropna=False))

print("\n=== 2. TRANSACTION ENCODER AUDIT ===")
miner = VisualAssociationMiner()
df_disc, bin_meta = miner.load_and_discretize()
print("Raw DataFrame shape:", miner.df_raw.shape)
print("Raw DataFrame columns with 'condition' or 'pathogen':", [c for c in miner.df_raw.columns if 'condition' in c or 'pathogen' in c])

print("\nMode A (Visual) Transaction Matrix:")
print("  Shape:", miner.df_transactions_visual.shape)
print("  Columns count:", len(miner.df_transactions_visual.columns))
print("  Sample columns:", miner.df_transactions_visual.columns[:8].tolist())
# Confirm NO labels in Mode A
labels_in_visual = [c for c in miner.df_transactions_visual.columns if any(k in c.lower() for k in ["healthy", "diseased", "pathogen", "crop", "status", "condition"])]
print("  Any labels in Mode A transactions?:", labels_in_visual)

print("\nMode B (Labeled) Transaction Matrix:")
print("  Shape:", miner.df_transactions_labeled.shape)
print("  Columns count:", len(miner.df_transactions_labeled.columns))
label_cols = [c for c in miner.df_transactions_labeled.columns if c not in miner.df_transactions_visual.columns]
print("  Label columns added in Mode B:", label_cols)
