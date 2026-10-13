import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

def compute_file_hash(file_path: Union[str, Path], algorithm: str = "md5", block_size: int = 65536) -> str:
    """
    Computes cryptographic checksum of a file. Default is md5.
    """
    hasher = hashlib.md5() if algorithm == "md5" else hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def save_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> None:
    """Safely saves data to a JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)

def load_json(file_path: Union[str, Path]) -> Any:
    """Loads data from a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
