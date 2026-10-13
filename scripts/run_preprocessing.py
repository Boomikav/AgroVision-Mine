"""
Phase 2 Image Preprocessing Execution Script for AgroVision-Mine.
Runs validation, duplicate detection, and standardization on the real dataset.
Generates cleaned metadata, preprocessing audit reports, and rejected images reports.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingestion.dataset_loader import DatasetInspector
from src.preprocessing.preprocessor import ImagePreprocessor
from src.utils.logger import setup_logger

logger = setup_logger("run_preprocessing")


def main():
    logger.info("========== EXECUTING PHASE 2: IMAGE PREPROCESSING PIPELINE ==========")

    # 1. Inspect raw inventory
    inspector = DatasetInspector()
    raw_inventory = inspector.scan_raw_directory()
    logger.info(f"Discovered {len(raw_inventory)} files in data/raw/")

    # 2. Run Preprocessing Pipeline
    preprocessor = ImagePreprocessor()
    report = preprocessor.run_pipeline(raw_inventory)

    stats = report["statistics"]
    reasons = report["failure_reasons"]

    print("\n" + "=" * 80)
    print("AGROVISION-MINE: PHASE 2 PREPROCESSING EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Discovered Candidate Files  : {stats['total_discovered']}")
    print(f"Valid Image Files                 : {stats['valid_images']}")
    print(f"Invalid / Corrupted Files         : {stats['invalid_images']}")
    print(f"Exact & Near Duplicates Flagged   : {stats['duplicate_images']}")
    print(f"Successfully Standardized Images  : {stats['processed_images']}")
    print(f"Total Excluded / Skipped Files    : {stats['skipped_images']}")
    print("-" * 80)
    print("REJECTION & EXCLUSION REASONS (Audited, Not Silently Deleted):")
    if reasons:
        for reason, count in reasons.items():
            print(f"  * {reason}: {count} file(s)")
    else:
        print("  * None (All images passed quality checks)")
    print("-" * 80)
    print("OUTPUT ARTIFACTS GENERATED:")
    print("  1. Processed Normalized Images    : data/processed/<crop>/<condition>/")
    print("  2. Cleaned Metadata CSV           : data/processed/cleaned_metadata.csv")
    print("  3. Cleaned Metadata JSON          : data/processed/cleaned_metadata.json")
    print("  4. Preprocessing Report JSON      : data/reports/preprocessing_report.json")
    print("  5. Preprocessing Report Markdown  : data/reports/preprocessing_report.md")
    print("  6. Rejected Images Report JSON    : data/reports/rejected_images_report.json")
    print("  7. Rejected Images Report Markdown: data/reports/rejected_images_report.md")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
