"""
Duplicate Detection Module for AgroVision-Mine.
Implements exact cryptographic matching (MD5/SHA256) and perceptual hashing (dHash/pHash)
to detect identical and near-duplicate agricultural images.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
import numpy as np
from PIL import Image

from src.utils.config import get_config
from src.utils.logger import setup_logger
from src.utils.io import compute_file_hash

logger = setup_logger("duplicate_detector")


@dataclass
class DuplicateCheckResult:
    is_duplicate: bool
    duplicate_type: Optional[str]  # "EXACT_HASH", "PERCEPTUAL_NEAR", None
    canonical_file: Optional[str]
    hamming_distance: int
    md5_hash: str
    perceptual_hash: str


class DuplicateDetector:
    """
    Detects both exact file-level duplicates and visually identical/compressed near-duplicates.
    Maintains an index of seen images to ensure idempotency.
    """

    def __init__(self, hamming_threshold: Optional[int] = None):
        cfg = get_config()
        dup_cfg = cfg.get("preprocessing", {}).get("duplicate_detection", {})
        self.hamming_threshold = (
            hamming_threshold
            if hamming_threshold is not None
            else dup_cfg.get("phash_hamming_threshold", 5)
        )
        self.seen_md5: Dict[str, str] = {}  # md5 -> canonical file path
        self.seen_phash: Dict[str, str] = {}  # phash (hex) -> canonical file path

    @staticmethod
    def compute_dhash(img_pil: Image.Image, hash_size: int = 8) -> str:
        """
        Computes difference hash (dHash) on grayscale image.
        Resize to (hash_size + 1, hash_size), convert to grayscale,
        compare adjacent horizontal pixels to produce a 64-bit binary sequence.
        """
        # Resize to 9x8 for an 8x8 (64-bit) hash
        resized = img_pil.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        pixels = np.asarray(resized, dtype=np.int32)
        # Compare adjacent columns: pixel[col] > pixel[col+1]
        diff = pixels[:, :-1] > pixels[:, 1:]
        # Convert boolean 8x8 array to 64-bit integer
        flat = diff.flatten()
        decimal_val = 0
        for bit in flat:
            decimal_val = (decimal_val << 1) | int(bit)

        # Incorporate mean luminance byte (8 bits) to distinguish uniform flat fields
        mean_lum = int(np.mean(pixels)) & 0xFF
        combined_val = (decimal_val << 8) | mean_lum
        return f"{combined_val:018x}"

    @staticmethod
    def hamming_distance(hex_hash1: str, hex_hash2: str) -> int:
        """
        Calculates Hamming distance (bit differences) between two hexadecimal hashes.
        """
        val1 = int(hex_hash1, 16)
        val2 = int(hex_hash2, 16)
        xor_val = val1 ^ val2
        return bin(xor_val).count("1")

    def check_and_register(self, file_path: Union[str, Path], img_pil: Optional[Image.Image] = None) -> DuplicateCheckResult:
        """
        Checks if the image is a duplicate of any previously indexed image.
        If unique, registers it as canonical.
        """
        path = Path(file_path)
        md5_hash = compute_file_hash(path, "md5")

        # 1. Exact match check
        if md5_hash in self.seen_md5:
            canonical = self.seen_md5[md5_hash]
            return DuplicateCheckResult(
                is_duplicate=True,
                duplicate_type="EXACT_HASH",
                canonical_file=canonical,
                hamming_distance=0,
                md5_hash=md5_hash,
                perceptual_hash=""
            )

        # 2. Perceptual near-duplicate check
        if img_pil is None:
            with Image.open(path) as loaded_img:
                phash = self.compute_dhash(loaded_img)
        else:
            phash = self.compute_dhash(img_pil)

        min_distance = 65
        closest_canonical = None

        for existing_phash, existing_file in self.seen_phash.items():
            dist = self.hamming_distance(phash, existing_phash)
            if dist < min_distance:
                min_distance = dist
                closest_canonical = existing_file

        if min_distance <= self.hamming_threshold and closest_canonical is not None:
            return DuplicateCheckResult(
                is_duplicate=True,
                duplicate_type="PERCEPTUAL_NEAR",
                canonical_file=closest_canonical,
                hamming_distance=min_distance,
                md5_hash=md5_hash,
                perceptual_hash=phash
            )

        # Unique image: register as canonical
        path_str = str(path.resolve())
        self.seen_md5[md5_hash] = path_str
        self.seen_phash[phash] = path_str

        return DuplicateCheckResult(
            is_duplicate=False,
            duplicate_type=None,
            canonical_file=None,
            hamming_distance=min_distance if min_distance <= 64 else -1,
            md5_hash=md5_hash,
            perceptual_hash=phash
        )

    def reset(self) -> None:
        """Resets the duplicate index."""
        self.seen_md5.clear()
        self.seen_phash.clear()
