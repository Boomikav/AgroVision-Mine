"""
Color Feature Extraction Module for AgroVision-Mine.
Computes RGB and HSV first-order and second-order color statistics.
"""
from typing import Any, Dict
import numpy as np
from PIL import Image

def rgb_to_hsv_numpy(rgb_arr: np.ndarray) -> np.ndarray:
    """
    Vectorized RGB to HSV conversion for numpy array in range [0, 255].
    Returns HSV array with H in [0, 360), S in [0, 1], V in [0, 1].
    """
    arr = rgb_arr.astype(np.float64) / 255.0
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin

    # Hue calculation
    h = np.zeros_like(cmax)
    mask_delta = delta > 1e-6

    # When cmax == r
    mask_r = mask_delta & (cmax == r)
    h[mask_r] = 60.0 * (((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6.0)

    # When cmax == g
    mask_g = mask_delta & (cmax == g)
    h[mask_g] = 60.0 * (((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2.0)

    # When cmax == b
    mask_b = mask_delta & (cmax == b)
    h[mask_b] = 60.0 * (((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4.0)

    # Saturation calculation
    s = np.zeros_like(cmax)
    mask_cmax = cmax > 1e-6
    s[mask_cmax] = delta[mask_cmax] / cmax[mask_cmax]

    # Value calculation
    v = cmax

    return np.stack([h, s, v], axis=-1)

def extract_color_features(img_pil: Image.Image) -> Dict[str, float]:
    """
    Extracts RGB and HSV color statistics (mean, std, dominant tone).
    """
    img_rgb = img_pil.convert("RGB")
    arr = np.asarray(img_rgb, dtype=np.float64)

    r = arr[..., 0]
    g = arr[..., 1]
    b = arr[..., 2]

    # RGB moments
    r_mean = float(np.mean(r))
    g_mean = float(np.mean(g))
    b_mean = float(np.mean(b))
    r_std = float(np.std(r))
    g_std = float(np.std(g))
    b_std = float(np.std(b))

    # HSV moments
    hsv_arr = rgb_to_hsv_numpy(arr)
    h = hsv_arr[..., 0]
    s = hsv_arr[..., 1]
    v = hsv_arr[..., 2]

    h_mean = float(np.mean(h))
    s_mean = float(np.mean(s))
    v_mean = float(np.mean(v))
    h_std = float(np.std(h))
    s_std = float(np.std(s))
    v_std = float(np.std(v))

    # Excess Green Index (2G - R - B) commonly used in agronomic imagery
    exg = 2.0 * g - r - b
    exg_mean = float(np.mean(exg))

    # Dominant tone classification based on HSV mean
    if v_mean < 0.2:
        dominant_tone = "Dark_Necrotic"
    elif s_mean < 0.15:
        dominant_tone = "Pale_Chlorotic"
    elif 35.0 <= h_mean <= 85.0:
        dominant_tone = "Yellowish_Lesion"
    elif 85.0 < h_mean <= 160.0:
        dominant_tone = "Foliar_Green"
    elif 10.0 <= h_mean < 35.0:
        dominant_tone = "Brown_Blight"
    else:
        dominant_tone = "Reddish_Rust"

    return {
        "rgb_r_mean": round(r_mean, 3),
        "rgb_g_mean": round(g_mean, 3),
        "rgb_b_mean": round(b_mean, 3),
        "rgb_r_std": round(r_std, 3),
        "rgb_g_std": round(g_std, 3),
        "rgb_b_std": round(b_std, 3),
        "rgb_r_norm": round(r_mean / 255.0, 4),
        "rgb_g_norm": round(g_mean / 255.0, 4),
        "rgb_b_norm": round(b_mean / 255.0, 4),
        "hsv_h_mean": round(h_mean, 3),
        "hsv_s_mean": round(s_mean, 3),
        "hsv_v_mean": round(v_mean, 3),
        "hsv_h_std": round(h_std, 3),
        "hsv_s_std": round(s_std, 3),
        "hsv_v_std": round(v_std, 3),
        "hsv_h_norm": round(h_mean / 360.0, 4),
        "hsv_s_norm": round(s_mean, 4),
        "hsv_v_norm": round(v_mean, 4),
        "exg_index_mean": round(exg_mean, 3),
        "dominant_color_tone": dominant_tone
    }
