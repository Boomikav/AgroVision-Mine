# Official Dataset Setup Guide: ICAR & Open Government Data Platform

This guide explains how to acquire, place, and profile the official agricultural crop disease and pest image dataset for **AgroVision-Mine**.

---

## 1. Where to Obtain the Official Dataset

Under the project mandate, the intended primary source is the **Government of India Open Government Data platform ([data.gov.in](https://data.gov.in))** and **ICAR (Indian Council of Agricultural Research)** institute repositories:

1. **Open Government Data (OGD) Portal ([data.gov.in](https://data.gov.in)):**
   - Search for **"ICAR Crop Pest"**, **"ICAR Disease Surveillance"**, or **"Rice Pest Surveillance"**.
   - Download the official ZIP or CSV manifest archive.

2. **ICAR Institutional Repositories:**
   - **ICAR-CRIDA** (Central Research Institute for Dryland Agriculture): [http://www.crida.in](http://www.crida.in) (Crop-Pest-Disease-Weather Database for Rice, Cotton, and Pulses).
   - **ICAR-IIRR** (Indian Institute of Rice Research): [https://www.icar-iirr.org](https://www.icar-iirr.org) (National Rice Blast and Bacterial Blight repositories).
   - **ICAR-NCIPM** (National Research Centre for Integrated Pest Management): [https://ncipm.icar.gov.in](https://ncipm.icar.gov.in) (National Pest Surveillance System).

3. **Mendeley Data / Zenodo (ICAR Academic Open Datasets):**
   - Verified open-access research repositories published by ICAR scientists (e.g., *ICAR-IARI Leaf Blast & Sheath Rot Image Dataset*, *ICAR Mustard Foliar Disease Archive*).

---

## 2. Exactly Where to Place the Dataset

Place all uncompressed folders and image files directly inside the `data/raw/` directory:

```text
Agro/
└── data/
    └── raw/                                <── DROP DATASET HERE
        ├── rice/
        │   ├── blast/
        │   │   ├── blast_001.jpg
        │   │   └── ...
        │   ├── brown_spot/
        │   │   ├── brown_001.jpg
        │   │   └── ...
        │   └── bacterial_blight/
        │       └── bb_001.jpg
        ├── wheat/
        │   └── rust/
        │       └── rust_001.jpg
        ├── cotton/
        │   └── bollworm/
        │       └── bw_001.jpg
        └── metadata.csv                    <── (Optional manifest file if provided by ICAR)
```

### Supported Layout Formats:
- **Hierarchical Layout (Recommended):** `data/raw/<crop>/<condition>/<image_file.jpg>`
- **Compound Folder Layout:** `data/raw/<crop>___<condition>/<image_file.jpg>`
- **Manifest-Accompanied Layout:** Place images in `data/raw/` with a `metadata.csv` or `annotations.json` describing image paths, crop names, and disease annotations.

---

## 3. How to Trigger Dataset Inspection & Profiling

Once files are placed into `data/raw/`, run the profiling script:

```bash
python scripts/inspect_dataset.py
```

Or run via the master CLI:
```bash
python run.py --stage extract
```

### What the Inspection Pipeline Does:
1. **Recursively scans** all files without modifying or moving them.
2. **Validates image headers, sizes, and formats** (JPEG, PNG, TIFF, WebP, etc.).
3. **Extracts genuine metadata** from directory hierarchy, CSV/JSON manifests, and EXIF headers.
4. **Detects whether date or geographic coordinates exist** (no fields are invented).
5. **Generates two audit reports:**
   - Machine-readable JSON: `data/reports/dataset_profiling_report.json`
   - Human-readable Markdown: `data/reports/dataset_profiling_report.md`

---

## 4. Academic Anti-Fabrication Guarantee

- **No synthetic labels:** If the dataset only contains foliar disease images without timestamps or GPS coordinates, `Dim_Time` and `Dim_Geography` will remain unpopulated or nullable.
- **Defensible Viva Representation:** The project derivation is 100% auditable directly from the files on disk.
