"""
Master CLI Entrypoint for AgroVision-Mine.
Coordinates pipeline execution, database operations, OLAP queries, and testing.
"""
import argparse
import sys
import subprocess
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.utils.config import get_config, ensure_directories
from src.utils.logger import setup_logger
from src.ingestion.dataset_loader import DatasetInspector
from src.warehouse.schema_manager import SchemaManager
from src.etl.pipeline import ETLPipeline
from src.olap.engine import OLAPEngine
from scripts.seed_benchmark_data import seed_benchmark_dataset

logger = setup_logger("run_master")


def parse_args():
    parser = argparse.ArgumentParser(
        description="AgroVision-Mine: Multimodal Data Warehouse and Pattern Mining System"
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=[
            "seed", "extract", "preprocess", "features",
            "init-db", "etl", "olap", "dashboard", "api", "test", "all"
        ],
        help="Pipeline stage to execute (default: all)"
    )
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop and recreate database tables during schema initialization"
    )
    parser.add_argument(
        "--dashboard-port",
        type=int,
        default=8501,
        help="Port for Streamlit dashboard"
    )
    parser.add_argument(
        "--api-port",
        type=int,
        default=8000,
        help="Port for FastAPI backend adapter"
    )
    return parser.parse_args()


def stage_seed():
    logger.info(">>> Stage: SEED BENCHMARK DATASET")
    seed_benchmark_dataset(force=False)


from src.preprocessing.preprocessor import ImagePreprocessor

def stage_extract():
    logger.info(">>> Stage: EXTRACT & DATASET INSPECTION")
    inspector = DatasetInspector()
    report = inspector.generate_inventory_report()
    logger.info(f"Discovered: {report['total_images_discovered']} images across {len(report['unique_crops_discovered'])} crops.")
    logger.info(f"Crop distribution: {report['crop_distribution']}")
    return report


def stage_preprocess():
    logger.info(">>> Stage: IMAGE PREPROCESSING & QUALITY GATES")
    inspector = DatasetInspector()
    inventory = inspector.scan_raw_directory()
    preprocessor = ImagePreprocessor()
    report = preprocessor.run_pipeline(inventory)
    stats = report["statistics"]
    reasons = report["failure_reasons"]
    logger.info(f"Preprocessing completed: {stats['processed_images']}/{stats['total_discovered']} standardized.")
    logger.info(f"Duplicates: {stats['duplicate_images']}, Corrupted/Invalid: {stats['invalid_images']}, Skipped: {stats['skipped_images']}")
    return report


def stage_features():
    logger.info(">>> Stage: VISUAL FEATURE EXTRACTION")
    from src.feature_extraction.pipeline import FeatureExtractionPipeline
    pipeline = FeatureExtractionPipeline()
    feature_rows = pipeline.run_batch_from_metadata()
    logger.info(f"Visual feature extraction completed: {len(feature_rows)} records extracted.")
    return feature_rows


def stage_init_db(drop_existing: bool = False):
    logger.info(f">>> Stage: INITIALIZE STAR SCHEMA DATABASE (drop_existing={drop_existing})")
    schema_mgr = SchemaManager()
    schema_mgr.initialize_schema(drop_existing=drop_existing)
    health = schema_mgr.get_warehouse_health()
    logger.info(f"Warehouse status: {health['status']}, Tables: {health['existing_tables']}")
    return health


def stage_etl(drop_existing: bool = False):
    logger.info(">>> Stage: END-TO-END ETL PIPELINE")
    etl = ETLPipeline()
    summary = etl.run(initialize_schema=True)
    logger.info(f"ETL completed in {summary['execution_time_seconds']}s")
    logger.info(f"Loaded Facts: {summary['load_statistics']['facts_loaded']}")
    return summary


def stage_olap():
    logger.info(">>> Stage: OLAP ANALYTICS ENGINE")
    engine = OLAPEngine()

    print("\n" + "=" * 80)
    print("1. OLAP OPERATION: ROLL-UP (Crop -> Crop Category)")
    print("=" * 80)
    res_rollup = engine.rollup()
    print("SQL Query:\n", res_rollup["sql"])
    print("\nResult Table:")
    print(res_rollup["data"].to_string(index=False))

    print("\n" + "=" * 80)
    print("2. OLAP OPERATION: DRILL-DOWN (Category -> Crop -> Disease -> Visual Tone)")
    print("=" * 80)
    res_drill = engine.drilldown()
    print("SQL Query:\n", res_drill["sql"])
    print("\nResult Table (Top 10 rows):")
    print(res_drill["data"].head(10).to_string(index=False))

    print("\n" + "=" * 80)
    print("3. OLAP OPERATION: SLICE (Crop = 'Rice')")
    print("=" * 80)
    res_slice = engine.slice_by_crop("Rice")
    print("SQL Query:\n", res_slice["sql"])
    print("\nResult Table:")
    print(res_slice["data"].to_string(index=False))

    print("\n" + "=" * 80)
    print("4. OLAP OPERATION: DICE (Crops in Rice, Wheat AND Pathogen in Fungal, Bacterial)")
    print("=" * 80)
    res_dice = engine.dice(
        selected_crops=["Rice", "Wheat"],
        selected_pathogens=["Fungal", "Bacterial"],
        min_contrast=0.0
    )
    print("SQL Query:\n", res_dice["sql"])
    print("\nResult Table:")
    print(res_dice["data"].to_string(index=False))

    print("\n" + "=" * 80)
    print("5. OLAP OPERATION: PIVOT (Rows: Crop x Columns: Pathogen Type)")
    print("=" * 80)
    res_pivot = engine.pivot(measure="observation_count")
    print("SQL Query:\n", res_pivot["sql"])
    print("\nResult Table:")
    print(res_pivot["data"].to_string(index=False))
    print("=" * 80 + "\n")


def stage_test():
    logger.info(">>> Stage: RUN UNIT & INTEGRATION TESTS")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"], check=False)
    if result.returncode != 0:
        logger.error(f"Tests failed with exit code: {result.returncode}")
        sys.exit(result.returncode)
    logger.info("All tests passed successfully.")


def stage_dashboard(port: int = 8501):
    logger.info(f">>> Stage: LAUNCH STREAMLIT DASHBOARD ON PORT {port}")
    dashboard_file = Path(__file__).resolve().parent / "dashboard" / "app.py"
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(dashboard_file),
        f"--server.port={port}",
        "--server.headless=true"
    ])


def stage_api(port: int = 8000, host: str = "127.0.0.1"):
    logger.info(f">>> Stage: LAUNCH FASTAPI BACKEND ADAPTER ON http://{host}:{port}")
    import uvicorn
    uvicorn.run("src.api.app:app", host=host, port=port, reload=False)


def main():
    args = parse_args()
    cfg = get_config()
    ensure_directories(cfg)

    stage = args.stage
    if stage == "seed":
        stage_seed()
    elif stage == "extract":
        stage_extract()
    elif stage == "preprocess":
        stage_preprocess()
    elif stage == "features":
        stage_features()
    elif stage == "init-db":
        stage_init_db(args.drop_existing)
    elif stage == "etl":
        stage_etl(args.drop_existing)
    elif stage == "olap":
        stage_olap()
    elif stage == "test":
        stage_test()
    elif stage == "dashboard":
        stage_dashboard(args.dashboard_port)
    elif stage == "api":
        stage_api(args.api_port)
    elif stage == "all":
        stage_seed()
        stage_extract()
        stage_init_db(args.drop_existing)
        stage_etl(args.drop_existing)
        stage_olap()
        logger.info("All Review 1 pipeline stages executed successfully.")


if __name__ == "__main__":
    main()
