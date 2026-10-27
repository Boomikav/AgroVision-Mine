# AgroVision-Mine — Unresolved Limitations and Pre-Submission Checklist

This document details all known scientific limitations, epistemological boundaries, and pre-submission checks for the revised manuscript:

**"AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence"**

---

## 1. Methodological and Experimental Limitations

### 1. Closed-World Taxonomic Scope
- **Current Scope:** The fine-tuned EfficientNet-B0 model is bounded strictly to 25 composite crop-condition classes across 12 host crops.
- **Limitation:** The classifier operates under a closed-world assumption ($\sum_{k=1}^{25} p_k = 1.0$). If an image of an unsupported crop species (e.g., Wheat, Cotton, Sugarcane) or an unmodeled exotic pathogen is presented, the model's softmax layer will force attribution into one of the 25 classes.
- **Transparent Manuscript Framing:** Explicitly identified in Section VII as Threat #1 to validity.

### 2. Dataset Confounding in Web-Scraped Field Imagery (PlantDoc)
- **Current Observation:** In the raw PlantDoc corpus, 7 of 14 crops (Bell Pepper, Blueberry, Peach, Raspberry, Soybean, Squash, Strawberry) contain exclusively healthy or exclusively diseased observations.
- **Limitation:** An unconditioned binary classifier (Healthy vs. Diseased) trained across heterogeneous crops is fundamentally confounded, learning to distinguish crop species rather than pathological lesions.
- **Mitigation:** AgroVision-Mine models 25 composite `Crop___Condition` classes rather than an unconditioned binary label, explicitly discouraging the network from using crop identity as a spurious diagnostic shortcut.

### 3. Field vs. Flatbed Scanner Domain Shift
- **Current Observation:** The 36 ICAR rice leaf observations were acquired using flatbed optical scanners with pure white backgrounds, whereas PlantDoc images were captured under varied natural in-field lighting.
- **Limitation:** The PCA ordination demonstrates that flatbed scanner imagery shifts PC1 (foliar luminance) markedly into an isolated cluster. Laboratory or scanner-trained models cannot generalize directly to natural farm environments without explicit domain adaptation.
- **Transparent Manuscript Framing:** Documented in Section VI-E and Section VII as Threat #3.

### 4. Exploratory Nature of Nearest-Neighbor Domain Screening
- **Current Audit Finding:** When tested across all 36 ICAR rice scanner images:
  - Standalone CNN inference falsely accepts 35 of 36 images (97.2%) as confident predictions (mean confidence 58.9%, max 64.06%), misdiagnosing them into Corn leaf diseases.
  - The multimodal pipeline intercepts all 36 images (100.0%) as `unsupported_domain` because the warehouse contains ICAR/OGD rice reference anchors.
- **Limitation:** If a completely novel crop or sensor modality is introduced with *no reference anchors* in the warehouse, the nearest-neighbor lookup may match an arbitrary supported reference, leading to failure of the screening mechanism and subsequent CNN misclassification.
- **Transparent Manuscript Framing:** Removed all claims of "guaranteed rejection" or "prevention of false clinical attributions." Reframed as an exploratory nearest-neighbor domain screener; identified formal out-of-distribution methods (energy-based OOD, temperature scaling, Mahalanobis distance) as necessary future work.

### 5. Non-Diagnostic Nature of Geometric Feature Proximity
- **Limitation:** Nearest-reference Euclidean proximity in the 32D handcrafted feature space reflects geometric, chromatic, and textural similarity—not certified microbiological or PCR-confirmed pathogen etiology.
- **Transparent Manuscript Framing:** Explicitly stated in Section VII. Softmax output probabilities reflect relative network activations within a closed label space, not calibrated epidemiological likelihoods.

---

## 2. Pre-Submission Author Checklist

Before final conference camera-ready submission, authors should verify:
- [x] All dataset accounting counts sum consistently: $2,447 \text{ benchmark} + 113 \text{ excluded} + 36 \text{ scanner OOD} = 2,596 \text{ total}$.
- [x] Excluded classes correctly reported as exactly 3 classes with $N < 60$.
- [x] Duplicate leakage prevention claims qualified as zero perceptual hash group overlap under 64-bit dHash ($D_H \le 10$).
- [x] Model tournament on validation set ($N=489$) kept separate from held-out test evaluation ($N=490$).
- [x] Standalone CNN closed-set failure on rice scanner images documented transparently alongside hybrid screening behavior.
- [x] Abstract condensed into a single concise paragraph (~190 words).
- [x] System architecture figure generated from clean, editable Mermaid source (`fig1_system_architecture.mmd`) and rendered at 300+ DPI.
- [x] Star schema figure accurately reflects deployed SQLite database schema and foreign keys.
- [x] All 22 bibliography citations verified with exact DOIs and 1-to-1 matching across `.bib`, `.tex`, `.docx`, and `.pdf`.
- [x] PDF compiled to exactly 7 balanced IEEE two-column pages without text overflow, clipped labels, or fake headers.
- [x] Test suite passing 117/117 automated tests (107 pytest unit/integration + 10 Playwright browser tests).
