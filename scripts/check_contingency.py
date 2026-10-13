import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import sys

df = pd.read_csv("data/features/clustering_assignments_v2.csv")

targets = [
    ("condition_status", "Health Status"),
    ("crop_name", "Crop Taxa"),
    ("pathogen_type", "Pathogen Type"),
    ("dataset_source", "Dataset Source"),
    ("disease_name", "Disease Name"),
]

results = []

for k_col, k_val in [("cluster_id_k2", 2), ("cluster_id_k4", 4)]:
    print(f"\n==================== K = {k_val} ====================", flush=True)
    labels = df[k_col].values
    n = len(labels)
    k_unique, label_idx = np.unique(labels, return_inverse=True)
    n_rows = len(k_unique)

    for col, name in targets:
        vals = df[col].fillna("Unknown").values
        col_unique, col_idx = np.unique(vals, return_inverse=True)
        n_cols = len(col_unique)

        # Observed table
        ct = pd.crosstab(df[k_col], df[col].fillna("Unknown"))
        chi2, p_asymp, dof, expected = chi2_contingency(ct)
        min_dim = min(ct.shape) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
        min_exp = float(expected.min())
        cells_lt_5 = int((expected < 5).sum())
        pct_lt_5 = float((cells_lt_5 / expected.size) * 100)
        cells_lt_1 = int((expected < 1).sum())
        pct_lt_1 = float((cells_lt_1 / expected.size) * 100)

        # Vectorized Monte Carlo permutation test (B=2000)
        np.random.seed(42)
        perm_ge_count = 0
        B = 2000
        # Expected frequencies under H0 for chi2 stat calculation:
        row_totals = np.bincount(label_idx, minlength=n_rows)
        col_totals = np.bincount(col_idx, minlength=n_cols)
        E = np.outer(row_totals, col_totals) / n
        nonzero_E = E > 0

        for _ in range(B):
            perm_label_idx = np.random.permutation(label_idx)
            # 2D histogram via bincount
            flat_idx = perm_label_idx * n_cols + col_idx
            obs = np.bincount(flat_idx, minlength=n_rows * n_cols).reshape(n_rows, n_cols)
            # chi2 = sum((O - E)^2 / E)
            sim_chi2 = np.sum((obs[nonzero_E] - E[nonzero_E]) ** 2 / E[nonzero_E])
            if sim_chi2 >= chi2:
                perm_ge_count += 1

        p_mc = (perm_ge_count + 1) / (B + 1)

        # Cochran Evaluation
        cochran_satisfied = (min_exp >= 1.0) and (pct_lt_5 <= 20.0)
        if min_exp < 1.0 and pct_lt_5 > 20.0:
            cochran_status = "VIOLATED (min expected < 1 AND > 20% cells < 5)"
        elif min_exp < 1.0:
            cochran_status = f"VIOLATED (min expected = {min_exp:.2f} < 1.0)"
        elif pct_lt_5 > 20.0:
            cochran_status = f"VIOLATED ({pct_lt_5:.1f}% cells < 5)"
        else:
            cochran_status = "Satisfied"

        print(f"\nTarget: {name} (Shape: {ct.shape}, df: {dof})", flush=True)
        print(f"  chi2: {chi2:.2f}, p_asymp: {p_asymp:.4e}, p_mc: {p_mc:.4f}, cramers_v: {cramers_v:.4f}", flush=True)
        print(f"  min_exp: {min_exp:.2f}, cells<1: {cells_lt_1}/{expected.size} ({pct_lt_1:.1f}%), cells<5: {cells_lt_5}/{expected.size} ({pct_lt_5:.1f}%)", flush=True)
        print(f"  Cochran Status: {cochran_status}", flush=True)

        results.append({
            "k": k_val,
            "target": name,
            "shape": f"{ct.shape[0]} x {ct.shape[1]}",
            "df": dof,
            "chi2": round(float(chi2), 2),
            "p_asymp": f"{p_asymp:.2e}",
            "p_mc": round(float(p_mc), 4),
            "cramers_v": round(float(cramers_v), 4),
            "min_exp": round(float(min_exp), 2),
            "cells_lt_1": f"{cells_lt_1}/{expected.size} ({pct_lt_1:.1f}%)",
            "cells_lt_5": f"{cells_lt_5}/{expected.size} ({pct_lt_5:.1f}%)",
            "cochran_status": cochran_status,
            "observed_table": ct.to_dict()
        })

import json
with open("data/reports/contingency_exact_audit.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved detailed results to data/reports/contingency_exact_audit.json", flush=True)
