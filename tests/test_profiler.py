from pathlib import Path
import pytest
from PIL import Image
from src.ingestion.profiler import DatasetProfiler

def test_profiler_empty_directory(tmp_path):
    profiler = DatasetProfiler(raw_dir=str(tmp_path))
    report = profiler.run_profiling()

    assert report["dataset_present"] is False
    assert report["file_counts"]["image_files"] == 0
    assert report["file_counts"]["annotation_files"] == 0

def test_profiler_with_structure_and_manifest(tmp_path):
    # Create sample crop/disease structure in temporary directory
    rice_blast = tmp_path / "rice" / "blast"
    rice_blast.mkdir(parents=True)
    img_path = rice_blast / "sample.jpg"
    Image.new("RGB", (64, 64), color=(30, 120, 30)).save(img_path, "JPEG")

    # Create CSV manifest
    csv_path = tmp_path / "manifest.csv"
    csv_path.write_text("image_id,crop_name,disease_label,state,survey_date\nsample.jpg,Rice,Blast,Punjab,2024-09-15\n")

    profiler = DatasetProfiler(raw_dir=str(tmp_path))
    report = profiler.run_profiling()

    assert report["dataset_present"] is True
    assert report["file_counts"]["image_files"] == 1
    assert report["file_counts"]["annotation_files"] == 1
    assert len(report["detected_fields"]["crop_fields"]) > 0
    assert len(report["detected_fields"]["disease_fields"]) > 0
    assert len(report["detected_fields"]["date_fields"]) > 0
    assert len(report["detected_fields"]["geography_fields"]) > 0
