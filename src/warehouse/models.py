"""
Star Schema Relational Models for AgroVision-Mine Multimodal Data Warehouse.
Defines the unified physical warehouse schema containing all 2,596 authentic observations:
- DimCrop: Botanical taxonomy and agronomic classification (14 crops)
- DimDisease: Pathology taxonomy, causal agents, and symptoms (19 conditions)
- DimImage: Physical image metadata, dimensions, hashes, source provenance
- DimVisualFeature: Complete 32 continuous visual descriptors + morphology
- DiseaseObservationFact: Central observation fact table (grain: 1 image observation)
"""
from datetime import datetime
from typing import Any, Dict
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Index, Text
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class DimCrop(Base):
    """
    Host Plant Dimension: Captures botanical taxonomy and agronomic classification.
    """
    __tablename__ = "dim_crop"

    crop_key = Column(Integer, primary_key=True, autoincrement=True)
    crop_code = Column(String(50), unique=True, nullable=False, index=True)
    crop_name = Column(String(100), nullable=False)
    botanical_name = Column(String(150), nullable=False)
    crop_category = Column(String(50), nullable=False, index=True)  # Cereal, Horticultural, Legume
    economic_significance = Column(String(100), default="Commercial Staple")

    observations = relationship("DiseaseObservationFact", back_populates="crop")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "crop_key": self.crop_key,
            "crop_code": self.crop_code,
            "crop_name": self.crop_name,
            "botanical_name": self.botanical_name,
            "crop_category": self.crop_category,
            "economic_significance": self.economic_significance
        }


class DimDisease(Base):
    """
    Pathology Dimension: Captures plant pathology taxonomy, causal agent, and symptoms.
    """
    __tablename__ = "dim_disease"

    disease_key = Column(Integer, primary_key=True, autoincrement=True)
    disease_code = Column(String(50), unique=True, nullable=False, index=True)
    disease_name = Column(String(150), nullable=False)
    pathogen_type = Column(String(50), nullable=False, index=True)  # Bacterial, Fungal, Viral, Pest, None
    causal_agent = Column(String(150), default="Unspecified")
    primary_symptom = Column(String(200), default="Foliar lesion")

    observations = relationship("DiseaseObservationFact", back_populates="disease")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "disease_key": self.disease_key,
            "disease_code": self.disease_code,
            "disease_name": self.disease_name,
            "pathogen_type": self.pathogen_type,
            "causal_agent": self.causal_agent,
            "primary_symptom": self.primary_symptom
        }


class DimImage(Base):
    """
    Image Dimension: Tracks physical parameters, optical metadata, and cryptographic provenance.
    """
    __tablename__ = "dim_image"

    image_key = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String(50), unique=True, nullable=False, index=True)  # AGRO_V2_...
    raw_id = Column(String(50), unique=True, nullable=False, index=True)  # Original identifier
    dataset_source = Column(String(50), nullable=False, default="plantdoc")  # plantdoc or icar_ogd
    filename = Column(String(255), nullable=False)
    file_format = Column(String(20), nullable=False)
    raw_width = Column(Integer, nullable=False)
    raw_height = Column(Integer, nullable=False)
    raw_channels = Column(Integer, nullable=False, default=3)
    raw_size_kb = Column(Float, nullable=False)
    processed_width = Column(Integer, default=256)
    processed_height = Column(Integer, default=256)
    processed_size_kb = Column(Float, nullable=False, default=0.0)
    md5_hash = Column(String(64), unique=True, nullable=False, index=True)
    phash = Column(String(64), nullable=True)  # Perceptual hash or dHash
    blur_score = Column(Float, default=0.0)
    is_blurry = Column(Boolean, default=False)
    original_path = Column(Text, nullable=False)
    processed_path = Column(Text, nullable=False)
    license = Column(String(100), default="Research/Educational")

    observations = relationship("DiseaseObservationFact", back_populates="image")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_key": self.image_key,
            "image_id": self.image_id,
            "raw_id": self.raw_id,
            "dataset_source": self.dataset_source,
            "filename": self.filename,
            "file_format": self.file_format,
            "raw_width": self.raw_width,
            "raw_height": self.raw_height,
            "raw_channels": self.raw_channels,
            "raw_size_kb": self.raw_size_kb,
            "processed_width": self.processed_width,
            "processed_height": self.processed_height,
            "processed_size_kb": self.processed_size_kb,
            "md5_hash": self.md5_hash,
            "blur_score": self.blur_score,
            "is_blurry": self.is_blurry,
            "original_path": self.original_path,
            "processed_path": self.processed_path,
            "license": self.license
        }


class DimVisualFeature(Base):
    """
    Visual Feature Dimension: Stores all 32 continuous visual descriptors
    (Color Moments, Excess Green Index, Haralick GLCM Textures, Morphometrics).
    """
    __tablename__ = "dim_visual_feature"

    feature_key = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String(50), unique=True, nullable=False, index=True)
    image_filename = Column(String(255), nullable=False, index=True)

    # 1. Color Moments & Chromaticity (18 Continuous Features)
    rgb_r_mean = Column(Float, nullable=False)
    rgb_g_mean = Column(Float, nullable=False)
    rgb_b_mean = Column(Float, nullable=False)
    rgb_r_std = Column(Float, nullable=False)
    rgb_g_std = Column(Float, nullable=False)
    rgb_b_std = Column(Float, nullable=False)
    rgb_r_norm = Column(Float, nullable=False)
    rgb_g_norm = Column(Float, nullable=False)
    rgb_b_norm = Column(Float, nullable=False)

    hsv_h_mean = Column(Float, nullable=False)
    hsv_s_mean = Column(Float, nullable=False)
    hsv_v_mean = Column(Float, nullable=False)
    hsv_h_std = Column(Float, nullable=False, default=0.0)
    hsv_s_std = Column(Float, nullable=False, default=0.0)
    hsv_v_std = Column(Float, nullable=False, default=0.0)
    hsv_h_norm = Column(Float, nullable=False)
    hsv_s_norm = Column(Float, nullable=False)
    hsv_v_norm = Column(Float, nullable=False)

    # 2. Foliar Vegetation Index (1 Continuous Feature)
    exg_index_mean = Column(Float, nullable=False)
    dominant_color_tone = Column(String(50), nullable=False, index=True)

    # 3. GLCM Haralick Textures (7 Continuous Features)
    glcm_contrast = Column(Float, nullable=False)
    glcm_contrast_norm = Column(Float, nullable=False, index=True)
    glcm_dissimilarity = Column(Float, nullable=False)
    glcm_homogeneity = Column(Float, nullable=False)
    glcm_energy = Column(Float, nullable=False)
    glcm_correlation = Column(Float, nullable=False)
    glcm_asm = Column(Float, nullable=False)

    # 4. Morphometrics & Lesion Coverage (6 Continuous Features)
    has_valid_contour = Column(Boolean, default=False)
    contour_area = Column(Float, default=0.0, nullable=False)
    contour_perimeter = Column(Float, default=0.0, nullable=False)
    contour_aspect_ratio = Column(Float, default=1.0, nullable=False)
    contour_circularity = Column(Float, default=0.0, nullable=False)
    contour_solidity = Column(Float, default=0.0, nullable=False)
    lesion_coverage_ratio = Column(Float, default=0.0, nullable=False)

    observations = relationship("DiseaseObservationFact", back_populates="feature")

    def to_feature_vector(self) -> Dict[str, float]:
        """Returns the canonical 32 continuous visual descriptors in model-input order."""
        return {
            "rgb_r_mean": self.rgb_r_mean,
            "rgb_g_mean": self.rgb_g_mean,
            "rgb_b_mean": self.rgb_b_mean,
            "rgb_r_std": self.rgb_r_std,
            "rgb_g_std": self.rgb_g_std,
            "rgb_b_std": self.rgb_b_std,
            "rgb_r_norm": self.rgb_r_norm,
            "rgb_g_norm": self.rgb_g_norm,
            "rgb_b_norm": self.rgb_b_norm,
            "hsv_h_mean": self.hsv_h_mean,
            "hsv_s_mean": self.hsv_s_mean,
            "hsv_v_mean": self.hsv_v_mean,
            "hsv_h_std": self.hsv_h_std,
            "hsv_s_std": self.hsv_s_std,
            "hsv_v_std": self.hsv_v_std,
            "hsv_h_norm": self.hsv_h_norm,
            "hsv_s_norm": self.hsv_s_norm,
            "hsv_v_norm": self.hsv_v_norm,
            "exg_index_mean": self.exg_index_mean,
            "glcm_contrast": self.glcm_contrast,
            "glcm_contrast_norm": self.glcm_contrast_norm,
            "glcm_dissimilarity": self.glcm_dissimilarity,
            "glcm_homogeneity": self.glcm_homogeneity,
            "glcm_energy": self.glcm_energy,
            "glcm_correlation": self.glcm_correlation,
            "glcm_asm": self.glcm_asm,
            "contour_area": self.contour_area,
            "contour_perimeter": self.contour_perimeter,
            "contour_aspect_ratio": self.contour_aspect_ratio,
            "contour_circularity": self.contour_circularity,
            "contour_solidity": self.contour_solidity,
            "lesion_coverage_ratio": self.lesion_coverage_ratio,
        }


class DiseaseObservationFact(Base):
    """
    Central Fact Table: DiseaseObservation_Fact
    Grain: Exactly ONE row per validated, preprocessed multimodal image observation.
    Links Crop, Disease, Image, and Visual Feature dimensions.
    """
    __tablename__ = "disease_observation_fact"

    observation_key = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String(50), unique=True, nullable=False, index=True)

    # Foreign Keys with Referential Integrity
    crop_key = Column(Integer, ForeignKey("dim_crop.crop_key"), nullable=False, index=True)
    disease_key = Column(Integer, ForeignKey("dim_disease.disease_key"), nullable=False, index=True)
    image_key = Column(Integer, ForeignKey("dim_image.image_key"), unique=True, nullable=False, index=True)
    feature_key = Column(Integer, ForeignKey("dim_visual_feature.feature_key"), unique=True, nullable=False, index=True)

    # Additive and Semi-Additive Measures
    observation_count = Column(Integer, default=1, nullable=False)
    lesion_severity_score = Column(Float, default=0.0, nullable=False)
    image_sharpness_score = Column(Float, default=0.0, nullable=False)
    lesion_coverage_ratio = Column(Float, default=0.0, nullable=False)
    texture_contrast_norm = Column(Float, default=0.0, nullable=False)
    processing_latency_ms = Column(Float, default=0.0, nullable=False)

    # Dimensional attributes denormalized for high-performance OLAP slicing
    dataset_source = Column(String(50), nullable=False, default="plantdoc", index=True)
    condition_status = Column(String(50), nullable=False, default="Diseased", index=True)
    is_pest = Column(Boolean, default=False, nullable=False)

    # Lineage Audit Attributes
    etl_batch_id = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ORM Relationships
    crop = relationship("DimCrop", back_populates="observations")
    disease = relationship("DimDisease", back_populates="observations")
    image = relationship("DimImage", back_populates="observations")
    feature = relationship("DimVisualFeature", back_populates="observations")


# Multi-Column Indices for OLAP Optimization
Index("idx_fact_crop_disease", DiseaseObservationFact.crop_key, DiseaseObservationFact.disease_key)
Index("idx_fact_crop_source", DiseaseObservationFact.crop_key, DiseaseObservationFact.dataset_source)
