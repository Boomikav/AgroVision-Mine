"""
ETL Load Step Module for AgroVision-Mine.
Loads:
1. Dimension tables first (DimCrop, DimDisease, DimImage, DimVisualFeature)
2. Central Fact table second (DiseaseObservationFact)
Enforces:
- Strict referential integrity (zero orphan foreign keys)
- Idempotency & duplicate prevention (safe repeated re-runs)
- ACID transaction safety (automatic rollback on exception)
- Lineage auditability (batch_id, timestamps)
- Detailed load statistics and error reporting
"""
import time
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from src.warehouse.connection import get_db_session
from src.warehouse.models import (
    DimCrop, DimDisease, DimImage, DimVisualFeature, DiseaseObservationFact
)
from src.utils.logger import setup_logger

logger = setup_logger("etl_load")


class Loader:
    """
    Handles relational dimension and fact loading with foreign key resolution
    and strict referential integrity across all 2,596 observations.
    """

    def __init__(self):
        pass

    def load_dimensions_and_facts(
        self,
        staged_data: Dict[str, Any],
        batch_id: str
    ) -> Dict[str, Any]:
        """
        Loads dimensions and facts transactionally with referential integrity.
        """
        start_time = time.perf_counter()
        session: Session = get_db_session()

        load_stats = {
            "batch_id": batch_id,
            "crops_inserted": 0,
            "crops_existing": 0,
            "crops_loaded": 0,
            "diseases_inserted": 0,
            "diseases_existing": 0,
            "diseases_loaded": 0,
            "images_inserted": 0,
            "images_existing": 0,
            "images_loaded": 0,
            "features_inserted": 0,
            "features_existing": 0,
            "features_loaded": 0,
            "facts_inserted": 0,
            "facts_loaded": 0,
            "facts_skipped_duplicate": 0,
            "orphan_foreign_keys": 0,
            "errors": [],
            "load_duration_ms": 0.0
        }

        try:
            # =================================================================
            # STEP 1: LOAD DIMENSION TABLES FIRST
            # =================================================================

            # 1.1 Load DimCrop
            crop_key_map: Dict[str, int] = {}
            for crop_data in staged_data.get("dim_crops", []):
                code = crop_data["crop_code"]
                existing = session.query(DimCrop).filter_by(crop_code=code).first()
                if not existing:
                    crop_obj = DimCrop(**crop_data)
                    session.add(crop_obj)
                    session.flush()
                    crop_key_map[code] = crop_obj.crop_key
                    load_stats["crops_inserted"] += 1
                else:
                    crop_key_map[code] = existing.crop_key
                    load_stats["crops_existing"] += 1

            # 1.2 Load DimDisease
            disease_key_map: Dict[str, int] = {}
            for dis_data in staged_data.get("dim_diseases", []):
                code = dis_data["disease_code"]
                existing = session.query(DimDisease).filter_by(disease_code=code).first()
                if not existing:
                    dis_obj = DimDisease(**dis_data)
                    session.add(dis_obj)
                    session.flush()
                    disease_key_map[code] = dis_obj.disease_key
                    load_stats["diseases_inserted"] += 1
                else:
                    disease_key_map[code] = existing.disease_key
                    load_stats["diseases_existing"] += 1

            # 1.3 Load DimImage
            image_key_map: Dict[str, int] = {}
            for img_data in staged_data.get("dim_images", []):
                image_id = img_data["image_id"]
                existing = session.query(DimImage).filter_by(image_id=image_id).first()
                if not existing:
                    img_obj = DimImage(**img_data)
                    session.add(img_obj)
                    session.flush()
                    image_key_map[image_id] = img_obj.image_key
                    load_stats["images_inserted"] += 1
                else:
                    image_key_map[image_id] = existing.image_key
                    load_stats["images_existing"] += 1

            # 1.4 Load DimVisualFeature
            feature_key_map: Dict[str, int] = {}
            for feat_data in staged_data.get("dim_features", []):
                image_id = feat_data["image_id"]
                existing = session.query(DimVisualFeature).filter_by(image_id=image_id).first()
                if not existing:
                    feat_obj = DimVisualFeature(**feat_data)
                    session.add(feat_obj)
                    session.flush()
                    feature_key_map[image_id] = feat_obj.feature_key
                    load_stats["features_inserted"] += 1
                else:
                    feature_key_map[image_id] = existing.feature_key
                    load_stats["features_existing"] += 1

            # =================================================================
            # STEP 2: LOAD CENTRAL FACT TABLE SECOND
            # =================================================================
            for f in staged_data.get("fact_records", []):
                image_id = f.get("image_id") or f.get("raw_id", "")

                crop_key = crop_key_map.get(f["crop_code"])
                disease_key = disease_key_map.get(f["disease_code"])
                image_key = image_key_map.get(image_id)
                feature_key = feature_key_map.get(image_id)

                # Strict referential integrity enforcement
                unresolved = []
                if not crop_key:
                    unresolved.append(f"crop_key ({f['crop_code']})")
                if not disease_key:
                    unresolved.append(f"disease_key ({f['disease_code']})")
                if not image_key:
                    unresolved.append(f"image_key ({image_id})")
                if not feature_key:
                    unresolved.append(f"feature_key ({image_id})")

                if unresolved:
                    err_msg = f"Orphan foreign key rejection for {image_id}: Missing {', '.join(unresolved)}"
                    logger.error(err_msg)
                    load_stats["errors"].append(err_msg)
                    load_stats["orphan_foreign_keys"] += 1
                    continue

                # Idempotency check: prevent duplicate fact records
                existing_fact = session.query(DiseaseObservationFact).filter_by(image_id=image_id).first()
                if existing_fact:
                    load_stats["facts_skipped_duplicate"] += 1
                    continue

                fact_obj = DiseaseObservationFact(
                    image_id=image_id,
                    crop_key=crop_key,
                    disease_key=disease_key,
                    image_key=image_key,
                    feature_key=feature_key,
                    observation_count=f.get("observation_count", 1),
                    lesion_severity_score=f.get("lesion_severity_score", 0.0),
                    image_sharpness_score=f.get("image_sharpness_score", 0.0),
                    lesion_coverage_ratio=f.get("lesion_coverage_ratio", 0.0),
                    texture_contrast_norm=f.get("texture_contrast_norm", 0.0),
                    processing_latency_ms=f.get("processing_latency_ms", 15.0),
                    dataset_source=f.get("dataset_source", "plantdoc"),
                    condition_status=f.get("condition_status", "Diseased"),
                    is_pest=f.get("is_pest", False),
                    etl_batch_id=batch_id
                )
                session.add(fact_obj)
                load_stats["facts_inserted"] += 1

            load_stats["facts_loaded"] = session.query(DiseaseObservationFact).count()
            load_stats["crops_loaded"] = session.query(DimCrop).count()
            load_stats["diseases_loaded"] = session.query(DimDisease).count()
            load_stats["images_loaded"] = session.query(DimImage).count()
            load_stats["features_loaded"] = session.query(DimVisualFeature).count()

            # Commit the atomic transaction
            session.commit()
            load_stats["load_duration_ms"] = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(
                f"ETL Load committed successfully for batch {batch_id} in {load_stats['load_duration_ms']}ms: "
                f"Facts Loaded={load_stats['facts_loaded']}, "
                f"Crops={load_stats['crops_loaded']}, "
                f"Diseases={load_stats['diseases_loaded']}, "
                f"Images={load_stats['images_loaded']}, "
                f"Features={load_stats['features_loaded']}."
            )

        except Exception as e:
            session.rollback()
            load_stats["load_duration_ms"] = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(f"ETL Load failed with transaction rollback: {e}")
            load_stats["errors"].append(str(e))
            raise
        finally:
            session.close()

        return load_stats
