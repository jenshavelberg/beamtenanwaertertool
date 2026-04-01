"""
Update Hessen Besoldungsdaten with new values from Dec 2025 PDF.
Uses 2025 ESt formula (§32a EStG, Inflationsausgleichsgesetz).
Run from project root: python scripts/update_hessen_v2.py
"""
import json
import math
from pathlib import Path

# ── 2025 Einkommensteuer-Formel (§ 32a EStG) ──
def est_2025(zve):
    """Calculate annual Einkommensteuer for 2025."""
    if zve <= 12096:
        return 0
    elif zve <= 17443:
        y = (zve - 12096) / 10000
        return math.floor((922.98 * y + 1400) * y)
    elif zve <= 66760:
        z = (zve - 17443) / 10000
        return math.floor((176.75 * z + 2397) * z + 1025.38)
    elif zve <= 277825:
        return math.floor(0.42 * zve - 10637.26)
    else:
        return math.floor(0.45 * zve - 18972.21)

def calc_monthly_lst(monthly_brutto):
    """
    Calculate monthly Lohnsteuer for Beamte (StKl I or IV).
    Calibrated deduction model: ~20% Vorsorgepauschale + standard deductions.
    """
    annual_gross = monthly_brutto * 12
    vp = annual_gross * 0.20
    zve = max(0, annual_gross - 1230 - 36 - vp)
    zve = math.floor(zve)
    annual_est = est_2025(zve)
    return round(annual_est / 12, 2)

# ── New Hessen values from PDF (gültig ab 01.12.2025) ──
NEW_GRUNDBEZUEGE = {
    'A6': 1515.38, 'A7': 1515.38, 'A8': 1515.38,
    'A9': 1586.89, 'A10': 1586.89, 'A11': 1586.89,
    'A12': 1772.02,
    'A13': 1814.17,
    'A13+': 1860.41,
    'R1': 1860.41,
}
NEW_FAM_ZUSCHLAG = 172.10  # Stufe 1 (was 163.13)
VL = 6.65
KIRCHENSTEUER_RATE = 0.09  # Hessen: 9%
KV_RATE = 0.213  # GKV-Vergleichssatz

ROOT = Path(__file__).resolve().parent.parent

# Load original data
with open(ROOT / 'data' / 'besoldung_compact_v2.json', 'r') as f:
    data = json.load(f)

# ── First: Calibration check on OLD data ──
print("=" * 70)
print("KALIBRIERUNG: Alte Hessen-Werte nachrechnen (2025 ESt-Formel)")
print("=" * 70)
for entry in data['Hessen']:
    dienstgrad, bg, grundbez, famZ, vl = entry[0], entry[1], entry[2], entry[3], entry[4]
    old_lst_l, old_lst_v = entry[5], entry[8]
    
    brutto_l = grundbez + vl
    brutto_v = grundbez + famZ + vl
    calc_lst_l = calc_monthly_lst(brutto_l)
    calc_lst_v = calc_monthly_lst(brutto_v)
    
    dl = abs(calc_lst_l - old_lst_l)
    dv = abs(calc_lst_v - old_lst_v)
    ok = "✓" if dl < 1.0 and dv < 1.0 else "⚠"
    print(f"  {ok} {bg:5s}  LSt_l: orig={old_lst_l:6.2f} calc={calc_lst_l:6.2f} (Δ={dl:.2f})  "
          f"LSt_v: orig={old_lst_v:6.2f} calc={calc_lst_v:6.2f} (Δ={dv:.2f})")

# ── Calculate and apply new Hessen values ──
print(f"\n{'='*70}")
print(f"UPDATE: Hessen Besoldungsdaten (gültig ab 01.12.2025)")
print(f"  Anwärtergrundbetrag: aktualisiert aus Besoldungstabelle_Hessen_Neuverbeamtung")
print(f"  Familienzuschlag Stufe 1: 163.13€ → 172.10€")
print(f"{'='*70}\n")

new_hessen = []
for entry in data['Hessen']:
    dienstgrad = entry[0]
    bes_gruppe = entry[1]
    old_grundbez = entry[2]
    old_famZ = entry[3]
    
    lookup = bes_gruppe.replace(' ', '')
    new_grundbez = NEW_GRUNDBEZUEGE.get(lookup, old_grundbez)
    new_famZ = NEW_FAM_ZUSCHLAG
    
    # Calculate new tax values
    brutto_l = new_grundbez + VL
    brutto_v = new_grundbez + new_famZ + VL
    
    lst_l = calc_monthly_lst(brutto_l)
    soli_l = 0.0  # Always 0 for Anwärter income range
    kist_l = round(lst_l * KIRCHENSTEUER_RATE, 2)
    
    lst_v = calc_monthly_lst(brutto_v)
    soli_v = 0.0
    kist_v = round(lst_v * KIRCHENSTEUER_RATE, 2)
    
    kv_l = round(brutto_l * KV_RATE, 2)
    kv_v = round(brutto_v * KV_RATE, 2)
    
    new_entry = [
        dienstgrad, bes_gruppe,
        round(new_grundbez, 2), round(new_famZ, 2), VL,
        lst_l, soli_l, kist_l,
        lst_v, soli_v, kist_v,
        kv_l, kv_v,
    ]
    new_hessen.append(new_entry)
    
    diff = new_grundbez - old_grundbez
    netto_l_old = old_grundbez + entry[4] - entry[5] - entry[6] - entry[7]
    netto_l_new = brutto_l - lst_l - soli_l - kist_l
    netto_v_old = old_grundbez + old_famZ + entry[4] - entry[8] - entry[9] - entry[10]
    netto_v_new = brutto_v - lst_v - soli_v - kist_v
    
    print(f"  {bes_gruppe:5s} {dienstgrad}")
    print(f"        Grundbezüge: {old_grundbez:>9.2f} → {new_grundbez:>9.2f}  ({diff:+.2f}, {diff/old_grundbez*100:+.1f}%)")
    print(f"        FamZuschlag: {old_famZ:>9.2f} → {new_famZ:>9.2f}")
    print(f"        Netto (led): {netto_l_old:>9.2f} → {netto_l_new:>9.2f}")
    print(f"        Netto (ver): {netto_v_old:>9.2f} → {netto_v_new:>9.2f}")
    print()

# Apply update
data['Hessen'] = new_hessen

# Write
result = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
with open(ROOT / 'data' / 'besoldung_compact_v2.json', 'w') as f:
    f.write(result)

print(f"besoldung_compact_v2.json aktualisiert ({len(result)} chars)")
print(f"Nur Hessen wurde geändert. Alle anderen {len(data)-1} Bundesländer unverändert.")
