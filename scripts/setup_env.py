"""
Environment and Directory Setup Script for AgroVision-Mine.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.config import get_config, ensure_directories
from src.utils.logger import setup_logger

logger = setup_logger("setup", level="INFO")

def main():
    logger.info("Initializing AgroVision-Mine directory hierarchy...")
    cfg = get_config()
    ensure_directories(cfg)
    logger.info("Project directories verified successfully:")
    for key, path in cfg["paths"].items():
        logger.info(f"  - {key}: {path}")

if __name__ == "__main__":
    main()
