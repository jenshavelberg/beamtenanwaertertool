"""Extract Familienzuschlag from Hessen PDF and check all values."""
import pdfplumber
import re

pdf = pdfplumber.open('pdfs/Hessen.pdf')
for i, page in enumerate(pdf.pages):
    text = page.extract_text() or ""
    tables = page.extract_tables()
    
    print(f"\n=== Page {i} ===")
    for j, table in enumerate(tables):
        if not table:
            continue
        header = str(table[0])[:120] if table[0] else "None"
        print(f"\nTable {j}: {header}")
        for row in table:
            print(f"  {row}")

print("\n\n=== FULL TEXT PAGE 0 ===")
print(pdf.pages[0].extract_text())
print("\n\n=== FULL TEXT PAGE 1 ===")
print(pdf.pages[1].extract_text())

pdf.close()
