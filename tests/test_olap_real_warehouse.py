"""
Phase 6 OLAP Operations Tests against the Real Populated Data Warehouse.
Verifies all 5 core dimensional OLAP operations against physical warehouse records:
1. ROLL-UP
2. DRILL-DOWN
3. SLICE (by crop, by pathogen)
4. DICE
5. PIVOT (observation counts, GLCM texture contrast)
"""
import pytest
from src.olap.engine import OLAPEngine
from src.warehouse.connection import get_db_engine


@pytest.fixture
def real_olap_engine():
    engine = get_db_engine()
    return OLAPEngine(engine=engine)


def test_real_warehouse_rollup(real_olap_engine):
    res = real_olap_engine.rollup()
    assert res["operation"] == "ROLL-UP"
    df = res["data"]
    assert len(df) > 0
    assert "crop_category" in df.columns
    assert "total_observations" in df.columns
    # Total observations across all categories must equal 2,596 in unified warehouse
    total_obs = df["total_observations"].sum()
    assert total_obs == 2596
    assert "Cereal" in df["crop_category"].values
    assert "Horticultural" in df["crop_category"].values


def test_real_warehouse_drilldown(real_olap_engine):
    res = real_olap_engine.drilldown(crop_category="Cereal")
    assert res["operation"] == "DRILL-DOWN"
    df = res["data"]
    assert len(df) > 0
    assert "crop_name" in df.columns
    assert "disease_name" in df.columns
    assert "pathogen_type" in df.columns
    assert "dominant_color_tone" in df.columns
    assert "observation_count" in df.columns
    # Cereal category includes Rice (36) and Corn (372) = 408
    assert df["observation_count"].sum() == 408


def test_real_warehouse_true_drilldown(real_olap_engine):
    # Test unconstrained true drill-down (Pathogen Type -> Disease Name)
    res = real_olap_engine.true_drilldown()
    assert res["operation"] == "TRUE OLAP DRILL-DOWN"
    assert res["hierarchy"] == "dim_disease: Pathogen Type -> Disease Name"
    df = res["data"]
    assert len(df) == 19  # 19 conditions/diseases across unified warehouse
    assert "pathogen_type" in df.columns
    assert "disease_name" in df.columns
    assert "total_observations" in df.columns
    assert df["total_observations"].sum() == 2596

    # Test drill-down constrained to Fungal pathogen
    res_fungal = real_olap_engine.true_drilldown(pathogen_type="Fungal")
    df_f = res_fungal["data"]
    assert len(df_f) == 13  # 13 fungal conditions
    assert df_f["total_observations"].sum() == 1426


def test_real_warehouse_slice_by_crop(real_olap_engine):
    res = real_olap_engine.slice_by_crop("Rice")
    assert res["operation"] == "SLICE"
    df = res["data"]
    assert len(df) > 0
    assert "disease_name" in df.columns
    assert "disease_observations" in df.columns
    assert df["disease_observations"].sum() == 36


def test_real_warehouse_slice_by_pathogen(real_olap_engine):
    # Slice Fungal
    res_fungal = real_olap_engine.slice_by_pathogen("Fungal")
    assert res_fungal["operation"] == "SLICE"
    df_f = res_fungal["data"]
    assert len(df_f) > 0
    assert df_f["observations"].sum() == 1426

    # Slice Bacterial
    res_bact = real_olap_engine.slice_by_pathogen("Bacterial")
    assert res_bact["operation"] == "SLICE"
    df_b = res_bact["data"]
    assert len(df_b) > 0
    assert df_b["observations"].sum() == 193


def test_real_warehouse_dice(real_olap_engine):
    res = real_olap_engine.dice(
        selected_crops=["Rice"],
        selected_pathogens=["Fungal", "Bacterial"],
        min_contrast=0.1
    )
    assert res["operation"] == "DICE"
    df = res["data"]
    assert len(df) > 0
    assert "crop_name" in df.columns
    assert "disease_name" in df.columns


def test_real_warehouse_pivot(real_olap_engine):
    res = real_olap_engine.pivot(measure="observation_count")
    assert res["operation"] == "PIVOT"
    df = res["data"]
    assert len(df) > 0
    assert "Crop" in df.columns
    assert "Fungal" in df.columns
    assert "Bacterial" in df.columns
    assert "Overall_Metric" in df.columns

    rice_row = df[df["Crop"] == "Rice"].iloc[0]
    assert rice_row["Fungal"] == 24
    assert rice_row["Bacterial"] == 12
    assert rice_row["Overall_Metric"] == 36
