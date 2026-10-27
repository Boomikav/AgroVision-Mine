# AgroVision-Mine — Revised Research Quality Assurance & Publication Audit Report

**Manuscript Title:** AgroVision-Mine: A Multimodal Data Warehouse and Visual Pattern Mining Framework for Crop Disease and Pest Intelligence  
**Target Venue:** IEEE Conference on Computer Vision / Data Mining / Agricultural Informatics  
**Revision Date:** October 2026  
**Auditor Role:** Rigorous research-paper auditor, computer-vision researcher, scientific editor, IEEE manuscript formatter, and bibliographic verifier.

---

## 1. Executive Deliverables Summary

| Deliverable Artifact | File Path | Format / Size | Status | Verification Notes |
|---|---|---|:---:|---|
| **Revised PDF Manuscript** | [`research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.pdf`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.pdf) | PDF (797 KB, 7 Pages) | **Complete** | Formatted in strict IEEE two-column conference layout via Microsoft Word COM. |
| **Revised Editable Word Manuscript** | [`research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.docx`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.docx) | DOCX (2.8 MB) | **Complete** | IEEE margins, Times New Roman, formatted tables, embedded high-res figures. |
| **Revised LaTeX Manuscript** | [`research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.tex`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/AgroVision_Mine_IEEE_Conference_Paper_Revised.tex) | LaTeX (IEEEtran) | **Complete** | Synchronized text, equations, tables, figures, and bib items. |
| **Canonical BibTeX Database** | [`research_paper/references.bib`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/references.bib) | BibTeX (22 entries) | **Complete** | Exactly 22 verified entries matching citations [1]–[22] with DOIs. |
| **Mermaid Architecture Source** | [`research_paper/figures/fig1_system_architecture.mmd`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/figures/fig1_system_architecture.mmd) | Text / Mermaid | **Complete** | Decoupled 5-layer pipeline and parallel analytical paths. |
| **Vector & High-Res Figure 1** | `research_paper/figures/fig1_system_architecture.svg` & `.png` | SVG (46 KB), PNG (5439x5688 px) | **Complete** | Rendered via Playwright Chrome; crisp 300+ DPI resolution. |
| **Revised Evidence Ledger** | [`research_paper/AgroVision_Mine_Evidence_Ledger_Revised.md`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/AgroVision_Mine_Evidence_Ledger_Revised.md) | Markdown | **Complete** | 23 audited claims with observed results and permitted wording. |
| **Revised Citation Ledger** | [`research_paper/AgroVision_Mine_Citation_Ledger_Revised.md`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/AgroVision_Mine_Citation_Ledger_Revised.md) | Markdown | **Complete** | Authoritative verification of all 22 references. |
| **Unresolved Limitations** | [`research_paper/AgroVision_Mine_Unresolved_Limitations.md`](file:///c:/Users/ajaya/Desktop/Agro/research_paper/AgroVision_Mine_Unresolved_Limitations.md) | Markdown | **Complete** | Transparent catalog of biological and methodological bounds. |

---

## 2. Rigorous Audit Gate Reconciliation

### A. Dataset and Partition Accounting
- **Total Canonical Observations:** Exactly **2,596** images across 14 host crops (PlantDoc in-field: 2,560; ICAR/OGD flatbed scanner rice: 36).
- **Primary Classification Benchmark ($N=2,447$):** Covers 25 composite classes across 12 host crops.
  - Training Partition: 1,468 images ($60.0\%$)
  - Validation Partition: 489 images ($20.0\%$)
  - Held-Out Test Partition: 490 images ($20.0\%$)
- **Resolution of Excluded Classes Contradiction:**
  - The previous text inadvertently stated "six excluded classes with fewer than 15 samples."
  - **Audit Finding:** The running code in `scripts/audit_and_prepare_splits.py` defines `MIN_CLASS_SUPPORT_THRESHOLD = 60`.
  - **Verified Excluded Classes:** Exactly **3 classes** in PlantDoc had fewer than 60 observations:
    1. `Tomato___Two-Spotted Spider Mite`: 2 observations
    2. `Tomato___Mosaic Virus`: 54 observations
    3. `Cherry___Healthy`: 57 observations
  - **Total Excluded Images:** $2 + 54 + 57 = 113$ images.
- **Partition Sum Check:** $2,447 \text{ (benchmark)} + 113 \text{ (excluded rare)} + 36 \text{ (scanner OOD)} = 2,596 \text{ total}$. **Reconciled with 0 discrepancy.**

### B. Duplicate Leakage Prevention Audit
- **Algorithm:** 64-bit difference hashing ($dHash$) with Hamming distance threshold $D_H \le 10$.
- **Grouping:** Transitive connected components group identical and burst-shot frames into disjoint equivalence clusters.
- **Partitioning:** `StratifiedGroupKFold` assigns entire clusters atomically to training, validation, or test sets.
- **Leakage Audit Result:** Zero perceptual hash clusters cross train, validation, or test partitions.
- **Permitted Framing:** Qualified as preventing duplicate/near-duplicate overlap under the $D_H \le 10$ perceptual hash metric, avoiding hyperbolic claims of "all conceivable leakage eliminated."

### C. Classification Metrics Reconciliation
- **Validation Tournament ($N=489$):**
  - Zero-Rule Majority Baseline: $0.58\%$ Val Macro-F1
  - RBF-SVM (standardized 32D handcrafted features): $15.12\%$ Val Macro-F1
  - Random Forest (standardized 32D handcrafted features): $17.02\%$ Val Macro-F1
  - EfficientNet-B0 (raw $224\times 224$ RGB image tensors): $63.26\%$ Val Macro-F1
- **Held-Out Test Set Evaluation ($N=490$):**
  - Top-1 Accuracy: $61.84\%$ ($303 / 490$ correct)
  - Balanced Accuracy: $61.43\%$
  - Macro-Averaged F1: $60.84\%$
  - Wilson 95% Confidence Interval: $[57.46\%, 66.03\%]$
- **Separation:** Validation tournament used strictly for model selection; held-out test evaluated exactly once without post-hoc threshold tuning.

### D. Out-of-Distribution (OOD) Safeguard Audit — Highest Priority
- **Empirical Test:** Executed `scripts/test_36_rice_ood.py` across all 36 ICAR flatbed scanner rice images.
- **Observed Behavior:**
  - **Standalone Closed-World CNN:**
    - Falsely accepted **35 of 36 images (97.2%)** as confident predictions (uncertainty flag `False`).
    - Mean confidence: **58.9%** (with peak confidence reaching 64.06%).
    - Predictions: **18 Corn Common Rust, 10 Corn Northern Leaf Blight, 8 Corn Gray Leaf Spot**.
    - Root cause: Corn is the sole graminoid monocot leaf with parallel venation in the 12-crop training set. Rice scanner blades trigger Corn convolutional filters, compelling the closed-world softmax function to attribute them to Corn.
  - **Full AgroVision-Mine Pipeline:**
    - Leverages 32D descriptor k-NN retrieval against warehouse references.
    - All 36 images matched warehouse reference anchors with `dataset_source = 'icar_ogd'` and `crop_name = 'Rice'`.
    - Because Rice is outside the 25 supported classes, the hybrid system flagged **36 of 36 images (100.0%)** as `unsupported_domain` with `is_uncertain: True`.
- **Manuscript Correction:**
  - Removed all statements claiming that the safeguard "prevents false clinical attributions" or "guarantees universal OOD rejection."
  - Explicitly reported the standalone CNN's vulnerability and Corn misclassifications.
  - Reframed the mechanism as **exploratory domain screening via warehouse reference anchors**, noting that unmodeled crops without warehouse anchors remain an open challenge requiring formal OOD algorithms (energy-based models, temperature scaling).

### E. Ingestion, Star Schema, OLAP, and Pattern Mining
- **5 Ingestion Quality Gates:** G1 (magic bytes), G2 (spatial geometry $\ge 100\times 100$), G3 (payload $\le 15$ MB), G4 (MD5 deduplication), G5 (EXIF transposition & RGB normalization). Verified.
- **Kimball Star Schema:** SQLite `disease_observation_fact` ($2,596$ rows) with foreign keys to `dim_crop` (14), `dim_disease` (20), `dim_image` (2,596), `dim_visual_feature` (2,596). Zero foreign-key violations under `PRAGMA foreign_key_check`.
- **OLAP Latency:** Sub-35 ms across Roll-up (33.26 ms), Drill-down (31.27 ms), Slice (14.99 ms), Dice (14.42 ms), Pivot (12.57 ms) on the physical SQLite instance.
- **Unsupervised Mining:** Optimal K-Means at $K=2$ (Silhouette 0.4060, DB 1.0990, CH 1,154.38); 2D PCA capturing $52.11\%$ variance; exact association rule mining parity ($\Delta = 0.0$) between Apriori and FP-Growth.

### F. Automated Software Test Suite
- Total automated tests: **117 tests** (107 pytest unit/integration tests + 10 Playwright browser E2E tests).
- All 117 tests execute with **100% passing status** (0 failed, 0 skipped).

---

## 3. Formatting, Typography, and Page Budget Verification (A4 Template Aligned)
- **Paper Size:** Exact **A4 Dimensions** ($210.0 \times 297.0$ mm / $595.3 \times 841.9$ pt) matching the supplied reference template `Paper_template-a4 (1).docx`.
- **Page Count:** Exactly **7 Pages** in the compiled PDF (`AgroVision_Mine_IEEE_Conference_Paper_Revised.pdf`).
- **First Page Layout:**
  - Section 1 (Title and Author Block): Single-column, centered title (24pt bold), 3-column author table ($2.34''$ column widths).
  - Continuous Section Break immediately follows author block.
  - Section 2 (Body): Two-column layout ($3.38''$ column width, $0.25''$ column gap, margins: top $0.75''$, bottom $1.0''$, sides $0.63''$).
  - **Abstract & Keywords Placement:** Positioned at the top of the **LEFT COLUMN** of the two-column body (not spanning full-width).
  - Introduction begins immediately below Keywords in the left column and naturally flows into the right column.
- **Figures & Tables:** All 7 figures and 3 tables numbered sequentially, referenced in body text, with high-resolution embeds and verified captions.
- **Bibliography:** 22 references matching `references.bib` with exact DOIs, zero citation count drift, and consistent IEEE numeric style.

---

## 4. Final Verification Sign-Off
All requirements of the Master Revision Prompt have been audited, corrected, and verified against reproducible repository code, saved evaluation artifacts, and physical database instances.
