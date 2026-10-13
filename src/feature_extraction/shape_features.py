"""
Shape and Contour Feature Extraction Module for AgroVision-Mine.
Extracts geometric and morphometric descriptors when distinct lesions/objects exist,
with fallback for uniform foliage.
"""
from typing import Any, Dict
import numpy as np
from PIL import Image

def otsu_threshold(gray_arr: np.ndarray) -> int:
    """
    Computes optimal global threshold using Otsu's method.
    """
    hist, _ = np.histogram(gray_arr, bins=256, range=(0, 256))
    total = gray_arr.size
    current_max, threshold = 0.0, 128
    sum_total = np.dot(np.arange(256), hist)

    weight_background, sum_background = 0.0, 0.0
    for t in range(256):
        weight_background += hist[t]
        if weight_background == 0:
            continue
        weight_foreground = total - weight_background
        if weight_foreground == 0:
            break

        sum_background += t * hist[t]
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground

        between_class_variance = (
            weight_background * weight_foreground * ((mean_background - mean_foreground) ** 2)
        )

        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = t

    return threshold

def extract_shape_features(img_pil: Image.Image, min_contour_area: float = 50.0) -> Dict[str, Any]:
    """
    Extracts morphometric descriptors: area, perimeter, circularity, aspect ratio, solidity.
    Falls back gracefully when no distinct contour is detected.
    """
    gray = img_pil.convert("L")
    gray_arr = np.asarray(gray, dtype=np.uint8)

    # Otsu thresholding for binary mask
    thresh = otsu_threshold(gray_arr)
    # Detect darker lesion spots or brighter areas (smaller mode)
    binary = gray_arr <= thresh
    if np.sum(binary) > (gray_arr.size // 2):
        binary = ~binary

    # Basic connected components analysis or foreground pixel density
    foreground_pixels = int(np.sum(binary))
    total_pixels = int(gray_arr.size)
    area_fraction = foreground_pixels / max(total_pixels, 1)

    if foreground_pixels < min_contour_area or area_fraction > 0.95:
        # Uniform or no distinct contour
        return {
            "has_valid_contour": False,
            "contour_area": 0.0,
            "contour_perimeter": 0.0,
            "contour_aspect_ratio": 1.0,
            "contour_circularity": 0.0,
            "contour_solidity": 0.0,
            "lesion_coverage_ratio": round(area_fraction, 4)
        }

    # Approximate bounding box and shape metrics from coordinate moments
    y_coords, x_coords = np.nonzero(binary)
    min_x, max_x = int(np.min(x_coords)), int(np.max(x_coords))
    min_y, max_y = int(np.min(y_coords)), int(np.max(y_coords))

    bb_width = max(max_x - min_x + 1, 1)
    bb_height = max(max_y - min_y + 1, 1)
    aspect_ratio = round(bb_width / bb_height, 4)

    # Boundary perimeter approximation: pixels on the edge of the binary mask
    eroded = (
        binary[1:-1, 1:-1] &
        binary[:-2, 1:-1] &
        binary[2:, 1:-1] &
        binary[1:-1, :-2] &
        binary[1:-1, 2:]
    )
    perimeter = int(np.sum(binary[1:-1, 1:-1]) - np.sum(eroded))
    perimeter = max(perimeter, 1)

    area = float(foreground_pixels)
    # Circularity = 4 * pi * Area / (Perimeter^2)
    circularity = round(min(4.0 * np.pi * area / (perimeter ** 2), 1.0), 4)

    # Solidity = Area / Bounding Box Area
    bb_area = float(bb_width * bb_height)
    solidity = round(min(area / max(bb_area, 1.0), 1.0), 4)

    return {
        "has_valid_contour": True,
        "contour_area": round(area, 2),
        "contour_perimeter": round(float(perimeter), 2),
        "contour_aspect_ratio": aspect_ratio,
        "contour_circularity": circularity,
        "contour_solidity": solidity,
        "lesion_coverage_ratio": round(area_fraction, 4)
    }
