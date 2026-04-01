# Beamtenanwärter-Tool – Vorsorgeanalyse

Interaktives Web-Tool zur Vorsorgeanalyse für Beamtenanwärter in Deutschland. Berechnet Besoldung, Beihilfeansprüche, Versorgungslücken und Versicherungsbedarf – für alle 16 Bundesländer und den Bund.

**[→ Live-Demo](https://jens.github.io/beamtenanwaertertool/)**

## Features

- Besoldungsberechnung nach Bundesland und Dienstgrad
- Beihilfesätze und -berechtigung je nach Familienstand
- Versorgungslücken-Analyse (Dienstunfähigkeit, Hinterbliebene, Rente)
- Handlungsempfehlungen für Versicherungsprodukte
- Responsive Design – funktioniert auf Desktop und Mobil

## Technik

Statische Single-Page-Anwendung – reines HTML/CSS/JavaScript, keine Build-Tools nötig.

| Datei | Beschreibung |
|---|---|
| `index.html` | Die komplette Web-App |
| `besoldung_compact_v2.json` | Besoldungsdaten aller Bundesländer (kompakt) |
| `LOGIK.md` | Vollständige Dokumentation der Berechnungslogik |

### Hilfsskripte (Python)

| Skript | Beschreibung |
|---|---|
| `download_pdfs.py` | Lädt Besoldungstabellen als PDF herunter |
| `extract_data.py` | Extrahiert Daten aus den PDFs |
| `compact_data_v2.py` | Komprimiert die Rohdaten |
| `update_hessen_v2.py` | Aktualisiert Hessen-spezifische Daten |
| `update_index_html.py` | Bettet Besoldungsdaten in index.html ein |

## Lokale Entwicklung

```bash
# Einfach index.html im Browser öffnen oder:
python3 -m http.server 8000
```

## Daten aktualisieren

```bash
python3 download_pdfs.py
python3 extract_data.py
python3 compact_data_v2.py
python3 update_index_html.py
```

## Lizenz

MIT
