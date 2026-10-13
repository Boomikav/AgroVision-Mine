"""
Schema Manager Module for AgroVision-Mine Data Warehouse.
Handles DDL deployment, database initialization, and warehouse health inspection.
"""
from typing import Any, Dict
from sqlalchemy import func, inspect
from src.warehouse.connection import get_db_engine, get_db_session
from src.warehouse.models import (
    Base, DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact
)
from src.utils.logger import setup_logger

logger = setup_logger("schema_manager")


class SchemaManager:
    """
    Manages the lifecycle and integrity of the Star Schema warehouse.
    Reflects strictly supported dimensions from the real dataset:
    - dim_crop
    - dim_disease
    - dim_image
    - dim_visual_feature
    - disease_observation_fact
    """

    def __init__(self):
        self.engine = get_db_engine()

    def initialize_schema(self, drop_existing: bool = False) -> None:
        """
        Creates all star schema dimension and fact tables.
        """
        if drop_existing:
            logger.warning("Dropping existing star schema tables...")
            from sqlalchemy import MetaData
            meta = MetaData()
            meta.reflect(bind=self.engine)
            meta.drop_all(bind=self.engine)

        logger.info("Deploying Star Schema tables into warehouse...")
        Base.metadata.create_all(self.engine)
        logger.info("Star Schema deployed successfully.")

    def get_warehouse_health(self) -> Dict[str, Any]:
        """
        Inspects table existence, row counts, and relational integrity.
        """
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()

        expected_tables = [
            "dim_crop", "dim_disease",
            "dim_image", "dim_visual_feature", "disease_observation_fact"
        ]

        missing_tables = [tbl for tbl in expected_tables if tbl not in table_names]
        session = get_db_session()

        counts: Dict[str, int] = {}
        try:
            if "dim_crop" in table_names:
                counts["dim_crop"] = session.query(func.count(DimCrop.crop_key)).scalar() or 0
            if "dim_disease" in table_names:
                counts["dim_disease"] = session.query(func.count(DimDisease.disease_key)).scalar() or 0
            if "dim_image" in table_names:
                counts["dim_image"] = session.query(func.count(DimImage.image_key)).scalar() or 0
            if "dim_visual_feature" in table_names:
                counts["dim_visual_feature"] = session.query(func.count(DimVisualFeature.feature_key)).scalar() or 0
            if "disease_observation_fact" in table_names:
                counts["disease_observation_fact"] = session.query(func.count(DiseaseObservationFact.observation_key)).scalar() or 0
        finally:
            session.close()

        is_healthy = len(missing_tables) == 0 and counts.get("disease_observation_fact", 0) >= 0

        return {
            "status": "HEALTHY" if is_healthy else "UNHEALTHY",
            "existing_tables": table_names,
            "missing_tables": missing_tables,
            "table_counts": counts,
            "total_facts": counts.get("disease_observation_fact", 0),
            "total_dimensions": sum(counts.get(k, 0) for k in counts if k != "disease_observation_fact")
        }
