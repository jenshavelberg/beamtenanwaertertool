"""
Extracts Anwärtergrundbetrag from all state PDFs and compares with existing data.
Also extracts Familienzuschlag Stufe 1 where available.
"""
import pdfplumber
import json
import re
import os

def parse_german_number(s):
    """Convert German number format (1.234,56) to float."""
    s = s.strip()
    s = s.replace('.', '').replace(',', '.')
    return float(s)

def extract_anwaerter_table(pdf_path):
    """Extract Anwärtergrundbetrag table from a PDF."""
    pdf = pdfplumber.open(pdf_path)
    result = {}
    
    for page in pdf.pages:
        tables = page.extract_tables()
        text = page.extract_text() or ""
        
        for table in tables:
            if not table or len(table) < 2:
                continue
            header = str(table[0]) if table[0] else ""
            
            # Look for Anwärtergrundbetrag table
            if ('nwärter' in header or 'Grundbetrag' in header) and 'Eingangsamt' in header or 'Laufbahn' in header:
                for row in table[1:]:
                    if not row or len(row) < 2:
                        continue
                    col0 = str(row[0] or "").strip()
                    col1 = str(row[1] or "").strip()
                    if not col0 or not col1:
                        continue
                    
                    # Handle multi-line cells (newline-separated)
                    grades_raw = col0.split('\n')
                    amounts_raw = col1.split('\n')
                    
                    if len(grades_raw) == len(amounts_raw):
                        for g, a in zip(grades_raw, amounts_raw):
                            g = g.strip()
                            a = a.strip()
                            if not g or not a:
                                continue
                            try:
                                amount = parse_german_number(a)
                                result[g] = amount
                            except ValueError:
                                pass
                    elif len(amounts_raw) == 1 and len(grades_raw) == 1:
                        try:
                            amount = parse_german_number(amounts_raw[0])
                            result[grades_raw[0].strip()] = amount
                        except ValueError:
                            pass
        
        # Also try text-based extraction for problematic PDFs (like Sachsen)
        if not result and 'nwärtergrundbetrag' in text.lower():
            lines = text.split('\n')
            for line in lines:
                # Pattern: "A 5 1.404,79" or "A 6 bis A 8 1.528,41"
                match = re.search(r'(A\s*\d+(?:\s*(?:bis|und)\s*A\s*\d+)?(?:\s*\+\s*\w+)?)\s+([\d.]+,\d{2})', line)
                if match:
                    grade = match.group(1).strip()
                    amount = parse_german_number(match.group(2))
                    result[grade] = amount
    
    pdf.close()
    return result

def extract_familienzuschlag(pdf_path):
    """Extract Familienzuschlag Stufe 1 from PDF."""
    pdf = pdfplumber.open(pdf_path)
    fam_zuschlag = None
    
    for page in pdf.pages:
        tables = page.extract_tables()
        
        for table in tables:
            if not table or len(table) < 2:
                continue
            header = str(table[0]) if table[0] else ""
            
            # Look for Familienzuschlag table
            if 'amilienzuschlag' in header and 'Stufe' in header:
                for row in table[1:]:
                    if not row:
                        continue
                    row_str = str(row)
                    # Find Stufe 1 values
                    if 'Stufe 1' in row_str or 'Stufe' in row_str:
                        continue  # Skip header rows
                    # Try to find Stufe 1 column
                    for cell in row:
                        if cell:
                            vals = str(cell).split('\n')
                            for v in vals:
                                try:
                                    fam_zuschlag = parse_german_number(v.strip())
                                except:
                                    pass
        
        # Text-based extraction for simpler tables
        text = page.extract_text() or ""
        if 'amilienzuschlag' in text:
            # Find "Stufe 1" value
            match = re.search(r'Stufe\s*1[^\d]*?([\d.]+,\d{2})', text)
            if match:
                try:
                    fam_zuschlag = parse_german_number(match.group(1))
                except:
                    pass
    
    pdf.close()
    return fam_zuschlag

# Grade mapping: normalize PDF grade descriptions to our tool's grade assignments
GRADE_MAP = {
    # Common patterns for each Besoldungsgruppe
    'A3': ['A 3', 'A3'],
    'A4': ['A 4', 'A4'],
    'A5': ['A 5', 'A5'],
    'A6': ['A 6', 'A6'],
    'A7': ['A 7', 'A7'],
    'A8': ['A 8', 'A8'],
    'A9': ['A 9', 'A9'],
    'A10': ['A 10', 'A10'],
    'A11': ['A 11', 'A11'],
    'A12': ['A 12', 'A12'],
    'A13': ['A 13', 'A13'],
    'A13+': ['A 13 +', 'A13+', 'A 13 mit', 'Strukturzulage', 'Zulage'],
    'R1': ['R 1', 'R1'],
}

def normalize_grade_ranges(raw_data):
    """Convert grade ranges like 'A 5 bis A 8' to individual grades with the same amount."""
    normalized = {}
    
    for key, amount in raw_data.items():
        key_clean = key.strip()
        
        # Check for A13+ (must check before A13)
        if re.search(r'A\s*13\s*\+|A\s*13\s*mit\s*(?:Struktur|Zulage)|A\s*13\s*\+\s*Zulage|Strukturzulage', key_clean):
            normalized['A13+'] = amount
            # R1 typically gets same as A13+
            normalized['R1'] = amount
            continue
        
        # Check for range patterns: "A X bis A Y" or "A X und A Y"
        range_match = re.match(r'A\s*(\d+)\s*(?:bis|und)\s*A\s*(\d+)', key_clean)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            for grade_num in range(start, end + 1):
                normalized[f'A{grade_num}'] = amount
            continue
        
        # Single grade: "A X"
        single_match = re.match(r'^A\s*(\d+)$', key_clean)
        if single_match:
            grade_num = int(single_match.group(1))
            normalized[f'A{grade_num}'] = amount
            continue
        
        # Special patterns with "oder R 1"
        if 'oder R 1' in key_clean or 'oder R1' in key_clean:
            # Extract the A grade
            a_match = re.search(r'A\s*(\d+)', key_clean)
            if a_match:
                grade_num = int(a_match.group(1))
                if 'Zulage' in key_clean or '+' in key_clean or 'Strukturzulage' in key_clean:
                    normalized['A13+'] = amount
                else:
                    normalized[f'A{grade_num}'] = amount
                normalized['R1'] = amount
            continue
        
        # Bund-specific: "einfacher Dienst", "mittlerer Dienst" etc.
        if 'einfacher Dienst' in key_clean:
            normalized['A3'] = amount
            normalized['A4'] = amount
        elif 'mittlerer Dienst' in key_clean:
            normalized['A5'] = amount
            normalized['A6'] = amount
            normalized['A7'] = amount
            normalized['A8'] = amount
            normalized['A9'] = amount  # For Bund, mittlerer Dienst goes up to A9
        elif 'gehobener Dienst' in key_clean:
            normalized['A10'] = amount
            normalized['A11'] = amount
            normalized['A12'] = amount
        elif 'höherer Dienst' in key_clean:
            normalized['A13'] = amount
            normalized['A13+'] = amount
            normalized['R1'] = amount
        
    return normalized

# State name mapping between PDF filenames and JSON keys  
STATE_MAP = {
    'Baden-Wuerttemberg': 'Baden-Württemberg',
    'Bayern': 'Bayern',
    'Berlin': 'Berlin',
    'Brandenburg': 'Brandenburg',
    'Bremen': 'Bremen',
    'Hamburg': 'Hamburg',
    'Hessen': 'Hessen',
    'Mecklenburg-Vorpommern': 'Mecklenburg-Vorpommern',
    'Niedersachsen': 'Niedersachsen',
    'Nordrhein-Westfalen': 'Nordrhein-Westfalen',
    'Rheinland-Pfalz': 'Rheinland-Pfalz',
    'Saarland': 'Saarland',
    'Sachsen': 'Sachsen',
    'Sachsen-Anhalt': 'Sachsen-Anhalt',
    'Schleswig-Holstein': 'Schleswig-Holstein',
    'Thueringen': 'Thüringen',
    'Bund': 'Bundesbeihilfe',
}

# Load existing data
with open('besoldung_compact_v2.json', 'r') as f:
    existing_data = json.load(f)

print("=" * 80)
print("VERGLEICH: Bestehende Daten vs. aktuelle Besoldungstabellen (PDFs)")
print("=" * 80)

all_changes = {}

for pdf_name, json_name in STATE_MAP.items():
    pdf_path = f'pdfs/{pdf_name}.pdf'
    if not os.path.exists(pdf_path):
        print(f"\nWARNING: {pdf_path} not found")
        continue
    
    raw = extract_anwaerter_table(pdf_path)
    normalized = normalize_grade_ranges(raw)
    
    print(f"\n{'─'*60}")
    print(f"  {json_name}")
    print(f"  PDF: {pdf_name}.pdf")
    print(f"  Extracted grades: {sorted(normalized.keys())}")
    
    if json_name not in existing_data:
        print(f"  WARNING: {json_name} not in existing data!")
        continue
    
    changes = []
    for entry in existing_data[json_name]:
        # entry = [dienstgrad, besGruppe, grundbezuege, famZuschlag, vl, ...]
        dienstgrad = entry[0]
        bes_gruppe = entry[1]  # e.g. "A7", "A13+"
        old_grundbezuege = entry[2]
        
        # Normalize bes_gruppe for lookup
        lookup_key = bes_gruppe.replace(' ', '')
        
        if lookup_key in normalized:
            new_grundbezuege = normalized[lookup_key]
            diff = round(new_grundbezuege - old_grundbezuege, 2)
            if abs(diff) > 0.01:
                changes.append({
                    'dienstgrad': dienstgrad,
                    'bes_gruppe': bes_gruppe,
                    'old': old_grundbezuege,
                    'new': new_grundbezuege,
                    'diff': diff,
                    'pct': round(diff / old_grundbezuege * 100, 2)
                })
                print(f"  ⚡ {bes_gruppe:6s} {dienstgrad:50s} {old_grundbezuege:>10.2f} → {new_grundbezuege:>10.2f}  ({diff:+.2f}, {diff/old_grundbezuege*100:+.1f}%)")
            else:
                print(f"  ✓  {bes_gruppe:6s} {old_grundbezuege:>10.2f} = {new_grundbezuege:>10.2f}")
        else:
            print(f"  ?  {bes_gruppe:6s} {old_grundbezuege:>10.2f} (kein neuer Wert im PDF gefunden)")
    
    if changes:
        all_changes[json_name] = changes
    else:
        print(f"  → Keine Änderungen")

print(f"\n{'='*80}")
print(f"ZUSAMMENFASSUNG: {len(all_changes)} Bundesländer mit Änderungen")
for state, changes in all_changes.items():
    print(f"  {state}: {len(changes)} Änderungen")
    for c in changes:
        print(f"    {c['bes_gruppe']}: {c['old']:.2f} → {c['new']:.2f} ({c['diff']:+.2f}, {c['pct']:+.1f}%)")
