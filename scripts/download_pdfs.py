import requests, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.makedirs(ROOT / 'pdfs', exist_ok=True)

base = 'https://www.dbb.de'
pdfs = {
    'Bund': '/fileadmin/user_upload/globale_elemente/pdfs/2023/231207_Besoldungstabelle_Bund_2024-03.pdf',
    'Baden-Wuerttemberg': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Baden-Wuerttemberg_01_02_2025.pdf',
    'Bayern': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Bayern_01_02_2025.pdf',
    'Berlin': '/fileadmin/user_upload/globale_elemente/pdfs/2026/Besoldungstabellen/260129_Besoldungstabelle_Berlin.pdf',
    'Brandenburg': '/fileadmin/user_upload/globale_elemente/pdfs/2024/besoldungstabellen/202407_Brandenburg.pdf',
    'Bremen': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Bremen_01_02_2025.pdf',
    'Hamburg': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Hamburg-Neuverbeamtung_01_02_2025.pdf',
    'Hessen': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/2025-12-01_Hessen_Neuverbeamtung.pdf',
    'Mecklenburg-Vorpommern': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Mecklenburg-Vorpommern_01_02_2025.pdf',
    'Niedersachsen': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Niedersachsen_01_02_2025.pdf',
    'Nordrhein-Westfalen': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Nordrhein-Westfalen_01_02_2025.pdf',
    'Rheinland-Pfalz': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/250402_Besoldungstabelle_Rheinland-Pfalz_02_2025_v.3.pdf',
    'Saarland': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Saarland_01_02_2025.pdf',
    'Sachsen': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Sachsen_01_02_2025.pdf',
    'Sachsen-Anhalt': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Sachsen-Anhalt_01_02_2025.pdf',
    'Schleswig-Holstein': '/fileadmin/user_upload/globale_elemente/pdfs/2024/besoldungstabellen/202411_Schleswig-Holstein.pdf',
    'Thueringen': '/fileadmin/user_upload/globale_elemente/pdfs/2025/Besoldungstabellen/Besoldungstabelle_Thueringen_01_02_2025.pdf',
}

for name, path in pdfs.items():
    url = base + path
    fname = ROOT / 'pdfs' / f'{name}.pdf'
    if not os.path.exists(fname):
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(fname, 'wb') as f:
                f.write(r.content)
            print(f'OK: {name} ({len(r.content)} bytes)')
        else:
            print(f'FAIL: {name} -> {r.status_code}')
    else:
        print(f'EXISTS: {name}')
