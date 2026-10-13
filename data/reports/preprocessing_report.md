# AgroVision-Mine: Preprocessing & Quality Diagnostics Audit Report

---

## 1. Preprocessing Execution Statistics
- **Total Discovered Candidate Files:** `36`
- **Valid Image Files:** `36`
- **Invalid / Corrupted Files:** `0`
- **Exact / Perceptual Duplicates:** `0`
- **Successfully Standardized & Saved:** `36`
- **Total Skipped / Excluded:** `0`
- **Configured Target Resolution:** `256 x 256 px`

---

## 2. Rejection & Diagnostic Reasons
- None (All images passed quality checks).

---

## 3. Preservation of Raw Assets
- Original raw images in `data/raw/` remain strictly read-only and unmodified.
- Standardized $256 \times 256$ RGB images are written into `data/processed/<crop>/<condition>/`.
- Cleaned metadata records are exported to `data/processed/cleaned_metadata.csv`.
- Detailed rejection diagnostics are recorded in `data/reports/rejected_images_report.md`.
