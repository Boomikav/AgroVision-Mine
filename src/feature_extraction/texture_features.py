"""
Texture Feature Extraction Module (GLCM) for AgroVision-Mine.
Computes Gray-Level Co-occurrence Matrix (GLCM) descriptors:
Contrast, Dissimilarity, Homogeneity, Energy, Correlation, and ASM.
"""
from typing import Dict
import numpy as np
from PIL import Image

def compute_glcm_matrix(gray_arr: np.ndarray, num_levels: int = 16) -> np.ndarray:
    """
    Computes a symmetric, normalized GLCM matrix averaged across horizontal
    and vertical offsets for quantized gray levels.
    """
    # Quantize grayscale image to num_levels (e.g. 0 to 15)
    quantized = np.clip((gray_arr / 256.0 * num_levels).astype(np.int32), 0, num_levels - 1)
    glcm = np.zeros((num_levels, num_levels), dtype=np.float64)

    # Horizontal pairs (dx = 1, dy = 0)
    row_curr, row_right = quantized[:, :-1], quantized[:, 1:]
    np.add.at(glcm, (row_curr, row_right), 1.0)
    np.add.at(glcm, (row_right, row_curr), 1.0)

    # Vertical pairs (dx = 0, dy = 1)
    col_curr, col_down = quantized[:-1, :], quantized[1:, :]
    np.add.at(glcm, (col_curr, col_down), 1.0)
    np.add.at(glcm, (col_down, col_curr), 1.0)

    # Normalize matrix to joint probability distribution
    total = np.sum(glcm)
    if total > 0:
        glcm /= total
    return glcm

def extract_texture_features(img_pil: Image.Image, num_levels: int = 16) -> Dict[str, float]:
    """
    Extracts Haralick texture features from the GLCM:
    Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM.
    """
    gray = img_pil.convert("L")
    gray_arr = np.asarray(gray, dtype=np.float64)

    glcm = compute_glcm_matrix(gray_arr, num_levels=num_levels)

    # Coordinate grids
    i_indices, j_indices = np.indices((num_levels, num_levels))
    diff = np.abs(i_indices - j_indices)

    # Contrast: sum( P(i,j) * |i-j|^2 )
    contrast = float(np.sum(glcm * (diff ** 2)))

    # Dissimilarity: sum( P(i,j) * |i-j| )
    dissimilarity = float(np.sum(glcm * diff))

    # Homogeneity: sum( P(i,j) / (1 + |i-j|^2) )
    homogeneity = float(np.sum(glcm / (1.0 + (diff ** 2))))

    # Energy: sum( P(i,j)^2 )
    energy = float(np.sum(glcm ** 2))
    asm = energy

    # Correlation: sum( (i - mu_i)*(j - mu_j) * P(i,j) ) / (sigma_i * sigma_j)
    marginal_i = np.sum(glcm, axis=1)
    marginal_j = np.sum(glcm, axis=0)
    mu_i = np.sum(np.arange(num_levels) * marginal_i)
    mu_j = np.sum(np.arange(num_levels) * marginal_j)
    sigma_i = np.sqrt(np.sum(((np.arange(num_levels) - mu_i) ** 2) * marginal_i))
    sigma_j = np.sqrt(np.sum(((np.arange(num_levels) - mu_j) ** 2) * marginal_j))

    if sigma_i > 1e-6 and sigma_j > 1e-6:
        correlation = float(np.sum((i_indices - mu_i) * (j_indices - mu_j) * glcm) / (sigma_i * sigma_j))
    else:
        correlation = 1.0

    contrast_norm = round(contrast / max(((num_levels - 1) ** 2), 1), 4)

    return {
        "glcm_contrast": round(contrast, 4),
        "glcm_contrast_norm": contrast_norm,
        "glcm_dissimilarity": round(dissimilarity, 4),
        "glcm_homogeneity": round(homogeneity, 4),
        "glcm_energy": round(energy, 4),
        "glcm_correlation": round(correlation, 4),
        "glcm_asm": round(asm, 4)
    }
