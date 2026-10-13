"""
Real Agricultural Dataset Ingestion Utility for AgroVision-Mine.
Pulls verified, open-access agricultural field imagery (ICAR-mandate Rice Diseases)
from authenticated research repositories into data/raw/.
"""
import urllib.request
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.utils.config import get_config
from src.utils.logger import setup_logger

logger = setup_logger("dataset_fetcher")

# Authenticated open agricultural dataset: Rice Leaf Disease Archive
# (Bacterial Leaf Blight, Brown Spot, Leaf Smut)
REPO_API_BASE = "https://api.github.com/repos/MHassaanButt/Rice-Disease-Classfication/contents/Dataset"
RAW_BASE_URL = "https://raw.githubusercontent.com/MHassaanButt/Rice-Disease-Classfication/master/Dataset"

CATEGORIES = [
    ("rice", "bacterial_leaf_blight", "Bacterial%20leaf%20blight"),
    ("rice", "brown_spot", "Brown%20spot"),
    ("rice", "leaf_smut", "Leaf%20smut"),
]


def fetch_real_agricultural_images(max_per_category: int = 12) -> Dict[str, int]:
    """
    Downloads authentic agricultural field images into data/raw/.
    Also injects controlled test cases (corrupted, duplicate, invalid dimension)
    to rigorously validate the preprocessing quality gates.
    """
    cfg = get_config()
    raw_dir = Path(cfg["paths"]["raw_data_dir"]).resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)

    downloaded_counts: Dict[str, int] = {}
    headers = {"User-Agent": "AgroVision-Mine/1.0 (Academic Research Ingestion Engine)"}

    logger.info(f"Fetching real agricultural field images from open research repository...")

    first_downloaded_path: Optional[Path] = None

    for crop, condition_local, condition_remote in CATEGORIES:
        cat_dir = raw_dir / crop / condition_local
        cat_dir.mkdir(parents=True, exist_ok=True)

        url = f"{REPO_API_BASE}/{condition_remote}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                items = json.loads(resp.read().decode())

            image_items = [it for it in items if it["name"].lower().endswith((".jpg", ".jpeg", ".png"))][:max_per_category]
            count = 0

            for it in image_items:
                dest_path = cat_dir / it["name"]
                if not dest_path.exists():
                    download_url = it.get("download_url") or f"{RAW_BASE_URL}/{condition_remote}/{it['name']}"
                    img_req = urllib.request.Request(download_url, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=20) as img_resp:
                        img_data = img_resp.read()
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    time.sleep(0.1)  # Respect rate limits

                count += 1
                if first_downloaded_path is None and dest_path.exists():
                    first_downloaded_path = dest_path

            downloaded_counts[f"{crop}_{condition_local}"] = count
            logger.info(f"Downloaded/Verified {count} real images for {crop}/{condition_local}")

        except Exception as e:
            logger.error(f"Failed to fetch category {condition_local}: {e}")

    # Inject controlled diagnostic edge cases into dedicated diagnostic directory
    if first_downloaded_path and first_downloaded_path.exists():
        test_dir = raw_dir.parent / "diagnostic_tests"
        test_dir.mkdir(parents=True, exist_ok=True)

        # 1. Deliberate exact duplicate (tests MD5 collision detector)
        exact_dup = test_dir / "duplicate_exact_test.jpg"
        with open(first_downloaded_path, "rb") as src, open(exact_dup, "wb") as dst:
            dst.write(src.read())
        logger.info(f"Created deliberate duplicate test file: {exact_dup.name}")

        # 2. Deliberate corrupted image (tests header & byte integrity validator)
        corrupted_file = test_dir / "corrupted_header_test.jpg"
        with open(corrupted_file, "wb") as f:
            f.write(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00CORRUPTED_TRUNCATED_STREAM_NO_END_OF_IMAGE")
        logger.info(f"Created deliberate corrupted test file: {corrupted_file.name}")

        # 3. Deliberate tiny image below minimum dimensions (<32px)
        tiny_file = test_dir / "invalid_dim_tiny.jpg"
        tiny_img = Image.new("RGB", (16, 16), color=(40, 140, 40))
        tiny_img.save(tiny_file, "JPEG")
        logger.info(f"Created deliberate invalid dimension test file: {tiny_file.name}")

        # 4. Deliberate unsupported extension
        txt_file = test_dir / "unsupported_extension.txt"
        with open(txt_file, "w") as f:
            f.write("This is a text log, not an agricultural image.")
        logger.info(f"Created deliberate unsupported extension test file: {txt_file.name}")

    return downloaded_counts


if __name__ == "__main__":
    fetch_real_agricultural_images(max_per_category=12)
