# Image Preprocessing & Quality Diagnostics Specification

## 1. Preprocessing Philosophy

In agricultural pathology research, image alteration must be conducted with extreme caution:
1. **Preservation of Raw Assets:** Original images in `data/raw/` are **strictly read-only** and never altered, overwritten, or compressed in-place.
2. **Standardized Secondary Store:** Normalized images are generated in `data/processed/<crop>/<condition>/` with strict foreign key linkage back to the raw source file.
3. **Rigorous Quality Gate:** Corrupted, truncated, or unreadable files are formally audited and rejected before feature extraction.

---

## 2. Pipeline Stages

```text
Raw Image File (data/raw/)
       ↓
[ Stage 1: File Integrity Validation ]
  - Existence & size (>0 bytes)
  - Magic byte header verification (JPEG, PNG, etc.)
  - Dimension constraints (min: 32px, max: 8192px)
       ↓
[ Stage 2: Quality & Blur Diagnostic ]
  - Discrete Laplacian convolution kernel
  - Sharpness variance: Var(ΔI)
  - Flag if sharpness < threshold (100.0)
       ↓
[ Stage 3: Duplicate Elimination ]
  - MD5 exact hash matching
  - Perceptual difference hash (dHash) 64-bit + 8-bit luminance
  - Hamming distance comparison (threshold ≤ 5 bits)
       ↓
[ Stage 4: Geometric & Color Normalization ]
  - High-fidelity Lanczos resampling to 256 × 256 pixels
  - Color mode standardization to 3-channel RGB
  - Output written to data/processed/
       ↓
[ Stage 5: Audit & Report Generation ]
  - Emitted to data/reports/preprocessing_report.json
```

---

## 3. Mathematical Foundations

### A. Discrete Laplacian Blur Variance
The sharpness score is computed using the variance of the 2D discrete Laplacian operator convolved across the luminance channel:

$$\Delta I(x, y) = I(x+1, y) + I(x-1, y) + I(x, y+1) + I(x, y-1) - 4 I(x, y)$$

$$\text{Blur Score} = \sigma^2(\Delta I) = \frac{1}{N} \sum_{x,y} \left( \Delta I(x, y) - \mu_{\Delta I} \right)^2$$

Images where $\sigma^2(\Delta I) < 100.0$ are flagged as blurry in the warehouse dimension table (`is_blurry = TRUE`), allowing downstream OLAP queries to filter or study the effect of optical degradation on feature extraction.

### B. Perceptual Difference Hashing (dHash)
To detect re-compressed, re-encoded, or slightly resized copies of identical leaves:
1. The image is converted to grayscale and resampled to $(8 + 1) \times 8 = 9 \times 8$ pixels.
2. Adjacent horizontal pixel gradients are compared:

$$B(x, y) = \begin{cases} 1 & \text{if } I(x, y) > I(x+1, y) \\ 0 & \text{otherwise} \end{cases}$$

3. The resulting 64-bit sequence is combined with the mean luminance byte to form a 72-bit perceptual fingerprint.
4. The Hamming distance (number of bit flips via XOR):

$$\mathcal{D}_H(h_1, h_2) = \text{popcount}(h_1 \oplus h_2)$$

If $\mathcal{D}_H \le 5$, the image is classified as a `PERCEPTUAL_NEAR` duplicate of the canonical original.

---

## 4. Audit Reporting Format

The preprocessing pipeline automatically outputs `data/reports/preprocessing_report.json` containing:
- `total_discovered`: Count of all candidate image files found on disk.
- `valid_images`: Images meeting format, header, and dimension constraints.
- `invalid_images`: Files failing validation (with explicit failure reasons).
- `duplicate_images`: Files identified as exact or near-duplicates.
- `processed_images`: Successfully standardized and saved into `data/processed/`.
- `skipped_images`: Total excluded from downstream warehouse loading.
