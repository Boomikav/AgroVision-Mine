import tempfile
from pathlib import Path
import pytest
from PIL import Image
from src.preprocessing.validator import ImageValidator

@pytest.fixture
def validator():
    return ImageValidator()

@pytest.fixture
def temp_image_dir(tmp_path):
    # Valid RGB image
    valid_path = tmp_path / "valid.jpg"
    img = Image.new("RGB", (256, 256), color=(50, 150, 50))
    img.save(valid_path, "JPEG")

    # Small image (below 32px)
    tiny_path = tmp_path / "tiny.jpg"
    tiny_img = Image.new("RGB", (16, 16), color=(50, 150, 50))
    tiny_img.save(tiny_path, "JPEG")

    # 0-byte file
    empty_path = tmp_path / "empty.jpg"
    empty_path.touch()

    # Corrupted header file
    corrupt_path = tmp_path / "corrupt.jpg"
    corrupt_path.write_bytes(b"NON_IMAGE_DATA_CORRUPT")

    # Unsupported format
    unsupported_path = tmp_path / "unsupported.txt"
    unsupported_path.write_text("plain text")

    return {
        "valid": valid_path,
        "tiny": tiny_path,
        "empty": empty_path,
        "corrupt": corrupt_path,
        "unsupported": unsupported_path
    }

def test_validate_valid_image(validator, temp_image_dir):
    res = validator.validate(temp_image_dir["valid"])
    assert res.is_valid is True
    assert res.status == "VALID"
    assert res.width == 256
    assert res.height == 256
    assert res.channels == 3
    assert res.file_size_kb > 0

def test_validate_empty_file(validator, temp_image_dir):
    res = validator.validate(temp_image_dir["empty"])
    assert res.is_valid is False
    assert res.status == "EMPTY_FILE"

def test_validate_corrupted_file(validator, temp_image_dir):
    res = validator.validate(temp_image_dir["corrupt"])
    assert res.is_valid is False
    assert res.status == "CORRUPTED"

def test_validate_invalid_dimensions(validator, temp_image_dir):
    res = validator.validate(temp_image_dir["tiny"])
    assert res.is_valid is False
    assert res.status == "INVALID_DIMENSIONS"

def test_validate_unsupported_format(validator, temp_image_dir):
    res = validator.validate(temp_image_dir["unsupported"])
    assert res.is_valid is False
    assert res.status == "UNSUPPORTED_FORMAT"
