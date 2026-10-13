"""
SQL-Backed OLAP Analytics Engine for AgroVision-Mine Multimodal Data Warehouse.
Implements the core analytical operations:
1. Roll-up
2. Drill-down
3. Slice
4. Dice
5. Pivot
All operations execute real SQL queries against the star schema and return
both raw queries and structured results for academic auditability.
"""
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.warehouse.connection import get_db_engine
from src.utils.logger import setup_logger

logger = setup_logger("olap_engine")


class OLAPEngine:
    """
    Executes dimensional OLAP operations directly against the Star Schema database.
    """

    def __init__(self, engine: Optional[Engine] = None):
        self.engine = engine or get_db_engine()

    def _execute_sql(self, sql_query: str, params: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, float]:
        """
        Executes SQL query using SQLAlchemy and returns a pandas DataFrame with execution latency.
        """
        start_time = time.perf_counter()
        with self.engine.connect() as conn:
            if params:
                result_df = pd.read_sql_query(text(sql_query), conn, params=params)
            else:
                result_df = pd.read_sql_query(text(sql_query), conn)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return result_df, latency_ms

    def rollup(self) -> Dict[str, Any]:
        """
        1. ROLL-UP OPERATION:
        Navigates up the agronomic hierarchy from specific observations/diseases
        to high-level Crop Categories.
        Aggregates measures (total observations, avg severity, avg texture contrast, avg greenness).
        """
        query = """
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
        """
        df, latency = self._execute_sql(query)
        return {
            "operation": "ROLL-UP",
            "hierarchy": "Observation -> Crop -> Crop Category",
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }

    def true_drilldown(self, pathogen_type: Optional[str] = None) -> Dict[str, Any]:
        """
        2A. TRUE OLAP DRILL-DOWN OPERATION (Single-Dimension Hierarchy):
        Navigates down the strict dimension hierarchy within dim_disease:
        Level 1: Pathogen Type (e.g., Fungal, Bacterial)
           ↓
        Level 2: Disease Name (e.g., Brown Spot, Leaf Smut, Bacterial Blight)
        Provides genuine single-dimension drill-down moving from coarse pathology class
        to granular disease diagnosis.
        """
        params = {}
        where_clause = ""
        if pathogen_type and pathogen_type != "All":
            where_clause = "WHERE LOWER(d.pathogen_type) = LOWER(:pathogen_type)"
            params["pathogen_type"] = pathogen_type

        query = f"""
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
        {where_clause}
        GROUP BY d.pathogen_type, d.disease_name, d.causal_agent
        ORDER BY d.pathogen_type, total_observations DESC;
        """
        df, latency = self._execute_sql(query, params)
        return {
            "operation": "TRUE OLAP DRILL-DOWN",
            "hierarchy": "dim_disease: Pathogen Type -> Disease Name",
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }

    def diagnostic_drilldown(self, crop_category: Optional[str] = None) -> Dict[str, Any]:
        """
        2B. DIAGNOSTIC MULTI-DIMENSIONAL BREAKDOWN (Drill-Across):
        Navigates across multiple dimension boundaries:
        Crop Category (dim_crop) -> Crop Name (dim_crop) -> Disease (dim_disease) -> Dominant Visual Tone (dim_visual_feature).
        Provides fine-grained diagnostic visibility into visual symptoms and texture metrics.
        Academically characterized as a multi-attribute diagnostic breakdown rather than a single-dimension hierarchy.
        """
        params = {}
        where_clause = ""
        if crop_category and crop_category != "All":
            where_clause = "WHERE c.crop_category = :category"
            params["category"] = crop_category

        query = f"""
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
        {where_clause}
        GROUP BY c.crop_category, c.crop_name, d.disease_name, d.pathogen_type, vf.dominant_color_tone
        ORDER BY c.crop_name, observation_count DESC;
        """
        df, latency = self._execute_sql(query, params)
        return {
            "operation": "DRILL-DOWN",
            "operation_type": "DIAGNOSTIC DRILL-ACROSS",
            "hierarchy": "Multi-Dimensional: Crop Category -> Crop Name -> Disease -> Dominant Visual Tone",
            "academic_classification": "Multi-Dimensional Diagnostic Breakdown (Drill-Across)",
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }

    def drilldown(self, crop_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Backward-compatible alias for diagnostic drill-across breakdown.
        """
        return self.diagnostic_drilldown(crop_category=crop_category)



    def slice_by_crop(self, crop_name: str) -> Dict[str, Any]:
        """
        3. SLICE OPERATION:
        Selects a 2D slice of the data warehouse hypercube where Dimension 'Crop' = crop_name.
        """
        query = """
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
        """
        df, latency = self._execute_sql(query, {"crop_name": crop_name})
        return {
            "operation": "SLICE",
            "sliced_dimension": f"Crop = '{crop_name}'",
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }

    def slice_by_pathogen(self, pathogen_type: str) -> Dict[str, Any]:
        """
        SLICE OPERATION alternative:
        Slices by Pathogen Type (e.g. Fungal, Bacterial, Viral).
        """
        query = """
        SELECT
            c.crop_name,
            c.crop_category,
            d.disease_name,
            COUNT(f.observation_key) AS observations,
            ROUND(AVG(f.lesion_severity_score), 2) AS avg_severity,
            ROUND(AVG(vf.glcm_contrast), 4) AS avg_contrast
        FROM disease_observation_fact f
        JOIN dim_crop c ON f.crop_key = c.crop_key
        JOIN dim_disease d ON f.disease_key = d.disease_key
        JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
        WHERE LOWER(d.pathogen_type) = LOWER(:pathogen_type)
        GROUP BY c.crop_name, c.crop_category, d.disease_name
        ORDER BY observations DESC;
        """
        df, latency = self._execute_sql(query, {"pathogen_type": pathogen_type})
        return {
            "operation": "SLICE",
            "sliced_dimension": f"Pathogen_Type = '{pathogen_type}'",
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }

    def dice(
        self,
        selected_crops: List[str],
        selected_pathogens: List[str],
        min_contrast: float = 0.0
    ) -> Dict[str, Any]:
        """
        4. DICE OPERATION:
        Defines a sub-cube by filtering across multiple dimensions simultaneously:
        - Crop Dimension: Crop in selected_crops
        - Disease Dimension: Pathogen Type in selected_pathogens
        - Feature Dimension: GLCM Texture Contrast >= min_contrast
        """
        # Build dynamic IN clauses safely
        crop_placeholders = ", ".join([f":c_{i}" for i in range(len(selected_crops))])
        path_placeholders = ", ".join([f":p_{i}" for i in range(len(selected_pathogens))])

        params: Dict[str, Any] = {"min_contrast": min_contrast}
        for i, crop in enumerate(selected_crops):
            params[f"c_{i}"] = crop.lower()
        for i, path in enumerate(selected_pathogens):
            params[f"p_{i}"] = path.lower()

        query = f"""
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
        WHERE LOWER(c.crop_name) IN ({crop_placeholders})
          AND LOWER(d.pathogen_type) IN ({path_placeholders})
          AND vf.glcm_contrast >= :min_contrast
        GROUP BY c.crop_category, c.crop_name, d.disease_name, d.pathogen_type, vf.dominant_color_tone
        ORDER BY c.crop_name, avg_severity DESC;
        """
        df, latency = self._execute_sql(query, params)
        return {
            "operation": "DICE",
            "diced_dimensions": {
                "crops": selected_crops,
                "pathogens": selected_pathogens,
                "min_contrast": min_contrast
            },
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }

    def pivot(self, measure: str = "observation_count") -> Dict[str, Any]:
        """
        5. PIVOT OPERATION:
        Cross-tabulates rows and columns.
        Rows: Crop Name
        Columns: Pathogen Type (Fungal, Bacterial, Viral, None)
        Cell: Sum of observation counts or Average Texture Contrast.
        Constructed using ANSI SQL conditional aggregation (CASE WHEN).
        """
        if measure == "avg_contrast":
            agg_fungal = "ROUND(AVG(CASE WHEN d.pathogen_type = 'Fungal' THEN vf.glcm_contrast END), 4)"
            agg_bacterial = "ROUND(AVG(CASE WHEN d.pathogen_type = 'Bacterial' THEN vf.glcm_contrast END), 4)"
            agg_viral = "ROUND(AVG(CASE WHEN d.pathogen_type = 'Viral' THEN vf.glcm_contrast END), 4)"
            agg_none = "ROUND(AVG(CASE WHEN d.pathogen_type = 'None' THEN vf.glcm_contrast END), 4)"
            total_measure = "ROUND(AVG(vf.glcm_contrast), 4)"
        else:
            agg_fungal = "SUM(CASE WHEN d.pathogen_type = 'Fungal' THEN 1 ELSE 0 END)"
            agg_bacterial = "SUM(CASE WHEN d.pathogen_type = 'Bacterial' THEN 1 ELSE 0 END)"
            agg_viral = "SUM(CASE WHEN d.pathogen_type = 'Viral' THEN 1 ELSE 0 END)"
            agg_none = "SUM(CASE WHEN d.pathogen_type = 'None' THEN 1 ELSE 0 END)"
            total_measure = "COUNT(f.observation_key)"

        query = f"""
        SELECT
            c.crop_name AS "Crop",
            c.crop_category AS "Category",
            {agg_fungal} AS "Fungal",
            {agg_bacterial} AS "Bacterial",
            {agg_viral} AS "Viral",
            {agg_none} AS "Healthy_or_None",
            {total_measure} AS "Overall_Metric"
        FROM disease_observation_fact f
        JOIN dim_crop c ON f.crop_key = c.crop_key
        JOIN dim_disease d ON f.disease_key = d.disease_key
        JOIN dim_visual_feature vf ON f.feature_key = vf.feature_key
        GROUP BY c.crop_name, c.crop_category
        ORDER BY "Overall_Metric" DESC;
        """
        df, latency = self._execute_sql(query)
        # Fill nulls resulting from empty categories with 0.0
        df = df.fillna(0.0)
        return {
            "operation": "PIVOT",
            "pivoted_dimensions": "Rows: Crop Name x Columns: Pathogen Type",
            "measure": measure,
            "sql": query.strip(),
            "data": df,
            "row_count": len(df),
            "latency_ms": latency
        }
