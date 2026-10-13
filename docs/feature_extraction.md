# Visual Feature Extraction Specification & Feature Dictionary

## 1. Classical Feature Extraction Rationale

In agricultural diagnostics and crop health intelligence, deep learning embeddings often operate as opaque "black-boxes." For academic defensibility and agronomist explainability, **AgroVision-Mine (Review 1)** establishes a baseline feature extraction pipeline grounded in classical computer vision:
1. **First & Second-Order Color Moments:** Quantifies chlorosis (yellowing), necrosis (browning/blackening), and healthy chlorophyll retention.
2. **Gray-Level Co-occurrence Matrix (GLCM):** Quantifies tissue surface roughness, lesion boundary gradients, and spatial textural disorganization.
3. **Morphometric Contour Descriptors:** Captures geometric lesion margins, pustule circularity, and foliar surface coverage ratios.
4. **Data Lineage:** Every feature vector maintains foreign key traceability back to `image_id`, `filename`, and cryptographic `md5_hash`.

---

## 2. Mathematical Formulations

### A. Color Descriptors (RGB & HSV Perceptual Spaces)
For an $M \times N$ image array across color channels $c \in \{R, G, B\}$:

$$\mu_c = \frac{1}{MN} \sum_{x=1}^{M} \sum_{y=1}^{N} I_c(x, y), \quad \sigma_c = \sqrt{\frac{1}{MN} \sum_{x=1}^{M} \sum_{y=1}^{N} (I_c(x, y) - \mu_c)^2}$$

- **Normalized Intensities:** $I_{c,\text{norm}} = \frac{\mu_c}{255.0} \in [0, 1]$
- **Excess Green Index (ExG):** A classic agronomic vegetation index highlighting chlorophyll absorption:
  $$\text{ExG} = 2 \cdot \mu_G - \mu_R - \mu_B$$
- **HSV Conversion:** Decouples chromaticity (Hue $H \in [0^\circ, 360^\circ)$), color purity (Saturation $S \in [0, 1]$), and luminance (Value $V \in [0, 1]$).
- **Dominant Color Tone:** Categorical classification based on Hue-Saturation-Value clusters (e.g. `Foliar_Green`, `Brown_Blight`, `Yellowish_Lesion`, `Dark_Necrotic`).

---

### B. Haralick Texture Descriptors (GLCM)
A symmetric, normalized Gray-Level Co-occurrence Matrix $P(i, j)$ is computed over quantized gray levels $N_g = 16$:

1. **Contrast:** Measures local intensity variations between pixel pairs:
   $$\text{Contrast} = \sum_{i=0}^{N_g-1} \sum_{j=0}^{N_g-1} |i - j|^2 P(i, j)$$
2. **Normalized Contrast:** Scaled by maximum pair distance $(N_g - 1)^2$:
   $$\text{Contrast}_{\text{norm}} = \frac{\text{Contrast}}{(N_g - 1)^2} \in [0, 1]$$
3. **Dissimilarity:** Linear measure of adjacent pixel differences:
   $$\text{Dissimilarity} = \sum_{i=0}^{N_g-1} \sum_{j=0}^{N_g-1} |i - j| P(i, j)$$
4. **Homogeneity:** Measures closeness of element distribution to the diagonal:
   $$\text{Homogeneity} = \sum_{i=0}^{N_g-1} \sum_{j=0}^{N_g-1} \frac{P(i, j)}{1 + |i - j|^2}$$
5. **Energy (Angular Second Moment):** Measures uniformity of textural pattern:
   $$\text{Energy} = \sum_{i=0}^{N_g-1} \sum_{j=0}^{N_g-1} P(i, j)^2$$
6. **Correlation:** Measures linear dependency of neighbor gray levels:
   $$\text{Correlation} = \sum_{i=0}^{N_g-1} \sum_{j=0}^{N_g-1} \frac{(i - \mu_i)(j - \mu_j) P(i, j)}{\sigma_i \sigma_j}$$

---

### C. Morphometric Shape Descriptors
Images are segmented using Otsu's optimal bimodal thresholding to isolate pathological lesions:
- **Contour Area ($A$):** Number of pixels in the primary lesion mask.
- **Contour Perimeter ($P$):** Boundary edge pixels of the lesion envelope.
- **Aspect Ratio ($AR$):** $\frac{\text{Width}}{\text{Height}}$ of the bounding box.
- **Circularity:** Isoperimetric quotient assessing circular lesion symmetry:
  $$\text{Circularity} = \min\left(1.0, \frac{4 \pi A}{P^2}\right) \in [0, 1]$$
- **Solidity:** Ratio of lesion area to bounding envelope area:
  $$\text{Solidity} = \min\left(1.0, \frac{A}{\text{BoundingBox Area}}\right) \in [0, 1]$$
- **Lesion Coverage Ratio:** Fraction of total foliar area occupied by lesion pixels:
  $$\text{Coverage Ratio} = \frac{A}{M \times N} \in [0, 1]$$

---

## 3. Extensible Deep Representation Interface

The pipeline provides the abstract class `BaseFeatureExtractor` in [`src/feature_extraction/pipeline.py`](file:///c:/Users/ajaya/Desktop/Agro/src/feature_extraction/pipeline.py):
```python
class BaseFeatureExtractor(ABC):
    @abstractmethod
    def extract(self, img_pil: Image.Image) -> Dict[str, Any]:
        pass
```
This enables drop-in integration of deep embeddings (e.g., 512-d ResNet or ViT latent vectors) for **Review 2** without redesigning the feature pipeline or the data warehouse star schema.
