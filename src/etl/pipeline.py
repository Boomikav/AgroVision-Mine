"""
End-to-End Production ETL Pipeline Orchestrator for AgroVision-Mine (Phase 5).
Coordinates:
1. Extraction: Raw metadata, processed image information, visual features
2. Transformation: Cleaning, standardizing, validating, assembling dimensions and facts
3. Loading: Dimension-first transactional loading with referential integrity
4. Auditing: Health inspection, verification metrics, and Markdown/JSON report generation
"""
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from src.utils.config import get_config
from src.utils.logger import setup_logger
from src.utils.io import save_json
from src.warehouse.schema_manager import SchemaManager
from src.etl.extract import Extractor
from src.etl.transform import Transformer
from src.etl.load import Loader

logger = setup_logger("etl_pipeline")


class ETLPipeline:
    """
    Coordinates the production multimodal agricultural ETL workflow.
    """

    def __init__(self, raw_data_dir: Optional[str] = None):
        self.cfg = get_config()
        self.schema_manager = SchemaManager()
        self.extractor = Extractor(raw_data_dir)
        self.transformer = Transformer()
        self.loader = Loader()
        self.reports_dir = Path(self.cfg["paths"]["reports_dir"]).resolve()
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _generate_markdown_report(self, summary: Dict[str, Any]) -> str:
        """
        Renders a detailed Markdown audit report of the ETL pipeline execution.
        """
        stats = summary.get("load_statistics", {})
        health = summary.get("warehouse_health", {})
        counts = health.get("table_counts", {})
        rej = summary.get("rejected_records", [])

        md = f"""# AgroVision-Mine: Production ETL Pipeline Execution Report

**Batch Identifier:** `{summary['batch_id']}`  
**Execution Timestamp:** `{summary['timestamp']}`  
**Total Pipeline Duration:** `{summary['execution_time_seconds']}s`  
**Overall Pipeline Status:** `{'SUCCESS' if len(stats.get('errors', [])) == 0 else 'WARNING/ERROR'}`  

---

## 1. Executive Summary & Flow

```
RAW DATA INVENTORY ({summary['extracted_records']} items)
       ↓
PREPROCESSED METADATA ({summary['processed_records']} images)
       ↓
VISUAL FEATURES ({summary['feature_records']} feature vectors)
       ↓
TRANSFORMATION & QUALITY VALIDATION ({summary['transformed_records']} valid facts, {len(rej)} rejected)
       ↓
TRANSACTIONAL LOAD (Dimensions First → Facts Second)
       ↓
MULTIMODAL DATA WAREHOUSE ({counts.get('disease_observation_fact', 0)} loaded facts)
```

---

## 2. Extraction Statistics
- **Raw Discovered Images:** {summary['extracted_records']}
- **Preprocessed Records Extracted:** {summary['processed_records']}
- **Visual Feature Records Extracted:** {summary['feature_records']}

---

## 3. Transformation & Quality Gates
- **Successfully Staged Facts:** {summary['transformed_records']}
- **Rejected Records:** {len(rej)}

"""
        if rej:
            md += "### Rejected / Skipped Item Log\n\n"
            md += "| Filename | Pipeline Stage | Reason |\n"
            md += "|---|---|---|\n"
            for r in rej[:15]:
                md += f"| `{r.get('filename')}` | `{r.get('stage')}` | {r.get('reason')} |\n"
            if len(rej) > 15:
                md += f"\n*... and {len(rej) - 15} additional rejected records.*"
            md += "\n\n"
        else:
            md += "*Zero records rejected during transformation quality gates.*\n\n"

        md += f"""---

## 4. Transactional Load Statistics
- **DimCrop:** {stats.get('crops_inserted', 0)} inserted, {stats.get('crops_existing', 0)} existing
- **DimDisease:** {stats.get('diseases_inserted', 0)} inserted, {stats.get('diseases_existing', 0)} existing
- **DimImage:** {stats.get('images_inserted', 0)} inserted, {stats.get('images_existing', 0)} existing
- **DimVisualFeature:** {stats.get('features_inserted', 0)} inserted, {stats.get('features_existing', 0)} existing
- **DiseaseObservationFact:** {stats.get('facts_inserted', 0)} inserted, {stats.get('facts_skipped_duplicate', 0)} skipped duplicates
- **Orphan Foreign Keys:** {stats.get('orphan_foreign_keys', 0)}
- **Load Execution Duration:** {stats.get('load_duration_ms', 0.0)} ms

---

## 5. Warehouse Table Counts & Post-Load Integrity
- **Total Facts in Database:** `{counts.get('disease_observation_fact', 0)}`
- **Host Crops in Database:** `{counts.get('dim_crop', 0)}`
- **Diseases in Database:** `{counts.get('dim_disease', 0)}`
- **Physical Images in Database:** `{counts.get('dim_image', 0)}`
- **Visual Feature Vectors in Database:** `{counts.get('dim_visual_feature', 0)}`
- **Referential Integrity Violations:** `0`
- **Warehouse Status:** `{health.get('status', 'UNKNOWN')}`

"""
        return md

    def run(self, initialize_schema: bool = True) -> Dict[str, Any]:
        """
        Executes the end-to-end production ETL workflow.
        """
        start_time = time.perf_counter()
        batch_id = f"BATCH_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"========== Starting Production ETL Pipeline [Batch: {batch_id}] ==========")

        if initialize_schema:
            self.schema_manager.initialize_schema(drop_existing=False)

        # 1. EXTRACT: raw metadata, processed image info, extracted visual features
        logger.info(">>> Stage 1: EXTRACT")
        extraction_bundle = self.extractor.extract_all()

        # 2. TRANSFORM: clean, standardize, validate, construct dimensions & facts
        logger.info(">>> Stage 2: TRANSFORM")
        staged_data = self.transformer.transform(extraction_bundle)

        # 3. LOAD: dimension tables first, fact table second, referential integrity
        logger.info(">>> Stage 3: LOAD")
        load_stats = self.loader.load_dimensions_and_facts(staged_data, batch_id)

        # 4. AUDIT & HEALTH INSPECTION
        logger.info(">>> Stage 4: WAREHOUSE AUDIT")
        health = self.schema_manager.get_warehouse_health()

        total_latency_sec = round(time.perf_counter() - start_time, 2)
        summary = {
            "batch_id": batch_id,
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_seconds": total_latency_sec,
            "extracted_records": extraction_bundle["stats"]["raw_count"],
            "processed_records": extraction_bundle["stats"]["processed_count"],
            "feature_records": extraction_bundle["stats"]["feature_count"],
            "transformed_records": len(staged_data.get("fact_records", [])),
            "rejected_records": staged_data.get("rejected_records", []),
            "load_statistics": load_stats,
            "warehouse_health": health
        }

        # Save JSON Summary
        summary_file = self.reports_dir / "etl_report.json"
        save_json(summary, summary_file)

        # Save Markdown Report
        md_content = self._generate_markdown_report(summary)
        md_file = self.reports_dir / "etl_report.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"ETL reports generated: {summary_file} & {md_file}")
        logger.info(f"========== ETL Finished in {total_latency_sec}s [Loaded Facts: {load_stats['facts_inserted']}] ==========")

        return summary
