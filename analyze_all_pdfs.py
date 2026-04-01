import pdfplumber
import os, re

pdfs_dir = 'pdfs'
for fname in sorted(os.listdir(pdfs_dir)):
    if not fname.endswith('.pdf'):
        continue
    state = fname.replace('.pdf', '')
    pdf = pdfplumber.open(os.path.join(pdfs_dir, fname))
    print(f"\n{'='*60}")
    print(f"=== {state} ({len(pdf.pages)} pages) ===")
    
    found = False
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            # Look for the Anwärtergrundbetrag table
            if table and len(table) >= 2:
                header = str(table[0]) if table[0] else ""
                if 'nwärter' in header or 'Grundbetrag' in header or 'nw\\xe4rter' in header:
                    print(f"  Page {i}, Table {j}: Anwärtergrundbetrag")
                    for row in table:
                        print(f"    {row}")
                    found = True
                # Also check for Familienzuschlag
                if 'amilienzuschlag' in header and 'Stufe' in header:
                    print(f"  Page {i}, Table {j}: Familienzuschlag")
                    for row in table:
                        print(f"    {row}")
    
    if not found:
        # Try text-based search
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if 'nwärtergrundbetrag' in text or 'nwärtergrundbetr' in text:
                # Extract relevant section
                lines = text.split('\n')
                for k, line in enumerate(lines):
                    if 'nwärtergrundbetrag' in line.lower() or 'nwärtergrundbetr' in line.lower():
                        start = max(0, k-1)
                        end = min(len(lines), k+10)
                        print(f"  Page {i}, Text match around line {k}:")
                        for l in range(start, end):
                            print(f"    {lines[l]}")
                        found = True
                        break
    
    if not found:
        print("  WARNING: Anwärtergrundbetrag NOT FOUND")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if 'nwärter' in text.lower():
                print(f"  Page {i} contains 'Anwärter' in text")

    pdf.close()
