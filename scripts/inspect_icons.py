import re
from pathlib import Path

root = Path('frontend/src')
pattern = re.compile(r'(<span[^>]*material-symbols-outlined[^>]*>([\s\S]*?)</span>)')

for f in sorted(root.rglob('*.tsx')):
    content = f.read_text(encoding='utf-8')
    matches = pattern.findall(content)
    if matches:
        print(f"\n=== {f.relative_to(root)}: {len(matches)} matches ===")
        for full, inner in matches:
            print(f"  FULL: {full.strip()}")
            print(f"  INNER: '{inner.strip()}'")
