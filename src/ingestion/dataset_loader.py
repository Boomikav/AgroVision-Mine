"""
Dataset Ingestion and Source Inspection Module for AgroVision-Mine.
Handles strict inspection of raw agricultural imagery without fabricating labels or metadata.
"""
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from src.utils.config import get_config
from src.utils.logger import setup_logger
from src.utils.io import compute_file_hash, save_json

logger = setup_logger("ingestion")

# Authentic ICAR / Agronomic taxonomy mapping for standardization
# Standardizes common label variations to clean botanical and agronomic categories
KNOWN_CROPS = {
    "rice": {"botanical": "Oryza sativa", "category": "Cereal", "economic": "Primary Food Grain / Commercial Staple"},
    "paddy": {"botanical": "Oryza sativa", "category": "Cereal", "economic": "Primary Food Grain / Commercial Staple"},
    "apple": {"botanical": "Malus domestica", "category": "Horticultural", "economic": "High-Value Commercial Fruit"},
    "bell_pepper": {"botanical": "Capsicum annuum", "category": "Horticultural", "economic": "Commercial Vegetable Crop"},
    "pepper": {"botanical": "Capsicum annuum", "category": "Horticultural", "economic": "Commercial Vegetable Crop"},
    "blueberry": {"botanical": "Vaccinium corymbosum", "category": "Horticultural", "economic": "High-Value Berry Crop"},
    "cherry": {"botanical": "Prunus avium", "category": "Horticultural", "economic": "High-Value Commercial Fruit"},
    "corn": {"botanical": "Zea mays", "category": "Cereal", "economic": "Major Feed Grain & Industrial Staple"},
    "maize": {"botanical": "Zea mays", "category": "Cereal", "economic": "Major Feed Grain & Industrial Staple"},
    "grape": {"botanical": "Vitis vinifera", "category": "Horticultural", "economic": "Viticulture & Commercial Fruit"},
    "peach": {"botanical": "Prunus persica", "category": "Horticultural", "economic": "Commercial Stone Fruit"},
    "potato": {"botanical": "Solanum tuberosum", "category": "Horticultural", "economic": "Essential Global Tuber Staple"},
    "raspberry": {"botanical": "Rubus idaeus", "category": "Horticultural", "economic": "High-Value Commercial Berry"},
    "soybean": {"botanical": "Glycine max", "category": "Legume", "economic": "Critical Global Protein & Oil Crop"},
    "squash": {"botanical": "Cucurbita pepo", "category": "Horticultural", "economic": "Commercial Cucurbit Vegetable"},
    "strawberry": {"botanical": "Fragaria × ananassa", "category": "Horticultural", "economic": "High-Value Commercial Berry"},
    "tomato": {"botanical": "Solanum lycopersicum", "category": "Horticultural", "economic": "Global Commercial Vegetable Staple"},
    "wheat": {"botanical": "Triticum aestivum", "category": "Cereal", "economic": "Major Global Cereal Staple"},
    "cotton": {"botanical": "Gossypium hirsutum", "category": "Fiber", "economic": "Global Commercial Fiber Crop"},
    "mustard": {"botanical": "Brassica nigra", "category": "Oilseed", "economic": "Commercial Oilseed Crop"}
}

KNOWN_PATHOGENS = {
    "healthy": {"pathogen_type": "None", "causal_agent": "None", "symptom": "Uniform green foliar tissue without macroscopic lesions"},
    "apple_scab": {"pathogen_type": "Fungal", "causal_agent": "Venturia inaequalis", "symptom": "Dull olive-green to black velvety spots on leaves"},
    "cedar_apple_rust": {"pathogen_type": "Fungal", "causal_agent": "Gymnosporangium juniperi-virginianae", "symptom": "Bright yellow-orange foliar lesions with small black pycnidia"},
    "bacterial_spot": {"pathogen_type": "Bacterial", "causal_agent": "Xanthomonas campestris pv. vesicatoria", "symptom": "Small, dark brown to black circular lesions with yellow halos"},
    "common_rust": {"pathogen_type": "Fungal", "causal_agent": "Puccinia sorghi", "symptom": "Golden brown to dark reddish-brown pustules on both leaf surfaces"},
    "gray_leaf_spot": {"pathogen_type": "Fungal", "causal_agent": "Cercospora zeae-maydis", "symptom": "Tan to gray rectangular lesions bounded by leaf veins"},
    "northern_leaf_blight": {"pathogen_type": "Fungal", "causal_agent": "Exserohilum turcicum", "symptom": "Long, elliptical grayish-green or tan lesions"},
    "black_rot": {"pathogen_type": "Fungal", "causal_agent": "Guignardia bidwellii", "symptom": "Circular reddish-brown necrotic spots with black pycnidia rings"},
    "early_blight": {"pathogen_type": "Fungal", "causal_agent": "Alternaria solani", "symptom": "Dark brown to black necrotic spots with concentric ring pattern"},
    "late_blight": {"pathogen_type": "Fungal", "causal_agent": "Phytophthora infestans", "symptom": "Pale green to dark water-soaked lesions with white mycelial margins"},
    "powdery_mildew": {"pathogen_type": "Fungal", "causal_agent": "Podosphaera xanthii", "symptom": "White talcum-like powdery fungal growth on foliar surfaces"},
    "bacterial_leaf_blight": {"pathogen_type": "Bacterial", "causal_agent": "Xanthomonas oryzae pv. oryzae", "symptom": "Water-soaked stripes turning yellowish-white along leaf margins"},
    "bacterial_blight": {"pathogen_type": "Bacterial", "causal_agent": "Xanthomonas oryzae", "symptom": "Water-soaked stripes turning yellowish-white along leaf margins"},
    "brown_spot": {"pathogen_type": "Fungal", "causal_agent": "Bipolaris oryzae", "symptom": "Oval to circular dark brown foliar lesions with yellow halo"},
    "leaf_smut": {"pathogen_type": "Fungal", "causal_agent": "Entyloma oryzae", "symptom": "Small, angular black spots or linear stripes on leaf blade"},
    "smut": {"pathogen_type": "Fungal", "causal_agent": "Entyloma oryzae", "symptom": "Small, angular black spots or linear stripes on leaf blade"},
    "leaf_mold": {"pathogen_type": "Fungal", "causal_agent": "Passalora fulva", "symptom": "Pale greenish-yellow spots on upper leaf with olive-brown velvety mold on underside"},
    "mosaic_virus": {"pathogen_type": "Viral", "causal_agent": "Tomato mosaic virus (ToMV)", "symptom": "Mottling with alternating yellowish and dark green patches and leaf distortion"},
    "yellow_leaf_curl_virus": {"pathogen_type": "Viral", "causal_agent": "Tomato yellow leaf curl virus (TYLCV)", "symptom": "Severe stunting, upward leaf curling, and chlorotic yellow foliar margins"},
    "septoria_leaf_spot": {"pathogen_type": "Fungal", "causal_agent": "Septoria lycopersici", "symptom": "Circular spots with dark brown margins and sunken tan or gray centers"},
    "two_spotted_spider_mite": {"pathogen_type": "Pest", "causal_agent": "Tetranychus urticae", "symptom": "Fine yellow or white stippling and webbing on foliar surfaces"},
    "spider_mite": {"pathogen_type": "Pest", "causal_agent": "Tetranychus urticae", "symptom": "Fine yellow or white stippling and webbing on foliar surfaces"},
    "blast": {"pathogen_type": "Fungal", "causal_agent": "Magnaporthe oryzae", "symptom": "Spindle-shaped lesions with grayish centers"},
    "sheath_blight": {"pathogen_type": "Fungal", "causal_agent": "Rhizoctonia solani", "symptom": "Oval water-soaked lesions on leaf sheaths"},
    "tungro": {"pathogen_type": "Viral", "causal_agent": "Rice tungro bacilliform virus", "symptom": "Yellow-orange foliar discoloration and stunting"},
    "rust": {"pathogen_type": "Fungal", "causal_agent": "Puccinia spp.", "symptom": "Pustules on leaf surfaces"},
    "leaf_curl": {"pathogen_type": "Viral", "causal_agent": "Begomovirus", "symptom": "Leaf curling and stunting"}
}

KNOWN_PESTS = {
    "stem_borer": {"scientific_name": "Scirpophaga incertulas", "pest_type": "Lepidoptera"},
    "brown_planthopper": {"scientific_name": "Nilaparvata lugens", "pest_type": "Hemiptera"},
    "bollworm": {"scientific_name": "Helicoverpa armigera", "pest_type": "Lepidoptera"},
    "aphid": {"scientific_name": "Aphis gossypii", "pest_type": "Hemiptera"},
    "whitefly": {"scientific_name": "Bemisia tabaci", "pest_type": "Hemiptera"},
    "fall_armyworm": {"scientific_name": "Spodoptera frugiperda", "pest_type": "Lepidoptera"},
    "none": {"scientific_name": "None", "pest_type": "None"}
}


class DatasetInspector:
    """
    Inspects the raw dataset folder, validates real file existence,
    extracts structural metadata, and creates a source inventory.
    """

    def __init__(self, raw_data_dir: Optional[str] = None):
        cfg = get_config()
        self.raw_data_dir = Path(raw_data_dir or cfg["paths"]["raw_data_dir"]).resolve()
        self.allowed_extensions = set(
            ext.lower() for ext in cfg["preprocessing"].get(
                "allowed_extensions", [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"]
            )
        )
        self.reports_dir = Path(cfg["paths"]["reports_dir"]).resolve()
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def scan_raw_directory(self) -> List[Dict[str, Any]]:
        """
        Recursively discovers all image files in raw_data_dir.
        Derives metadata from genuine folder hierarchy or manifests.
        """
        if not self.raw_data_dir.exists():
            logger.warning(f"Raw data directory does not exist: {self.raw_data_dir}")
            return []

        inventory: List[Dict[str, Any]] = []
        file_count = 0

        for root, dirs, files in os.walk(self.raw_data_dir):
            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                if ext in self.allowed_extensions:
                    file_count += 1
                    rel_path = file_path.relative_to(self.raw_data_dir)
                    parts = rel_path.parts

                    # Derive taxonomy from directory structure
                    crop_label, condition_label = self._parse_path_components(parts, file_path.stem)
                    file_size_kb = round(file_path.stat().st_size / 1024, 2)
                    file_hash = compute_file_hash(file_path, "md5")

                    # Classify if disease or pest
                    is_pest, pest_label, disease_label = self._classify_condition(condition_label)

                    record = {
                        "raw_id": f"RAW_{file_count:06d}",
                        "filename": file,
                        "relative_path": str(rel_path).replace("\\", "/"),
                        "absolute_path": str(file_path.resolve()),
                        "file_extension": ext,
                        "file_size_kb": file_size_kb,
                        "md5_hash": file_hash,
                        "crop_label": crop_label,
                        "condition_raw": condition_label,
                        "is_pest": is_pest,
                        "disease_label": disease_label,
                        "pest_label": pest_label
                    }
                    inventory.append(record)

        logger.info(f"Scanned {self.raw_data_dir}: Found {len(inventory)} valid image files.")
        return inventory

    def _parse_path_components(self, parts: Tuple[str, ...], stem: str) -> Tuple[str, str]:
        """
        Derives crop and condition labels from directory structure.
        Supports:
          1. crop/condition/filename.jpg (len >= 3)
          2. crop_condition/filename.jpg (len == 2)
          3. flat folder with filename pattern: Crop___Disease_img.jpg
        """
        if len(parts) >= 3:
            crop = parts[0].strip().replace("-", "_").lower()
            condition = parts[1].strip().replace("-", "_").lower()
            return crop, condition
        elif len(parts) == 2:
            parent = parts[0].strip()
            if "___" in parent:
                c, cond = parent.split("___", 1)
                return c.lower().replace("-", "_"), cond.lower().replace("-", "_")
            elif "_" in parent:
                c, cond = parent.split("_", 1)
                return c.lower().replace("-", "_"), cond.lower().replace("-", "_")
            else:
                return parent.lower(), "unspecified"
        else:
            # Fallback to filename analysis
            if "___" in stem:
                c, cond = stem.split("___", 1)
                return c.lower().replace("-", "_"), cond.lower().replace("-", "_")
            return "unspecified_crop", "unspecified_condition"

    def _classify_condition(self, condition: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Classifies condition into disease or pest using standard agricultural taxonomy.
        """
        condition_norm = condition.lower().replace(" ", "_")
        for pest_key in KNOWN_PESTS:
            if pest_key != "none" and pest_key in condition_norm:
                return True, pest_key, "none"

        for disease_key in KNOWN_PATHOGENS:
            if disease_key in condition_norm:
                return False, "none", disease_key

        # Default classification
        if "healthy" in condition_norm:
            return False, "none", "healthy"

        return False, "none", condition_norm

    def generate_inventory_report(self) -> Dict[str, Any]:
        """
        Generates source inventory and saves it to data/reports/source_inventory.json.
        """
        inventory = self.scan_raw_directory()
        crops_dist: Dict[str, int] = {}
        conditions_dist: Dict[str, int] = {}
        total_size_kb = 0.0

        for item in inventory:
            crop = item["crop_label"]
            cond = item["condition_raw"]
            crops_dist[crop] = crops_dist.get(crop, 0) + 1
            conditions_dist[cond] = conditions_dist.get(cond, 0) + 1
            total_size_kb += item["file_size_kb"]

        report = {
            "source_directory": str(self.raw_data_dir),
            "total_images_discovered": len(inventory),
            "total_size_mb": round(total_size_kb / 1024, 2),
            "unique_crops_discovered": list(crops_dist.keys()),
            "crop_distribution": crops_dist,
            "condition_distribution": conditions_dist,
            "records": inventory
        }

        report_file = self.reports_dir / "source_inventory.json"
        save_json(report, report_file)
        logger.info(f"Source inventory report saved to: {report_file}")
        return report
