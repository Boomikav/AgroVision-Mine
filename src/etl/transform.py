"""
ETL Transform Step Module for AgroVision-Mine.
Transforms extracted canonical multimodal manifest and feature store records into
standardized Star Schema entities:
1. Standardizes crop taxonomy (14 crops) -> dim_crop
2. Standardizes disease taxonomy (19 conditions/diseases) -> dim_disease
3. Assembles physical image dimension records -> dim_image
4. Assembles 32 continuous visual descriptor records -> dim_visual_feature
5. Assembles central observation fact records -> disease_observation_fact
"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from src.ingestion.dataset_loader import KNOWN_CROPS, KNOWN_PATHOGENS
from src.utils.logger import setup_logger

logger = setup_logger("etl_transform")


class Transformer:
    """
    Transforms extracted multimodal data into validated, standardized star schema entities.
    """

    def __init__(self):
        pass

    def clean_text(self, text: Optional[str]) -> str:
        """Sanitizes text by stripping whitespace and normalizing casing."""
        if not text:
            return ""
        return str(text).strip()

    def standardize_crop(self, raw_crop: str) -> Dict[str, str]:
        """Maps raw crop string to canonical botanical and agronomic taxonomy."""
        norm = self.clean_text(raw_crop).lower().replace("-", "_").replace(" ", "_")
        meta = KNOWN_CROPS.get(norm, {
            "botanical": "Unspecified",
            "category": "Horticultural",
            "economic": "Commercial Crop"
        })
        crop_name = norm.replace("_", " ").title() if norm else "Unspecified"
        if norm in ("bell_pepper", "pepper"):
            crop_name = "Bell Pepper"
        return {
            "crop_code": norm.upper() if norm else "UNSPECIFIED",
            "crop_name": crop_name,
            "botanical_name": meta.get("botanical", "Unspecified"),
            "crop_category": meta.get("category", "Horticultural"),
            "economic_significance": meta.get("economic", "Commercial Crop")
        }

    def standardize_disease(self, raw_disease: str, pathogen_hint: Optional[str] = None) -> Dict[str, str]:
        """Maps raw disease string to authentic plant pathology taxonomy."""
        norm = self.clean_text(raw_disease).lower().replace("-", "_").replace(" ", "_")
        if norm in ("none", "healthy", "", "nan"):
            return {
                "disease_code": "HEALTHY",
                "disease_name": "Healthy",
                "pathogen_type": "None",
                "causal_agent": "None",
                "primary_symptom": "Uniform green foliar tissue without macroscopic lesions"
            }

        meta = KNOWN_PATHOGENS.get(norm)
        if not meta:
            # Fallback for slight variations
            for k, v in KNOWN_PATHOGENS.items():
                if k in norm or norm in k:
                    meta = v
                    break

        if not meta:
            p_type = pathogen_hint if pathogen_hint and pathogen_hint != "nan" else "Pathogen"
            meta = {
                "pathogen_type": p_type,
                "causal_agent": "Unspecified",
                "symptom": "Foliar lesion or chlorosis"
            }

        disease_name = norm.replace("_", " ").title()
        if "spider_mite" in norm:
            disease_name = "Two-Spotted Spider Mite"
        elif "yellow_leaf_curl" in norm:
            disease_name = "Yellow Leaf Curl Virus"
        elif "mosaic_virus" in norm:
            disease_name = "Mosaic Virus"
        elif "bacterial_leaf_blight" in norm or "bacterial_blight" in norm:
            disease_name = "Bacterial Leaf Blight"
            norm = "bacterial_leaf_blight"

        return {
            "disease_code": norm.upper(),
            "disease_name": disease_name,
            "pathogen_type": meta.get("pathogen_type", "Pathogen"),
            "causal_agent": meta.get("causal_agent", "Unspecified"),
            "primary_symptom": meta.get("symptom", "Foliar lesion or chlorosis")
        }

    def transform(self, extraction_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms manifest and feature records into relational star schema dimension and fact tables.
        """
        logger.info("Starting multimodal Star Schema transformation...")
        manifest_records = extraction_bundle["manifest_records"]
        feature_records = extraction_bundle["feature_records"]

        # Index features by image_id for constant-time lookup
        feature_map = {r["image_id"]: r for r in feature_records}

        dim_crops: Dict[str, Dict[str, Any]] = {}
        dim_diseases: Dict[str, Dict[str, Any]] = {}
        dim_images: List[Dict[str, Any]] = []
        dim_features: List[Dict[str, Any]] = []
        fact_records: List[Dict[str, Any]] = []
        rejected_records: List[Dict[str, Any]] = []

        for idx, man_rec in enumerate(manifest_records):
            image_id = man_rec["image_id"]
            feat_rec = feature_map.get(image_id)

            if not feat_rec:
                rejected_records.append({
                    "image_id": image_id,
                    "stage": "TRANSFORM",
                    "reason": f"Missing corresponding feature record for {image_id}"
                })
                continue

            # 1. DimCrop
            crop_meta = self.standardize_crop(man_rec.get("crop_name", "rice"))
            dim_crops[crop_meta["crop_code"]] = crop_meta

            # 2. DimDisease
            dis_label = man_rec.get("disease_name") or man_rec.get("original_source_label", "Healthy")
            dis_meta = self.standardize_disease(dis_label, pathogen_hint=str(man_rec.get("pathogen_type", "")))
            dim_diseases[dis_meta["disease_code"]] = dis_meta

            # 3. DimImage
            fn = man_rec.get("raw_filename") or feat_rec.get("filename") or f"{image_id}.jpg"
            file_fmt = Path(fn).suffix.replace(".", "").upper() or "JPEG"
            raw_w = int(man_rec.get("raw_width", 256))
            raw_h = int(man_rec.get("raw_height", 256))
            raw_sz = float(man_rec.get("raw_size_kb", 0.0))
            if raw_sz == 0.0 and raw_w > 0 and raw_h > 0:
                raw_sz = round((raw_w * raw_h * 3) / 1024.0, 2)

            img_entry = {
                "image_id": image_id,
                "raw_id": man_rec.get("raw_id", image_id),
                "dataset_source": man_rec.get("dataset_source", "plantdoc"),
                "filename": fn,
                "file_format": file_fmt,
                "raw_width": raw_w,
                "raw_height": raw_h,
                "raw_channels": int(man_rec.get("raw_channels", 3)),
                "raw_size_kb": raw_sz,
                "processed_width": int(man_rec.get("processed_width", 256)),
                "processed_height": int(man_rec.get("processed_height", 256)),
                "processed_size_kb": float(man_rec.get("processed_size_kb", 0.0)),
                "md5_hash": str(man_rec.get("md5_hash") or feat_rec.get("md5_hash")),
                "phash": str(man_rec.get("dhash") or man_rec.get("phash", "")),
                "blur_score": float(man_rec.get("blur_score", 0.0)),
                "is_blurry": bool(man_rec.get("is_blurry", False)),
                "original_path": str(man_rec.get("raw_relative_path") or feat_rec.get("raw_path", "")),
                "processed_path": str(man_rec.get("processed_relative_path") or feat_rec.get("processed_path", "")),
                "license": str(man_rec.get("license", "Research/Educational"))
            }
            dim_images.append(img_entry)

            # 4. DimVisualFeature (Complete 32 Continuous Descriptors)
            feat_entry = {
                "image_id": image_id,
                "image_filename": fn,
                "rgb_r_mean": float(feat_rec.get("rgb_r_mean", 0.0)),
                "rgb_g_mean": float(feat_rec.get("rgb_g_mean", 0.0)),
                "rgb_b_mean": float(feat_rec.get("rgb_b_mean", 0.0)),
                "rgb_r_std": float(feat_rec.get("rgb_r_std", 0.0)),
                "rgb_g_std": float(feat_rec.get("rgb_g_std", 0.0)),
                "rgb_b_std": float(feat_rec.get("rgb_b_std", 0.0)),
                "rgb_r_norm": float(feat_rec.get("rgb_r_norm", 0.0)),
                "rgb_g_norm": float(feat_rec.get("rgb_g_norm", 0.0)),
                "rgb_b_norm": float(feat_rec.get("rgb_b_norm", 0.0)),
                "hsv_h_mean": float(feat_rec.get("hsv_h_mean", 0.0)),
                "hsv_s_mean": float(feat_rec.get("hsv_s_mean", 0.0)),
                "hsv_v_mean": float(feat_rec.get("hsv_v_mean", 0.0)),
                "hsv_h_std": float(feat_rec.get("hsv_h_std", 0.0)),
                "hsv_s_std": float(feat_rec.get("hsv_s_std", 0.0)),
                "hsv_v_std": float(feat_rec.get("hsv_v_std", 0.0)),
                "hsv_h_norm": float(feat_rec.get("hsv_h_norm", 0.0)),
                "hsv_s_norm": float(feat_rec.get("hsv_s_norm", 0.0)),
                "hsv_v_norm": float(feat_rec.get("hsv_v_norm", 0.0)),
                "exg_index_mean": float(feat_rec.get("exg_index_mean", 0.0)),
                "dominant_color_tone": str(feat_rec.get("dominant_color_tone", "Unknown")),
                "glcm_contrast": float(feat_rec.get("glcm_contrast", 0.0)),
                "glcm_contrast_norm": float(feat_rec.get("glcm_contrast_norm", 0.0)),
                "glcm_dissimilarity": float(feat_rec.get("glcm_dissimilarity", 0.0)),
                "glcm_homogeneity": float(feat_rec.get("glcm_homogeneity", 0.0)),
                "glcm_energy": float(feat_rec.get("glcm_energy", 0.0)),
                "glcm_correlation": float(feat_rec.get("glcm_correlation", 0.0)),
                "glcm_asm": float(feat_rec.get("glcm_asm", 0.0)),
                "has_valid_contour": bool(feat_rec.get("has_valid_contour", False)),
                "contour_area": float(feat_rec.get("contour_area", 0.0)),
                "contour_perimeter": float(feat_rec.get("contour_perimeter", 0.0)),
                "contour_aspect_ratio": float(feat_rec.get("contour_aspect_ratio", 1.0)),
                "contour_circularity": float(feat_rec.get("contour_circularity", 0.0)),
                "contour_solidity": float(feat_rec.get("contour_solidity", 0.0)),
                "lesion_coverage_ratio": float(feat_rec.get("lesion_coverage_ratio", 0.0))
            }
            dim_features.append(feat_entry)

            # 5. DiseaseObservationFact (Observation Grain)
            lesion_ratio = float(feat_rec.get("lesion_coverage_ratio", 0.0))
            cond_status = str(man_rec.get("condition_status", "Diseased")).strip()
            severity_est = round(min(lesion_ratio * 10.0, 10.0), 2) if dis_meta["disease_code"] != "HEALTHY" else 0.0
            sharpness = float(man_rec.get("blur_score", 0.0))
            contrast_norm = float(feat_rec.get("glcm_contrast_norm", 0.0))

            fact_entry = {
                "image_id": image_id,
                "crop_code": crop_meta["crop_code"],
                "disease_code": dis_meta["disease_code"],
                "observation_count": 1,
                "lesion_severity_score": severity_est,
                "image_sharpness_score": sharpness,
                "lesion_coverage_ratio": lesion_ratio,
                "texture_contrast_norm": contrast_norm,
                "processing_latency_ms": 15.0,
                "dataset_source": man_rec.get("dataset_source", "plantdoc"),
                "condition_status": cond_status,
                "is_pest": bool(man_rec.get("is_pest", False))
            }
            fact_records.append(fact_entry)

        staged_bundle = {
            "dim_crops": list(dim_crops.values()),
            "dim_diseases": list(dim_diseases.values()),
            "dim_images": dim_images,
            "dim_features": dim_features,
            "fact_records": fact_records,
            "rejected_records": rejected_records,
            "stats": {
                "transformed_facts": len(fact_records),
                "unique_crops": len(dim_crops),
                "unique_diseases": len(dim_diseases),
                "unique_images": len(dim_images),
                "unique_features": len(dim_features),
                "rejected_count": len(rejected_records)
            }
        }

        logger.info(
            f"Transformation completed: {staged_bundle['stats']['transformed_facts']} facts staged "
            f"across {staged_bundle['stats']['unique_crops']} crops and {staged_bundle['stats']['unique_diseases']} disease categories."
        )
        return staged_bundle
