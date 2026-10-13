import os
import sys
import subprocess
from pathlib import Path
import re

repo_dir = Path("data/external_raw/plantdoc")
output_dir = Path("data/external_raw/plantdoc/images")

# 1. Query git tree
p = subprocess.run(["git", "ls-tree", "-r", "HEAD"], cwd=repo_dir, capture_output=True, text=True, encoding="utf-8")
lines = p.stdout.strip().split("\n")

print(f"Total entries in git tree: {len(lines)}")

# We only extract files in train/ and test/
image_entries = []
for l in lines:
    parts = l.split("\t")
    if len(parts) == 2:
        meta, rel_path = parts
        sha = meta.split()[2]
        if rel_path.startswith("train/") or rel_path.startswith("test/"):
            image_entries.append((sha, rel_path))

print(f"Total image files to extract: {len(image_entries)}")

def sanitize_rel_path(path_str):
    # Split into directories and filename
    parts = path_str.split("/")
    clean_parts = []
    for part in parts:
        # replace invalid Windows characters: ? : * " < > |
        cleaned = re.sub(r'[?:\*"<>|]', '_', part)
        clean_parts.append(cleaned)
    return "/".join(clean_parts)

extracted_count = 0
failed_count = 0

for sha, rel_path in image_entries:
    clean_rel = sanitize_rel_path(rel_path)
    dest_path = output_dir / clean_rel
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract blob directly from git object database
    cmd = ["git", "cat-file", "blob", sha]
    p_cat = subprocess.run(cmd, cwd=repo_dir, capture_output=True)
    if p_cat.returncode == 0:
        with open(dest_path, "wb") as f:
            f.write(p_cat.stdout)
        extracted_count += 1
    else:
        print(f"Failed to extract {rel_path} ({sha}): {p_cat.stderr}")
        failed_count += 1

print(f"\nExtraction complete:")
print(f"  Successfully extracted: {extracted_count}")
print(f"  Failed: {failed_count}")
