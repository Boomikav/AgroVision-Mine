import os
import sys
from pathlib import Path
import win32com.client
import pythoncom

sys.stdout.reconfigure(encoding='utf-8')

pythoncom.CoInitialize()
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc_path = Path("Paper_template-a4 (1).docx").resolve()
doc = word.Documents.Open(str(doc_path))

styles_to_check = [
    "paper title", "Author", "Abstract", "Keywords", "Heading 1", 
    "Heading 2", "Heading 3", "Heading 4", "Body Text", "Normal",
    "figure caption", "table head", "References", "bullet list", "sponsors"
]

print("=== TEMPLATE STYLES AUDIT ===")
for s_name in styles_to_check:
    try:
        st = doc.Styles(s_name)
        f = st.Font
        pf = st.ParagraphFormat
        print(f"Style: '{s_name}'")
        print(f"  Font: {f.Name}, Size: {f.Size} pt, Bold: {f.Bold}, Italic: {f.Italic}, AllCaps: {f.AllCaps}")
        print(f"  Para: Align: {pf.Alignment}, SpaceBefore: {pf.SpaceBefore} pt, SpaceAfter: {pf.SpaceAfter} pt, LineSpacing: {pf.LineSpacing} pt, FirstLineIndent: {pf.FirstLineIndent} pt")
    except Exception as e:
        print(f"Style '{s_name}' not found: {e}")

print("\n=== PARAGRAPH SPECIFICS (FIRST 20) ===")
for i in range(1, min(22, doc.Paragraphs.Count + 1)):
    p = doc.Paragraphs(i)
    txt = p.Range.Text.strip().replace('\r', ' ').replace('\n', ' ')
    if not txt:
        continue
    f = p.Range.Font
    pf = p.Format
    print(f"P{i:02d} [{p.Range.Style.NameLocal}]: '{txt[:70]}'")
    print(f"     Font: {f.Name} {f.Size}pt b={f.Bold} it={f.Italic} | Align={pf.Alignment} Sb={pf.SpaceBefore} Sa={pf.SpaceAfter} Ind={pf.FirstLineIndent}")

doc.Close(False)
word.Quit()
pythoncom.CoUninitialize()
