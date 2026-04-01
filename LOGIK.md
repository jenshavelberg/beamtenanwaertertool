# Beamtenanwärter-Tool – Vollständige Logik-Dokumentation

> **Quelle:** `Beamtenanwärter-Tool.xlsx` (Stand: 25.04.2025)  
> **Zweck:** Vorsorgeanalyse für Beamtenanwärter – Berechnung von Besoldung, Beihilfeansprüchen, Versorgungslücken und Versicherungsbedarf

---

## 1. Überblick & Tabellenblätter

| Blatt | Zweck |
|---|---|
| **Dateneingabe** | Eingabeformular (Name, Geburtsdatum, Bundesland, Dienstgrad, Familienstand, Versicherungsprodukte) |
| **Beamtenvorsorge** | Ausgabe/Präsentation der Vorsorgeanalyse (PDF-fähig) |
| **Berechnung** | Kernlogik: 17 Besoldungstabellen, Beihilfe-Berechnung, Versorgungslücken, Diagrammdaten |
| **Beihilfeberechtigung** | Nachschlagetabelle: Einkommensgrenzen für Ehegatten-Beihilfe je Bundesland |
| **Daten** | Schnittstelle für externen Datenimport (156 Spaltenheader für CRM/Maklerverwaltung) |
| **System** | Konfiguration: Vertriebsschiene, Textbausteine |
| **Logo** | Dienstgrad-Liste mit Bild-Zuordnung |
| **OK** | Interner Hinweis |

---

## 2. Eingabeparameter (Blatt: Dateneingabe)

### 2.1 Persönliche Daten

| Feld | Typ | Beispielwert | Beschreibung |
|---|---|---|---|
| **Name** | Text | `Lisa Lehrerin` | Vor- und Nachname |
| **Geburtsdatum** | Datum | `14.01.1994` | Geburtsdatum (TT.MM.JJJJ) |
| **Bundesland** | Auswahl (Index) | `Bayern` | Eines von 17 Bundesländern + Bundesbeihilfe |
| **Dienstgrad** | Auswahl (Index) | `LAA Real- u. So. (A13)` | Eines von 15 Dienstgraden |
| **Familienstand** | Auswahl (Index) | `ledig` / `verheiratet` | Steuerklasse I (ledig) oder IV (verheiratet) |
| **Ehegatte beihilfeberechtigt** | Auswahl | `Ja` / `Nein` | Relevant für Beihilfesätze |
| **Anzahl der Kinder** | Auswahl (0-4+) | `2` | Beeinflusst Beihilfesätze |

### 2.2 Versicherungsprodukte (manuell eingegeben)

| Bereich | Felder |
|---|---|
| **Dienstunfähigkeit** | Beitrag (€/Monat), Monatsrente (€), Beitragsbefreiung bis Lebensjahr, Rückzahlung Fondsrente |
| **Unfall** | Beitrag (€/Monat), Leistung bei Vollinvalidität (€), Leistung bei Unfalltod (€) |
| **Alter** | Beitrag (€/Monat), Riester-/Privatrente (€/Monat) |
| **Krankheit** | Beitrag (€/Monat), Stationär-Absicherung (%), Ambulant-Absicherung (%), KH-Tagegeld, Kurtagegeld, Beihilfeergänzung |
| **Haftpflicht** | Beitrag (€/Monat), Privat- und Amtshaftpflicht |

---

## 3. Auswahl-Indizes (Steuerung der Berechnung)

Die gesamte Berechnung wird durch **drei Auswahl-Indizes** gesteuert:

### 3.1 Bundesland-Index (`Berechnung!C370`)

| Index | Bundesland |
|---|---|
| 1 | (Bitte auswählen) |
| 2 | Baden-Württemberg |
| 3 | Bayern |
| 4 | Berlin |
| 5 | Brandenburg |
| 6 | Bremen |
| 7 | Hamburg |
| 8 | Hessen |
| 9 | Mecklenburg-Vorpommern |
| 10 | Niedersachsen |
| 11 | Nordrhein-Westfalen |
| 12 | Rheinland-Pfalz |
| 13 | Saarland |
| 14 | Sachsen |
| 15 | Sachsen-Anhalt |
| 16 | Schleswig-Holstein |
| 17 | Thüringen |
| 18 | Bundesbeihilfe |

### 3.2 Dienstgrad-Index (`Berechnung!D4`)

| Index | Dienstgrad | Besoldungsgruppe |
|---|---|---|
| 1 | (Bitte auswählen) | – |
| 2 | Oberamtsgehilfe, Wachtmeister | A3 |
| 3 | Hauptamtsgehilfe, Oberwachtmeister | A3 |
| 4 | Amtsmeister, Hauptwachtmeister | A4 |
| 5 | Ass. Anwärter | A5 |
| 6 | Ass. Anwärter | A6 |
| 7 | Polizeimeister-/Ass.-Anwärter | A7 |
| 8 | Ass. Anwärter | A8 |
| 9 | Polizeikommissar-/Inspektor-/Finanz-Anwärter | A9 |
| 10 | Forst-Ing., Inspektor-/Finanz-Anwärter | A10 |
| 11 | Inspektor-/Finanz-Anwärter | A11 |
| 12 | LAA GHS | A12 |
| 13 | LAA Real- u. So. | A13 |
| 14 | Referendar Gymnasium | A13+ |
| 15 | Richter | R1 |

### 3.3 Familienstand-Index (`Berechnung!C320`)

| Index | Familienstand | Steuerklasse |
|---|---|---|
| 1 | (bitte auswählen) | – |
| 2 | ledig | I |
| 3 | verheiratet | IV |

### 3.4 Weitere Auswahl-Indizes

| Index-Zelle | Optionen | Beschreibung |
|---|---|---|
| `C325` (Kinder) | 1=bitte auswählen, 2=0, 3=1, 4=2, 5=3, 6=4+ | Anzahl der Kinder |
| `E326` (Inklusivleistungen) | 1=ohne freie Arztwahl/2-Bett, 2=freie Arztwahl/2-Bett, 3=freie Arztwahl/1-Bett, 4=Kurtagegeld | Wahlleistungen Krankenhaus |
| `H326` (Krankheit-Typ) | 1=aktive KV, 2=kleine Anwartschaft, 3=große Anwartschaft | Art der Krankenversicherung |
| `M325` (Ehepartner beihilfeberechtigt) | 1=bitte auswählen, 2=Ja, 3=Nein | Ehepartner Beihilfestatus |
| `C428` (DU-Lebensjahr) | 1=bitte wählen, 2=55, 3=56, ..., 14=67 | Beitragsbefreiung bis Lebensjahr |
| `C444` (Altersvorsorge-Typ) | 1=Riester-Rente, 2=Privatrente | Art der Altersvorsorge |

---

## 4. Besoldungsberechnung (Kernlogik)

### 4.1 Wertetabelle (Named Range: `Wertetabelle`)

Die `Wertetabelle` umfasst `Berechnung!A7:W310` und enthält **17 identische Tabellen** (eine pro Bundesland + Bundesbeihilfe), jeweils mit 15 Dienstgraden.

**Struktur jeder Tabelle:**

Jede Bundesland-Tabelle beginnt alle 18 Zeilen und hat folgende Spaltenstruktur:

| Spalte | Ledig | Verheiratet | Beschreibung |
|---|---|---|---|
| A | Lookup-Key | – | `Bundesland & Dienstgrad` (Verkettung) |
| B | Anwärter-Bezeichnung | – | Name des Dienstgrads |
| C | Familienstand | – | `ledig` |
| D | Besoldungsgruppe | – | z.B. `A9`, `A13`, `R1` |
| **E** | Grundbezüge | – | Festwert in € |
| **F** | Familienzuschlag | – | Festwert in € (nur bei verheiratet relevant) |
| **G** | VL | – | Vermögenswirksame Leistungen (meist 6,65 €) |
| **H** | steuerpfl. Bruttobezüge | – | `= E + G` (ledig) |
| I | Steuerklasse | – | `I` (ledig) |
| **J** | Lohnsteuer | – | Festwert in € |
| **K** | Soli.-Zuschlag | – | Festwert in € (meist 0) |
| **L** | Kirchensteuer 9% | – | Festwert in € |
| **M** | Steuer gesamt | – | `= J + K + L` |
| **N** | Nettobezüge | – | `= H - M` |
| **O** | gesetzl. KV* | – | `= H × KV-Satz%` (Vergleichswert) |
| **P** | – | steuerpfl. Bruttobezüge | `= E + F + G` (verheiratet) |
| Q | – | Steuerklasse | `IV` (verheiratet) |
| **R** | – | Lohnsteuer | Festwert in € |
| **S** | – | Soli.-Zuschlag | Festwert in € |
| **T** | – | Kirchensteuer 9% | Festwert in € |
| **U** | – | Steuer gesamt | `= R + S + T` |
| **V** | – | Nettobezüge | `= P - U` |
| **W** | – | gesetzl. KV* | `= P × KV-Satz%` (Vergleichswert) |

### 4.2 Startzeilen der Bundesland-Tabellen

| Bundesland | Startzeile (Header) | Datenzeilen |
|---|---|---|
| Baden-Württemberg | 4 | 7–20 |
| Bayern | 22 | 25–38 |
| Berlin | 40 | 43–56 |
| Brandenburg | 58 | 61–74 |
| Bremen | 76 | 79–92 |
| Hamburg | 94 | 97–110 |
| Hessen | 112 | 115–128 |
| Mecklenburg-Vorpommern | 130 | 133–146 |
| Niedersachsen | 148 | 151–164 |
| Nordrhein-Westfalen | 166 | 169–182 |
| Rheinland-Pfalz | 184 | 187–200 |
| Saarland | 202 | 205–218 |
| Sachsen | 220 | 223–236 |
| Sachsen-Anhalt | 238 | 241–254 |
| Schleswig-Holstein | 256 | 259–272 |
| Thüringen | 274 | 277–290 |
| Bundesbeihilfe | 294 | 297–310 |

### 4.3 Berechnungsformeln

```
Brutto (ledig)       = Grundbezüge + VL
Brutto (verheiratet) = Grundbezüge + Familienzuschlag + VL
Steuer gesamt        = Lohnsteuer + Soli.-Zuschlag + Kirchensteuer (9%)
Netto                = Brutto - Steuer gesamt
Gesetzl. KV (Vergl.) = Brutto × KV-Satz
```

### 4.4 Gesetzliche KV-Sätze je Bundesland (Vergleichswert)

| KV-Satz | Bundesländer |
|---|---|
| **14,0%** | Hamburg (Grundbesoldung A3-A4) |
| **17,45%** | Brandenburg (A3), Bremen (A3), Rheinland-Pfalz (A3), Sachsen (A3-A4), Sachsen-Anhalt (A3) |
| **18,55%** | Bundesbeihilfe (A3) |
| **18,95%** | Berlin (A3-A4), Rheinland-Pfalz (A4), Schleswig-Holstein (A3-A4), Thüringen (A3-A4) |
| **19,25%** | Hessen (nur verheiratet, bestimmte Grade) |
| **19,6%** | Hessen (A8), Sachsen (A5) |
| **21,3%** | Alle Bundesländer ab ca. A5/A7 aufwärts (Standardsatz) |

> **Hinweis:** Die KV-Sätze sind **Vergleichswerte**, um die Ersparnis der privaten Beihilfe-KV gegenüber der gesetzlichen KV darzustellen.

---

## 5. Lookup-Logik (Datenabruf)

### 5.1 VLOOKUP über Wertetabelle

Der Schlüssel für den Lookup ist die **Verkettung von Bundesland + Dienstgrad-Text**:

```
Lookup-Key = Bundesland (z.B. "Bayern") & Dienstgrad (z.B. "LAA Real- u. So. (A13)")
→ "BayernLAA Real- u. So. (A13)"
```

Die Abfrage erfolgt per `VLOOKUP` in der Named Range `Wertetabelle` (`Berechnung!A7:W310`):

```
VLOOKUP(Bundesland & Dienstgrad, Wertetabelle, Spalten-Nr, FALSE)
```

**Spalten-Mapping (Wertetabelle, 1-basiert):**

| Spalte | Nr. | Inhalt |
|---|---|---|
| A | 1 | Lookup-Key |
| B | 2 | Dienstgrad-Text |
| C | 3 | Familienstand |
| D | 4 | Besoldungsgruppe |
| E | 5 | Grundbezüge (ledig) |
| F | 6 | Familienzuschlag |
| G | 7 | VL |
| H | 8 | Brutto (ledig) |
| I | 9 | Steuerklasse (ledig) |
| J | 10 | Lohnsteuer (ledig) |
| K | 11 | Soli (ledig) |
| L | 12 | Kirchensteuer (ledig) |
| M | 13 | Steuer gesamt (ledig) |
| N | 14 | Netto (ledig) |
| O | 15 | gesetzl. KV (ledig) |
| P | 16 | Brutto (verheiratet) |
| Q | 17 | Steuerklasse (verheiratet) |
| R | 18 | Lohnsteuer (verheiratet) |
| S | 19 | Soli (verheiratet) |
| T | 20 | Kirchensteuer (verheiratet) |
| U | 21 | Steuer gesamt (verheiratet) |
| V | 22 | Netto (verheiratet) |
| W | 23 | gesetzl. KV (verheiratet) |

### 5.2 INDEX-basierter Abruf (Zeilen 321-323)

Für die Ausgabe werden die Werte je nach Familienstand in Zeilen 321-323 aufbereitet:

```
Zeile 321: "bitte auswählen" (Fallback)
Zeile 322: Werte für "ledig" → VLOOKUP mit Spalten 2,4,5,0,7,8,14,9,10,11,12,13,15
Zeile 323: Werte für "verheiratet" → VLOOKUP mit Spalten 2,4,5,6,7,16,22,17,18,19,20,21,23
```

Die Ausgabe nutzt dann:
```
INDEX(F321:P323, C320, Spalte)
```

wobei `C320` der Familienstand-Index (1/2/3) ist.

---

## 6. Beihilfe-Berechnung

### 6.1 Beihilfesätze – Standard (alle Bundesländer außer Bremen & Hessen)

| Person | Ambulant/Zahn | Stationär |
|---|---|---|
| Beihilfeberechtigter (≤2 Kinder) | **50%** | **50%** |
| Beihilfeberechtigter (>2 Kinder) | **70%** | **70%** |
| Ehepartner | **70%** | **70%** |
| je Kind | **80%** | **80%** |

**Formel:**
```
Beihilfesatz (Berechtigter) = IF(Kinder > 3, 70%, 50%)
Beihilfesatz (Ehepartner)   = IF(Bundesland ∈ {Bremen, Hessen}, Sonderlogik, 70%)
Beihilfesatz (Kind)          = IF(Bundesland ∈ {Bremen, Hessen}, Sonderlogik, 80%)
```

> **Hinweis zum Kinder-Index:** `C325` ist ein Auswahl-Index (1–6). `C325 > 3` bedeutet mehr als 2 Kinder (da Index 2=0 Kinder, 3=1 Kind, 4=2 Kinder, 5=3 Kinder, 6=4+).

### 6.2 Sonderlogik Bremen (Bundesland-Index = 6)

Bremen berechnet Beihilfesätze dynamisch basierend auf der Anzahl **zusätzlicher Beihilfeberechtigter**:

```
Zusätzlich Beihilfeberechtigte = Ehepartner_beihilfeberechtigt (0 oder 1) 
                                + MAX(0, Kinder - 2)  // Kinder über den Grundwert hinaus

Ambulant-Satz = MIN(Basis 50% + (Zusätzliche × 5%), Obergrenze 70%)
Stationär-Satz = MIN(Basis 50% + (Zusätzliche × 5%), Obergrenze 70%)
```

**Ermittlung Ehepartner:**
```
Ehepartner_beihilfeberechtigt = IF(M325 = 2, 1, 0)   // M325=2 → "Ja"
Kinder_über_Basis = IF(C325 ≤ 2, 0, C325 - 2)         // C325 ist Index (2=0 Kinder)
```

### 6.3 Sonderlogik Hessen (Bundesland-Index = 8)

Hessen nutzt dieselbe Dynamik wie Bremen, aber mit abweichenden Obergrenzen:

```
Ambulant-Satz  = MIN(Basis 50% + (Zusätzliche × 5%), Obergrenze 70%)
Stationär-Satz = MIN(Basis 65% + (Zusätzliche × 5%), Obergrenze 85%)
```

### 6.4 Ambulante vs. Stationäre Beihilfe (Entscheidungslogik)

```
Ambulant (Berechtigter):
  IF Bundesland = Bremen    → Bremen-Satz (dynamisch)
  IF Bundesland = Hessen    → Hessen-Satz (dynamisch)
  ELSE                      → Standard-Satz

Stationär (Berechtigter):
  IF Bundesland = Bremen    → Bremen-Stationär-Satz
  IF Bundesland = Hessen    → Hessen-Stationär-Satz
  ELSE                      → Standard-Satz (gleich wie Ambulant)

Ehepartner:
  IF Bremen & verheiratet   → Basis 50% + 5%
  IF Bremen & nicht verh.   → 0%
  IF Hessen & verheiratet   → Basis 50% + 5% (ambulant) / 65% + 5% (stationär)
  IF Hessen & nicht verh.   → 0%
  ELSE                      → 70%

Kind:
  IF Bremen                 → Bremen-Ambulant-Satz / Bremen-Stationär-Satz
  IF Hessen                 → Hessen-Ambulant-Satz / Hessen-Stationär-Satz
  ELSE                      → 80%
```

### 6.5 KV-Eigenanteil (für Versicherungsvorschlag)

Der **zu versichernde Eigenanteil** berechnet sich als:
```
Eigenanteil = 100% - Beihilfesatz
```

Beispiel: Bei 50% Beihilfe → 50% müssen privat versichert werden.

### 6.6 Wahlleistungen im Krankenhaus (je Bundesland)

| Index | Bundesland | Wahlleistungen beihilfefähig? | Stationär Basis | Stationär mit Wahlleistung |
|---|---|---|---|---|
| 2 | Baden-Württemberg | ja (bei Gehaltsabzug 22€) | 50% | 100% |
| 3 | Bayern | ja | 50% | 50% |
| 4 | Berlin | nein | 50% | 100% |
| 5 | Brandenburg | nein | 50% | 100% |
| 6 | Bremen | nein | 50% | 100% |
| 7 | Hamburg | nein | 50% | 100% |
| 8 | Hessen | ja | 50% | 100% |
| 9 | Mecklenburg-Vorpommern | nein | 50% | 100% |
| 10 | Niedersachsen | nein | 50% | 100% |
| 11 | Nordrhein-Westfalen | ja | 50% | 50% |
| 12 | Rheinland-Pfalz | ja (bei Gehaltsabzug 26€) | 50% | 100% |
| 13 | Saarland | nein | 50% | 100% |
| 14 | Sachsen | ja | 50% | 50% |
| 15 | Sachsen-Anhalt | ja | 50% | 50% |
| 16 | Schleswig-Holstein | nein | 50% | 100% |
| 17 | Thüringen | ja | 50% | 50% |
| 18 | Bundesbeihilfe | ja | 50% | 50% |

---

## 7. Beihilfeberechtigung des Ehegatten

| Bundesland | Einkommensgrenze | Bezugsjahr | KH-Wahlleistungen beihilfefähig? |
|---|---|---|---|
| Bund | 17.000 € | vorletztes KJ | ja |
| Baden-Württemberg | 20.000 € | jeweils in den letzten 3 Jahren (max. 30.000 €) | ja, bei Gehaltsabzug 22 € |
| Bayern | 20.000 € | vorletztes KJ | ja |
| Berlin | 17.000 € | vorletztes KJ | nein |
| Brandenburg | 20.000 € | vorletztes KJ | nein |
| Bremen | 12.000 € | letztes KJ | nein |
| Hamburg | 18.000 € | letztes KJ | nein |
| Hessen | 19.488 € | vorletztes KJ | ja |
| Mecklenburg-Vorpommern | 20.000 € | vorletztes KJ | nein |
| Niedersachsen | 18.000 € | vorletztes KJ | nein |
| Nordrhein-Westfalen | 18.000 € | letztes KJ | ja |
| Rheinland-Pfalz | 17.000 € | vorletztes KJ | ja, bei Gehaltsabzug 26 € |
| Saarland | 16.000 € | letztes KJ | nein |
| Sachsen | 18.000 € | Durchschnitt letzte 3 Jahre | ja |
| Sachsen-Anhalt | 20.000 € | vorletztes KJ | ja |
| Schleswig-Holstein | 20.000 € | vorletztes KJ | nein |
| Thüringen | 18.000 € | vorletztes KJ | ja |

> **Hinweis Rheinland-Pfalz:** Bei Heirat nach 31.12.2011: 17.000 € im VVKJ. Bei Heirat vor 01.01.2012: 20.450 € im VVKJ.

---

## 8. Versorgungslücke bei Dienstunfähigkeit

### 8.1 Risiko-Statistik (für Diagramm)

| Ursache | Häufigkeit |
|---|---|
| Nervenkrankheiten | 31,52% |
| Motorische Erkrankungen | 21,02% |
| Krebs | 15,48% |
| Sonstige | 15,66% |
| Unfälle | 8,98% |
| Herz/Kreislauf | 7,34% |

### 8.2 Versorgungslücke nach Dienstjahren

| Ruhegehaltfähige Dienstjahre | Prozentuale Versorgungslücke |
|---|---|
| 0 | 0% |
| 5 | 0% |
| 6 | 35,00% |
| 19 | 35,00% |
| 20 | 35,88% |
| 25 | 44,84% |
| 30 | 53,81% |
| 35 | 62,76% |
| 40 | 71,75% |

> **Beamtenanwärter haben in den ersten 5 Dienstjahren KEINEN Versorgungsanspruch** bei Dienstunfähigkeit (außer bei Dienstunfall). Ab 6 Jahren greift die Mindestversorgung mit 35% Lücke.

---

## 9. Netto-Berechnung & Gesamtvorschlag

### 9.1 Gesamtbeitrag Vorsorge

```
Vorsorgebeitrag = Beitrag_DU + Beitrag_Unfall + Beitrag_Alter + Beitrag_KV + Beitrag_Haftpflicht
```

### 9.2 Netto zur Verfügung

```
Netto_verfügbar = Nettobezüge - Vorsorgebeitrag - VL_Anlagebeitrag (40 €)
```

### 9.3 Vergleich mit gesetzlicher KV

```
Gesetzl_KV_Beitrag = VLOOKUP(Bundesland & Dienstgrad, Wertetabelle, 15, FALSE)  // ledig
                   = VLOOKUP(Bundesland & Dienstgrad, Wertetabelle, 23, FALSE)  // verheiratet
```

---

## 10. Ausgabe-Texte (dynamisch generiert)

### 10.1 Dienstunfähigkeit-Text
```
IF Lebensjahr gewählt:
  "Leistung Monatliche Rente und Beitragsbefreiung bis zum {Lebensjahr}. Lebensjahr: in den ersten 5 Jahren"
ELSE:
  "" (leer)
```

### 10.2 Altersvorsorge-Text
```
IF Typ = Riester:
  "Monatliche Riester-Rente inklusive Fondsguthaben ca.\n
   (Steigerung durch einkommensbedingte Erhöhung des Eigenbeitrags nicht berücksichtigt)"
IF Typ = Privatrente:
  "Privatrente inklusive Fondsguthaben ca."
```

### 10.3 Krankheits-Text
```
"Bei Krankheit: " & KV-Art (aktive KV / kleine Anwartschaft / große Anwartschaft)
```

### 10.4 Stationäre Behandlung-Text
```
"Stationäre Behandlung und " & Inklusivleistung (Kurtagegeld / freie Arztwahl etc.)
```

---

## 11. Besoldungsdaten (Beispiel: Bayern)

### 11.1 Bayern – ledig (Steuerklasse I)

| Dienstgrad | Bes.Gr. | Grundbezüge | VL | Brutto | Lohnsteuer | Soli | KiSt 9% | Steuer ges. | Netto |
|---|---|---|---|---|---|---|---|---|---|
| Oberamtsgehilfe | A3 | 1.389,33 | 6,65 | 1.395,98 | 0,00 | 0,00 | 0,00 | 0,00 | 1.395,98 |
| Ass. Anwärter | A5 | 1.509,93 | 6,65 | 1.516,58 | 15,08 | 0,00 | 1,20 | 16,28 | 1.500,30 |
| Polizeimeister-Anw. | A7 | 1.509,93 | 6,65 | 1.516,58 | 15,08 | 0,00 | 1,20 | 16,28 | 1.500,30 |
| Inspektor-/Finanz-Anw. | A9 | 1.563,85 | 6,65 | 1.570,50 | 22,33 | 0,00 | 1,78 | 24,11 | 1.546,39 |
| LAA GHS | A12 | 1.703,44 | 6,65 | 1.710,09 | 43,00 | 0,00 | 3,44 | 46,44 | 1.663,65 |
| LAA Real- u. So. | A13 | 1.735,21 | 6,65 | 1.741,86 | 48,00 | 0,00 | 3,84 | 51,84 | 1.690,02 |
| Referendar Gymnasium | A13+ | 1.770,08 | 6,65 | 1.776,73 | 53,75 | 0,00 | 4,30 | 58,05 | 1.718,68 |
| Richter | R1 | 1.770,08 | 6,65 | 1.776,73 | 53,75 | 0,00 | 4,30 | 58,05 | 1.718,68 |

### 11.2 Bayern – verheiratet (Steuerklasse IV)

| Dienstgrad | Bes.Gr. | Grundbezüge | Fam.Zusch. | VL | Brutto | Lohnsteuer | Soli | KiSt 9% | Steuer ges. | Netto |
|---|---|---|---|---|---|---|---|---|---|---|
| Oberamtsgehilfe | A3 | 1.389,33 | 165,59 | 6,65 | 1.561,57 | 21,08 | 0,00 | 1,68 | 22,76 | 1.538,81 |
| Ass. Anwärter | A5 | 1.509,93 | 165,59 | 6,65 | 1.682,17 | 38,66 | 0,00 | 3,09 | 41,75 | 1.640,42 |
| Inspektor-/Finanz-Anw. | A9 | 1.563,85 | 165,59 | 6,65 | 1.736,09 | 47,16 | 0,00 | 3,77 | 50,93 | 1.685,16 |
| LAA GHS | A12 | 1.703,44 | 165,59 | 6,65 | 1.875,68 | 71,00 | 0,00 | 5,68 | 76,68 | 1.799,00 |
| LAA Real- u. So. | A13 | 1.735,21 | 165,59 | 6,65 | 1.907,45 | 76,83 | 0,00 | 6,14 | 82,97 | 1.824,48 |
| Referendar Gymnasium | A13+ | 1.770,08 | 165,59 | 6,65 | 1.942,32 | 83,41 | 0,00 | 6,67 | 90,08 | 1.852,24 |

> **Alle 17 Bundesländer + Bundesbeihilfe haben eigene Tabellen mit abweichenden Grundbezügen und Familienzuschlägen.** Die Berechnungslogik (Formeln) ist identisch.

---

## 12. Systemkonfiguration

### 12.1 Vertriebsschiene (`System!D21`)

| Index | Vertriebsschiene |
|---|---|
| 1 | vfm-Makler |
| 2 | ADMINOVA |
| 3 | vfm-Vermittler |
| 4 | BDF-Version (Bund dt. Forstleute) |

### 12.2 Verwendungszweck (`System!D22`)

| Index | Zweck |
|---|---|
| 1 | IA-Vorlage (InfoAgent-Vorlage) |
| 2 | Einzelprogramm |

---

## 13. Datenfluss-Diagramm

```
                    ┌─────────────────────┐
                    │   DATENEINGABE       │
                    │                     │
                    │ • Name              │
                    │ • Geburtsdatum      │
                    │ • Bundesland-Index  │
                    │ • Dienstgrad-Index  │
                    │ • Familienstand     │
                    │ • Kinder            │
                    │ • Ehepartner-BH     │
                    │ • Versicherungen    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    BERECHNUNG        │
                    │                     │
                    │  ┌───────────────┐  │
                    │  │ Wertetabelle  │  │
                    │  │ (17 BL × 15  │  │
                    │  │  Dienstgrade) │  │
                    │  └───────┬───────┘  │
                    │          │           │
                    │  ┌───────▼───────┐  │
                    │  │ VLOOKUP       │  │
                    │  │ BL+Dienstgrad │  │
                    │  └───────┬───────┘  │
                    │          │           │
                    │  ┌───────▼───────┐  │
                    │  │ Beihilfe-     │  │
                    │  │ Berechnung    │  │
                    │  │ (Std/HB/HE)  │  │
                    │  └───────┬───────┘  │
                    │          │           │
                    │  ┌───────▼───────┐  │
                    │  │ Versorgungs-  │  │
                    │  │ lücke / BU    │  │
                    │  └───────────────┘  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  BEAMTENVORSORGE     │
                    │  (Ausgabe/PDF)       │
                    │                     │
                    │ • Besoldungsübersicht│
                    │ • Beihilfesätze      │
                    │ • Versorgungslücke   │
                    │ • Versicherungs-     │
                    │   vorschlag          │
                    │ • Netto-Berechnung   │
                    └─────────────────────┘
```

---

## 14. Zusammenfassung für Web-Implementierung

### Benötigte Datenstrukturen

1. **Besoldungstabelle** (JSON/DB): 17 Bundesländer × 15 Dienstgrade × 2 Familienstand-Varianten = **510 Datensätze** mit je: Grundbezüge, Familienzuschlag, VL, Lohnsteuer, Soli, Kirchensteuer
2. **Beihilfe-Regeln** (Konfiguration): Standard-Sätze + Sonderregeln Bremen/Hessen
3. **Bundesland-Metadaten**: Wahlleistungen ja/nein, KV-Sätze, Ehegatten-Einkommensgrenzen
4. **Versorgungslücke-Tabelle**: 9 Datenpunkte (Dienstjahre → Lückenprozent)
5. **BU-Risiko-Statistik**: 6 Ursachenkategorien mit Prozentanteilen

### Berechnungsschritte (Algorithmus)

```
1. Eingabe: Bundesland, Dienstgrad, Familienstand, Kinder, Ehepartner-BH
2. Lookup: Besoldungsdaten aus Wertetabelle (Bundesland + Dienstgrad)
3. Wähle Spalten: ledig (E-O) oder verheiratet (E,F,G,P-W)
4. Berechne Beihilfesätze:
   a. Prüfe ob Bremen oder Hessen → Sonderlogik
   b. Sonst: Standardsätze (50%/70%/80%, bzw. 70% bei >2 Kindern)
5. Berechne Eigenanteile: 100% - Beihilfesatz
6. Zeige Versorgungslücke-Diagramm
7. Addiere Versicherungsbeiträge
8. Berechne Netto: Brutto - Steuern - Versicherungsbeiträge - VL
9. Vergleiche mit gesetzlicher KV
```
