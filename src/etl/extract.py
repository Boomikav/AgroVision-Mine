"""
ETL Extract Step Module for AgroVision-Mine.
Extracts and validates data from the canonical v2 multimodal feature store and manifest:
1. Canonical Dataset Manifest: data/manifests/canonical_dataset_v2.csv (2,596 records)
2. Canonical Visual Feature Store: data/features/image_features_v2.csv (2,596 records)
3. Cryptographic hash verification against expected invariant SHA-256 baselines.
4. Identifies and reconciles the 36 authentic ICAR/OGD Rice observations alongside the 2,560 PlantDoc observations.
"""
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

from src.utils.config import get_config
from src.utils.logger import setup_logger

logger = setup_logger("etl_extract")

CANONICAL_MANIFEST_SHA256 = "c7fd16dcd6c1f8623f3e25a48b572387cba2b42855e4b5ddc482095d40f11cb8"
CANONICAL_FEATURES_SHA256 = "f6caf70bd07eeda335e471705e3763d3dd3ef543c0ae406e902a5741ec4093c1"


class Extractor:
    """
    Extracts canonical multimodal dataset records, visual feature vectors, and provenance metadata.
    """

    def __init__(
        self,
        manifest_path: Optional[str] = None,
        features_path: Optional[str] = None
    ):
        self.cfg = get_config()
        self.manifest_file = Path(
            manifest_path or self.cfg.get("paths", {}).get("canonical_manifest", "data/manifests/canonical_dataset_v2.csv")
        ).resolve()
        self.features_file = Path(
            features_path or self.cfg.get("paths", {}).get("canonical_features", "data/features/image_features_v2.csv")
        ).resolve()

    def verify_sha256(self, file_path: Path, expected_hash: str) -> bool:
        """Verifies cryptographic SHA-256 integrity of input file."""
        if not file_path.exists():
            return False
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        actual = h.hexdigest().lower()
        match = (actual == expected_hash.lower())
        if not match:
            logger.warning(f"SHA-256 mismatch for {file_path.name}: expected {expected_hash}, got {actual}")
        return match

    def extract_canonical_manifest(self) -> List[Dict[str, Any]]:
        """
        Loads and validates canonical manifest records.
        """
        if not self.manifest_file.exists():
            raise FileNotFoundError(f"Canonical manifest not found at: {self.manifest_file}")

        logger.info(f"Extracting canonical manifest from {self.manifest_file}...")
        df = pd.read_csv(self.manifest_file)
        if len(df) != 2596:
            raise ValueError(f"Expected 2,596 manifest records, found {len(df)}")

        # Verify presence of all 36 authentic rice records
        rice_records = df[df["crop_name"].str.lower() == "rice"]
        if len(rice_records) != 36:
            raise ValueError(f"Expected exactly 36 authentic rice observations, found {len(rice_records)}")

        # Ensure no null image_ids
        if df["image_id"].isnull().any():
            raise ValueError("Canonical manifest contains null image_id values.")

        records = df.to_dict(orient="records")
        logger.info(f"Successfully extracted {len(records)} manifest records (including {len(rice_records)} authentic rice records).")
        return records

    def extract_visual_features(self) -> List[Dict[str, Any]]:
        """
        Loads and validates canonical visual feature store records.
        """
        if not self.features_file.exists():
            raise FileNotFoundError(f"Canonical feature store not found at: {self.features_file}")

        logger.info(f"Extracting visual features from {self.features_file}...")
        df = pd.read_csv(self.features_file)
        if len(df) != 2596:
            raise ValueError(f"Expected 2,596 feature records, found {len(df)}")

        # Check for 32 continuous numeric features
        req_features = [
            "rgb_r_mean", "rgb_g_mean", "rgb_b_mean",
            "rgb_r_std", "rgb_g_std", "rgb_b_std",
            "rgb_r_norm", "rgb_g_norm", "rgb_b_norm",
            "hsv_h_mean", "hsv_s_mean", "hsv_v_mean",
            "hsv_h_std", "hsv_s_std", "hsv_v_std",
            "hsv_h_norm", "hsv_s_norm", "hsv_v_norm",
            "exg_index_mean", "glcm_contrast", "glcm_contrast_norm",
            "glcm_dissimilarity", "glcm_homogeneity", "glcm_energy",
            "glcm_correlation", "glcm_asm", "contour_area",
            "contour_perimeter", "contour_aspect_ratio",
            "contour_circularity", "contour_solidity", "lesion_coverage_ratio"
        ]
        missing_feats = [col for col in req_features if col not in df.columns]
        if missing_feats:
            raise ValueError(f"Missing required continuous features in feature store: {missing_feats}")

        # Check for nulls in required features
        null_counts = df[req_features].isnull().sum()
        if null_counts.sum() > 0:
            bad_cols = null_counts[null_counts > 0].to_dict()
            raise ValueError(f"Feature store contains null values in required features: {bad_cols}")

        records = df.to_dict(orient="records")
        logger.info(f"Successfully extracted {len(records)} visual feature records.")
        return records

    def extract_all(self) -> Dict[str, Any]:
        """
        Orchestrates full extraction and reconciliation across canonical manifest and feature store.
        """
        logger.info("Starting complete canonical ETL Extraction phase...")
        manifest_hash_valid = self.verify_sha256(self.manifest_file, CANONICAL_MANIFEST_SHA256)
        features_hash_valid = self.verify_sha256(self.features_file, CANONICAL_FEATURES_SHA256)

        manifest_records = self.extract_canonical_manifest()
        feature_records = self.extract_visual_features()

        # Reconcile one-to-one ID alignment
        manifest_ids = [r["image_id"] for r in manifest_records]
        feature_ids = [r["image_id"] for r in feature_records]

        if manifest_ids != feature_ids:
            set_diff = set(manifest_ids).symmetric_difference(set(feature_ids))
            raise ValueError(f"Manifest IDs and Feature Store IDs do not match one-to-one! Mismatches: {len(set_diff)}")

        rice_count = sum(1 for r in manifest_records if str(r.get("crop_name", "")).lower() == "rice")
        plantdoc_count = sum(1 for r in manifest_records if str(r.get("dataset_source", "")).lower() == "plantdoc")
        icar_count = sum(1 for r in manifest_records if str(r.get("dataset_source", "")).lower() == "icar_ogd")

        bundle = {
            "manifest_records": manifest_records,
            "feature_records": feature_records,
            "raw_metadata": manifest_records,
            "processed_metadata": manifest_records,
            "visual_features": feature_records,
            "stats": {
                "total_records": len(manifest_records),
                "raw_count": len(manifest_records),
                "processed_count": len(manifest_records),
                "feature_count": len(feature_records),
                "rice_records": rice_count,
                "plantdoc_records": plantdoc_count,
                "icar_records": icar_count,
                "manifest_sha256_verified": manifest_hash_valid,
                "features_sha256_verified": features_hash_valid,
            }
        }

        logger.info(
            f"Canonical extraction complete: {bundle['stats']['total_records']} total records "
            f"({bundle['stats']['plantdoc_records']} PlantDoc, {bundle['stats']['icar_records']} ICAR/OGD Rice)."
        )
        return bundle
