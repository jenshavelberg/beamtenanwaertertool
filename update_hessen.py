"""
Update Hessen Besoldungsdaten with new values from Dec 2025 PDF.
Recalculates taxes using calibrated approach matching existing data methodology.
"""
import json
import math

# ── 2025 Einkommensteuer-Formel (§ 32a EStG, Inflationsausgleichsgesetz) ──
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

def calc_monthly_taxes(monthly_brutto, kv_rate=0.213, kirchensteuer_rate=0.09):
    """
    Calculate monthly Lohnsteuer, Soli, Kirchensteuer for Beamte (StKl I or IV).
    
    Deduction model calibrated against existing data:
    - Werbungskostenpauschale: 1,230€/year
    - Sonderausgabenpauschale: 36€/year  
    - Vorsorgepauschale: ~20% of annual gross (calibrated against existing Hessen data)
    """
    annual_gross = monthly_brutto * 12
    
    # Deductions
    wk = 1230  # Werbungskosten-Pauschbetrag
    sap = 36   # Sonderausgaben-Pauschbetrag
    vp = annual_gross * 0.20  # Vorsorgepauschale (calibrated: ~20% for Beamte)
    
    zve = max(0, annual_gross - wk - sap - vp)
    zve = math.floor(zve)  # Round down to full Euro
    
    annual_est = est_2025(zve)
    monthly_lst = round(annual_est / 12, 2)
    
    # Solidaritätszuschlag: 5.5% of LSt, but Freigrenze 18,130€ (annual ESt)
    # For our income range, annual ESt is always well below this → Soli = 0
    monthly_soli = 0.0
    
    # Kirchensteuer: 9% of Lohnsteuer (Hessen uses 9%)
    monthly_kist = round(monthly_lst * kirchensteuer_rate, 2)
    
    # GKV-Vergleichswert
    kv_betrag = round(monthly_brutto * kv_rate, 2)
    
    return monthly_lst, monthly_soli, monthly_kist, kv_betrag

# ── New Hessen values from PDF (gültig ab 01.12.2025) ──
NEW_HESSEN_GRUNDBEZUEGE = {
    'A6': 1515.38,
    'A7': 1515.38,
    'A8': 1515.38,
    'A9': 1586.89,
    'A10': 1586.89,
    'A11': 1586.89,
    'A12': 1772.02,
    'A13': 1814.17,
    'A13+': 1860.41,
    'R1': 1860.41,
}

NEW_HESSEN_FAM_ZUSCHLAG = 172.10  # Stufe 1, was 163.13
VL = 6.65

# Load existing data
with open('besoldung_compact_v2.json', 'r') as f:
    data = json.load(f)

# ── Verify calculation approach against existing data first ──
print("=== KALIBRIERUNG: Bestehende Hessen-Werte nachrechnen ===")
for entry in data['Hessen']:
    dienstgrad, bes_gruppe, grundbezuege, famZuschlag, vl = entry[0], entry[1], entry[2], entry[3], entry[4]
    old_lst_l, old_soli_l, old_kist_l = entry[5], entry[6], entry[7]
    old_lst_v, old_soli_v, old_kist_v = entry[8], entry[9], entry[10]
    old_kv_l, old_kv_v = entry[11], entry[12]
    
    brutto_l = grundbezuege + vl
    brutto_v = grundbezuege + famZuschlag + vl
    
    calc_lst_l, calc_soli_l, calc_kist_l, calc_kv_l = calc_monthly_taxes(brutto_l)
    calc_lst_v, calc_soli_v, calc_kist_v, calc_kv_v = calc_monthly_taxes(brutto_v)
    
    diff_l = abs(calc_lst_l - old_lst_l)
    diff_v = abs(calc_lst_v - old_lst_v)
    status = "✓" if diff_l < 1.0 and diff_v < 1.0 else "⚠"
    
    print(f"  {status} {bes_gruppe:5s} LSt_l: alt={old_lst_l:6.2f} calc={calc_lst_l:6.2f} (Δ={diff_l:.2f})  "
          f"LSt_v: alt={old_lst_v:6.2f} calc={calc_lst_v:6.2f} (Δ={diff_v:.2f})  "
          f"KV_l: alt={old_kv_l:.2f} calc={calc_kv_l:.2f}")

# ── Calculate new values for Hessen ──
print(f"\n=== NEUE HESSEN-WERTE (gültig ab 01.12.2025) ===")
print(f"Familienzuschlag Stufe 1: {NEW_HESSEN_FAM_ZUSCHLAG:.2f}€ (vorher: 163.13€)")
print()

new_hessen_data = []
for entry in data['Hessen']:
    dienstgrad = entry[0]
    bes_gruppe = entry[1]
    old_grundbezuege = entry[2]
    
    lookup = bes_gruppe.replace(' ', '')
    if lookup in NEW_HESSEN_GRUNDBEZUEGE:
        new_grundbezuege = NEW_HESSEN_GRUNDBEZUEGE[lookup]
    else:
        new_grundbezuege = old_grundbezuege
        print(f"  WARNING: No new value for {bes_gruppe}, keeping old value")
    
    new_famzuschlag = NEW_HESSEN_FAM_ZUSCHLAG
    
    brutto_l = new_grundbezuege + VL
    brutto_v = new_grundbezuege + new_famzuschlag + VL
    
    lst_l, soli_l, kist_l, kv_l = calc_monthly_taxes(brutto_l)
    lst_v, soli_v, kist_v, kv_v = calc_monthly_taxes(brutto_v)
    
    new_entry = [
        dienstgrad,
        bes_gruppe,
        round(new_grundbezuege, 2),
        round(new_famzuschlag, 2),
        VL,
        lst_l, soli_l, kist_l,
        lst_v, soli_v, kist_v,
        kv_l, kv_v,
    ]
    new_hessen_data.append(new_entry)
    
    diff_gb = new_grundbezuege - old_grundbezuege
    print(f"  {bes_gruppe:5s} {dienstgrad:55s}")
    print(f"         Grundbezüge: {old_grundbezuege:>9.2f} → {new_grundbezuege:>9.2f}  ({diff_gb:+.2f})")
    print(f"         FamZuschlag: {entry[3]:>9.2f} → {new_famzuschlag:>9.2f}")
    print(f"         LSt ledig:   {entry[5]:>9.2f} → {lst_l:>9.2f}")
    print(f"         LSt verh:    {entry[8]:>9.2f} → {lst_v:>9.2f}")
    print(f"         KV ledig:    {entry[11]:>9.2f} → {kv_l:>9.2f}")
    print(f"         KV verh:     {entry[12]:>9.2f} → {kv_v:>9.2f}")

# ── Update data ──
data['Hessen'] = new_hessen_data

# ── Write updated JSON ──
result = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
with open('besoldung_compact_v2.json', 'w') as f:
    f.write(result)

print(f"\n=== FERTIG ===")
print(f"besoldung_compact_v2.json aktualisiert ({len(result)} chars)")
