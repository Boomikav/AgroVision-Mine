"""
ETL Extract Step Module for AgroVision-Mine (Phase 5).
Extracts:
1. Raw image metadata & inventory from data/raw/
2. Processed image metadata from data/processed/cleaned_metadata.csv
3. Extracted classical visual features from data/features/image_features.csv
"""
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

from src.ingestion.dataset_loader import DatasetInspector
from src.preprocessing.preprocessor import ImagePreprocessor
from src.feature_extraction.pipeline import FeatureExtractionPipeline
from src.utils.config import get_config
from src.utils.logger import setup_logger

logger = setup_logger("etl_extract")


class Extractor:
    """
    Extracts raw image metadata, processed image information, and visual features.
    """

    def __init__(self, raw_data_dir: Optional[str] = None):
        self.cfg = get_config()
        self.raw_data_dir = raw_data_dir or self.cfg["paths"]["raw_data_dir"]
        self.inspector = DatasetInspector(self.raw_data_dir)
        self.processed_dir = Path(self.cfg["paths"].get("processed_data_dir", "data/processed"))
        self.features_dir = Path(self.cfg["paths"].get("features_data_dir", "data/features"))

    def extract_raw_metadata(self) -> List[Dict[str, Any]]:
        """
        Discovers raw images and parses directory-level metadata.
        """
        logger.info("Extracting raw metadata from raw storage...")
        raw_inventory = self.inspector.scan_raw_directory()
        logger.info(f"Extracted {len(raw_inventory)} raw image metadata records.")
        return raw_inventory

    def extract_processed_metadata(self, raw_inventory: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Extracts preprocessed image metadata from cleaned_metadata.csv.
        If file is absent, runs the preprocessing pipeline to generate it.
        """
        metadata_file = self.processed_dir / "cleaned_metadata.csv"
        if metadata_file.exists():
            logger.info(f"Extracting processed metadata from {metadata_file}...")
            df = pd.read_csv(metadata_file)
            # Replace NaN failure reasons with empty string
            df["failure_reason"] = df["failure_reason"].fillna("")
            records = df.to_dict(orient="records")
            logger.info(f"Extracted {len(records)} preprocessed image records.")
            return records

        logger.warning("cleaned_metadata.csv not found on disk. Running ImagePreprocessor...")
        if raw_inventory is None:
            raw_inventory = self.extract_raw_metadata()
        preprocessor = ImagePreprocessor()
        report = preprocessor.run_pipeline(raw_inventory)
        return report["processed_records"]

    def extract_visual_features(self, valid_processed: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Extracts visual feature records from image_features.csv.
        If file is absent, runs the feature extraction pipeline.
        """
        features_file = self.features_dir / "image_features.csv"
        if features_file.exists():
            logger.info(f"Extracting visual features from {features_file}...")
            df = pd.read_csv(features_file)
            records = df.to_dict(orient="records")
            logger.info(f"Extracted {len(records)} visual feature records.")
            return records

        logger.warning("image_features.csv not found on disk. Running FeatureExtractionPipeline...")
        pipeline = FeatureExtractionPipeline()
        if valid_processed is not None:
            return pipeline.run_pipeline(valid_processed)
        return pipeline.run_batch_from_metadata()

    def extract_all(self) -> Dict[str, Any]:
        """
        Orchestrates full extraction across raw metadata, processed image metadata,
        and extracted visual features.
        """
        logger.info("Starting complete ETL Extraction phase...")
        raw_records = self.extract_raw_metadata()
        processed_records = self.extract_processed_metadata(raw_records)
        
        # Valid processed subset for feature alignment
        valid_processed = [r for r in processed_records if r.get("status") == "SUCCESS"]
        feature_records = self.extract_visual_features(valid_processed)

        extraction_bundle = {
            "raw_metadata": raw_records,
            "processed_metadata": processed_records,
            "visual_features": feature_records,
            "stats": {
                "raw_count": len(raw_records),
                "processed_count": len(processed_records),
                "valid_processed_count": len(valid_processed),
                "feature_count": len(feature_records)
            }
        }
        logger.info(
            f"Extraction completed successfully: {extraction_bundle['stats']['raw_count']} raw, "
            f"{extraction_bundle['stats']['processed_count']} processed, "
            f"{extraction_bundle['stats']['feature_count']} features."
        )
        return extraction_bundle
