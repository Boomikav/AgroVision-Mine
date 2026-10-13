"""
Dataset Profiling and Schema Discovery Module for AgroVision-Mine (Phase 1).
Performs non-destructive, fact-based inspection of raw agricultural datasets.
Identifies genuine image assets, annotation files, EXIF metadata, and taxonomy without fabricating attributes.
"""
import os
import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from PIL import Image, ExifTags

from src.utils.config import get_config
from src.utils.logger import setup_logger
from src.utils.io import compute_file_hash, save_json

logger = setup_logger("profiler")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
ANNOTATION_EXTENSIONS = {".csv", ".json", ".xml", ".txt", ".tsv"}
METADATA_EXTENSIONS = {".yaml", ".yml", ".md", ".xlsx", ".xls"}

# Keywords used to detect potential column/manifest semantics
CROP_KEYWORDS = {"crop", "host", "plant", "cultivar", "species"}
DISEASE_KEYWORDS = {"disease", "pathology", "pathogen", "symptom", "condition", "infection", "disorder"}
PEST_KEYWORDS = {"pest", "insect", "infestation", "larva", "vector"}
GEO_KEYWORDS = {"state", "district", "region", "location", "latitude", "longitude", "lat", "lon", "gps", "village", "field", "taluk", "block"}
DATE_KEYWORDS = {"date", "year", "month", "season", "survey_date", "collection_date", "timestamp", "time"}


class DatasetProfiler:
    """
    Analyzes data/raw/ to discover the actual structure of the dataset.
    Strictly reports ground truth without synthetic fabrication.
    """

    def __init__(self, raw_dir: Optional[str] = None):
        cfg = get_config()
        self.raw_dir = Path(raw_dir or cfg["paths"]["raw_data_dir"]).resolve()
        self.reports_dir = Path(cfg["paths"]["reports_dir"]).resolve()
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def run_profiling(self) -> Dict[str, Any]:
        """
        Executes complete inspection across filesystem, file formats,
        metadata manifests, directory hierarchies, and EXIF attributes.
        """
        logger.info(f"Inspecting raw dataset directory: {self.raw_dir}")

        if not self.raw_dir.exists():
            return {
                "dataset_present": False,
                "error": f"Raw data directory does not exist: {self.raw_dir}",
                "total_files": 0
            }

        # 1. Discover all files
        all_files: List[Path] = [p for p in self.raw_dir.rglob("*") if p.is_file()]

        image_files: List[Path] = []
        annotation_files: List[Path] = []
        metadata_files: List[Path] = []
        other_files: List[Path] = []

        for p in all_files:
            ext = p.suffix.lower()
            if ext in IMAGE_EXTENSIONS:
                image_files.append(p)
            elif ext in ANNOTATION_EXTENSIONS and p.name.lower() not in {"readme.md"}:
                annotation_files.append(p)
            elif ext in METADATA_EXTENSIONS and p.name.lower() != "readme.md":
                metadata_files.append(p)
            else:
                other_files.append(p)

        is_empty = len(image_files) == 0 and len(annotation_files) == 0

        # 2. Inspect Annotation/Manifest files
        annotation_analysis = self._inspect_annotation_files(annotation_files)

        # 3. Inspect Directory Taxonomy
        directory_taxonomy = self._inspect_directory_hierarchy(image_files)

        # 4. Inspect Image Metadata & EXIF
        image_metadata_analysis = self._inspect_image_samples(image_files)

        # 5. Determine detected fields
        detected_fields = self._summarize_detected_fields(annotation_analysis, directory_taxonomy, image_metadata_analysis)

        # 6. Assess missing fields & schema implications
        schema_implications = self._derive_schema_implications(detected_fields, len(image_files))

        report = {
            "source_directory": str(self.raw_dir),
            "dataset_present": not is_empty,
            "file_counts": {
                "total_files": len(all_files),
                "image_files": len(image_files),
                "annotation_files": len(annotation_files),
                "metadata_files": len(metadata_files),
                "other_files": len(other_files)
            },
            "discovered_files": {
                "images": [str(p.relative_to(self.raw_dir)).replace("\\", "/") for p in image_files[:50]],
                "annotations": [str(p.relative_to(self.raw_dir)).replace("\\", "/") for p in annotation_files],
                "metadata": [str(p.relative_to(self.raw_dir)).replace("\\", "/") for p in metadata_files]
            },
            "annotation_schema": annotation_analysis,
            "directory_taxonomy": directory_taxonomy,
            "image_metadata_summary": image_metadata_analysis,
            "detected_fields": detected_fields,
            "schema_implications": schema_implications
        }

        # Save to JSON and Markdown reports
        json_report_file = self.reports_dir / "dataset_profiling_report.json"
        save_json(report, json_report_file)

        md_report_file = self.reports_dir / "dataset_profiling_report.md"
        self._write_markdown_report(report, md_report_file)

        logger.info(f"Dataset profiling completed. Found {len(image_files)} image files. Reports saved to {self.reports_dir}")
        return report

    def _inspect_annotation_files(self, annotation_files: List[Path]) -> Dict[str, Any]:
        """
        Parses CSV or JSON manifests to discover real column headers and data types.
        """
        results: Dict[str, Any] = {}
        for af in annotation_files:
            rel = str(af.relative_to(self.raw_dir)).replace("\\", "/")
            ext = af.suffix.lower()
            try:
                if ext == ".csv":
                    with open(af, "r", encoding="utf-8", errors="ignore") as f:
                        reader = csv.reader(f)
                        headers = next(reader, [])
                        sample_row = next(reader, [])
                    results[rel] = {
                        "type": "CSV",
                        "headers": headers,
                        "sample_row": sample_row,
                        "num_columns": len(headers)
                    }
                elif ext == ".json":
                    with open(af, "r", encoding="utf-8", errors="ignore") as f:
                        data = json.load(f)
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                        keys = list(data[0].keys())
                    elif isinstance(data, dict):
                        keys = list(data.keys())
                    else:
                        keys = []
                    results[rel] = {
                        "type": "JSON",
                        "top_level_keys": keys,
                        "record_count": len(data) if isinstance(data, list) else 1
                    }
            except Exception as e:
                results[rel] = {"type": ext, "error": str(e)}
        return results

    def _inspect_directory_hierarchy(self, image_files: List[Path]) -> Dict[str, Any]:
        """
        Extracts organizational depth and distinct directory categories from image paths.
        """
        if not image_files:
            return {"hierarchy_depth": 0, "patterns": [], "discovered_categories": {}}

        depths: Set[int] = set()
        level_values: Dict[int, Set[str]] = {}

        for p in image_files:
            rel = p.relative_to(self.raw_dir)
            parts = rel.parts[:-1]  # Exclude filename
            depths.add(len(parts))
            for idx, part in enumerate(parts):
                level_values.setdefault(idx, set()).add(part)

        discovered = {
            f"level_{idx + 1}": sorted(list(vals))
            for idx, vals in level_values.items()
        }

        return {
            "hierarchy_depths_detected": sorted(list(depths)),
            "level_categories": discovered
        }

    def _inspect_image_samples(self, image_files: List[Path], max_samples: int = 15) -> Dict[str, Any]:
        """
        Inspects sample images for physical dimensions, formats, and authentic EXIF data.
        """
        if not image_files:
            return {"samples_inspected": 0, "exif_detected": False}

        formats: Set[str] = set()
        resolutions: Set[Tuple[int, int]] = set()
        has_exif_data = False
        exif_keys_found: Set[str] = set()

        for p in image_files[:max_samples]:
            try:
                with Image.open(p) as img:
                    formats.add(img.format or p.suffix.upper().replace(".", ""))
                    resolutions.add(img.size)

                    # Check for genuine camera/GPS EXIF metadata
                    exif = img.getexif()
                    if exif:
                        has_exif_data = True
                        for tag_id in exif:
                            tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                            exif_keys_found.add(tag_name)
            except Exception as e:
                logger.debug(f"Could not read metadata for {p}: {e}")

        return {
            "samples_inspected": min(len(image_files), max_samples),
            "image_formats": sorted(list(formats)),
            "resolutions_sample": [f"{w}x{h}" for w, h in list(resolutions)[:5]],
            "exif_metadata_present": has_exif_data,
            "exif_tags_discovered": sorted(list(exif_keys_found))
        }

    def _summarize_detected_fields(
        self,
        annotations: Dict[str, Any],
        dir_taxonomy: Dict[str, Any],
        img_meta: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes detected fields across manifests, folder paths, and EXIF headers.
        """
        detected = {
            "crop_fields": [],
            "disease_fields": [],
            "pest_fields": [],
            "date_fields": [],
            "geography_fields": []
        }

        # Check annotation headers
        for rel_file, meta in annotations.items():
            headers = meta.get("headers", []) + meta.get("top_level_keys", [])
            for h in headers:
                hl = h.lower()
                if any(k in hl for k in CROP_KEYWORDS):
                    detected["crop_fields"].append(f"{rel_file}::{h}")
                if any(k in hl for k in DISEASE_KEYWORDS):
                    detected["disease_fields"].append(f"{rel_file}::{h}")
                if any(k in hl for k in PEST_KEYWORDS):
                    detected["pest_fields"].append(f"{rel_file}::{h}")
                if any(k in hl for k in DATE_KEYWORDS):
                    detected["date_fields"].append(f"{rel_file}::{h}")
                if any(k in hl for k in GEO_KEYWORDS):
                    detected["geography_fields"].append(f"{rel_file}::{h}")

        # Check directory hierarchy
        level_cats = dir_taxonomy.get("level_categories", {})
        if "level_1" in level_cats:
            detected["crop_fields"].append("directory_level_1")
        if "level_2" in level_cats:
            detected["disease_fields"].append("directory_level_2")

        # Check EXIF
        exif_tags = img_meta.get("exif_tags_discovered", [])
        for tag in exif_tags:
            tl = tag.lower()
            if "date" in tl or "time" in tl:
                detected["date_fields"].append(f"EXIF::{tag}")
            if "gps" in tl or "location" in tl:
                detected["geography_fields"].append(f"EXIF::{tag}")

        return detected

    def _derive_schema_implications(self, detected: Dict[str, Any], image_count: int) -> Dict[str, Any]:
        """
        Derives defensible data warehouse schema rules based on ground truth.
        """
        has_crops = len(detected["crop_fields"]) > 0
        has_diseases = len(detected["disease_fields"]) > 0
        has_pests = len(detected["pest_fields"]) > 0
        has_dates = len(detected["date_fields"]) > 0
        has_geo = len(detected["geography_fields"]) > 0

        recommendations: List[str] = [
            "Dim_Image is REQUIRED (stores physical resolution, format, MD5 hash, blur variance, file storage paths).",
            "Dim_VisualFeature is REQUIRED (stores classical RGB/HSV color moments, GLCM texture, and morphometric shape contours)."
        ]

        if has_crops:
            recommendations.append("Dim_Crop is SUPPORTED by raw data (link host crop taxonomy and botanical names).")
        else:
            recommendations.append("Dim_Crop cannot be derived automatically without user annotations.")

        if has_diseases or has_pests:
            recommendations.append("Dim_Disease and Dim_Pest are SUPPORTED by condition categorization.")

        if has_dates:
            recommendations.append("Dim_Time is SUPPORTED by legitimate timestamps discovered in raw data.")
        else:
            recommendations.append("Dim_Time MUST NOT be populated with synthetic dates (leave as nullable FK or exclude from Review 1 star schema).")

        if has_geo:
            recommendations.append("Dim_Geography is SUPPORTED by legitimate location/GPS fields.")
        else:
            recommendations.append("Dim_Geography MUST NOT invent fake districts/states (leave as nullable FK or exclude from Review 1 star schema).")

        return {
            "total_images_available": image_count,
            "dim_crop_supported": has_crops,
            "dim_disease_supported": has_diseases,
            "dim_pest_supported": has_pests,
            "dim_time_supported": has_dates,
            "dim_geography_supported": has_geo,
            "recommendations": recommendations
        }

    def _write_markdown_report(self, report: Dict[str, Any], output_path: Path) -> None:
        """
        Renders a clean academic markdown summary of the profiling inspection.
        """
        counts = report["file_counts"]
        schema = report["schema_implications"]
        detected = report["detected_fields"]
        rec_lines = "\n".join(["- " + r for r in schema["recommendations"]])
        cats_json = json.dumps(report["directory_taxonomy"].get("level_categories", {}), indent=2)

        md_content = f"""# AgroVision-Mine: Dataset Profiling & Ground-Truth Report
Generated by: `DatasetProfiler` (Phase 1 Ingestion Engine)
Inspected Path: `{report['source_directory']}`

---

## 1. Physical File Discovery
- **Dataset Present:** `{'YES' if report['dataset_present'] else 'NO (Awaiting Official ICAR Drop-in)'}`
- **Total Files Scanned:** `{counts['total_files']}`
- **Image Assets:** `{counts['image_files']}`
- **Annotation / Manifest Files:** `{counts['annotation_files']}`
- **Metadata Files:** `{counts['metadata_files']}`
- **Other Files:** `{counts['other_files']}`

---

## 2. Taxonomy & Structural Ground-Truth
- **Directory Hierarchy Depths:** `{report['directory_taxonomy'].get('hierarchy_depths_detected', [])}`
- **Discovered Categories by Level:**
```json
{cats_json}
```

---

## 3. Detected Field Semantics
- **Crop Fields:** `{detected['crop_fields']}`
- **Disease Fields:** `{detected['disease_fields']}`
- **Pest Fields:** `{detected['pest_fields']}`
- **Date Fields (Temporal):** `{detected['date_fields']}`
- **Geography Fields (Spatial):** `{detected['geography_fields']}`

---

## 4. Academic Schema Recommendations (No-Fabrication Mandate)
{rec_lines}

---
*AgroVision-Mine strictly derives dimensional schema entities from ground-truth data.*
"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
