import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

_CONFIG_CACHE: Optional[Dict[str, Any]] = None

def get_project_root() -> Path:
    """Returns the absolute root directory of the project."""
    # Assuming this file is located at <project_root>/src/utils/config.py
    return Path(__file__).resolve().parent.parent.parent

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads YAML configuration and resolves path references relative to project root.
    """
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None and config_path is None:
        return _CONFIG_CACHE

    root = get_project_root()
    if config_path is None:
        target_path = root / "config" / "config.yaml"
    else:
        target_path = Path(config_path)
        if not target_path.is_absolute():
            target_path = root / target_path

    if not target_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {target_path}")

    with open(target_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    # Resolve paths to absolute paths
    if "paths" in cfg:
        for k, v in cfg["paths"].items():
            if isinstance(v, str):
                cfg["paths"][k] = str((root / v).resolve())

    # Ensure sqlite path is resolved
    if "warehouse" in cfg and "sqlite_path" in cfg["warehouse"]:
        sql_path = cfg["warehouse"]["sqlite_path"]
        if not os.path.isabs(sql_path):
            cfg["warehouse"]["sqlite_path"] = str((root / sql_path).resolve())

    _CONFIG_CACHE = cfg
    return cfg

def get_config() -> Dict[str, Any]:
    """Helper to retrieve the current cached config or load default."""
    return load_config()

def ensure_directories(cfg: Optional[Dict[str, Any]] = None) -> None:
    """Ensures all standard project directories exist."""
    if cfg is None:
        cfg = get_config()

    if "paths" in cfg:
        for path_name, path_val in cfg["paths"].items():
            Path(path_val).mkdir(parents=True, exist_ok=True)
