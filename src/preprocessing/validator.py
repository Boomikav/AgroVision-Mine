"""
Image Validation and Quality Diagnostics Module for AgroVision-Mine.
Detects corrupted, unreadable, truncated, or invalid images.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image, ImageStat

from src.utils.config import get_config
from src.utils.logger import setup_logger

logger = setup_logger("validator")


@dataclass
class ValidationResult:
    is_valid: bool
    status: str  # "VALID", "CORRUPTED", "INVALID_DIMENSIONS", "UNSUPPORTED_FORMAT", "UNREADABLE"
    failure_reason: Optional[str]
    width: int
    height: int
    channels: int
    file_size_kb: float
    blur_score: float
    is_blurry: bool
    aspect_ratio: float


class ImageValidator:
    """
    Validates agricultural images against file integrity, dimensionality,
    color channel specifications, and image-quality thresholds.
    """

    def __init__(self):
        cfg = get_config()
        prep_cfg = cfg.get("preprocessing", {})
        self.allowed_extensions = set(
            ext.lower() for ext in prep_cfg.get(
                "allowed_extensions", [".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"]
            )
        )
        self.min_dim = prep_cfg.get("min_dimension", 32)
        self.max_dim = prep_cfg.get("max_dimension", 8192)
        self.blur_threshold = prep_cfg.get("blur_laplacian_threshold", 100.0)

    def compute_blur_score(self, img_pil: Image.Image) -> float:
        """
        Computes sharpness/blur score using variance of the Laplacian filter.
        Pure PIL/NumPy implementation for maximum portability.
        Higher variance indicates sharper edges; lower variance indicates blur.
        """
        try:
            gray = img_pil.convert("L")
            img_arr = np.asarray(gray, dtype=np.float64)

            # Discrete Laplacian kernel 3x3: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
            # Vectorized slice convolution (fast & no external dependencies)
            if img_arr.shape[0] < 3 or img_arr.shape[1] < 3:
                return 0.0

            laplacian = (
                img_arr[:-2, 1:-1] +
                img_arr[2:, 1:-1] +
                img_arr[1:-1, :-2] +
                img_arr[1:-1, 2:] -
                4.0 * img_arr[1:-1, 1:-1]
            )
            return float(np.var(laplacian))
        except Exception as e:
            logger.debug(f"Blur calculation exception: {e}")
            return 0.0

    def validate(self, file_path: Union[str, Path]) -> ValidationResult:
        """
        Validates an image file thoroughly without modifying it.
        """
        path = Path(file_path)

        # 1. Existence and size check
        if not path.exists():
            return ValidationResult(
                is_valid=False,
                status="FILE_NOT_FOUND",
                failure_reason=f"File does not exist: {path}",
                width=0, height=0, channels=0,
                file_size_kb=0.0, blur_score=0.0, is_blurry=False, aspect_ratio=0.0
            )

        file_size_kb = round(path.stat().st_size / 1024, 2)
        if file_size_kb <= 0:
            return ValidationResult(
                is_valid=False,
                status="EMPTY_FILE",
                failure_reason="File has 0 bytes",
                width=0, height=0, channels=0,
                file_size_kb=0.0, blur_score=0.0, is_blurry=False, aspect_ratio=0.0
            )

        # 2. Extension check
        if path.suffix.lower() not in self.allowed_extensions:
            return ValidationResult(
                is_valid=False,
                status="UNSUPPORTED_FORMAT",
                failure_reason=f"Extension {path.suffix} is not in allowed extensions {self.allowed_extensions}",
                width=0, height=0, channels=0,
                file_size_kb=file_size_kb, blur_score=0.0, is_blurry=False, aspect_ratio=0.0
            )

        # 3. Image opening and integrity verification
        try:
            with Image.open(path) as img:
                # verify() tests header and block integrity
                img.verify()

            # Re-open after verify to load raster pixels and check dimensions
            with Image.open(path) as img:
                width, height = img.size
                mode = img.mode

                # Channels determination
                channels = len(mode) if mode not in ("1", "L", "P") else 1

                # 4. Dimension constraints
                if width < self.min_dim or height < self.min_dim:
                    return ValidationResult(
                        is_valid=False,
                        status="INVALID_DIMENSIONS",
                        failure_reason=f"Dimensions ({width}x{height}) below minimum {self.min_dim}px",
                        width=width, height=height, channels=channels,
                        file_size_kb=file_size_kb, blur_score=0.0, is_blurry=False,
                        aspect_ratio=round(width / max(height, 1), 4)
                    )

                if width > self.max_dim or height > self.max_dim:
                    return ValidationResult(
                        is_valid=False,
                        status="INVALID_DIMENSIONS",
                        failure_reason=f"Dimensions ({width}x{height}) exceed maximum {self.max_dim}px",
                        width=width, height=height, channels=channels,
                        file_size_kb=file_size_kb, blur_score=0.0, is_blurry=False,
                        aspect_ratio=round(width / max(height, 1), 4)
                    )

                # 5. Blur/Quality analysis
                blur_score = self.compute_blur_score(img)
                is_blurry = blur_score < self.blur_threshold
                aspect_ratio = round(width / max(height, 1), 4)

                return ValidationResult(
                    is_valid=True,
                    status="VALID",
                    failure_reason=None,
                    width=width,
                    height=height,
                    channels=channels,
                    file_size_kb=file_size_kb,
                    blur_score=round(blur_score, 2),
                    is_blurry=is_blurry,
                    aspect_ratio=aspect_ratio
                )

        except (IOError, SyntaxError) as e:
            return ValidationResult(
                is_valid=False,
                status="CORRUPTED",
                failure_reason=f"Corrupted or invalid image data: {str(e)}",
                width=0, height=0, channels=0,
                file_size_kb=file_size_kb, blur_score=0.0, is_blurry=False, aspect_ratio=0.0
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                status="UNREADABLE",
                failure_reason=f"Unexpected reading error: {str(e)}",
                width=0, height=0, channels=0,
                file_size_kb=file_size_kb, blur_score=0.0, is_blurry=False, aspect_ratio=0.0
            )
