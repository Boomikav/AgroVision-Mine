"""
Phase 3 Feature Extraction Execution Script for AgroVision-Mine.
Executes batch classical visual feature extraction across all preprocessed images,
computes color moments, GLCM textures, and morphometrics, and saves image_features.csv.
"""
import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.feature_extraction.pipeline import FeatureExtractionPipeline
from src.utils.logger import setup_logger

logger = setup_logger("run_feature_extraction")


def main():
    logger.info("========== EXECUTING PHASE 3: VISUAL FEATURE EXTRACTION ==========")

    pipeline = FeatureExtractionPipeline()
    feature_rows = pipeline.run_batch_from_metadata()

    if not feature_rows:
        logger.error("No features extracted. Please ensure Phase 2 preprocessing has been executed.")
        return

    df = pd.DataFrame(feature_rows)
    csv_file = Path("data/features/image_features.csv")

    print("\n" + "=" * 80)
    print("AGROVISION-MINE: PHASE 3 FEATURE EXTRACTION EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Visual Feature Records Extracted : {len(df)}")
    print(f"Total Features per Record             : {len(df.columns)}")
    print(f"Unique Crops Represented              : {df['crop_label'].unique().tolist()}")
    print(f"Unique Conditions Represented         : {df['condition_label'].unique().tolist()}")
    print("-" * 80)
    print("SAMPLE EXTRACTED FEATURES (Top 3 Records):")
    sample_cols = [
        "image_id", "filename", "crop_label", "condition_label",
        "rgb_r_norm", "rgb_g_norm", "hsv_h_mean", "dominant_color_tone",
        "glcm_contrast", "glcm_homogeneity", "glcm_energy",
        "has_valid_contour", "contour_area", "lesion_coverage_ratio"
    ]
    print(df[sample_cols].head(3).to_string(index=False))
    print("-" * 80)
    print("OUTPUT ARTIFACTS GENERATED:")
    print(f"  1. Feature Analytical Store (CSV)   : {csv_file}")
    print(f"  2. Feature Analytical Store (JSON)  : data/features/image_features.json")
    print(f"  3. Feature Metadata Dictionary      : data/features/feature_dictionary.json")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
