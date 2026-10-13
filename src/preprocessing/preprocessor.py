"""
Image Preprocessing Pipeline Module for AgroVision-Mine (Phase 2).
Executes validation, duplicate elimination, non-destructive normalization,
and generates cleaned metadata and detailed rejection audit reports.
"""
import csv
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image

from src.utils.config import get_config
from src.utils.logger import setup_logger
from src.utils.io import save_json, compute_file_hash
from src.preprocessing.validator import ImageValidator, ValidationResult
from src.preprocessing.duplicate_detector import DuplicateDetector, DuplicateCheckResult

logger = setup_logger("preprocessor")


class ImagePreprocessor:
    """
    Executes end-to-end preprocessing, validation, and audit tracking.
    Guarantees no records are silently deleted and all rejections are auditable.
    """

    def __init__(self):
        self.cfg = get_config()
        prep_cfg = self.cfg.get("preprocessing", {})
        self.target_size = tuple(prep_cfg.get("target_size", [256, 256]))  # (width, height)
        self.color_space = prep_cfg.get("color_space", "RGB")
        self.processed_dir = Path(self.cfg["paths"]["processed_data_dir"]).resolve()
        self.reports_dir = Path(self.cfg["paths"]["reports_dir"]).resolve()
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.validator = ImageValidator()
        self.duplicate_detector = DuplicateDetector()

    def process_image(
        self,
        raw_image_path: Path,
        crop_label: str = "unspecified",
        condition_label: str = "unspecified"
    ) -> Dict[str, Any]:
        """
        Processes a single raw image through validation, duplicate detection, and standardization.
        """
        start_time = time.perf_counter()
        raw_path = Path(raw_image_path).resolve()

        record: Dict[str, Any] = {
            "filename": raw_path.name,
            "raw_path": str(raw_path).replace("\\", "/"),
            "crop_label": crop_label,
            "condition_label": condition_label,
            "processed_path": None,
            "status": "PENDING",
            "is_valid": False,
            "is_duplicate": False,
            "failure_reason": None,
            "processing_latency_ms": 0.0,
            "raw_width": 0,
            "raw_height": 0,
            "raw_channels": 0,
            "raw_size_kb": 0.0,
            "blur_score": 0.0,
            "is_blurry": False,
            "md5_hash": None,
            "phash": None,
            "processed_width": 0,
            "processed_height": 0,
            "processed_size_kb": 0.0
        }

        # Step 1: Validation
        val_res: ValidationResult = self.validator.validate(raw_path)
        record["raw_width"] = val_res.width
        record["raw_height"] = val_res.height
        record["raw_channels"] = val_res.channels
        record["raw_size_kb"] = val_res.file_size_kb
        record["blur_score"] = val_res.blur_score
        record["is_blurry"] = val_res.is_blurry

        if not val_res.is_valid:
            record["status"] = val_res.status
            record["is_valid"] = False
            record["failure_reason"] = val_res.failure_reason
            record["processing_latency_ms"] = round((time.perf_counter() - start_time) * 1000, 2)
            return record

        record["is_valid"] = True

        # Step 2: Open image and Duplicate Check
        try:
            with Image.open(raw_path) as img:
                # Duplicate check
                dup_res: DuplicateCheckResult = self.duplicate_detector.check_and_register(raw_path, img)
                record["md5_hash"] = dup_res.md5_hash
                record["phash"] = dup_res.perceptual_hash

                if dup_res.is_duplicate:
                    record["status"] = f"DUPLICATE_{dup_res.duplicate_type}"
                    record["is_duplicate"] = True
                    record["failure_reason"] = (
                        f"Duplicate of {dup_res.canonical_file} "
                        f"(Hamming distance: {dup_res.hamming_distance})"
                    )
                    record["processing_latency_ms"] = round((time.perf_counter() - start_time) * 1000, 2)
                    return record

                # Step 3: Standardization & Saving
                # Convert color space if necessary
                if img.mode != self.color_space:
                    processed_img = img.convert(self.color_space)
                else:
                    processed_img = img.copy()

                # High quality resize
                resized_img = processed_img.resize(self.target_size, Image.Resampling.LANCZOS)

                # Destination path
                crop_safe = crop_label.lower().replace(" ", "_")
                cond_safe = condition_label.lower().replace(" ", "_")
                dest_dir = self.processed_dir / crop_safe / cond_safe
                dest_dir.mkdir(parents=True, exist_ok=True)

                dest_file = dest_dir / f"proc_{raw_path.stem}.png"
                resized_img.save(dest_file, format="PNG", optimize=True)

                record["processed_path"] = str(dest_file.resolve()).replace("\\", "/")
                record["processed_width"] = self.target_size[0]
                record["processed_height"] = self.target_size[1]
                record["processed_size_kb"] = round(dest_file.stat().st_size / 1024, 2)
                record["status"] = "SUCCESS"

        except Exception as e:
            record["status"] = "PROCESSING_ERROR"
            record["is_valid"] = False
            record["failure_reason"] = f"Error during image processing: {str(e)}"

        record["processing_latency_ms"] = round((time.perf_counter() - start_time) * 1000, 2)
        return record

    def run_pipeline(self, raw_inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes preprocessing over the complete raw inventory.
        Generates:
          1. Cleaned metadata (CSV & JSON)
          2. Preprocessing statistics report (JSON & MD)
          3. Rejected images audit report (JSON & MD)
        """
        logger.info(f"Starting preprocessing pipeline on {len(raw_inventory)} inventory items...")
        self.duplicate_detector.reset()

        all_results: List[Dict[str, Any]] = []
        cleaned_records: List[Dict[str, Any]] = []
        rejected_records: List[Dict[str, Any]] = []
        failure_reasons: Dict[str, int] = {}

        counts = {
            "total_discovered": len(raw_inventory),
            "valid_images": 0,
            "invalid_images": 0,
            "corrupted_images": 0,
            "duplicate_images": 0,
            "processed_images": 0,
            "skipped_images": 0
        }

        for item in raw_inventory:
            raw_path = Path(item["absolute_path"])
            crop = item.get("crop_label", "unspecified")
            cond = item.get("condition_raw", "unspecified")

            res = self.process_image(raw_path, crop, cond)
            res["raw_id"] = item.get("raw_id", f"RAW_{len(all_results)+1:06d}")
            res["disease_label"] = item.get("disease_label", "none")
            res["pest_label"] = item.get("pest_label", "none")
            res["is_pest"] = item.get("is_pest", False)
            all_results.append(res)

            status = res["status"]
            if res["is_valid"]:
                counts["valid_images"] += 1
            else:
                counts["invalid_images"] += 1
                if status == "CORRUPTED":
                    counts["corrupted_images"] += 1

            if res["is_duplicate"]:
                counts["duplicate_images"] += 1

            if status == "SUCCESS":
                counts["processed_images"] += 1
                cleaned_records.append(res)
            else:
                counts["skipped_images"] += 1
                reason = res["failure_reason"] or status
                failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
                rejected_records.append(res)

        # 1. Save Cleaned Metadata (CSV & JSON)
        cleaned_csv_file = self.processed_dir / "cleaned_metadata.csv"
        cleaned_json_file = self.processed_dir / "cleaned_metadata.json"
        if cleaned_records:
            fieldnames = list(cleaned_records[0].keys())
            with open(cleaned_csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_records)
            save_json(cleaned_records, cleaned_json_file)
            logger.info(f"Saved cleaned metadata for {len(cleaned_records)} valid images to {cleaned_csv_file}")

        # 2. Save Rejected Images Report (JSON & MD)
        rejected_json_file = self.reports_dir / "rejected_images_report.json"
        rejected_md_file = self.reports_dir / "rejected_images_report.md"
        rejected_report = {
            "total_rejected": len(rejected_records),
            "rejection_summary": failure_reasons,
            "rejected_records": rejected_records
        }
        save_json(rejected_report, rejected_json_file)
        self._write_rejected_markdown(rejected_report, rejected_md_file)
        logger.info(f"Saved rejected images audit report ({len(rejected_records)} entries) to {rejected_json_file}")

        # 3. Save Overall Preprocessing Report (JSON & MD)
        prep_report = {
            "statistics": counts,
            "failure_reasons": failure_reasons,
            "target_resolution": list(self.target_size),
            "cleaned_images_count": len(cleaned_records),
            "rejected_images_count": len(rejected_records),
            "processed_records": all_results
        }
        report_json_file = self.reports_dir / "preprocessing_report.json"
        report_md_file = self.reports_dir / "preprocessing_report.md"
        save_json(prep_report, report_json_file)
        self._write_preprocessing_markdown(prep_report, report_md_file)

        logger.info(
            f"Preprocessing finished: {counts['processed_images']}/{counts['total_discovered']} standardized. "
            f"Duplicates: {counts['duplicate_images']}, Corrupted: {counts['corrupted_images']}, Skipped: {counts['skipped_images']}."
        )
        return prep_report

    def _write_rejected_markdown(self, rejected_report: Dict[str, Any], output_path: Path) -> None:
        """Writes human-readable markdown report of all rejected/skipped images."""
        recs = rejected_report["rejected_records"]
        summary = rejected_report["rejection_summary"]

        summary_rows = "\n".join([f"- **{k}**: `{v} file(s)`" for k, v in summary.items()])
        table_rows = []
        for r in recs:
            table_rows.append(
                f"| `{r['filename']}` | `{r['status']}` | {r['raw_size_kb']} KB | `{r['failure_reason']}` |"
            )
        table_content = "\n".join(table_rows) if table_rows else "| None | None | 0 | None |"

        content = f"""# AgroVision-Mine: Rejected & Skipped Images Audit Report

**Total Flagged / Excluded Records:** `{rejected_report['total_rejected']}`

> **Academic Integrity Rule:** Problematic or duplicate files are never silently deleted.
> Every skipped record is preserved in this audit report with exact technical failure reasons.

---

## 1. Summary by Rejection Category
{summary_rows if summary_rows else "- No records were rejected."}

---

## 2. Itemized Rejection Log
| Filename | Status Flag | File Size | Technical Failure Reason |
| :--- | :--- | :--- | :--- |
{table_content}

---
*Generated by AgroVision-Mine Image Preprocessor (Phase 2).*
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_preprocessing_markdown(self, prep_report: Dict[str, Any], output_path: Path) -> None:
        """Writes comprehensive preprocessing audit markdown."""
        s = prep_report["statistics"]
        reasons = prep_report["failure_reasons"]
        reason_rows = "\n".join([f"- **{k}**: `{v} file(s)`" for k, v in reasons.items()])

        content = f"""# AgroVision-Mine: Preprocessing & Quality Diagnostics Audit Report

---

## 1. Preprocessing Execution Statistics
- **Total Discovered Candidate Files:** `{s['total_discovered']}`
- **Valid Image Files:** `{s['valid_images']}`
- **Invalid / Corrupted Files:** `{s['invalid_images']}`
- **Exact / Perceptual Duplicates:** `{s['duplicate_images']}`
- **Successfully Standardized & Saved:** `{s['processed_images']}`
- **Total Skipped / Excluded:** `{s['skipped_images']}`
- **Configured Target Resolution:** `{prep_report['target_resolution'][0]} x {prep_report['target_resolution'][1]} px`

---

## 2. Rejection & Diagnostic Reasons
{reason_rows if reason_rows else "- None (All images passed quality checks)."}

---

## 3. Preservation of Raw Assets
- Original raw images in `data/raw/` remain strictly read-only and unmodified.
- Standardized $256 \\times 256$ RGB images are written into `data/processed/<crop>/<condition>/`.
- Cleaned metadata records are exported to `data/processed/cleaned_metadata.csv`.
- Detailed rejection diagnostics are recorded in `data/reports/rejected_images_report.md`.
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
