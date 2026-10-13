-- =======================================================================
-- AgroVision-Mine: Star Schema DDL for Multimodal Agricultural Warehouse
-- Ground-Truth Derived Architecture (Phase 4)
-- Dialect: ANSI SQL (SQLite & PostgreSQL Compatible)
-- =======================================================================

-- 1. Dimension: Dim_Crop (Host Plant Dimension)
CREATE TABLE IF NOT EXISTS dim_crop (
    crop_key INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_code VARCHAR(50) NOT NULL UNIQUE,
    crop_name VARCHAR(100) NOT NULL,
    botanical_name VARCHAR(150) NOT NULL,
    crop_category VARCHAR(50) NOT NULL,
    economic_significance VARCHAR(100) DEFAULT 'Commercial Staple'
);
CREATE INDEX IF NOT EXISTS idx_dim_crop_category ON dim_crop(crop_category);
CREATE INDEX IF NOT EXISTS idx_dim_crop_code ON dim_crop(crop_code);

-- 2. Dimension: Dim_Disease (Pathology Dimension)
CREATE TABLE IF NOT EXISTS dim_disease (
    disease_key INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_code VARCHAR(50) NOT NULL UNIQUE,
    disease_name VARCHAR(150) NOT NULL,
    pathogen_type VARCHAR(50) NOT NULL,
    causal_agent VARCHAR(150) DEFAULT 'Unspecified',
    primary_symptom VARCHAR(200) DEFAULT 'Foliar lesion'
);
CREATE INDEX IF NOT EXISTS idx_dim_disease_pathogen ON dim_disease(pathogen_type);
CREATE INDEX IF NOT EXISTS idx_dim_disease_code ON dim_disease(disease_code);

-- 3. Dimension: Dim_Image (Physical & Technical Image Dimension)
CREATE TABLE IF NOT EXISTS dim_image (
    image_key INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_id VARCHAR(50) NOT NULL UNIQUE,
    filename VARCHAR(255) NOT NULL,
    file_format VARCHAR(20) NOT NULL,
    raw_width INTEGER NOT NULL,
    raw_height INTEGER NOT NULL,
    raw_channels INTEGER NOT NULL DEFAULT 3,
    raw_size_kb FLOAT NOT NULL,
    processed_width INTEGER DEFAULT 256,
    processed_height INTEGER DEFAULT 256,
    processed_size_kb FLOAT NOT NULL,
    md5_hash VARCHAR(64) NOT NULL UNIQUE,
    phash VARCHAR(32),
    blur_score FLOAT DEFAULT 0.0,
    is_blurry BOOLEAN DEFAULT 0,
    original_path TEXT NOT NULL,
    processed_path TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_dim_image_raw_id ON dim_image(raw_id);
CREATE INDEX IF NOT EXISTS idx_dim_image_hash ON dim_image(md5_hash);

-- 4. Dimension: Dim_VisualFeature (Visual Pattern Descriptor Dimension)
CREATE TABLE IF NOT EXISTS dim_visual_feature (
    feature_key INTEGER PRIMARY KEY AUTOINCREMENT,
    image_filename VARCHAR(255) NOT NULL UNIQUE,
    -- Color Moments & Normalizations
    rgb_r_mean FLOAT NOT NULL,
    rgb_g_mean FLOAT NOT NULL,
    rgb_b_mean FLOAT NOT NULL,
    rgb_r_std FLOAT NOT NULL,
    rgb_g_std FLOAT NOT NULL,
    rgb_b_std FLOAT NOT NULL,
    rgb_r_norm FLOAT NOT NULL,
    rgb_g_norm FLOAT NOT NULL,
    rgb_b_norm FLOAT NOT NULL,
    hsv_h_mean FLOAT NOT NULL,
    hsv_s_mean FLOAT NOT NULL,
    hsv_v_mean FLOAT NOT NULL,
    hsv_h_norm FLOAT NOT NULL,
    hsv_s_norm FLOAT NOT NULL,
    hsv_v_norm FLOAT NOT NULL,
    exg_index_mean FLOAT NOT NULL,
    dominant_color_tone VARCHAR(50) NOT NULL,
    -- GLCM Haralick Textures
    glcm_contrast FLOAT NOT NULL,
    glcm_contrast_norm FLOAT NOT NULL,
    glcm_dissimilarity FLOAT NOT NULL,
    glcm_homogeneity FLOAT NOT NULL,
    glcm_energy FLOAT NOT NULL,
    glcm_correlation FLOAT NOT NULL,
    glcm_asm FLOAT NOT NULL,
    -- Morphometric Shape Descriptors
    has_valid_contour BOOLEAN DEFAULT 0,
    contour_area FLOAT DEFAULT 0.0,
    contour_perimeter FLOAT DEFAULT 0.0,
    contour_aspect_ratio FLOAT DEFAULT 1.0,
    contour_circularity FLOAT DEFAULT 0.0,
    contour_solidity FLOAT DEFAULT 0.0,
    lesion_coverage_ratio FLOAT DEFAULT 0.0
);
CREATE INDEX IF NOT EXISTS idx_dim_feature_tone ON dim_visual_feature(dominant_color_tone);
CREATE INDEX IF NOT EXISTS idx_dim_feature_contrast ON dim_visual_feature(glcm_contrast_norm);

-- 5. Central Fact Table: DiseaseObservation_Fact
-- Grain: Exactly ONE row per validated, preprocessed multimodal image observation
CREATE TABLE IF NOT EXISTS disease_observation_fact (
    observation_key INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_key INTEGER NOT NULL,
    disease_key INTEGER NOT NULL,
    image_key INTEGER NOT NULL UNIQUE,
    feature_key INTEGER NOT NULL UNIQUE,
    -- Additive and Semi-Additive Measures
    observation_count INTEGER NOT NULL DEFAULT 1,
    lesion_severity_score FLOAT NOT NULL DEFAULT 0.0,
    image_sharpness_score FLOAT NOT NULL DEFAULT 0.0,
    lesion_coverage_ratio FLOAT NOT NULL DEFAULT 0.0,
    texture_contrast_norm FLOAT NOT NULL DEFAULT 0.0,
    processing_latency_ms FLOAT NOT NULL DEFAULT 0.0,
    -- Audit Lineage & Batch Degenerate Attributes
    etl_batch_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Foreign Key Referential Integrity Constraints
    FOREIGN KEY (crop_key) REFERENCES dim_crop(crop_key) ON DELETE RESTRICT,
    FOREIGN KEY (disease_key) REFERENCES dim_disease(disease_key) ON DELETE RESTRICT,
    FOREIGN KEY (image_key) REFERENCES dim_image(image_key) ON DELETE RESTRICT,
    FOREIGN KEY (feature_key) REFERENCES dim_visual_feature(feature_key) ON DELETE RESTRICT
);

-- Compound Indices for OLAP Performance Acceleration
CREATE INDEX IF NOT EXISTS idx_fact_crop_disease ON disease_observation_fact(crop_key, disease_key);
CREATE INDEX IF NOT EXISTS idx_fact_batch ON disease_observation_fact(etl_batch_id);
