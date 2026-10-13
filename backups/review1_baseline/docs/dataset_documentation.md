# Dataset Documentation: ICAR & Open Government Data Platform

## 1. Primary Source Identification

**AgroVision-Mine** is designed to ingest agricultural crop disease and pest imagery directly from official Indian agrarian repositories:
- **Primary Source:** Official Government of India Open Government Data platform ([data.gov.in](https://data.gov.in)) and the **Indian Council of Agricultural Research (ICAR)** constituent research institutes:
  - **ICAR-CRIDA** (Central Research Institute for Dryland Agriculture): Crop-Pest-Disease-Weather Surveillance Repositories.
  - **ICAR-IIRR** (Indian Institute of Rice Research): Decadal Production-Oriented Survey & National Rice Disease Image Datasets.
  - **ICAR-NCIPM** (National Research Centre for Integrated Pest Management): National Pest Surveillance System (NPSS).
  - **ICAR-IARI** (Indian Agricultural Research Institute): Pulse, cereal, and oilseed foliar pathology datasets.

## 2. Academic Anti-Fabrication Mandate

In strict accordance with project requirements:
- **No Synthetic Fabrication:** Image counts, crop names, disease labels, causal pathogens, and metadata attributes are **never** fabricated.
- **Dynamic Inspection:** The system dynamically inspects whatever actual dataset is placed inside `data/raw/`, discovers directory hierarchies or metadata manifests, computes cryptographic file hashes, and validates image dimensions and channels directly from disk.
- **Botanical & Pathological Alignment:** All discovered labels are normalized to authenticated botanical names (e.g., *Oryza sativa*, *Triticum aestivum*, *Gossypium hirsutum*) and taxonomically verified causal organisms (e.g., *Magnaporthe oryzae*, *Xanthomonas oryzae*, *Bipolaris oryzae*).

---

## 3. Agronomic Taxonomy & Classification Catalog

### A. Host Crops (Host Plants)
| Crop Code | Common Name | Botanical Name | Crop Category | Agronomic Role |
| :--- | :--- | :--- | :--- | :--- |
| `RICE` | Rice / Paddy | *Oryza sativa* | Cereal | Primary national staple food grain |
| `WHEAT` | Wheat | *Triticum aestivum* | Cereal | Major rabi cereal food grain |
| `COTTON` | Cotton | *Gossypium hirsutum* | Fiber | Primary commercial cash fiber crop |
| `MAIZE` | Maize / Corn | *Zea mays* | Cereal | Coarse grain and industrial feedstock |
| `TOMATO` | Tomato | *Solanum lycopersicum* | Horticultural | High-value perishable vegetable |
| `MUSTARD` | Indian Mustard | *Brassica nigra* | Oilseed | Key edible oilseed crop |

### B. Plant Diseases & Causal Pathogens
| Disease Code | Disease Name | Pathogen Type | Causal Organism | Primary Foliar Symptom | Warehouse Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `BACTERIAL_BLIGHT`| Bacterial Leaf Blight | Bacterial | *Xanthomonas oryzae* | Water-soaked to yellowish-white wavy lesions along leaf margins | Populated (12 Facts) |
| `BROWN_SPOT` | Brown Spot | Fungal | *Bipolaris oryzae* | Oval, brown spots with yellow halos covering leaf blades | Populated (12 Facts) |
| `LEAF_SMUT` | Leaf Smut | Fungal | *Entyloma oryzae* | Small, linear black spots (sori) scattered across foliar blades | Populated (12 Facts) |
| `HEALTHY` | Healthy / Asymptomatic | None | None | Normal chlorophyll pigmentation, absence of lesions | **Unpopulated Control Baseline** |

> **Taxonomy Reference Value Rationale (`HEALTHY`):**
> The current ICAR research collection contains pathological specimens only; therefore no healthy observations are loaded into the fact table. `HEALTHY` is maintained in `dim_disease` as an unpopulated control reference domain / baseline catalog item, allowing future ingestion of non-diseased control imagery without altering the warehouse dimension schema.

### C. Insect Pests
| Pest Code | Common Name | Pest Order | Scientific Name | Damage Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| `STEM_BORER` | Yellow Stem Borer | Lepidoptera | *Scirpophaga incertulas* | Deadheart in vegetative stage; whitehead in reproductive stage |
| `BOLLWORM` | Cotton Bollworm | Lepidoptera | *Helicoverpa armigera* | Foliar feeding and square/boll boring in cotton plants |
| `BROWN_PLANTHOPPER` | Brown Planthopper | Hemiptera | *Nilaparvata lugens* | Phloem sap sucking leading to "hopper burn" |
| `NONE` | No Pest Infestation | None | None | Asymptomatic |

---

## 4. Dataset Isolation: Authentic Source vs. Diagnostic Edge Cases

To prevent diagnostic synthetic files from contaminating genuine agronomic data while maintaining rigorous automated quality gates, storage is strictly partitioned:

1. **`data/raw/` (Authentic Source Dataset Exclusively):**
   - Contains **exactly 36 authentic, unadulterated field photographs** of rice foliar diseases:
     - `data/raw/rice/bacterial_leaf_blight/` (12 images, `DSC_0365.JPG` to `DSC_0379.JPG`)
     - `data/raw/rice/brown_spot/` (12 images, `DSC_0100.jpg` to `DSC_0113.jpg`)
     - `data/raw/rice/leaf_smut/` (12 images, `DSC_0293.JPG` to `DSC_0319.jpg`)
   - All 36 images pass extension whitelisting, header verification, dimension thresholds, and duplicate detection.

2. **`data/diagnostic_tests/` (Controlled Test Harness Artifacts):**
   - `corrupted_header_test.jpg`: Validates `ImageValidator` rejection of truncated or invalid file headers (`CORRUPTED`).
   - `duplicate_exact_test.jpg`: Validates `DuplicateDetector` cryptographic hash collision detection (`EXACT_HASH`).
   - `invalid_dim_tiny.jpg`: Validates dimension boundary guards for sub-threshold images (`INVALID_DIMENSIONS`).
   - `unsupported_extension.txt`: Validates MIME/extension rejection (`UNSUPPORTED_FORMAT`).

---

## 5. Ingestion Mechanics

1. **Drop-in Location:** `data/raw/<crop>/<condition>/<filename.jpg>`
2. **Scanner:** `DatasetInspector.scan_raw_directory()` performs recursive traversal over authentic directories.
3. **Integrity Auditing:** Calculates MD5 checksum for cryptographic immutability and generates `data/reports/source_inventory.json`.
4. **Idempotency:** Re-running the scanner on existing datasets creates no duplicated records.

