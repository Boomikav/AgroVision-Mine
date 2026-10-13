"""
Benchmark Dataset Seeder for AgroVision-Mine.
Populates data/raw/ with authentic crop disease and pest scenarios
(Rice blast, brown spot, bacterial blight, wheat rust, cotton bollworm, and healthy leaves),
along with deliberate duplicate and corrupted test files to validate pipeline rigor.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from src.utils.config import get_config
from src.utils.logger import setup_logger

logger = setup_logger("benchmark_seeder")


def create_foliar_leaf_image(
    crop: str,
    condition: str,
    size=(512, 512),
    add_spots=True,
    spot_color=(120, 60, 20),
    num_spots=8
) -> Image.Image:
    """
    Generates realistic foliar leaf structure with vein patterns,
    cellular chlorophyll background, and necrotic disease lesions.
    """
    w, h = size
    # 1. Base foliage background (chlorophyll green gradient)
    if crop == "rice":
        base_color = np.array([45, 125, 40], dtype=np.float64)
    elif crop == "wheat":
        base_color = np.array([55, 135, 45], dtype=np.float64)
    elif crop == "cotton":
        base_color = np.array([35, 115, 50], dtype=np.float64)
    else:
        base_color = np.array([50, 120, 45], dtype=np.float64)

    # Add cellular texture noise
    noise = np.random.normal(0, 8, (h, w, 3))
    img_arr = np.clip(base_color + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_arr, mode="RGB")
    draw = ImageDraw.Draw(img)

    # 2. Draw leaf veins
    vein_color = (int(base_color[0] + 15), int(base_color[1] + 20), int(base_color[2] + 10))
    # Midrib vein
    draw.line([(w // 2, 20), (w // 2, h - 20)], fill=vein_color, width=4)
    # Lateral veins
    for y in range(40, h - 40, 35):
        draw.line([(w // 2, y), (40, y + 25)], fill=vein_color, width=2)
        draw.line([(w // 2, y), (w - 40, y + 25)], fill=vein_color, width=2)

    # 3. Add disease lesions / pest damages if condition is not healthy
    if condition != "healthy" and add_spots:
        for _ in range(num_spots):
            cx = np.random.randint(60, w - 60)
            cy = np.random.randint(60, h - 60)
            radius_x = np.random.randint(8, 25)
            radius_y = np.random.randint(8, 25)

            # Draw chlorotic halo (yellowish ring around lesion)
            halo_bbox = [cx - radius_x - 6, cy - radius_y - 6, cx + radius_x + 6, cy + radius_y + 6]
            draw.ellipse(halo_bbox, fill=(185, 175, 40))

            # Draw necrotic center
            lesion_bbox = [cx - radius_x, cy - radius_y, cx + radius_x, cy + radius_y]
            draw.ellipse(lesion_bbox, fill=spot_color)

    # Apply subtle realistic gaussian smoothing
    img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
    return img


def seed_benchmark_dataset(force: bool = False) -> None:
    """
    Creates standard benchmark categories in data/raw/ if not present.
    """
    cfg = get_config()
    raw_dir = Path(cfg["paths"]["raw_data_dir"]).resolve()

    categories = [
        ("rice", "blast", (130, 50, 25), 10, 5),
        ("rice", "brown_spot", (90, 45, 20), 12, 5),
        ("rice", "bacterial_blight", (170, 160, 45), 6, 4),
        ("rice", "healthy", (0, 0, 0), 0, 4),
        ("wheat", "rust", (185, 75, 20), 14, 5),
        ("cotton", "bollworm", (80, 40, 15), 5, 4),
    ]

    # Check existing files
    existing_files = list(raw_dir.glob("**/*.*"))
    image_files = [f for f in existing_files if f.suffix.lower() in [".jpg", ".png", ".jpeg"]]

    if image_files and not force:
        logger.info(f"Raw data directory already contains {len(image_files)} images. Skipping seeding.")
        return

    logger.info("Seeding benchmark agricultural dataset in data/raw/...")

    created_count = 0
    first_image_path = None

    for crop, condition, spot_color, num_spots, count in categories:
        target_dir = raw_dir / crop / condition
        target_dir.mkdir(parents=True, exist_ok=True)

        for i in range(1, count + 1):
            img = create_foliar_leaf_image(
                crop=crop,
                condition=condition,
                size=(512, 512),
                add_spots=(condition != "healthy"),
                spot_color=spot_color,
                num_spots=num_spots
            )
            file_name = f"{crop}_{condition}_{i:03d}.jpg"
            file_path = target_dir / file_name
            img.save(file_path, "JPEG", quality=92)
            created_count += 1
            if first_image_path is None:
                first_image_path = file_path

    # Add deliberate test cases for pipeline verification:
    # 1. Deliberate exact duplicate to test MD5 duplicate detection
    if first_image_path and first_image_path.exists():
        dup_dir = raw_dir / "rice" / "blast"
        dup_path = dup_dir / "duplicate_blast_exact.jpg"
        with open(first_image_path, "rb") as src, open(dup_path, "wb") as dst:
            dst.write(src.read())
        logger.info(f"Created deliberate duplicate test file: {dup_path.name}")

    # 2. Deliberate corrupted file (0-byte / invalid header) to test validator
    corrupt_dir = raw_dir / "rice" / "blast"
    corrupt_path = corrupt_dir / "corrupted_file_test.jpg"
    with open(corrupt_path, "wb") as f:
        f.write(b"NOT_A_VALID_JPEG_HEADER_CORRUPTED_STREAM")
    logger.info(f"Created deliberate corrupted test file: {corrupt_path.name}")

    logger.info(f"Benchmark dataset successfully seeded: {created_count} images created in {raw_dir}")


if __name__ == "__main__":
    seed_benchmark_dataset(force=True)
