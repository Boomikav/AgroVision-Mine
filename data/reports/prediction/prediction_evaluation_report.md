# AgroVision-Mine — Supervised Model Evaluation and Benchmark Report

**Evaluation Date:** 2026-10-19  
**Status:** Validated on Held-Out Test Set (Zero Leakage, Grouped Stratified Partition)  

---

## 1. Executive Summary & Benchmark Comparison

| Model Architecture | Input Representation | Val Macro-F1 | Val Acc | Test Macro-F1 | Test Balanced Acc | Test Accuracy | 95% Confidence Interval |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Majority Baseline** | Label Prior | 0.6% | 7.8% | 0.6% | 4.0% | 7.8% | N/A |
| **Classical Random Forest** | 32D Features | 17.0% | 17.4% | 19.2% | 19.8% | 19.8% | [16.3%, 23.3%] |
| **Classical RBF-SVM** | 32D Features | 15.1% | 16.4% | 19.0% | 20.1% | 19.8% | [16.3%, 23.3%] |
| **EfficientNet-B0 (Transfer)** | 224x224 RGB | **63.3%** | **63.6%** | **60.8%** | **61.4%** | **61.8%** | **[57.5%, 66.0%]** |

---

## 2. Model Selection Rationale
- **Selection Criterion:** Strict peak **Validation Macro-F1** across 25 supported classes ($N=2,447$).
- **Selected Model:** **`EfficientNet_B0`** achieved superior multi-class discrimination on validation data, exceeding classical baselines by learning spatial lesion geometry and local pathological textures directly from raw pixels rather than global 32-descriptor averages.

---

## 3. Held-Out Test Set Performance Breakdown (N=490)

| Class Label | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `Apple - Apple Scab` | 57.1% | 63.2% | 60.0% | 19 |
| `Apple - Cedar Apple Rust` | 80.0% | 70.6% | 75.0% | 17 |
| `Apple - Healthy` | 70.6% | 66.7% | 68.6% | 18 |
| `Bell Pepper - Bacterial Spot` | 61.5% | 53.3% | 57.1% | 15 |
| `Bell Pepper - Healthy` | 34.8% | 66.7% | 45.7% | 12 |
| `Blueberry - Healthy` | 66.7% | 78.3% | 72.0% | 23 |
| `Corn - Common Rust` | 80.0% | 69.6% | 74.4% | 23 |
| `Corn - Gray Leaf Spot` | 43.5% | 76.9% | 55.6% | 13 |
| `Corn - Northern Leaf Blight` | 79.4% | 71.0% | 75.0% | 38 |
| `Grape - Black Rot` | 83.3% | 38.5% | 52.6% | 13 |
| `Grape - Healthy` | 71.4% | 76.9% | 74.1% | 13 |
| `Peach - Healthy` | 81.0% | 77.3% | 79.1% | 22 |
| `Potato - Early Blight` | 42.9% | 26.1% | 32.4% | 23 |
| `Potato - Late Blight` | 32.3% | 50.0% | 39.2% | 20 |
| `Raspberry - Healthy` | 83.3% | 83.3% | 83.3% | 24 |
| `Soybean - Healthy` | 46.7% | 53.8% | 50.0% | 13 |
| `Squash - Powdery Mildew` | 88.9% | 92.3% | 90.6% | 26 |
| `Strawberry - Healthy` | 93.3% | 70.0% | 80.0% | 20 |
| `Tomato - Bacterial Spot` | 27.8% | 22.7% | 25.0% | 22 |
| `Tomato - Early Blight` | 36.7% | 61.1% | 45.8% | 18 |
| `Tomato - Healthy` | 50.0% | 53.8% | 51.8% | 13 |
| `Tomato - Late Blight` | 66.7% | 63.6% | 65.1% | 22 |
| `Tomato - Leaf Mold` | 66.7% | 33.3% | 44.4% | 18 |
| `Tomato - Septoria Leaf Spot` | 54.2% | 43.3% | 48.1% | 30 |
| `Tomato - Yellow Leaf Curl Virus` | 78.6% | 73.3% | 75.9% | 15 |

---

## 4. Domain Shift & Out-of-Distribution Findings
- **Scanner Images (ICAR/OGD Rice, N=36):** Evaluated against the PlantDoc-trained model. Average maximum softmax probability dropped to **59.3%**, with **4 of 36** specimens flagged with high uncertainty.
- **Scientific Implication:** Laboratory flatbed scanner images possess entirely disparate background distributions, leaf presentations, and lighting. Pooling scanner data with in-the-wild field data into a single headline score would introduce severe cross-domain bias.

---

## 5. Methodological & Diagnostic Limitations
1. **Decision Support, Not Diagnosis:** Model outputs are probabilistic inferences derived from statistical gradient optimization. They must not be treated as a definitive phytopathological diagnosis.
2. **Excluded Rare Classes:** 3 classes (`Tomato Two-Spotted Spider Mite`, `Tomato Mosaic Virus`, `Cherry Healthy`) could not be responsibly included due to $N < 60$.
3. **Background Shortcut Risk:** In-the-wild field photography inherently contains background contextual clues (soil, sky, trellises) that convolutional networks may partially exploit alongside leaf lesion morphology.
