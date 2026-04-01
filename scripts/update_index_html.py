"""Replace BESOLDUNG_DATA in index.html with updated JSON.
Run from project root: python scripts/update_index_html.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Read updated data
with open(ROOT / 'data' / 'besoldung_compact_v2.json', 'r') as f:
    data = json.load(f)

# Create compact JSON string (matching original format)
new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

# Read index.html
with open(ROOT / 'index.html', 'r') as f:
    html = f.read()

# Replace BESOLDUNG_DATA assignment
pattern = r'(const BESOLDUNG_DATA = ){.*?};'
replacement = f'\\1{new_json};'
new_html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)

if count == 1:
    with open(ROOT / 'index.html', 'w') as f:
        f.write(new_html)
    print(f"index.html aktualisiert (BESOLDUNG_DATA ersetzt)")
    
    # Verify
    match = re.search(r'const BESOLDUNG_DATA = ({.*?});', new_html, re.DOTALL)
    if match:
        verify = json.loads(match.group(1))
        print(f"Verfizierung: {len(verify)} Bundesländer")
        print(f"Hessen A6 grundbezuege: {verify['Hessen'][0][2]} (erwartet: 1515.38)")
        print(f"Hessen A6 famZuschlag: {verify['Hessen'][0][3]} (erwartet: 172.10)")
        print(f"Bayern A7 grundbezuege: {verify['Bayern'][5][2]} (unverändert: 1509.93)")
else:
    print(f"ERROR: {count} replacements made (expected 1)")
