"""
Dataset Inspection Script for AgroVision-Mine (Phase 1).
Executes deep dataset discovery, structure detection, and schema ground-truth analysis.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingestion.profiler import DatasetProfiler
from src.utils.logger import setup_logger

logger = setup_logger("inspect_dataset")


def main():
    logger.info("Executing Phase 1 Dataset Inspection & Profiling...")
    profiler = DatasetProfiler()
    report = profiler.run_profiling()

    print("\n" + "=" * 80)
    print("AGROVISION-MINE: DATASET PROFILING & GROUND-TRUTH REPORT")
    print("=" * 80)
    print(f"Target Directory         : {report['source_directory']}")
    print(f"Dataset Present          : {'YES' if report['dataset_present'] else 'NO (Awaiting Official ICAR Placement)'}")
    print(f"Total Files Found        : {report['file_counts']['total_files']}")
    print(f"Image Files Found        : {report['file_counts']['image_files']}")
    print(f"Annotation Manifests     : {report['file_counts']['annotation_files']}")
    print(f"Metadata Files           : {report['file_counts']['metadata_files']}")
    print("-" * 80)
    print("DETECTED SEMANTIC FIELDS:")
    print(f"  - Crop Fields          : {report['detected_fields']['crop_fields']}")
    print(f"  - Disease Fields       : {report['detected_fields']['disease_fields']}")
    print(f"  - Pest Fields          : {report['detected_fields']['pest_fields']}")
    print(f"  - Date / Temporal      : {report['detected_fields']['date_fields']}")
    print(f"  - Geography / Spatial  : {report['detected_fields']['geography_fields']}")
    print("-" * 80)
    print("ACADEMIC SCHEMA IMPLICATIONS (NO-FABRICATION RULE):")
    for rec in report["schema_implications"]["recommendations"]:
        print(f"  * {rec}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
