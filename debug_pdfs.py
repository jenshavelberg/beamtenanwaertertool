"""Debug specific PDFs that failed extraction."""
import pdfplumber

for state in ['Berlin', 'Brandenburg', 'Hessen', 'Mecklenburg-Vorpommern', 'Saarland', 'Sachsen', 'Nordrhein-Westfalen']:
    fname = state.replace('ü', 'ue')
    pdf_path = f'pdfs/{fname}.pdf'
    try:
        pdf = pdfplumber.open(pdf_path)
    except:
        continue
    
    print(f"\n{'='*60}")
    print(f"=== {state} ===")
    
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            if not table:
                continue
            # Show all table headers and first few rows
            header_text = str(table[0])[:100] if table[0] else "None"
            if 'nwärter' in header_text.lower() or 'Eingangsamt' in header_text or 'Grundbetrag' in header_text or 'grundbetrag' in header_text.lower():
                print(f"\n  Page {i}, Table {j} [MATCH]: header={header_text}")
                for row in table:
                    print(f"    {row}")
    
    pdf.close()
