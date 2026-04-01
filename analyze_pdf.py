import pdfplumber

# Analyze Bayern PDF as sample
pdf = pdfplumber.open('pdfs/Bayern.pdf')
print(f"Pages: {len(pdf.pages)}")
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    if text and ('nwärter' in text or 'Anwärter' in text or 'nw\u00e4rter' in text):
        print(f"\n=== PAGE {i} (contains Anwärter) ===")
        print(text)
        print("\n--- TABLES ---")
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"\nTable {j}:")
            for row in table:
                print(row)
pdf.close()
