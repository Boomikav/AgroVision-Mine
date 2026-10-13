"""
ETL Transform Step Module for AgroVision-Mine (Phase 5).
Performs:
1. Cleaning and sanitization of extracted metadata and feature records.
2. Standardizing crop and disease taxonomies based on verified ground truth.
3. Quality validation gates (rejects incomplete or corrupted records).
4. Constructing dimension entities (dim_crop, dim_disease, dim_image, dim_visual_feature).
5. Constructing fact staging records (disease_observation_fact).
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
            "botanical": "Oryza sativa",
            "category": "Cereal"
        })
        return {
            "crop_code": norm.upper() if norm else "RICE",
            "crop_name": norm.replace("_", " ").title() if norm else "Rice",
            "botanical_name": meta.get("botanical", "Oryza sativa"),
            "crop_category": meta.get("category", "Cereal"),
            "economic_significance": "Primary Food Grain / Commercial Staple"
        }

    def standardize_disease(self, raw_disease: str) -> Dict[str, str]:
        """Maps raw disease string to authentic plant pathology taxonomy."""
        norm = self.clean_text(raw_disease).lower().replace("-", "_").replace(" ", "_")
        if norm in ("none", "healthy", ""):
            return {
                "disease_code": "HEALTHY",
                "disease_name": "Healthy Foliage",
                "pathogen_type": "None",
                "causal_agent": "None",
                "primary_symptom": "Uniform green foliar tissue without macroscopic lesions"
            }

        if norm in ("bacterial_leaf_blight", "bacterial_blight"):
            return {
                "disease_code": "BACTERIAL_BLIGHT",
                "disease_name": "Bacterial Leaf Blight",
                "pathogen_type": "Bacterial",
                "causal_agent": "Xanthomonas oryzae pv. oryzae",
                "primary_symptom": "Water-soaked stripes turning yellowish-white along leaf margins"
            }
        elif norm == "brown_spot":
            return {
                "disease_code": "BROWN_SPOT",
                "disease_name": "Brown Spot",
                "pathogen_type": "Fungal",
                "causal_agent": "Bipolaris oryzae",
                "primary_symptom": "Oval to circular dark brown foliar lesions with yellow halo"
            }
        elif norm in ("leaf_smut", "smut"):
            return {
                "disease_code": "LEAF_SMUT",
                "disease_name": "Leaf Smut",
                "pathogen_type": "Fungal",
                "causal_agent": "Entyloma oryzae",
                "primary_symptom": "Small, angular black spots or linear stripes on leaf blade"
            }

        meta = KNOWN_PATHOGENS.get(norm, {
            "pathogen_type": "Pathogen",
            "causal_agent": "Unspecified"
        })
        return {
            "disease_code": norm.upper(),
            "disease_name": norm.replace("_", " ").title(),
            "pathogen_type": meta.get("pathogen_type", "Pathogen"),
            "causal_agent": meta.get("causal_agent", "Unspecified"),
            "primary_symptom": "Foliar lesion or chlorosis"
        }

    def validate_image_record(self, record: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates mandatory physical and optical attributes."""
        if record.get("status") != "SUCCESS":
            return False, f"Preprocessing status: {record.get('status')} ({record.get('failure_reason', 'Unknown')})"
        if not record.get("md5_hash"):
            return False, "Missing cryptographic MD5 digest"
        if not record.get("processed_path") or not Path(str(record["processed_path"])).exists():
            return False, "Missing processed image file on disk"
        if not record.get("raw_id"):
            return False, "Missing raw_id identifier"
        return True, ""

    def validate_feature_record(self, record: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates completeness of extracted numerical visual features."""
        required_numeric = [
            "rgb_r_mean", "rgb_g_mean", "rgb_b_mean",
            "hsv_h_mean", "hsv_s_mean", "hsv_v_mean",
            "glcm_contrast", "glcm_homogeneity"
        ]
        for field in required_numeric:
            val = record.get(field)
            if val is None or not isinstance(val, (int, float)):
                return False, f"Missing or non-numeric feature: {field}"
        return True, ""

    def transform(self, extraction_bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes end-to-end transformation and constructs dimension and fact staging dictionaries.
        """
        processed_metadata = extraction_bundle.get("processed_metadata", [])
        visual_features = extraction_bundle.get("visual_features", [])

        logger.info(
            f"Transforming extraction bundle: {len(processed_metadata)} processed images, "
            f"{len(visual_features)} visual feature records."
        )

        # Build feature lookup map keyed by filename
        feature_lookup: Dict[str, Dict[str, Any]] = {}
        for feat in visual_features:
            fn = feat.get("filename")
            if fn:
                feature_lookup[fn] = feat

        dim_crops: Dict[str, Dict[str, Any]] = {}
        dim_diseases: Dict[str, Dict[str, Any]] = {}
        dim_images: List[Dict[str, Any]] = []
        dim_features: List[Dict[str, Any]] = []
        fact_records: List[Dict[str, Any]] = []
        rejected_records: List[Dict[str, Any]] = []

        # Always include standard reference baselines
        healthy_ref = self.standardize_disease("healthy")
        dim_diseases[healthy_ref["disease_code"]] = healthy_ref

        for proc_rec in processed_metadata:
            fn = proc_rec.get("filename", "")

            # 1. Image record validation
            is_valid_img, img_err = self.validate_image_record(proc_rec)
            if not is_valid_img:
                rejected_records.append({
                    "filename": fn,
                    "reason": img_err,
                    "stage": "IMAGE_VALIDATION"
                })
                continue

            # 2. Visual feature alignment & validation
            feat_rec = feature_lookup.get(fn)
            if not feat_rec:
                rejected_records.append({
                    "filename": fn,
                    "reason": f"No visual features extracted for file: {fn}",
                    "stage": "FEATURE_LOOKUP"
                })
                continue

            is_valid_feat, feat_err = self.validate_feature_record(feat_rec)
            if not is_valid_feat:
                rejected_records.append({
                    "filename": fn,
                    "reason": feat_err,
                    "stage": "FEATURE_VALIDATION"
                })
                continue

            # 3. Construct DimCrop record
            crop_meta = self.standardize_crop(proc_rec.get("crop_label", "rice"))
            dim_crops[crop_meta["crop_code"]] = crop_meta

            # 4. Construct DimDisease record
            disease_label = proc_rec.get("disease_label") or proc_rec.get("condition_label", "none")
            dis_meta = self.standardize_disease(disease_label)
            dim_diseases[dis_meta["disease_code"]] = dis_meta

            # 5. Construct DimImage record
            file_fmt = Path(fn).suffix.replace(".", "").upper() or "JPEG"
            img_entry = {
                "raw_id": proc_rec["raw_id"],
                "filename": fn,
                "file_format": file_fmt,
                "raw_width": int(proc_rec["raw_width"]),
                "raw_height": int(proc_rec["raw_height"]),
                "raw_channels": int(proc_rec.get("raw_channels", 3)),
                "raw_size_kb": float(proc_rec["raw_size_kb"]),
                "processed_width": int(proc_rec.get("processed_width", 256)),
                "processed_height": int(proc_rec.get("processed_height", 256)),
                "processed_size_kb": float(proc_rec.get("processed_size_kb", 0.0)),
                "md5_hash": str(proc_rec["md5_hash"]),
                "phash": str(proc_rec.get("phash", "")),
                "blur_score": float(proc_rec.get("blur_score", 0.0)),
                "is_blurry": bool(proc_rec.get("is_blurry", False)),
                "original_path": str(proc_rec["raw_path"]),
                "processed_path": str(proc_rec["processed_path"])
            }
            dim_images.append(img_entry)

            # 6. Construct DimVisualFeature record
            feat_entry = {
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

            # 7. Construct DiseaseObservationFact record
            lesion_ratio = float(feat_rec.get("lesion_coverage_ratio", 0.0))
            severity_est = round(min(lesion_ratio * 10.0, 10.0), 2) if dis_meta["disease_code"] != "HEALTHY" else 0.0
            sharpness = float(proc_rec.get("blur_score", 0.0))
            contrast_norm = float(feat_rec.get("glcm_contrast_norm", 0.0))
            latency = float(proc_rec.get("processing_latency_ms", 0.0))

            fact_entry = {
                "crop_code": crop_meta["crop_code"],
                "disease_code": dis_meta["disease_code"],
                "raw_id": proc_rec["raw_id"],
                "image_filename": fn,
                "observation_count": 1,
                "lesion_severity_score": severity_est,
                "image_sharpness_score": sharpness,
                "lesion_coverage_ratio": lesion_ratio,
                "texture_contrast_norm": contrast_norm,
                "processing_latency_ms": latency
            }
            fact_records.append(fact_entry)

        logger.info(
            f"Transformation complete: Staged {len(fact_records)} facts, "
            f"{len(dim_crops)} crops, {len(dim_diseases)} diseases, "
            f"{len(dim_images)} images, {len(dim_features)} features, "
            f"{len(rejected_records)} rejected."
        )

        return {
            "dim_crops": list(dim_crops.values()),
            "dim_diseases": list(dim_diseases.values()),
            "dim_images": dim_images,
            "dim_features": dim_features,
            "fact_records": fact_records,
            "rejected_records": rejected_records
        }
