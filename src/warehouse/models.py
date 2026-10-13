"""
Star Schema Relational Models for AgroVision-Mine Multimodal Data Warehouse (Phase 4).
Reflects strictly supported ground-truth dimensions derived from the actual dataset:
- Dim_Crop
- Dim_Disease
- Dim_Image
- Dim_VisualFeature
- Central Fact: DiseaseObservation_Fact
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
    crop_category = Column(String(50), nullable=False, index=True)  # Cereal, Fiber, Horticultural
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
    pathogen_type = Column(String(50), nullable=False, index=True)  # Bacterial, Fungal, Viral, None
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
    Image Dimension: Tracks physical/optical parameters, dimensions, and cryptographic lineage.
    """
    __tablename__ = "dim_image"

    image_key = Column(Integer, primary_key=True, autoincrement=True)
    raw_id = Column(String(50), unique=True, nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_format = Column(String(20), nullable=False)
    raw_width = Column(Integer, nullable=False)
    raw_height = Column(Integer, nullable=False)
    raw_channels = Column(Integer, nullable=False, default=3)
    raw_size_kb = Column(Float, nullable=False)
    processed_width = Column(Integer, default=256)
    processed_height = Column(Integer, default=256)
    processed_size_kb = Column(Float, nullable=False)
    md5_hash = Column(String(64), unique=True, nullable=False, index=True)
    phash = Column(String(32), nullable=True)
    blur_score = Column(Float, default=0.0)
    is_blurry = Column(Boolean, default=False)
    original_path = Column(Text, nullable=False)
    processed_path = Column(Text, nullable=False)

    observations = relationship("DiseaseObservationFact", back_populates="image")


class DimVisualFeature(Base):
    """
    Visual Feature Dimension: Stores extracted explainable color, GLCM, and shape descriptors.
    """
    __tablename__ = "dim_visual_feature"

    feature_key = Column(Integer, primary_key=True, autoincrement=True)
    image_filename = Column(String(255), unique=True, nullable=False, index=True)

    # Color Moments & Normalizations
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
    hsv_h_norm = Column(Float, nullable=False)
    hsv_s_norm = Column(Float, nullable=False)
    hsv_v_norm = Column(Float, nullable=False)
    exg_index_mean = Column(Float, nullable=False)
    dominant_color_tone = Column(String(50), nullable=False, index=True)

    # GLCM Haralick Textures
    glcm_contrast = Column(Float, nullable=False)
    glcm_contrast_norm = Column(Float, nullable=False, index=True)
    glcm_dissimilarity = Column(Float, nullable=False)
    glcm_homogeneity = Column(Float, nullable=False)
    glcm_energy = Column(Float, nullable=False)
    glcm_correlation = Column(Float, nullable=False)
    glcm_asm = Column(Float, nullable=False)

    # Morphometric Shape Descriptors
    has_valid_contour = Column(Boolean, default=False)
    contour_area = Column(Float, default=0.0)
    contour_perimeter = Column(Float, default=0.0)
    contour_aspect_ratio = Column(Float, default=1.0)
    contour_circularity = Column(Float, default=0.0)
    contour_solidity = Column(Float, default=0.0)
    lesion_coverage_ratio = Column(Float, default=0.0)

    observations = relationship("DiseaseObservationFact", back_populates="feature")


class DiseaseObservationFact(Base):
    """
    Central Fact Table: DiseaseObservation_Fact
    Grain: Exactly ONE row per validated, preprocessed multimodal image observation.
    Links Crop, Disease, Image, and Visual Feature dimensions.
    """
    __tablename__ = "disease_observation_fact"

    observation_key = Column(Integer, primary_key=True, autoincrement=True)

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
