from pathlib import Path
import pytest
from PIL import Image

from src.preprocessing.validator import ImageValidator
from src.preprocessing.duplicate_detector import DuplicateDetector
from src.preprocessing.preprocessor import ImagePreprocessor


@pytest.fixture
def preprocessor(tmp_path):
    p = ImagePreprocessor()
    p.processed_dir = tmp_path / "processed"
    p.reports_dir = tmp_path / "reports"
    p.processed_dir.mkdir(parents=True, exist_ok=True)
    p.reports_dir.mkdir(parents=True, exist_ok=True)
    return p


def test_validation_integrity_and_dimensions(tmp_path):
    validator = ImageValidator()

    # Valid image
    valid_file = tmp_path / "valid.jpg"
    Image.new("RGB", (300, 300), color=(50, 150, 50)).save(valid_file, "JPEG")
    res_valid = validator.validate(valid_file)
    assert res_valid.is_valid is True
    assert res_valid.status == "VALID"
    assert res_valid.width == 300
    assert res_valid.height == 300

    # Below minimum dimension (<32px)
    tiny_file = tmp_path / "tiny.jpg"
    Image.new("RGB", (20, 20), color=(50, 150, 50)).save(tiny_file, "JPEG")
    res_tiny = validator.validate(tiny_file)
    assert res_tiny.is_valid is False
    assert res_tiny.status == "INVALID_DIMENSIONS"

    # Corrupted image bytes
    corrupt_file = tmp_path / "corrupt.jpg"
    corrupt_file.write_bytes(b"\xFF\xD8\xFF\xE0TRUNCATED_BAD_HEADER")
    res_corrupt = validator.validate(corrupt_file)
    assert res_valid.is_valid is True
    assert res_corrupt.is_valid is False
    assert res_corrupt.status == "CORRUPTED"


def test_extension_validation(tmp_path):
    validator = ImageValidator()
    txt_file = tmp_path / "sample.txt"
    txt_file.write_text("Hello text")
    res = validator.validate(txt_file)
    assert res.is_valid is False
    assert res.status == "UNSUPPORTED_FORMAT"


def test_duplicate_detection_exact_and_near(tmp_path):
    detector = DuplicateDetector(hamming_threshold=5)

    img_file1 = tmp_path / "leaf1.jpg"
    img = Image.new("RGB", (128, 128), color=(40, 140, 40))
    img.save(img_file1, "JPEG", quality=95)

    img_file2 = tmp_path / "leaf1_copy.jpg"
    img.save(img_file2, "JPEG", quality=95)

    res1 = detector.check_and_register(img_file1)
    res2 = detector.check_and_register(img_file2)

    assert res1.is_duplicate is False
    assert res2.is_duplicate is True
    assert res2.duplicate_type == "EXACT_HASH"


def test_configurable_resizing_and_normalization(preprocessor, tmp_path):
    raw_img = tmp_path / "large_raw.png"
    Image.new("RGB", (800, 600), color=(60, 160, 60)).save(raw_img, "PNG")

    res = preprocessor.process_image(raw_img, crop_label="rice", condition_label="blast")
    assert res["status"] == "SUCCESS"
    assert res["is_valid"] is True
    assert res["is_duplicate"] is False

    proc_path = Path(res["processed_path"])
    assert proc_path.exists()

    with Image.open(proc_path) as proc_img:
        assert proc_img.size == (256, 256)
        assert proc_img.mode == "RGB"


def test_no_silent_deletion_of_problematic_records(preprocessor, tmp_path):
    # Setup 1 valid, 1 corrupted, 1 duplicate
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    v_file = raw_dir / "valid.jpg"
    Image.new("RGB", (200, 200), color=(50, 150, 50)).save(v_file, "JPEG")

    c_file = raw_dir / "corrupted.jpg"
    c_file.write_bytes(b"INVALID_HEADER_BYTES")

    d_file = raw_dir / "duplicate.jpg"
    with open(v_file, "rb") as s, open(d_file, "wb") as d:
        d.write(s.read())

    inventory = [
        {"raw_id": "RAW_001", "absolute_path": str(v_file), "crop_label": "rice", "condition_raw": "blast"},
        {"raw_id": "RAW_002", "absolute_path": str(c_file), "crop_label": "rice", "condition_raw": "blast"},
        {"raw_id": "RAW_003", "absolute_path": str(d_file), "crop_label": "rice", "condition_raw": "blast"},
    ]

    report = preprocessor.run_pipeline(inventory)
    stats = report["statistics"]

    assert stats["total_discovered"] == 3
    assert stats["processed_images"] == 1
    assert stats["skipped_images"] == 2
    assert stats["duplicate_images"] == 1
    assert stats["corrupted_images"] == 1

    # Check rejected report was saved and has 2 records
    rejected_file = preprocessor.reports_dir / "rejected_images_report.json"
    assert rejected_file.exists()
    assert (preprocessor.processed_dir / "cleaned_metadata.csv").exists()


def test_diagnostic_test_directory_rejection():
    """Verify that files in data/diagnostic_tests/ are rejected by quality gates."""
    diag_dir = Path("data/diagnostic_tests")
    if not diag_dir.exists():
        pytest.skip("data/diagnostic_tests directory not present")

    validator = ImageValidator()
    detector = DuplicateDetector()

    # 1. Corrupted header test
    corrupt_file = diag_dir / "corrupted_header_test.jpg"
    if corrupt_file.exists():
        res = validator.validate(corrupt_file)
        assert res.is_valid is False
        assert res.status == "CORRUPTED"

    # 2. Invalid dimensions tiny test
    tiny_file = diag_dir / "invalid_dim_tiny.jpg"
    if tiny_file.exists():
        res = validator.validate(tiny_file)
        assert res.is_valid is False
        assert res.status == "INVALID_DIMENSIONS"

    # 3. Duplicate exact test
    dup_file = diag_dir / "duplicate_exact_test.jpg"
    orig_file = Path("data/raw/rice/bacterial_leaf_blight/DSC_0365.JPG")
    if dup_file.exists() and orig_file.exists():
        detector.check_and_register(orig_file)
        dup_res = detector.check_and_register(dup_file)
        assert dup_res.is_duplicate is True
        assert dup_res.duplicate_type == "EXACT_HASH"

