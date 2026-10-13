"""
AgroVision-Mine: Canonical Dataset v2 Pipeline (Phases 3 & 4).
Processes authentic multi-crop image sources (ICAR Rice + PlantDoc ACM 2020),
executes quality gate auditing, deduplication, standardized 256x256 RGB preprocessing,
feature extraction (34 visual descriptors + 10 metadata columns),
and generates versioned manifests and audit reports.
"""
import os
import sys
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
from PIL import Image

root = Path(r"c:\Users\ajaya\Desktop\Agro")
sys.path.insert(0, str(root))

from src.utils.logger import setup_logger
from src.preprocessing.duplicate_detector import DuplicateDetector
from src.preprocessing.validator import ImageValidator
from src.feature_extraction.pipeline import ClassicalFeatureExtractor

logger = setup_logger("canonical_v2_pipeline")

# =============================================================================
# 1. TAXONOMY MAPPING DEFINITIONS
# =============================================================================

# PlantDoc 28 classes + ICAR 3 classes -> Canonical Mapping
CLASS_MAPPING = {
    # ICAR Rice subset
    "bacterial_leaf_blight": {
        "crop": "Rice", "disease": "Bacterial Leaf Blight",
        "pathogen": "Bacterial", "status": "Diseased", "is_pest": False, "source": "icar_ogd"
    },
    "brown_spot": {
        "crop": "Rice", "disease": "Brown Spot",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "icar_ogd"
    },
    "leaf_smut": {
        "crop": "Rice", "disease": "Leaf Smut",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "icar_ogd"
    },
    # PlantDoc Classes
    "Apple Scab Leaf": {
        "crop": "Apple", "disease": "Apple Scab",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Apple leaf": {
        "crop": "Apple", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Apple rust leaf": {
        "crop": "Apple", "disease": "Cedar Apple Rust",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Bell_pepper leaf": {
        "crop": "Bell Pepper", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Bell_pepper leaf spot": {
        "crop": "Bell Pepper", "disease": "Bacterial Spot",
        "pathogen": "Bacterial", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Blueberry leaf": {
        "crop": "Blueberry", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Cherry leaf": {
        "crop": "Cherry", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Corn Gray leaf spot": {
        "crop": "Corn", "disease": "Gray Leaf Spot",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Corn leaf blight": {
        "crop": "Corn", "disease": "Northern Leaf Blight",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Corn rust leaf": {
        "crop": "Corn", "disease": "Common Rust",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Peach leaf": {
        "crop": "Peach", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Potato leaf early blight": {
        "crop": "Potato", "disease": "Early Blight",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Potato leaf late blight": {
        "crop": "Potato", "disease": "Late Blight",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Raspberry leaf": {
        "crop": "Raspberry", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Soyabean leaf": {
        "crop": "Soybean", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Squash Powdery mildew leaf": {
        "crop": "Squash", "disease": "Powdery Mildew",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Strawberry leaf": {
        "crop": "Strawberry", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Tomato Early blight leaf": {
        "crop": "Tomato", "disease": "Early Blight",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato Septoria leaf spot": {
        "crop": "Tomato", "disease": "Septoria Leaf Spot",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato leaf": {
        "crop": "Tomato", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "Tomato leaf bacterial spot": {
        "crop": "Tomato", "disease": "Bacterial Spot",
        "pathogen": "Bacterial", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato leaf late blight": {
        "crop": "Tomato", "disease": "Late Blight",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato leaf mosaic virus": {
        "crop": "Tomato", "disease": "Mosaic Virus",
        "pathogen": "Viral", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato leaf yellow virus": {
        "crop": "Tomato", "disease": "Yellow Leaf Curl Virus",
        "pathogen": "Viral", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato mold leaf": {
        "crop": "Tomato", "disease": "Leaf Mold",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    },
    "Tomato two spotted spider mites leaf": {
        "crop": "Tomato", "disease": "Two-Spotted Spider Mite",
        "pathogen": "Pest", "status": "Diseased", "is_pest": True, "source": "plantdoc"
    },
    "grape leaf": {
        "crop": "Grape", "disease": "Healthy",
        "pathogen": "None", "status": "Healthy", "is_pest": False, "source": "plantdoc"
    },
    "grape leaf black rot": {
        "crop": "Grape", "disease": "Black Rot",
        "pathogen": "Fungal", "status": "Diseased", "is_pest": False, "source": "plantdoc"
    }
}

SOURCE_REGISTRY = [
    {
        "source_id": "icar_ogd",
        "dataset_name": "Government of India / ICAR Crop Pathology Subset",
        "provenance_url": "https://data.gov.in/catalogs",
        "institution": "ICAR-CRIDA / ICAR-IIRR / Government of India",
        "license": "Government Open Data License - India (GODL-India)",
        "crops": ["Rice"],
        "imaging_setting": "Field Macro Photography",
        "role_in_study": "Baseline Authentic Cereal Pathology"
    },
    {
        "source_id": "plantdoc",
        "dataset_name": "PlantDoc: A Dataset for Visual Plant Disease Detection",
        "provenance_url": "https://github.com/pratikkayal/PlantDoc-Dataset",
        "institution": "IIT Kharagpur / ACM CoDS-COMAD 2020",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "crops": ["Apple", "Bell Pepper", "Blueberry", "Cherry", "Corn", "Peach", "Potato", "Raspberry", "Soybean", "Squash", "Strawberry", "Tomato", "Grape"],
        "imaging_setting": "In-Field Complex Natural Agricultural Environments",
        "role_in_study": "Multi-Crop Generalization & Diverse Pathologies"
    }
]

# =============================================================================
# 2. AUDIT & EXTRACTION ENGINE
# =============================================================================

def compute_md5(file_path: Path) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def compute_laplacian_variance(img_pil: Image.Image) -> float:
    gray = img_pil.convert("L")
    arr = np.asarray(gray, dtype=np.float64)
    # 3x3 Laplacian kernel
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)
    # Simple convolution for variance estimation
    from scipy.signal import convolve2d
    lap = convolve2d(arr, kernel, mode="valid")
    return float(np.var(lap))

def run_canonical_pipeline():
    print("=" * 80)
    print("AGROVISION-MINE: CANONICAL DATASET V2 PIPELINE EXECUTION")
    print("=" * 80)

    t_start = time.perf_counter()

    # Directories
    manifests_dir = root / "data" / "manifests"
    reports_dir = root / "data" / "reports"
    processed_v2_dir = root / "data" / "processed_v2"
    features_dir = root / "data" / "features"

    manifests_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    processed_v2_dir.mkdir(parents=True, exist_ok=True)
    features_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save Class Mapping and Source Registry
    pd.DataFrame(SOURCE_REGISTRY).to_csv(manifests_dir / "source_registry_v2.csv", index=False)
    
    mapping_rows = []
    for k, v in CLASS_MAPPING.items():
        mapping_rows.append({
            "original_source_label": k,
            "canonical_crop_name": v["crop"],
            "canonical_disease_name": v["disease"],
            "pathogen_type": v["pathogen"],
            "condition_status": v["status"],
            "is_pest": v["is_pest"],
            "dataset_source": v["source"]
        })
    pd.DataFrame(mapping_rows).to_csv(manifests_dir / "class_mapping_v2.csv", index=False)
    print("Saved source_registry_v2.csv and class_mapping_v2.csv")

    # 2. Gather All Candidate Files
    candidates = []

    # ICAR Rice (36 images)
    raw_rice_dir = root / "data" / "raw" / "rice"
    for disease_folder in ["bacterial_leaf_blight", "brown_spot", "leaf_smut"]:
        f_dir = raw_rice_dir / disease_folder
        if f_dir.exists():
            for img_file in sorted(f_dir.glob("*.*")):
                if img_file.is_file() and img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    candidates.append({
                        "source": "icar_ogd",
                        "orig_class": disease_folder,
                        "raw_path": img_file,
                        "filename": img_file.name
                    })

    # PlantDoc (2572 images)
    plantdoc_images_dir = root / "data" / "external_raw" / "plantdoc" / "images"
    for split_dir in sorted(plantdoc_images_dir.glob("*")):
        if split_dir.is_dir():
            for cls_dir in sorted(split_dir.glob("*")):
                if cls_dir.is_dir():
                    cls_name = cls_dir.name
                    for img_file in sorted(cls_dir.glob("*.*")):
                        if img_file.is_file() and img_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
                            candidates.append({
                                "source": "plantdoc",
                                "orig_class": cls_name,
                                "raw_path": img_file,
                                "filename": img_file.name
                            })

    print(f"Total raw candidate files discovered: {len(candidates)}")

    # 3. Deduplication and Validation Gate
    seen_md5: Dict[str, str] = {} # md5 -> image_id
    seen_phash: Dict[str, str] = {} # phash -> image_id
    exclusions: List[Dict[str, Any]] = []
    canonical_records: List[Dict[str, Any]] = []

    feature_extractor = ClassicalFeatureExtractor()
    feature_records: List[Dict[str, Any]] = []

    processed_count = 0
    duplicate_count = 0
    invalid_count = 0

    print("Beginning Quality Validation, Deduplication, Preprocessing & Feature Extraction...")

    for idx, cand in enumerate(candidates):
        raw_path: Path = cand["raw_path"]
        orig_class = cand["orig_class"]
        source_id = cand["source"]

        # Validate file readability and dimensions
        try:
            with Image.open(raw_path) as img:
                w, h = img.size
                mode = img.mode
                if w < 32 or h < 32:
                    invalid_count += 1
                    exclusions.append({
                        "filename": cand["filename"],
                        "raw_path": str(raw_path.relative_to(root)),
                        "reason": f"INVALID_DIMENSIONS: {w}x{h} < 32px",
                        "source": source_id
                    })
                    continue

                # Compute MD5
                file_md5 = compute_md5(raw_path)
                if file_md5 in seen_md5:
                    duplicate_count += 1
                    exclusions.append({
                        "filename": cand["filename"],
                        "raw_path": str(raw_path.relative_to(root)),
                        "reason": f"EXACT_MD5_DUPLICATE: Matches {seen_md5[file_md5]}",
                        "source": source_id
                    })
                    continue

                # Compute dHash
                dhash_str = DuplicateDetector.compute_dhash(img)

                # Ensure RGB conversion
                img_rgb = img.convert("RGB")
                blur_score = compute_laplacian_variance(img_rgb)

                # Assign Canonical Surrogate ID
                image_id = f"AGRO_V2_{processed_count + 1:05d}"
                seen_md5[file_md5] = image_id
                seen_phash[dhash_str] = image_id

                # Taxonomy Lookup
                tax_info = CLASS_MAPPING.get(orig_class, {
                    "crop": "Unknown", "disease": orig_class,
                    "pathogen": "Unspecified", "status": "Diseased", "is_pest": False, "source": source_id
                })

                # Standardize Image to 256x256 RGB (Lanczos)
                dest_sub = processed_v2_dir / source_id / tax_info["crop"].lower().replace(" ", "_") / tax_info["disease"].lower().replace(" ", "_")
                dest_sub.mkdir(parents=True, exist_ok=True)
                dest_path = dest_sub / f"proc_{image_id}.png"

                img_std = img_rgb.resize((256, 256), Image.Resampling.LANCZOS)
                img_std.save(dest_path, format="PNG")

                # Extract Visual Features (34 Explainable Descriptors)
                features = feature_extractor.extract(img_std)

                # Combine with 10 Lineage & Metadata Fields
                features_row = {
                    "image_id": image_id,
                    "filename": cand["filename"],
                    "raw_path": str(raw_path.relative_to(root)).replace("\\", "/"),
                    "processed_path": str(dest_path.relative_to(root)).replace("\\", "/"),
                    "crop_label": tax_info["crop"],
                    "condition_label": tax_info["disease"],
                    "disease_label": tax_info["disease"],
                    "pest_label": "Two-Spotted Spider Mite" if tax_info["is_pest"] else "None",
                    "is_pest": tax_info["is_pest"],
                    "md5_hash": file_md5
                }
                # Add all 34 numeric descriptors
                features_row.update(features)
                feature_records.append(features_row)

                # Canonical record
                canonical_records.append({
                    "image_id": image_id,
                    "dataset_source": source_id,
                    "crop_name": tax_info["crop"],
                    "disease_name": tax_info["disease"],
                    "pathogen_type": tax_info["pathogen"],
                    "condition_status": tax_info["status"],
                    "is_pest": tax_info["is_pest"],
                    "original_source_label": orig_class,
                    "raw_filename": cand["filename"],
                    "raw_relative_path": str(raw_path.relative_to(root)).replace("\\", "/"),
                    "processed_relative_path": str(dest_path.relative_to(root)).replace("\\", "/"),
                    "raw_width": w,
                    "raw_height": h,
                    "raw_mode": mode,
                    "processed_width": 256,
                    "processed_height": 256,
                    "md5_hash": file_md5,
                    "dhash": dhash_str,
                    "blur_score": round(blur_score, 2),
                    "is_blurry": blur_score < 100.0,
                    "license": "GODL-India" if source_id == "icar_ogd" else "CC BY 4.0"
                })

                processed_count += 1
                if processed_count % 500 == 0:
                    print(f"  Processed {processed_count} unique images...")

        except Exception as e:
            invalid_count += 1
            exclusions.append({
                "filename": cand["filename"],
                "raw_path": str(raw_path.relative_to(root)),
                "reason": f"CORRUPTED_READ_ERROR: {str(e)}",
                "source": source_id
            })

    t_end = time.perf_counter()
    print(f"\nProcessing completed in {t_end - t_start:.2f} seconds:")
    print(f"  Retained Canonical Images: {len(canonical_records)}")
    print(f"  Exact Duplicates Excluded: {duplicate_count}")
    print(f"  Invalid / Sub-dimension Excluded: {invalid_count}")

    # 4. Save Canonical Manifest & Feature Store
    df_canonical = pd.DataFrame(canonical_records)
    df_canonical.to_csv(manifests_dir / "canonical_dataset_v2.csv", index=False)
    print(f"Saved: {manifests_dir / 'canonical_dataset_v2.csv'}")

    df_features = pd.DataFrame(feature_records)
    df_features.to_csv(features_dir / "image_features_v2.csv", index=False)
    print(f"Saved: {features_dir / 'image_features_v2.csv'} (Shape: {df_features.shape})")

    # 5. Save Reports
    # Exclusions
    with open(reports_dir / "dataset_exclusion_audit_v2.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_candidates": len(candidates),
            "retained_count": len(canonical_records),
            "duplicate_count": duplicate_count,
            "invalid_count": invalid_count,
            "exclusions": exclusions
        }, f, indent=2)

    # Class Distribution
    crop_dist = df_canonical["crop_name"].value_counts().to_dict()
    disease_dist = df_canonical["disease_name"].value_counts().to_dict()
    source_dist = df_canonical["dataset_source"].value_counts().to_dict()
    status_dist = df_canonical["condition_status"].value_counts().to_dict()
    pathogen_dist = df_canonical["pathogen_type"].value_counts().to_dict()

    class_dist_data = {
        "total_images": len(df_canonical),
        "source_distribution": source_dist,
        "crop_distribution": crop_dist,
        "disease_distribution": disease_dist,
        "status_distribution": status_dist,
        "pathogen_distribution": pathogen_dist
    }
    with open(reports_dir / "dataset_class_distribution_v2.json", "w", encoding="utf-8") as f:
        json.dump(class_dist_data, f, indent=2)

    # Duplicate Audit
    with open(reports_dir / "dataset_duplicate_audit_v2.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_hashes_evaluated": len(candidates),
            "unique_md5_hashes": len(seen_md5),
            "unique_dhashes": len(seen_phash),
            "exact_duplicate_exclusions": duplicate_count
        }, f, indent=2)

    # Dataset Acquisition Report
    with open(reports_dir / "dataset_acquisition_v2.json", "w", encoding="utf-8") as f:
        json.dump({
            "retrieval_date": "2026-10-12",
            "sources": SOURCE_REGISTRY,
            "total_candidates_discovered": len(candidates),
            "total_canonical_retained": len(canonical_records)
        }, f, indent=2)

    # Quality Report
    with open(reports_dir / "dataset_quality_v2.json", "w", encoding="utf-8") as f:
        json.dump({
            "mean_raw_width": float(df_canonical["raw_width"].mean()),
            "mean_raw_height": float(df_canonical["raw_height"].mean()),
            "mean_blur_score": float(df_canonical["blur_score"].mean()),
            "blurry_count": int(df_canonical["is_blurry"].sum()),
            "standardized_dimension": "256x256 RGB",
            "feature_columns_count": len(df_features.columns),
            "missing_feature_values": int(df_features.isna().sum().sum())
        }, f, indent=2)

    print("\nAll canonical manifests and audit reports generated successfully!")
    print(f"Summary: {len(df_canonical)} unique images across {len(crop_dist)} crops and {len(disease_dist)} disease categories.")

if __name__ == "__main__":
    run_canonical_pipeline()
