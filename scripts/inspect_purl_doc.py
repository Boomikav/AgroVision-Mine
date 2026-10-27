import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('Paper_template-a4 (1).docx', 'r') as z:
    doc_xml = z.read('word/document.xml')
    styles_xml = z.read('word/styles.xml')

root = ET.fromstring(doc_xml)
W_NS = 'http://purl.oclc.org/ooxml/wordprocessingml/main'
ns = {'w': W_NS}

print('--- PARAGRAPHS IN TEMPLATE ---')
for idx, p in enumerate(root.iter(f'{{{W_NS}}}p')):
    pStyle = p.find('.//w:pStyle', ns)
    style_val = pStyle.attrib.get(f'{{{W_NS}}}val') if pStyle is not None else 'None'
    texts = [t.text for t in p.iter(f'{{{W_NS}}}t') if t.text]
    full_text = ''.join(texts)[:90].replace('\n', ' ')
    sectPr = p.find('.//w:sectPr', ns)
    has_sect = 'YES (Section Break)' if sectPr is not None else 'no'
    if sectPr is not None:
        type_elem = sectPr.find('w:type', ns)
        type_val = type_elem.attrib.get(f'{{{W_NS}}}val') if type_elem is not None else 'default'
        cols_elem = sectPr.find('w:cols', ns)
        cols_num = cols_elem.attrib.get(f'{{{W_NS}}}num') if cols_elem is not None else '1'
        cols_space = cols_elem.attrib.get(f'{{{W_NS}}}space') if cols_elem is not None else 'none'
        pgSz = sectPr.find('w:pgSz', ns)
        pg_w = pgSz.attrib.get(f'{{{W_NS}}}w') if pgSz is not None else '?'
        pg_h = pgSz.attrib.get(f'{{{W_NS}}}h') if pgSz is not None else '?'
        pgMar = sectPr.find('w:pgMar', ns)
        top_m = pgMar.attrib.get(f'{{{W_NS}}}top') if pgMar is not None else '?'
        bot_m = pgMar.attrib.get(f'{{{W_NS}}}bottom') if pgMar is not None else '?'
        left_m = pgMar.attrib.get(f'{{{W_NS}}}left') if pgMar is not None else '?'
        right_m = pgMar.attrib.get(f'{{{W_NS}}}right') if pgMar is not None else '?'
        print(f'*** SECTION BREAK at P{idx:02d}: type={type_val}, cols={cols_num}, space={cols_space}, size={pg_w}x{pg_h}, margins: top={top_m}, bot={bot_m}, left={left_m}, right={right_m} ***')
    if full_text or has_sect == 'YES (Section Break)':
        print(f'P{idx:02d} [Style: {style_val:15s}]: {full_text}')

body = root.find(f'{{{W_NS}}}body')
final_sectPr = body.find('w:sectPr', ns)
if final_sectPr is not None:
    type_elem = final_sectPr.find('w:type', ns)
    type_val = type_elem.attrib.get(f'{{{W_NS}}}val') if type_elem is not None else 'default'
    cols_elem = final_sectPr.find('w:cols', ns)
    cols_num = cols_elem.attrib.get(f'{{{W_NS}}}num') if cols_elem is not None else '1'
    cols_space = cols_elem.attrib.get(f'{{{W_NS}}}space') if cols_elem is not None else 'none'
    pgSz = final_sectPr.find('w:pgSz', ns)
    pg_w = pgSz.attrib.get(f'{{{W_NS}}}w') if pgSz is not None else '?'
    pg_h = pgSz.attrib.get(f'{{{W_NS}}}h') if pgSz is not None else '?'
    pgMar = final_sectPr.find('w:pgMar', ns)
    top_m = pgMar.attrib.get(f'{{{W_NS}}}top') if pgMar is not None else '?'
    bot_m = pgMar.attrib.get(f'{{{W_NS}}}bottom') if pgMar is not None else '?'
    left_m = pgMar.attrib.get(f'{{{W_NS}}}left') if pgMar is not None else '?'
    right_m = pgMar.attrib.get(f'{{{W_NS}}}right') if pgMar is not None else '?'
    print(f'\n*** FINAL BODY SECTION: type={type_val}, cols={cols_num}, space={cols_space}, size={pg_w}x{pg_h}, margins: top={top_m}, bot={bot_m}, left={left_m}, right={right_m} ***')
