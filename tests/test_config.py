import pytest
from pathlib import Path
from src.utils.config import get_config, get_project_root, ensure_directories

def test_get_project_root():
    root = get_project_root()
    assert root.exists()
    assert (root / "config" / "config.yaml").exists()

def test_load_config():
    cfg = get_config()
    assert "project" in cfg
    assert cfg["project"]["name"] == "AgroVision-Mine"
    assert "paths" in cfg
    assert "preprocessing" in cfg
    assert "warehouse" in cfg

def test_ensure_directories():
    cfg = get_config()
    ensure_directories(cfg)
    for path_key in ["raw_data_dir", "interim_data_dir", "processed_data_dir", "features_data_dir"]:
        dir_path = Path(cfg["paths"][path_key])
        assert dir_path.exists()
        assert dir_path.is_dir()
