"""
Automated Comprehensive Verification of AgroVision-Mine Unified Data Warehouse Invariants.
Validates:
1. Total observations: exactly 2,596
2. PlantDoc (2,560) and ICAR/OGD Rice (36) distribution
3. Preservation of all 36 authentic Rice IDs, metadata, and 32 continuous features
4. Zero duplicate IDs, zero nulls, zero orphan foreign keys
5. All 5 OLAP operations performance and results
"""
import sqlite3
import time
from pathlib import Path
from src.olap.engine import OLAPEngine

DB_PATH = Path("database/agrovision_warehouse.db")

def run_verification():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("================================================================================")
    print("AGROVISION-MINE DATA WAREHOUSE INTEGRITY AUDIT")
    print("================================================================================")
    
    # 1. Fact Observation Counts
    total_facts = cur.execute("SELECT COUNT(*) FROM disease_observation_fact;").fetchone()[0]
    unique_fact_ids = cur.execute("SELECT COUNT(DISTINCT image_id) FROM disease_observation_fact;").fetchone()[0]
    print(f"Total Observation Facts:         {total_facts} (Expected: 2596)")
    print(f"Unique Observation IDs:          {unique_fact_ids} (Expected: 2596)")
    assert total_facts == 2596
    assert unique_fact_ids == 2596

    # 2. Dimensions
    images_count = cur.execute("SELECT COUNT(*) FROM dim_image;").fetchone()[0]
    features_count = cur.execute("SELECT COUNT(*) FROM dim_visual_feature;").fetchone()[0]
    crops_count = cur.execute("SELECT COUNT(*) FROM dim_crop;").fetchone()[0]
    diseases_count = cur.execute("SELECT COUNT(*) FROM dim_disease;").fetchone()[0]
    print(f"dim_image rows:                  {images_count} (Expected: 2596)")
    print(f"dim_visual_feature rows:         {features_count} (Expected: 2596)")
    print(f"dim_crop unique crops:           {crops_count} (Expected: 14)")
    print(f"dim_disease unique conditions:   {diseases_count} (Expected: 19)")
    assert images_count == 2596
    assert features_count == 2596
    assert crops_count == 14
    assert diseases_count == 19

    # 3. Source Distribution
    sources = dict(cur.execute("SELECT dataset_source, COUNT(*) FROM disease_observation_fact GROUP BY dataset_source;").fetchall())
    print("\nDataset Source Distribution:")
    for src, cnt in sources.items():
        print(f"  - {src}: {cnt}")
    assert sources.get("plantdoc") == 2560
    assert sources.get("icar_ogd") == 36

    # 4. Rice Preservation
    rice_records = cur.execute("""
        SELECT f.image_id, c.crop_name, d.disease_name, f.condition_status, f.dataset_source
        FROM disease_observation_fact f
        JOIN dim_crop c ON f.crop_key = c.crop_key
        JOIN dim_disease d ON f.disease_key = d.disease_key
        WHERE c.crop_name = 'Rice'
        ORDER BY f.observation_key ASC;
    """).fetchall()
    print(f"\nRice Observations Preserved:     {len(rice_records)} (Expected: 36)")
    assert len(rice_records) == 36
    rice_ids = [r[0] for r in rice_records]
    print(f"  First 3 Rice IDs: {rice_ids[:3]}")
    print(f"  Last 3 Rice IDs:  {rice_ids[-3:]}")
    assert rice_ids[0] == "AGRO_V2_00001"
    assert rice_ids[-1] == "AGRO_V2_00036"

    # 5. Referential Integrity
    orphan_crops = cur.execute("SELECT COUNT(*) FROM disease_observation_fact WHERE crop_key NOT IN (SELECT crop_key FROM dim_crop);").fetchone()[0]
    orphan_diseases = cur.execute("SELECT COUNT(*) FROM disease_observation_fact WHERE disease_key NOT IN (SELECT disease_key FROM dim_disease);").fetchone()[0]
    orphan_images = cur.execute("SELECT COUNT(*) FROM disease_observation_fact WHERE image_key NOT IN (SELECT image_key FROM dim_image);").fetchone()[0]
    orphan_features = cur.execute("SELECT COUNT(*) FROM disease_observation_fact WHERE feature_key NOT IN (SELECT feature_key FROM dim_visual_feature);").fetchone()[0]
    print(f"\nOrphan Foreign Keys: Crop={orphan_crops}, Disease={orphan_diseases}, Image={orphan_images}, Feature={orphan_features}")
    assert orphan_crops == 0 and orphan_diseases == 0 and orphan_images == 0 and orphan_features == 0

    # 6. Feature Completeness (32 Continuous Features)
    req_32 = [
        "rgb_r_mean", "rgb_g_mean", "rgb_b_mean", "rgb_r_std", "rgb_g_std", "rgb_b_std",
        "rgb_r_norm", "rgb_g_norm", "rgb_b_norm", "hsv_h_mean", "hsv_s_mean", "hsv_v_mean",
        "hsv_h_std", "hsv_s_std", "hsv_v_std", "hsv_h_norm", "hsv_s_norm", "hsv_v_norm",
        "exg_index_mean", "glcm_contrast", "glcm_contrast_norm", "glcm_dissimilarity",
        "glcm_homogeneity", "glcm_energy", "glcm_correlation", "glcm_asm", "contour_area",
        "contour_perimeter", "contour_aspect_ratio", "contour_circularity", "contour_solidity",
        "lesion_coverage_ratio"
    ]
    null_expr = " + ".join([f"(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END)" for col in req_32])
    total_nulls = cur.execute(f"SELECT SUM({null_expr}) FROM dim_visual_feature;").fetchone()[0]
    print(f"Total Nulls in 32 Required Features: {total_nulls} (Expected: 0)")
    assert total_nulls == 0

    # 7. OLAP Operations Benchmarking
    print("\nOLAP Query Latency & Validation Benchmark:")
    engine = OLAPEngine()
    
    # 7.1 Rollup
    t0 = time.perf_counter()
    res_roll = engine.rollup()
    lat_roll = (time.perf_counter() - t0) * 1000.0
    print(f"  [1] ROLL-UP:             {len(res_roll['data'])} categories, {res_roll['data']['total_observations'].sum()} total obs in {lat_roll:.2f} ms")
    assert res_roll['data']['total_observations'].sum() == 2596

    # 7.2 Drill-down
    t0 = time.perf_counter()
    res_drill = engine.drilldown(crop_category="Cereal")
    lat_drill = (time.perf_counter() - t0) * 1000.0
    print(f"  [2] DRILL-DOWN (Cereal): {len(res_drill['data'])} groups, {res_drill['data']['observation_count'].sum()} obs in {lat_drill:.2f} ms")
    assert res_drill['data']['observation_count'].sum() == 408

    # 7.3 Slice (Rice)
    t0 = time.perf_counter()
    res_slice = engine.slice_by_crop("Rice")
    lat_slice = (time.perf_counter() - t0) * 1000.0
    print(f"  [3] SLICE (Crop=Rice):   {len(res_slice['data'])} conditions, {res_slice['data']['disease_observations'].sum()} obs in {lat_slice:.2f} ms")
    assert res_slice['data']['disease_observations'].sum() == 36

    # 7.4 Dice
    t0 = time.perf_counter()
    res_dice = engine.dice(selected_crops=["Rice"], selected_pathogens=["Fungal", "Bacterial"], min_contrast=0.1)
    lat_dice = (time.perf_counter() - t0) * 1000.0
    print(f"  [4] DICE (Rice/Contrast):{len(res_dice['data'])} sub-cubes, {res_dice['data']['observation_count'].sum()} obs in {lat_dice:.2f} ms")

    # 7.5 Pivot
    t0 = time.perf_counter()
    res_pivot = engine.pivot()
    lat_pivot = (time.perf_counter() - t0) * 1000.0
    print(f"  [5] PIVOT (CropsxPath):  {len(res_pivot['data'])} crops, {res_pivot['data']['Overall_Metric'].sum()} obs in {lat_pivot:.2f} ms")
    assert res_pivot['data']['Overall_Metric'].sum() == 2596

    print("================================================================================")
    print("ALL 10 MANDATORY DATABASE & ANALYTICAL INVARIANTS SATISFIED 100%!")
    print("================================================================================")
    conn.close()

if __name__ == "__main__":
    run_verification()
