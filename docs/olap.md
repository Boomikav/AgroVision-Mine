# SQL-Backed OLAP Operations Engine

## 1. Overview & Academic Rationale

Online Analytical Processing (OLAP) provides the multi-dimensional querying foundation of **AgroVision-Mine**. While standard computer vision pipelines output isolated classification labels, OLAP operations allow agricultural researchers, plant pathologists, and extension officers to interactively traverse, aggregate, slice, and cross-tabulate multidimensional hypercubes of host crops, microbial pathologies, and extracted visual descriptors.

In this implementation, **all 5 OLAP operations execute genuine ANSI SQL queries** directly against the relational star schema warehouse (`database/agrovision_warehouse.db`). Zero operations use fabricated or static mock datasets.

---

## 2. The 5 Core OLAP Operations

### 1. ROLL-UP (Aggregation along a Dimensional Hierarchy)
- **Academic Definition:** Navigates up the dimensional hierarchy from granular individual observations to broad agronomic categories.
- **Hierarchy:** `Individual Observation -> Crop Name -> Crop Category`
- **Agronomic Question:** *"What are the total observation counts, average lesion severities, texture contrasts, and foliar greenness across broad crop categories?"*
- **Python Method:** [`OLAPEngine.rollup()`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L45-L78)
- **ANSI SQL Query:**
```sql
SELECT
    c.crop_category,
    COUNT(f.observation_key) AS total_observations,
    COUNT(DISTINCT c.crop_key) AS unique_crops_count,
    COUNT(DISTINCT f.disease_key) AS unique_diseases_count,
    ROUND(AVG(f.lesion_severity_score), 2) AS avg_lesion_severity,
    ROUND(AVG(vf.glcm_contrast), 4) AS avg_texture_contrast,
    ROUND(AVG(vf.rgb_g_mean), 2) AS avg_green_intensity,
    ROUND(AVG(f.image_sharpness_score), 2) AS avg_sharpness
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key = d.disease_key
JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
GROUP BY c.crop_category
ORDER BY total_observations DESC;
```
- **Real Warehouse Output:**

| crop_category | total_observations | unique_crops_count | unique_diseases_count | avg_lesion_severity | avg_texture_contrast | avg_green_intensity | avg_sharpness |
|---|---|---|---|---|---|---|---|
| **Cereal** | 36 | 1 | 3 | 3.61 | 0.3204 | 133.51 | 181.71 |

---

### 2A. TRUE OLAP DRILL-DOWN (Single-Dimension Hierarchy)
- **Academic Definition:** Navigates down a single dimension hierarchy from a higher aggregation level to a finer granularity within the same dimension.
- **Hierarchy:** `dim_disease: Pathogen Type -> Disease Name`
- **Agronomic Question:** *"Breaking down the microbial kingdom classifications, what specific foliar diseases manifest within the Fungal and Bacterial kingdoms, and what are their individual observation counts and severities?"*
- **Python Method:** [`OLAPEngine.true_drilldown(pathogen_type)`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L79-L125)
- **ANSI SQL Query:**
```sql
SELECT
    d.pathogen_type,
    d.disease_name,
    d.causal_agent,
    COUNT(f.observation_key) AS total_observations,
    ROUND(AVG(f.lesion_severity_score), 2) AS avg_lesion_severity,
    ROUND(AVG(vf.glcm_contrast), 4) AS avg_glcm_contrast,
    ROUND(AVG(vf.glcm_homogeneity), 4) AS avg_glcm_homogeneity,
    ROUND(AVG(vf.lesion_coverage_ratio), 4) AS avg_lesion_coverage
FROM disease_observation_fact f
JOIN dim_disease d ON f.disease_key = d.disease_key
JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
GROUP BY d.pathogen_type, d.disease_name, d.causal_agent
ORDER BY d.pathogen_type, total_observations DESC;
```
- **Real Warehouse Output:**

| pathogen_type | disease_name | causal_agent | total_observations | avg_lesion_severity | avg_glcm_contrast | avg_glcm_homogeneity | avg_lesion_coverage |
|---|---|---|---|---|---|---|---|
| Bacterial | Bacterial Leaf Blight | *Xanthomonas oryzae* | 12 | 3.67 | 0.2131 | 0.9314 | 0.3669 |
| Fungal | Brown Spot | *Bipolaris oryzae* | 12 | 3.94 | 0.5599 | 0.8586 | 0.3941 |
| Fungal | Leaf Smut | *Entyloma oryzae* | 12 | 3.11 | 0.1804 | 0.9490 | 0.3106 |

---

### 2B. DIAGNOSTIC MULTI-DIMENSIONAL BREAKDOWN (Drill-Across / Multi-Attribute Analysis)
- **Academic Definition:** Traverses multiple dimension boundaries (`dim_crop`, `dim_disease`, `dim_visual_feature`) to inspect multi-attribute interactions across host plants, diseases, and microscopic visual tone patterns.
- **Hierarchy:** `Crop Category (dim_crop) -> Crop Name (dim_crop) -> Specific Disease (dim_disease) -> Dominant Visual Tone (dim_visual_feature)`
- **Agronomic Question:** *"Within Cereals, what specific diseases manifest in Rice, what pathogens cause them, and what are their diagnostic visual tones, GLCM homogeneity, and lesion coverage ratios?"*
- **Python Method:** [`OLAPEngine.diagnostic_drilldown(crop_category)`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L127-L168)
- **ANSI SQL Query:**
```sql
SELECT
    c.crop_category,
    c.crop_name,
    d.disease_name,
    d.pathogen_type,
    vf.dominant_color_tone,
    COUNT(f.observation_key) AS observation_count,
    ROUND(AVG(f.lesion_severity_score), 2) AS avg_lesion_severity,
    ROUND(AVG(vf.glcm_contrast), 4) AS avg_glcm_contrast,
    ROUND(AVG(vf.glcm_homogeneity), 4) AS avg_glcm_homogeneity,
    ROUND(AVG(vf.lesion_coverage_ratio), 4) AS avg_lesion_coverage
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key = d.disease_key
JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
GROUP BY c.crop_category, c.crop_name, d.disease_name, d.pathogen_type, vf.dominant_color_tone
ORDER BY c.crop_name, observation_count DESC;
```
- **Real Warehouse Output (Top Rows):**

| crop_category | crop_name | disease_name | pathogen_type | dominant_color_tone | observation_count | avg_lesion_severity | avg_glcm_contrast | avg_glcm_homogeneity | avg_lesion_coverage |
|---|---|---|---|---|---|---|---|---|---|
| Cereal | Rice | Brown Spot | Fungal | Yellowish_Lesion | 11 | 3.99 | 0.5483 | 0.8561 | 0.3987 |
| Cereal | Rice | Bacterial Leaf Blight | Bacterial | Yellowish_Lesion | 8 | 4.05 | 0.2272 | 0.9258 | 0.4052 |
| Cereal | Rice | Leaf Smut | Fungal | Brown_Blight | 7 | 2.79 | 0.1780 | 0.9491 | 0.2792 |
| Cereal | Rice | Leaf Smut | Fungal | Yellowish_Lesion | 5 | 3.55 | 0.1839 | 0.9489 | 0.3544 |
| Cereal | Rice | Bacterial Leaf Blight | Bacterial | Brown_Blight | 4 | 2.90 | 0.1848 | 0.9426 | 0.2902 |
| Cereal | Rice | Brown Spot | Fungal | Brown_Blight | 1 | 3.44 | 0.6880 | 0.8857 | 0.3435 |


---

### 3. SLICE (Single-Dimension Filtering)
- **Academic Definition:** Fixes one dimension to a single constant value, slicing a 2D hyperplane from the multimodal data hypercube.
- **Examples:**
  1. Slice by Crop: `Crop = 'Rice'`
  2. Slice by Pathogen: `Pathogen_Type = 'Fungal'` or `Pathogen_Type = 'Bacterial'`
- **Agronomic Question:** *"For Rice specifically, what are the observed diseases, their causal agents, and texture contrast metrics?"*
- **Python Method:** [`OLAPEngine.slice_by_crop("Rice")`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L121-L154) and [`OLAPEngine.slice_by_pathogen("Fungal")`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L156-L185)
- **ANSI SQL Query (Slice by Crop):**
```sql
SELECT
    d.disease_name,
    d.pathogen_type,
    d.causal_agent,
    vf.dominant_color_tone,
    COUNT(f.observation_key) AS disease_observations,
    ROUND(AVG(f.lesion_severity_score), 2) AS avg_severity,
    ROUND(AVG(vf.glcm_contrast), 4) AS avg_contrast,
    ROUND(AVG(vf.glcm_energy), 4) AS avg_energy,
    ROUND(AVG(vf.lesion_coverage_ratio), 4) AS avg_lesion_coverage
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key = d.disease_key
JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
WHERE LOWER(c.crop_name) = LOWER(:crop_name)
GROUP BY d.disease_name, d.pathogen_type, d.causal_agent, vf.dominant_color_tone
ORDER BY disease_observations DESC;
```
- **Real Warehouse Output (Slice Crop = 'Rice'):**

| disease_name | pathogen_type | causal_agent | dominant_color_tone | disease_observations | avg_severity | avg_contrast | avg_energy | avg_lesion_coverage |
|---|---|---|---|---|---|---|---|---|
| Brown Spot | Fungal | *Bipolaris oryzae* | Yellowish_Lesion | 11 | 3.99 | 0.5483 | 0.1432 | 0.3987 |
| Bacterial Leaf Blight | Bacterial | *Xanthomonas oryzae pv. oryzae* | Yellowish_Lesion | 8 | 4.05 | 0.2272 | 0.2578 | 0.4052 |
| Leaf Smut | Fungal | *Entyloma oryzae* | Brown_Blight | 7 | 2.79 | 0.1780 | 0.4777 | 0.2792 |
| Leaf Smut | Fungal | *Entyloma oryzae* | Yellowish_Lesion | 5 | 3.55 | 0.1839 | 0.4189 | 0.3544 |
| Bacterial Leaf Blight | Bacterial | *Xanthomonas oryzae pv. oryzae* | Brown_Blight | 4 | 2.90 | 0.1848 | 0.4404 | 0.2902 |
| Brown Spot | Fungal | *Bipolaris oryzae* | Brown_Blight | 1 | 3.44 | 0.6880 | 0.4111 | 0.3435 |

---

### 4. DICE (Multi-Dimensional Sub-Cube Filtering)
- **Academic Definition:** Extracts a sub-cube by applying simultaneous filtering predicates across multiple dimensions (Crop, Pathogen Type, and Visual Texture Contrast).
- **Example Predicates:** `Crop IN ('Rice') AND Pathogen IN ('Fungal', 'Bacterial') AND GLCM Texture Contrast >= 0.10`.
- **Agronomic Question:** *"Which severe fungal or bacterial infections occur in Rice where visual texture disruption exceeds our baseline threshold of 0.10?"*
- **Python Method:** [`OLAPEngine.dice(selected_crops, selected_pathogens, min_contrast)`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L186-L243)
- **ANSI SQL Query:**
```sql
SELECT
    c.crop_category,
    c.crop_name,
    d.disease_name,
    d.pathogen_type,
    vf.dominant_color_tone,
    COUNT(f.observation_key) AS observation_count,
    ROUND(AVG(f.lesion_severity_score), 2) AS avg_severity,
    ROUND(AVG(vf.glcm_contrast), 4) AS avg_glcm_contrast,
    ROUND(AVG(vf.glcm_homogeneity), 4) AS avg_glcm_homogeneity
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key = d.disease_key
JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
WHERE LOWER(c.crop_name) IN (:c_0)
  AND LOWER(d.pathogen_type) IN (:p_0, :p_1)
  AND vf.glcm_contrast >= :min_contrast
GROUP BY c.crop_category, c.crop_name, d.disease_name, d.pathogen_type, vf.dominant_color_tone
ORDER BY c.crop_name, avg_severity DESC;
```
- **Real Warehouse Output:**

| crop_category | crop_name | disease_name | pathogen_type | dominant_color_tone | observation_count | avg_severity | avg_glcm_contrast | avg_glcm_homogeneity |
|---|---|---|---|---|---|---|---|---|
| Cereal | Rice | Bacterial Leaf Blight | Bacterial | Yellowish_Lesion | 8 | 4.05 | 0.2272 | 0.9258 |
| Cereal | Rice | Brown Spot | Fungal | Yellowish_Lesion | 11 | 3.99 | 0.5483 | 0.8561 |
| Cereal | Rice | Leaf Smut | Fungal | Yellowish_Lesion | 5 | 3.55 | 0.1839 | 0.9489 |
| Cereal | Rice | Brown Spot | Fungal | Brown_Blight | 1 | 3.44 | 0.6880 | 0.8857 |
| Cereal | Rice | Bacterial Leaf Blight | Bacterial | Brown_Blight | 4 | 2.90 | 0.1848 | 0.9426 |
| Cereal | Rice | Leaf Smut | Fungal | Brown_Blight | 7 | 2.79 | 0.1780 | 0.9491 |

---

### 5. PIVOT (Cross-Tabulation & Dimension Rotation)
- **Academic Definition:** Rotates the axes of the warehouse cube so that one dimension forms rows, another forms columns, and intersecting cells contain aggregated numerical measures.
- **Axes:** Rows = `Crop Name` | Columns = `Pathogen Type` (`Fungal`, `Bacterial`, `Viral`, `Healthy/None`).
- **Measures Supported:** Total Observation Counts (`SUM(CASE WHEN ...)`) or Average GLCM Texture Contrast (`ROUND(AVG(CASE WHEN ...), 4)`).
- **Agronomic Question:** *"What is the cross-tabulation of host crops versus pathogen classes across the national observation archive?"*
- **Python Method:** [`OLAPEngine.pivot(measure="observation_count")`](file:///c:/Users/ajaya/Desktop/Agro/src/olap/engine.py#L244-L294)
- **ANSI SQL Query:**
```sql
SELECT
    c.crop_name AS "Crop",
    c.crop_category AS "Category",
    SUM(CASE WHEN d.pathogen_type = 'Fungal' THEN 1 ELSE 0 END) AS "Fungal",
    SUM(CASE WHEN d.pathogen_type = 'Bacterial' THEN 1 ELSE 0 END) AS "Bacterial",
    SUM(CASE WHEN d.pathogen_type = 'Viral' THEN 1 ELSE 0 END) AS "Viral",
    SUM(CASE WHEN d.pathogen_type = 'None' THEN 1 ELSE 0 END) AS "Healthy_or_None",
    COUNT(f.observation_key) AS "Overall_Metric"
FROM disease_observation_fact f
JOIN dim_crop c ON f.crop_key = c.crop_key
JOIN dim_disease d ON f.disease_key = d.disease_key
JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
GROUP BY c.crop_name, c.crop_category
ORDER BY "Overall_Metric" DESC;
```
- **Real Warehouse Output (Pivot Table):**

| Crop | Category | Fungal | Bacterial | Viral | Healthy_or_None | Overall_Metric |
|---|---|---|---|---|---|---|
| **Rice** | **Cereal** | **24** | **12** | **0** | **0** | **36** |

> **Taxonomy Audit Note (`Healthy_or_None = 0`):**
> The `Healthy_or_None` column returns `0` because the authentic ICAR research dataset comprises pathological specimens exclusively. `HEALTHY` is retained in `dim_disease` as an unpopulated control reference category.


---

## 3. Dashboard Integration

All 5 operations are dynamically exposed through the interactive Streamlit dashboard ([`dashboard/app.py`](file:///c:/Users/ajaya/Desktop/Agro/dashboard/app.py#L345-L443)):
- **Interactive Controls:** Dynamic dropdowns populated directly from database distinct values (`avail_crops`, `avail_categories`, `avail_pathogens`), contrast sliders, and measure selectors.
- **Visual Feedback:** Data table display, sub-second query latency indicators, and live ANSI SQL syntax inspection.

---

## 4. Verification & Testing

Execution commands to audit and verify all OLAP operations:

```bash
# 1. Run standalone CLI OLAP demonstration against real warehouse
python run.py --stage olap

# 2. Run unit tests against isolated mock engine
pytest tests/test_olap.py -v

# 3. Run integration tests directly against physical warehouse records
pytest tests/test_olap_real_warehouse.py -v
```
