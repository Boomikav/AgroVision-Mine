"""
Ground-Truth Dimension Seed Script for AgroVision-Mine Data Warehouse (Phase 4).
Populates reference dimensions based strictly on the ICAR/agricultural research dataset:
- Dim_Crop (Rice)
- Dim_Disease (Bacterial Leaf Blight, Brown Spot, Leaf Smut, Healthy baseline)
Idempotent execution: ensures unique constraint integrity and prevents duplicate keys.
"""
from typing import Dict, List
from src.warehouse.connection import get_db_session
from src.warehouse.models import DimCrop, DimDisease
from src.utils.logger import setup_logger

logger = setup_logger("seed_dimensions")

# Reference seed data derived strictly from ground-truth agronomic taxonomy
CROP_SEEDS: List[Dict[str, str]] = [
    {
        "crop_code": "RICE",
        "crop_name": "Rice",
        "botanical_name": "Oryza sativa",
        "crop_category": "Cereal",
        "economic_significance": "Primary Food Grain / Commercial Staple"
    }
]

DISEASE_SEEDS: List[Dict[str, str]] = [
    {
        "disease_code": "BACTERIAL_BLIGHT",
        "disease_name": "Bacterial Leaf Blight",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas oryzae pv. oryzae",
        "primary_symptom": "Water-soaked stripes turning yellowish-white along leaf margins"
    },
    {
        "disease_code": "BROWN_SPOT",
        "disease_name": "Brown Spot",
        "pathogen_type": "Fungal",
        "causal_agent": "Bipolaris oryzae",
        "primary_symptom": "Oval to circular dark brown foliar lesions with yellow halo"
    },
    {
        "disease_code": "LEAF_SMUT",
        "disease_name": "Leaf Smut",
        "pathogen_type": "Fungal",
        "causal_agent": "Entyloma oryzae",
        "primary_symptom": "Small, angular black soral spots or linear stripes on leaf blade"
    },
    {
        "disease_code": "HEALTHY",
        "disease_name": "Healthy Foliage",
        "pathogen_type": "None",
        "causal_agent": "None",
        "primary_symptom": "Uniform green foliar tissue without macroscopic lesions"
    }
]


def seed_reference_dimensions() -> Dict[str, int]:
    """
    Seeds reference dimensions into the warehouse idempotently.
    Returns count of newly inserted records.
    """
    session = get_db_session()
    stats = {"crops_seeded": 0, "diseases_seeded": 0}

    try:
        # 1. Seed DimCrop
        for c in CROP_SEEDS:
            existing = session.query(DimCrop).filter_by(crop_code=c["crop_code"]).first()
            if not existing:
                crop_obj = DimCrop(**c)
                session.add(crop_obj)
                stats["crops_seeded"] += 1
                logger.info(f"Seeded DimCrop: {c['crop_code']} ({c['crop_name']})")

        # 2. Seed DimDisease
        for d in DISEASE_SEEDS:
            existing = session.query(DimDisease).filter_by(disease_code=d["disease_code"]).first()
            if not existing:
                dis_obj = DimDisease(**d)
                session.add(dis_obj)
                stats["diseases_seeded"] += 1
                logger.info(f"Seeded DimDisease: {d['disease_code']} ({d['disease_name']})")

        session.commit()
        logger.info(
            f"Reference dimension seeding complete: "
            f"{stats['crops_seeded']} crops, {stats['diseases_seeded']} diseases added."
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Error seeding reference dimensions: {e}")
        raise
    finally:
        session.close()

    return stats


if __name__ == "__main__":
    from src.warehouse.schema_manager import SchemaManager
    schema_mgr = SchemaManager()
    schema_mgr.initialize_schema(drop_existing=False)
    results = seed_reference_dimensions()
    print(f"Dimension Seeding Results: {results}")
