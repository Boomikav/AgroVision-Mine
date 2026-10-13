"""
Feature Extraction Pipeline Module for AgroVision-Mine (Phase 3).
Coordinates classical color moments, GLCM texture metrics, and morphometric shape contours.
Enforces complete traceability back to Image_ID and original raw file hashes.
Architected with an extensible interface for future deep embeddings.
"""
import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from PIL import Image

from src.utils.config import get_config
from src.utils.logger import setup_logger
from src.utils.io import save_json, load_json
from src.feature_extraction.color_features import extract_color_features
from src.feature_extraction.texture_features import extract_texture_features
from src.feature_extraction.shape_features import extract_shape_features

logger = setup_logger("feature_pipeline")

FEATURE_DICTIONARY: Dict[str, Dict[str, Any]] = {
    # Provenance
    "image_id": {"category": "Provenance", "type": "string", "description": "Unique surrogate identifier for the source image record"},
    "filename": {"category": "Provenance", "type": "string", "description": "Original raw filename on disk"},
    "crop_label": {"category": "Taxonomy", "type": "string", "description": "Host crop category (e.g. rice, wheat)"},
    "condition_label": {"category": "Taxonomy", "type": "string", "description": "Annotated disease or healthy condition"},
    "md5_hash": {"category": "Provenance", "type": "string", "description": "128-bit cryptographic MD5 checksum for data lineage"},

    # Color Moments
    "rgb_r_mean": {"category": "Color", "type": "float", "range": "[0, 255]", "description": "First-order mean intensity of the Red channel"},
    "rgb_g_mean": {"category": "Color", "type": "float", "range": "[0, 255]", "description": "First-order mean intensity of the Green channel (chlorophyll indicator)"},
    "rgb_b_mean": {"category": "Color", "type": "float", "range": "[0, 255]", "description": "First-order mean intensity of the Blue channel"},
    "rgb_r_std": {"category": "Color", "type": "float", "range": ">= 0", "description": "Standard deviation of the Red channel (color variance)"},
    "rgb_g_std": {"category": "Color", "type": "float", "range": ">= 0", "description": "Standard deviation of the Green channel"},
    "rgb_b_std": {"category": "Color", "type": "float", "range": ">= 0", "description": "Standard deviation of the Blue channel"},
    "rgb_r_norm": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Normalized Red intensity in unit range [0, 1]"},
    "rgb_g_norm": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Normalized Green intensity in unit range [0, 1]"},
    "rgb_b_norm": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Normalized Blue intensity in unit range [0, 1]"},
    "hsv_h_mean": {"category": "Color", "type": "float", "range": "[0, 360)", "description": "Mean Hue angle in degrees"},
    "hsv_s_mean": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Mean Saturation (color purity)"},
    "hsv_v_mean": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Mean Value / Brightness"},
    "hsv_h_norm": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Normalized Hue angle in unit range [0, 1]"},
    "hsv_s_norm": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Normalized Saturation in unit range [0, 1]"},
    "hsv_v_norm": {"category": "Color", "type": "float", "range": "[0, 1]", "description": "Normalized Value in unit range [0, 1]"},
    "exg_index_mean": {"category": "Color", "type": "float", "range": "[-255, 510]", "description": "Excess Green Index (2G - R - B) for vegetative foliar contrast"},
    "dominant_color_tone": {"category": "Color", "type": "string", "description": "Categorical dominant tone (e.g. Foliar_Green, Brown_Blight, Yellowish_Lesion)"},

    # Texture (GLCM)
    "glcm_contrast": {"category": "Texture", "type": "float", "range": ">= 0", "description": "Haralick contrast: measures intensity contrast between pixel pairs"},
    "glcm_contrast_norm": {"category": "Texture", "type": "float", "range": "[0, 1]", "description": "Normalized GLCM contrast scaled by maximum theoretical pair distance"},
    "glcm_dissimilarity": {"category": "Texture", "type": "float", "range": ">= 0", "description": "Linear difference between adjacent pixel gray levels"},
    "glcm_homogeneity": {"category": "Texture", "type": "float", "range": "[0, 1]", "description": "Measures closeness of element distribution to diagonal (local uniformity)"},
    "glcm_energy": {"category": "Texture", "type": "float", "range": "[0, 1]", "description": "Angular Second Moment (ASM): measures orderliness of textural patterns"},
    "glcm_correlation": {"category": "Texture", "type": "float", "range": "[-1, 1]", "description": "Linear dependency of gray levels of neighbor pixels"},
    "glcm_asm": {"category": "Texture", "type": "float", "range": "[0, 1]", "description": "Sum of squared elements in GLCM (equals energy)"},

    # Shape
    "has_valid_contour": {"category": "Shape", "type": "boolean", "description": "Flag indicating whether a distinct pathological lesion contour exists"},
    "contour_area": {"category": "Shape", "type": "float", "range": ">= 0", "description": "Pixel area of the segmented lesion region"},
    "contour_perimeter": {"category": "Shape", "type": "float", "range": ">= 0", "description": "Boundary perimeter in pixels of the segmented lesion"},
    "contour_aspect_ratio": {"category": "Shape", "type": "float", "range": ">= 0", "description": "Bounding box aspect ratio (width / height)"},
    "contour_circularity": {"category": "Shape", "type": "float", "range": "[0, 1]", "description": "Isoperimetric quotient (4 * pi * Area / Perimeter^2)"},
    "contour_solidity": {"category": "Shape", "type": "float", "range": "[0, 1]", "description": "Area fraction of lesion relative to its bounding envelope"},
    "lesion_coverage_ratio": {"category": "Shape", "type": "float", "range": "[0, 1]", "description": "Fraction of total leaf foliage affected by lesion spots"}
}


class BaseFeatureExtractor(ABC):
    """
    Abstract interface for feature extractors. Enables drop-in extension
    for classical visual descriptors or deep embedding backbones (e.g., ResNet/CLIP).
    """

    @abstractmethod
    def extract(self, img_pil: Image.Image) -> Dict[str, Any]:
        """Extracts numerical features from PIL image."""
        pass


class ClassicalFeatureExtractor(BaseFeatureExtractor):
    """
    Baseline classical visual extractor: Color moments, GLCM texture, and morphometrics.
    """

    def __init__(self, min_contour_area: Optional[float] = None):
        cfg = get_config()
        self.min_contour_area = (
            min_contour_area
            if min_contour_area is not None
            else cfg.get("feature_extraction", {}).get("shape", {}).get("min_contour_area", 50.0)
        )

    def extract(self, img_pil: Image.Image) -> Dict[str, Any]:
        color_feats = extract_color_features(img_pil)
        texture_feats = extract_texture_features(img_pil)
        shape_feats = extract_shape_features(img_pil, min_contour_area=self.min_contour_area)

        combined: Dict[str, Any] = {}
        combined.update(color_feats)
        combined.update(texture_feats)
        combined.update(shape_feats)
        return combined


class FeatureExtractionPipeline:
    """
    Orchestrates batch feature extraction across standardized preprocessed images,
    enforces Image_ID traceability, and exports database-ready analytical stores.
    """

    def __init__(self, extractor: Optional[BaseFeatureExtractor] = None):
        self.cfg = get_config()
        self.features_dir = Path(self.cfg["paths"]["features_data_dir"]).resolve()
        self.processed_dir = Path(self.cfg["paths"]["processed_data_dir"]).resolve()
        self.features_dir.mkdir(parents=True, exist_ok=True)
        self.extractor = extractor or ClassicalFeatureExtractor()

    def process_image(self, processed_image_path: Union[str, Path]) -> Dict[str, Any]:
        """Extracts visual features from a single standardized image."""
        path = Path(processed_image_path)
        if not path.exists():
            raise FileNotFoundError(f"Processed image does not exist: {path}")

        with Image.open(path) as img:
            return self.extractor.extract(img)

    def run_pipeline(self, processed_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs feature extraction over a list of preprocessed records.
        """
        logger.info(f"Extracting visual features for {len(processed_records)} image records...")
        feature_rows: List[Dict[str, Any]] = []

        for rec in processed_records:
            proc_path = rec.get("processed_path")
            if not proc_path or not Path(proc_path).exists():
                logger.warning(f"Skipping record without valid processed_path: {rec.get('filename')}")
                continue

            try:
                feats = self.process_image(proc_path)
                combined_row = {
                    "image_id": rec.get("raw_id") or rec.get("filename"),
                    "filename": rec.get("filename"),
                    "raw_path": rec.get("raw_path"),
                    "processed_path": proc_path,
                    "crop_label": rec.get("crop_label", "unspecified"),
                    "condition_label": rec.get("condition_label", "unspecified"),
                    "disease_label": rec.get("disease_label", "none"),
                    "pest_label": rec.get("pest_label", "none"),
                    "is_pest": rec.get("is_pest", False),
                    "md5_hash": rec.get("md5_hash"),
                    **feats
                }
                feature_rows.append(combined_row)
            except Exception as e:
                logger.error(f"Failed feature extraction on {proc_path}: {e}")

        # Save artifacts
        self._export_feature_store(feature_rows)
        return feature_rows

    def run_batch_from_metadata(self) -> List[Dict[str, Any]]:
        """
        Loads data/processed/cleaned_metadata.csv and runs batch feature extraction.
        """
        cleaned_csv = self.processed_dir / "cleaned_metadata.csv"
        cleaned_json = self.processed_dir / "cleaned_metadata.json"

        records: List[Dict[str, Any]] = []
        if cleaned_json.exists():
            records = load_json(cleaned_json)
        elif cleaned_csv.exists():
            with open(cleaned_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                records = list(reader)
        else:
            raise FileNotFoundError(f"Cleaned metadata file not found at {cleaned_csv}")

        return self.run_pipeline(records)

    def _export_feature_store(self, feature_rows: List[Dict[str, Any]]) -> None:
        """Exports image_features.csv, image_features.json, and feature_dictionary.json."""
        csv_file = self.features_dir / "image_features.csv"
        json_file = self.features_dir / "image_features.json"
        dict_file = self.features_dir / "feature_dictionary.json"

        if feature_rows:
            fieldnames = list(feature_rows[0].keys())
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(feature_rows)

            save_json(feature_rows, json_file)
            save_json(FEATURE_DICTIONARY, dict_file)
            logger.info(f"Exported {len(feature_rows)} feature records to {csv_file}")
            logger.info(f"Exported feature metadata dictionary to {dict_file}")
        else:
            logger.warning("No feature rows available to export.")
