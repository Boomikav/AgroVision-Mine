# AgroVision-Mine: Expanded Multi-Crop Research Dataset v2 Documentation

## 1. Executive Summary & Purpose
The AgroVision-Mine Canonical Dataset v2 represents a rigorous expansion from the initial 36-image Rice proof-of-concept into a multi-crop, multi-pathology benchmark dataset. It integrates authentic field observations from two verified, peer-reviewed public agricultural sources while preserving the integrity, lineage, and explainable feature space established in Review 1.

* **Total Canonical Retained Observations:** 2,596 verified unique images.
* **Crop Species Represented:** 14 botanical host crops (Rice, Tomato, Corn, Apple, Potato, Grape, Bell Pepper, Squash, Raspberry, Blueberry, Peach, Strawberry, Soybean, Cherry).
* **Conditions / Pathologies Represented:** 31 unique crop-condition combinations across 19 distinct pathology classes and authentic healthy foliage baselines.
* **Standardized Analytical Representation:** 256 × 256 × 3 RGB (Lanczos anti-aliased interpolation).
* **Analytical Feature Store:** 2,596 rows × 44 columns (34 explainable visual descriptors + 10 metadata/lineage fields).

---

## 2. Source Repositories & Licensing

| Source ID | Dataset Name | Source Organization / Reference | License | Imaging Modality | Retained Images |
|---|---|---|---|---|---|
| `icar_ogd` | Government of India / ICAR Crop Pathology Subset | ICAR-CRIDA / ICAR-IIRR / [data.gov.in](https://data.gov.in) | Government Open Data License - India (GODL-India) | Field Macro Photography | 36 |
| `plantdoc` | PlantDoc: Visual Plant Disease Detection | ACM CoDS-COMAD 2020 / [PlantDoc GitHub](https://github.com/pratikkayal/PlantDoc-Dataset) | Creative Commons Attribution 4.0 International (CC BY 4.0) | In-Field Complex Natural Agricultural Environments | 2,560 |

---

## 3. Host Crop & Taxonomic Representation

| Crop Name | Botanical Name | Agricultural Category | Retained Images | Primary Conditions Present |
|---|---|---|---|---|
| **Tomato** | *Solanum lycopersicum* | Solanaceous Vegetable | 743 | Early Blight, Late Blight, Bacterial Spot, Septoria Leaf Spot, Leaf Mold, Mosaic Virus, Yellow Leaf Curl, Spider Mites, Healthy |
| **Corn (Maize)** | *Zea mays* | Cereal Grain | 372 | Gray Leaf Spot, Northern Leaf Blight, Common Rust |
| **Apple** | *Malus domestica* | Pome Fruit | 272 | Apple Scab, Cedar Apple Rust, Healthy |
| **Potato** | *Solanum tuberosum* | Tuber / Vegetable | 216 | Early Blight, Late Blight |
| **Grape** | *Vitis vinifera* | Viticulture / Fruit | 133 | Black Rot, Healthy |
| **Bell Pepper** | *Capsicum annuum* | Solanaceous Vegetable | 132 | Bacterial Spot, Healthy |
| **Squash** | *Cucurbita pepo* | Cucurbit Vegetable | 130 | Powdery Mildew |
| **Raspberry** | *Rubus idaeus* | Caneberry / Fruit | 119 | Healthy |
| **Blueberry** | *Vaccinium corymbosum* | Berry / Fruit | 114 | Healthy |
| **Peach** | *Prunus persica* | Stone Fruit | 111 | Healthy |
| **Strawberry** | *Fragaria × ananassa* | Berry / Fruit | 96 | Healthy |
| **Soybean** | *Glycine max* | Legume / Oilseed | 65 | Healthy |
| **Cherry** | *Prunus avium* | Stone Fruit | 57 | Healthy |
| **Rice** | *Oryza sativa* | Cereal Grain | 36 | Bacterial Leaf Blight, Brown Spot, Leaf Smut |

---

## 4. Pathology & Health Status Distribution

* **Health Breakdown:**
  * **Diseased Foliage:** 1,750 images (67.4%)
  * **Healthy Foliage:** 846 images (32.6%)
* **Pathogen Kingdom Distribution:**
  * **Fungal Pathogens:** 1,426 observations (*Venturia*, *Gymnosporangium*, *Cercospora*, *Setosphaeria*, *Puccinia*, *Alternaria*, *Phytophthora*, *Podosphaera*, *Septoria*, *Passalora*, *Guignardia*, *Bipolaris*, *Entyloma*)
  * **Bacterial Pathogens:** 193 observations (*Xanthomonas campestris*, *Xanthomonas perforans*, *Xanthomonas oryzae*)
  * **Viral Pathogens:** 129 observations (*Tobacco mosaic virus*, *Tomato yellow leaf curl virus*)
  * **Agricultural Pests:** 2 observations (*Tetranychus urticae* / Two-Spotted Spider Mites)
  * **Healthy Baselines (Pathogen: None):** 846 observations

---

## 5. Data Quality, Deduplication, and Exclusions
* **Total Discovered Candidates:** 2,608 files.
* **Exact MD5 Duplicates Excluded:** 12 files (repeated identical images across train/test splits).
* **Corrupt / Sub-dimension Rejections:** 0 files (all candidate files satisfied format and $W, H \ge 32$ px criteria).
* **Mean Raw Image Dimensions:** $812.4 \times 749.6$ pixels.
* **Standardized Resolution:** $256 \times 256 \times 3$ RGB.
* **Laplacian Blur Quality:** Mean score = 338.41 (images below 100.0 flagged with `is_blurry = True` for auditability).
* **Traceability:** Every row maps 1:1 via `image_id` and `md5_hash` to its physical raw path and processed image on disk.
