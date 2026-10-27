import re
from pathlib import Path

files_to_update = [
    Path('frontend/src/components/common/SpecimenModal.tsx'),
    Path('frontend/src/pages/AssociationRulesPage.tsx'),
    Path('frontend/src/pages/DataQualityPage.tsx'),
    Path('frontend/src/pages/DatasetExplorerPage.tsx'),
    Path('frontend/src/pages/ImageAnalysisPage.tsx'),
    Path('frontend/src/pages/OLAPAnalyticsPage.tsx'),
    Path('frontend/src/pages/OverviewPage.tsx'),
    Path('frontend/src/pages/ReportsMethodologyPage.tsx'),
    Path('frontend/src/pages/VisualPatternMiningPage.tsx'),
    Path('frontend/src/pages/WarehousePage.tsx'),
]

# Pattern for span with material-symbols-outlined
# Matches <span className="material-symbols-outlined ...">...</span> or with single quotes
pattern = re.compile(r'<span\s+className=["\']([^"\']*material-symbols-outlined[^"\']*)["\']>([\s\S]*?)</span>')

for filepath in files_to_update:
    if not filepath.exists():
        print(f"Skipping {filepath}, does not exist")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    
    # Determine appropriate relative import path for AppIcon
    if 'components/common' in str(filepath).replace('\\', '/'):
        import_stmt = "import { AppIcon } from './AppIcon'"
    else:
        import_stmt = "import { AppIcon } from '../components/common/AppIcon'"
        
    if "import { AppIcon }" not in content:
        # Insert after last import
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                last_import_idx = i
        lines.insert(last_import_idx + 1, import_stmt)
        content = '\n'.join(lines)
    
    def replacer(match):
        class_str = match.group(1)
        inner = match.group(2).strip()
        
        # Clean classes: remove 'material-symbols-outlined'
        classes = [c for c in class_str.split() if c != 'material-symbols-outlined']
        
        # In CSS, text-[18px] etc. won't resize lucide svg icons unless size is set or we use w- / h- or inline classes.
        # But lucide-react SVGs inherit currentColor and respect w- and h- classes or size prop!
        # If classes include text-[...px], text-4xl etc., let's convert or keep classes.
        # Lucide icons default to 24px if no size or w/h is set, but can take w-* h-* or className.
        # Let's map common text-[...px] or font size classes to appropriate w-* h-* classes if helpful,
        # or leave them so Lucide inherits styling!
        new_classes = ' '.join(classes).strip()
        
        # Check if inner is dynamic like {s.icon}
        if inner.startswith('{') and inner.endswith('}'):
            var_name = inner[1:-1].strip()
            if new_classes:
                return f'<AppIcon name={{{var_name}}} className="{new_classes}" />'
            else:
                return f'<AppIcon name={{{var_name}}} />'
        else:
            if new_classes:
                return f'<AppIcon name="{inner}" className="{new_classes}" />'
            else:
                return f'<AppIcon name="{inner}" />'

    new_content = pattern.sub(replacer, content)
    filepath.write_text(new_content, encoding='utf-8')
    print(f"Updated {filepath}")

print("Replacement complete.")
