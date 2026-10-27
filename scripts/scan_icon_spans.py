import re
from pathlib import Path

root = Path('frontend/src')
# Match span tags with material-symbols-outlined
pattern = re.compile(r'<span[^>]*material-symbols-outlined[^>]*>([\s\S]*?)</span>')

for f in sorted(root.rglob('*.tsx')):
    content = f.read_text(encoding='utf-8')
    matches = pattern.findall(content)
    if matches:
        print(f"{f.relative_to(root)}: {len(matches)} spans")
        for m in matches[:3]:
            print(f"    sample: '{m.strip()}'")
