# Star Schema Entity-Relationship Specification

## 1. Dimensional Architecture Diagram

```mermaid
erDiagram
    DIM_CROP ||--o{ DISEASE_OBSERVATION_FACT : "hosts"
    DIM_DISEASE ||--o{ DISEASE_OBSERVATION_FACT : "afflicts"
    DIM_PEST ||--o{ DISEASE_OBSERVATION_FACT : "infests"
    DIM_IMAGE ||--o{ DISEASE_OBSERVATION_FACT : "captures"
    DIM_VISUAL_FEATURE ||--o{ DISEASE_OBSERVATION_FACT : "quantifies"

    DIM_CROP {
        int crop_key PK
        string crop_code UK
        string crop_name
        string botanical_name
        string crop_category
        string economic_significance
    }

    DIM_DISEASE {
        int disease_key PK
        string disease_code UK
        string disease_name
        string pathogen_type
        string causal_agent
        string primary_symptom
    }

    DIM_PEST {
        int pest_key PK
        string pest_code UK
        string pest_name
        string pest_type
        string scientific_name
    }

    DIM_IMAGE {
        int image_key PK
        string raw_id UK
        string filename
        int raw_width
        int raw_height
        float raw_size_kb
        int processed_width
        int processed_height
        string md5_hash
        string phash
        float blur_score
        boolean is_blurry
        string original_path
        string processed_path
    }

    DIM_VISUAL_FEATURE {
        int feature_key PK
        string image_filename UK
        float rgb_r_mean
        float rgb_g_mean
        float rgb_b_mean
        float hsv_h_mean
        float hsv_s_mean
        float hsv_v_mean
        string dominant_color_tone
        float glcm_contrast
        float glcm_homogeneity
        float glcm_energy
        float glcm_correlation
        boolean has_valid_contour
        float contour_area
        float contour_circularity
        float lesion_coverage_ratio
    }

    DISEASE_OBSERVATION_FACT {
        int observation_key PK
        int crop_key FK
        int disease_key FK
        int pest_key FK
        int image_key FK
        int feature_key FK
        int observation_count
        float lesion_severity_score
        float image_sharpness_score
        float processing_latency_ms
        string etl_batch_id
        timestamp created_at
    }
```

---

## 2. Table Indexing & Physical Storage Strategy

| Table Name | Index Name | Indexed Columns | Index Purpose |
| :--- | :--- | :--- | :--- |
| `dim_crop` | `idx_dim_crop_category` | `crop_category` | Speeds up Roll-up and Drill-down operations |
| `dim_disease` | `idx_dim_disease_pathogen`| `pathogen_type` | Speeds up Slice and Dice by pathogen class |
| `dim_image` | `idx_dim_image_hash` | `md5_hash` | O(1) duplicate checks and lookup |
| `dim_visual_feature` | `idx_dim_feature_tone` | `dominant_color_tone` | Enables rapid visual tone filtering |
| `disease_observation_fact`| `idx_fact_crop_disease` | `crop_key, disease_key` | High-frequency fact join optimization |
| `disease_observation_fact`| `idx_fact_crop_pathogen`| `crop_key, disease_key, pest_key` | Multi-dimensional aggregation acceleration |
