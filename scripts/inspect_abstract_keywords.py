import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('Paper_template-a4 (1).docx', 'r') as z:
    doc_xml = z.read('word/document.xml')
    styles_xml = z.read('word/styles.xml')

root = ET.fromstring(doc_xml)
W_NS = 'http://purl.oclc.org/ooxml/wordprocessingml/main'
ns = {'w': W_NS}

paragraphs = list(root.iter(f'{{{W_NS}}}p'))

for idx in [10, 11, 12, 13]:
    p = paragraphs[idx]
    print(f'=== PARAGRAPH {idx} ===')
    pPr = p.find('w:pPr', ns)
    if pPr is not None:
        pStyle = pPr.find('w:pStyle', ns)
        print('  pStyle:', pStyle.attrib if pStyle is not None else None)
        jc = pPr.find('w:jc', ns)
        print('  jc (align):', jc.attrib if jc is not None else None)
        spacing = pPr.find('w:spacing', ns)
        print('  spacing:', spacing.attrib if spacing is not None else None)
        ind = pPr.find('w:ind', ns)
        print('  ind:', ind.attrib if ind is not None else None)
    for r in p.iter(f'{{{W_NS}}}r'):
        rPr = r.find('w:rPr', ns)
        r_txt = ''.join([t.text for t in r.iter(f'{{{W_NS}}}t') if t.text])
        r_styles = {}
        if rPr is not None:
            for child in rPr:
                tag = child.tag.replace(f'{{{W_NS}}}', '')
                r_styles[tag] = child.attrib.get(f'{{{W_NS}}}val', 'true')
        print(f'  Run: "{r_txt[:50]}" -> styles: {r_styles}')

# Also inspect styles in styles_xml
s_root = ET.fromstring(styles_xml)
print('\n=== STYLES DEFINITION IN STYLES.XML ===')
for s in s_root.iter(f'{{{W_NS}}}style'):
    sId = s.attrib.get(f'{{{W_NS}}}styleId')
    if sId in ['Abstract', 'Keywords', 'Heading1', 'Heading2', 'Heading3', 'BodyText', 'papertitle', 'Author']:
        name = s.find('w:name', ns)
        name_val = name.attrib.get(f'{{{W_NS}}}val') if name is not None else sId
        rPr = s.find('w:rPr', ns)
        pPr = s.find('w:pPr', ns)
        r_fonts = rPr.find('w:rFonts', ns).attrib if rPr is not None and rPr.find('w:rFonts', ns) is not None else {}
        sz = rPr.find('w:sz', ns).attrib if rPr is not None and rPr.find('w:sz', ns) is not None else {}
        b = rPr.find('w:b', ns) is not None if rPr is not None else False
        i = rPr.find('w:i', ns) is not None if rPr is not None else False
        print(f'Style: {sId} ("{name_val}"): font={r_fonts}, sz={sz} (half-pts), bold={b}, italic={i}')
