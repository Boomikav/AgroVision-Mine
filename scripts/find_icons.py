import re
from pathlib import Path

root = Path('frontend/src')
icons = set()
pattern1 = re.compile(r'material-symbols-outlined[^>]*>([^<]+)<', re.DOTALL)
pattern2 = re.compile(r'icon:\s*[\'"]([a-zA-Z0-9_\-]+)[\'"]')
pattern3 = re.compile(r'icon=[\'"]([a-zA-Z0-9_\-]+)[\'"]')

for f in root.rglob('*.tsx'):
    content = f.read_text(encoding='utf-8')
    for m in pattern1.findall(content):
        c = m.strip()
        if c and '\n' not in c and '{' not in c:
            icons.add(c)
    for m in pattern2.findall(content):
        icons.add(m.strip())
    for m in pattern3.findall(content):
        icons.add(m.strip())

print("ALL UNIQUE ICON NAMES ({}):".format(len(icons)))
for i in sorted(icons):
    print("  ", i)
