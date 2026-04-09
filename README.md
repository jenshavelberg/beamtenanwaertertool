# Beamtenanwärter-Tool – Vorsorgeanalyse

Interaktives Web-Tool zur Vorsorgeanalyse für Beamtenanwärter in Deutschland. Berechnet Besoldung, Beihilfeansprüche, Versorgungslücken und Versicherungsbedarf – für alle 16 Bundesländer und den Bund.

**[→ Live-Demo](https://vfm.github.io/beamtenanwaertertool/)**

## Features

- Besoldungsberechnung nach Bundesland und Dienstgrad
- Beihilfesätze und -berechtigung je nach Familienstand
- Versorgungslücken-Analyse (Dienstunfähigkeit, Hinterbliebene, Rente)
- Handlungsempfehlungen für Versicherungsprodukte
- Responsive Design – funktioniert auf Desktop und Mobil

## Projektstruktur

```
├── index.html              # Die komplette Web-App (standalone)
├── data/
│   └── besoldung_compact_v2.json  # Besoldungsdaten (Zwischen-Datei für Updates)
├── scripts/
│   ├── download_pdfs.py    # Lädt Besoldungstabellen-PDFs herunter
│   ├── update_hessen_v2.py # Aktualisiert Hessen-Daten (Template für andere BL)
│   └── update_index_html.py # Schreibt aktualisierte Daten in index.html
├── LOGIK.md                # Dokumentation der Berechnungslogik
└── .github/workflows/      # GitHub Pages Deployment
```

Die Besoldungsdaten sind direkt in `index.html` eingebettet – keine externen Abhängigkeiten zur Laufzeit.

## Lokale Entwicklung

```bash
# Einfach index.html im Browser öffnen oder:
python3 -m http.server 8000
```

## Daten aktualisieren

```bash
# 1. Neue PDFs herunterladen
python3 scripts/download_pdfs.py

# 2. Bundesland-Daten aktualisieren (z.B. Hessen)
python3 scripts/update_hessen_v2.py

# 3. Aktualisierte Daten in index.html einbetten
python3 scripts/update_index_html.py
```

## Lizenz

MIT
