from pathlib import Path
import pytest
from PIL import Image
from src.preprocessing.duplicate_detector import DuplicateDetector

@pytest.fixture
def detector():
    return DuplicateDetector(hamming_threshold=5)

def test_exact_duplicate_detection(detector, tmp_path):
    # Base image
    img_path1 = tmp_path / "img1.png"
    img = Image.new("RGB", (100, 100), color=(100, 200, 100))
    img.save(img_path1)

    # Identical copy
    img_path2 = tmp_path / "img2.png"
    img.save(img_path2)

    res1 = detector.check_and_register(img_path1)
    assert res1.is_duplicate is False

    res2 = detector.check_and_register(img_path2)
    assert res2.is_duplicate is True
    assert res2.duplicate_type == "EXACT_HASH"

def test_perceptual_near_duplicate(detector, tmp_path):
    img_path1 = tmp_path / "orig.jpg"
    img = Image.new("RGB", (128, 128), color=(120, 180, 120))
    img.save(img_path1, "JPEG", quality=95)

    # Slightly re-compressed / minimal noise version
    img_path2 = tmp_path / "recompressed.jpg"
    img.save(img_path2, "JPEG", quality=80)

    detector.check_and_register(img_path1)
    res = detector.check_and_register(img_path2)
    assert res.is_duplicate is True
    assert res.duplicate_type in ("EXACT_HASH", "PERCEPTUAL_NEAR")

def test_distinct_images_not_duplicate(detector, tmp_path):
    img_path1 = tmp_path / "white.jpg"
    img_path2 = tmp_path / "black.jpg"
    Image.new("RGB", (64, 64), color=(255, 255, 255)).save(img_path1)
    Image.new("RGB", (64, 64), color=(0, 0, 0)).save(img_path2)

    res1 = detector.check_and_register(img_path1)
    res2 = detector.check_and_register(img_path2)

    assert res1.is_duplicate is False
    assert res2.is_duplicate is False
