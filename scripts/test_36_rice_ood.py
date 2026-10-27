"""Test all 36 ICAR/OGD rice flatbed scanner images through the real ImageAnalysisEngine.
Records status, is_uncertain, top candidate, and top nearest reference.
"""
import json
from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.mining.image_analyzer import get_image_analyzer
from src.mining.predictor import get_crop_disease_predictor

def test_rice_ood():
    analyzer = get_image_analyzer()
    predictor = get_crop_disease_predictor()
    df_manifest = pd.read_csv(ROOT / "data" / "manifests" / "canonical_dataset_v2.csv")
    rice_rows = df_manifest[df_manifest["dataset_source"] == "icar_ogd"]
    print(f"Total ICAR rice scanner images to test: {len(rice_rows)}")

    results = []
    for idx, row in rice_rows.iterrows():
        img_p = ROOT / row["processed_relative_path"]
        if not img_p.exists():
            img_p = ROOT / row["raw_relative_path"]
        if not img_p.exists():
            print(f"File not found: {img_p}")
            continue

        with open(img_p, "rb") as f:
            bytes_data = f.read()

        # 1. Full ImageAnalysisEngine (with cross-modal nearest reference context)
        res_full = analyzer.analyze(bytes_data, img_p.name)
        pred_full = res_full.get("prediction", {})
        top_ref = res_full.get("nearest_specimens", [{}])[0]

        # 2. Raw direct CNN prediction (without nearest reference context)
        pred_raw = predictor.predict(bytes_data)

        results.append({
            "image_id": row["image_id"],
            "filename": row["raw_filename"],
            "ground_truth_disease": row["disease_name"],
            # Full pipeline with cross-modal context
            "top_ref_id": top_ref.get("image_id"),
            "top_ref_crop": top_ref.get("crop_name"),
            "top_ref_source": top_ref.get("dataset_source"),
            "top_ref_distance": top_ref.get("euclidean_distance"),
            "full_status": pred_full.get("status"),
            "full_is_uncertain": pred_full.get("is_uncertain"),
            "full_predicted_class": pred_full.get("top_candidates", [{}])[0].get("composite_class"),
            "full_confidence": pred_full.get("top_candidates", [{}])[0].get("probability"),
            # Raw direct CNN prediction
            "raw_status": pred_raw.get("status"),
            "raw_is_uncertain": pred_raw.get("is_uncertain"),
            "raw_predicted_class": pred_raw.get("top_candidates", [{}])[0].get("composite_class"),
            "raw_confidence": pred_raw.get("top_candidates", [{}])[0].get("probability")
        })

    df_res = pd.DataFrame(results)
    
    out_csv = ROOT / "data" / "reports" / "rice_ood_audit_results.csv"
    df_res.to_csv(out_csv, index=False)
    print(f"\nSaved detailed audit results to: {out_csv}")

    print("\n======================================================================")
    print("OOD AUDIT RESULTS: 36 ICAR/OGD RICE SCANNER IMAGES")
    print("======================================================================")
    print("\n1. FULL PIPELINE (WITH 32D CROSS-MODAL REFERENCE CONTEXT):")
    print("Status counts:")
    print(df_res["full_status"].value_counts(dropna=False))
    print("Is uncertain counts:")
    print(df_res["full_is_uncertain"].value_counts(dropna=False))
    print("\nTop Reference Source counts:")
    print(df_res["top_ref_source"].value_counts())
    print("\nTop Reference Crop counts:")
    print(df_res["top_ref_crop"].value_counts())

    print("\n2. RAW DIRECT CNN PREDICTOR (WITHOUT CROSS-MODAL CONTEXT):")
    print("Raw Status counts:")
    print(df_res["raw_status"].value_counts(dropna=False))
    print("Raw Predicted Class counts:")
    print(df_res["raw_predicted_class"].value_counts())
    print("Raw Mean Confidence on OOD Rice:")
    print(df_res["raw_confidence"].mean())

    # Summary statistics
    n_rejected_full = (df_res["full_status"] == "unsupported_domain").sum()
    n_accepted_full = len(df_res) - n_rejected_full
    print(f"\nSummary for Full Pipeline: {n_rejected_full}/{len(df_res)} ({n_rejected_full/len(df_res)*100:.1f}%) rejected as unsupported_domain.")
    if n_accepted_full > 0:
        print(f"WARNING: {n_accepted_full}/{len(df_res)} ({n_accepted_full/len(df_res)*100:.1f}%) false acceptances in full pipeline!")

    n_rejected_raw = (df_res["raw_status"] != "confident").sum()
    print(f"Summary for Raw CNN: {n_rejected_raw}/{len(df_res)} ({n_rejected_raw/len(df_res)*100:.1f}%) rejected by entropy/threshold alone.")

if __name__ == "__main__":
    test_rice_ood()
