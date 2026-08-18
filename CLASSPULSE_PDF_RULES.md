# ClassPulse — PDF Export Rules

Dieses Dokument beschreibt das Design und den Workflow für den PDF-Export.
Bei der PDF-Generierung in Claude immer diese Datei + das JSON-Backup hochladen.

---

## Workflow

1. In der App: **Mehr → Backup herunterladen** (.json Datei)
2. Claude Momentum-Chat öffnen
3. Beide Dateien hochladen: `ClassPulse_Backup_DATUM.json` + `CLASSPULSE_PDF_RULES.md`
4. Schreiben: „Erstell mir die ClassPulse PDF-Exports aus diesem Backup"
5. Claude generiert: Klassenliste (intern) + Detailseiten pro Schüler (für Gespräche)
6. PDF herunterladen — fertig für Zeugniskonferenz oder Elterngespräch

Der Python-Code für die Generierung liegt in `classpulse_export.py` im selben Repo.

---

## Design-Regeln

### Font
- **Montserrat** durchgehend (Regular, SemiBold, Bold, Italic)
- Installiert auf dem Generierungs-Server via `fonts-montserrat`

### Farbpalette (aus Grootmoor Teaching Hub)

| Name        | Hex       | Verwendung                              |
|-------------|-----------|------------------------------------------|
| PRUSSIAN    | `#023A5D` | Titel, linke Border, Hauptakzent         |
| TEAL        | `#1B5E79` | Bereichs-Labels, Notiz-Border            |
| TEAL_LIGHT  | `#E8F2F5` | Notiz-Hintergrund, Key Terms Background  |
| DARK_HEADER | `#44546A` | Tabellen-Header, Abschnitts-Banner       |
| GREY_LIGHT  | `#F5F5F5` | Alternierende Tabellenzeilen             |
| GREY_TEXT   | `#555555` | Metadaten, Datum, Fußzeilen              |
| BLACK       | `#111111` | Fließtext                                |
| GREEN       | `#2D7A4F` | Positive Tendenz                         |
| GREEN_LIGHT | `#E8F5EE` | Hintergrund positive Kacheln             |
| RED         | `#B03A2E` | Negative Tendenz / Förderbedarf          |
| RED_LIGHT   | `#FDECEA` | Hintergrund negative Kacheln             |
| AMBER       | `#8B6914` | Ausgeglichene Tendenz                    |
| AMBER_LIGHT | `#FEF9E7` | Hintergrund ausgeglichene Kacheln        |

### Seitenformat
- DIN A4, Hochformat
- Ränder: 18mm alle Seiten
- Reportlab SimpleDocTemplate

---

## Seite 1 — Klassenliste (intern)

- Überschrift: „ClassPulse" in PRUSSIAN, 18pt Bold
- Untertitel: Kursname · Halbjahr · Lehrkraft, 10pt GREY_TEXT
- Trennlinie: 1.5pt PRUSSIAN
- Label: „KLASSENLISTE — INTERNER ÜBERBLICK" in TEAL, 9pt Bold
- Fußzeile: „Nur für interne Verwendung"

**Tabelle:**
- Header: DARK_HEADER Hintergrund, weiß, 8pt Bold
- Linke Border: 3pt PRUSSIAN auf Namensspalte
- Zeilen alternierend: GREY_LIGHT / weiß
- Inhalt: Zahlen (+X/−Y) + Tendenz-Symbol (↑ → ↓) in Farbe
- Gesamt-Spalte: farbiges Label (über/entspricht/unter Erwartung)

---

## Seiten 2+ — Detailseiten pro Schüler (für Gespräche)

**Keine Zahlen — nur Tendenz-Labels.**

- Name: 14pt Bold PRUSSIAN
- Gesamttendenz: rechts oben, farbig
- Metazeile: Kurs · Halbjahr · Fehlzeiten · HA-Quote
- Trennlinie: 1.5pt PRUSSIAN

**Kriterien-Grid (2 Spalten):**
- Pro Kachel: Kurzname links + Tendenz-Label rechts
- Tendenz-Labels (kein Pfeil, nur Text):
  - „über Erwartung" — GREEN auf GREEN_LIGHT, 3pt GREEN linke Border
  - „entspricht Erwartung" — AMBER auf AMBER_LIGHT, 3pt AMBER linke Border
  - „unter Erwartung" — RED auf RED_LIGHT, 3pt RED linke Border
  - „nicht beobachtet" — GREY_TEXT auf GREY_LIGHT
- Darunter in 7.5pt Italic: „überwiegend positiv" / „ausgeglichen" / „überwiegend schwach"
- Gruppiert nach Bereich (ENGAGEMENT / ARBEITSVERHALTEN / SPRACHE etc.)
- Bereichs-Label: 8pt Bold TEAL, uppercase

**Notizen:**
- Trennlinie 0.5pt GREY_TEXT
- Label: „BEOBACHTUNGEN & NOTIZEN" in TEAL
- Pro Notiz: TEAL_LIGHT Hintergrund, 3pt TEAL linke Border
- Text links (Italic 8.5pt), Datum rechts (7.5pt GREY_TEXT)

**Fußzeile:**
- Disclaimer: „Die Einschätzungen basieren auf pädagogischen Beobachtungen im Unterricht. Über die Gewichtung der Kriterien entscheidet die Lehrkraft in pädagogischer Verantwortung (Grootmoor-Bogen)."
- Letzte Zeile: „ClassPulse · Kursname · Export Datum · Lehrkraft: Name"

---

## Bewertungsbögen

### Fremdsprachen (Englisch: 8a Englisch, 12. Kl. Englisch)
8 Kriterien aus dem Grootmoor Fremdsprachen-Bogen:

| ID   | Kurzname       | Bereich          |
|------|----------------|------------------|
| fs1  | Beteiligung    | Engagement       |
| fs2  | Beiträge       | Engagement       |
| fs3  | HA & Heft      | Arbeitsverhalten |
| fs4  | Verantwortung  | Arbeitsverhalten |
| fs5  | Vokabeln/Gram. | Sprache          |
| fs6  | Sprachfluss    | Sprache          |
| fs7  | Fremdsprache   | Sprache          |
| fs8  | Tests          | Sprache          |

### Allgemein (alle anderen Fächer) — 3/2/3
8 Kriterien aus dem Grootmoor Allgemein-Bogen:

| ID   | Kurzname            | Bereich           |
|------|---------------------|-------------------|
| gi1  | Sachlich richtig    | Inhalt            |
| gi2  | Argumente           | Inhalt            |
| gi3  | Reflexion           | Inhalt            |
| gm1  | Bezugstexte         | Fachmethoden      |
| gm2  | Arbeitsplanung      | Fachmethoden      |
| gs1  | Fachsprache         | Sprache & Komm.   |
| gs2  | Sprachrichtigkeit   | Sprache & Komm.   |
| gs3  | Auf andere eingehen | Sprache & Komm.   |

---

## Notenvorschlag-Logik

Nur anzeigen ab: **6 Einträge / 3 verschiedene Tage**

(6 statt 5: Bei genau 5 Einträgen liegt keine ganze Zahl von „+" im Band
45–60 %, die Note **3** wäre also im Moment der Freischaltung rechnerisch
unerreichbar. Ab 6 Einträgen ist jedes Notenband erreichbar.)

| Ratio +/(+−) | Note    | Label                         |
|-------------|---------|-------------------------------|
| ≥ 80%       | 1–2     | sehr gut / gut                |
| ≥ 60%       | 2–3     | gut / befriedigend            |
| ≥ 45%       | 3       | befriedigend                  |
| ≥ 30%       | 3–4     | befriedigend / ausreichend    |
| ≥ 15%       | 4–5     | ausreichend / mangelhaft      |
| < 15%       | 5–6     | mangelhaft / ungenügend       |

Disclaimer immer: „Pädagogische Einschätzung der Lehrkraft entscheidet."

---

## Kurse & Kalender (Schuljahr 2026/27)

| Kurs               | Typ           | Klasse |
|--------------------|---------------|--------|
| 8a Englisch        | fremdsprachen | 8a     |
| Jg8 History        | general       | Jg8    |
| Jg9 Social Studies | general       | Jg9    |
| 11P Social Studies | general       | 11P    |
| Jg10 Social Studies| general       | Jg10   |
| Jg10 History       | general       | Jg10   |
| 12. Kl. Englisch   | fremdsprachen | 12Kl   |
| 11P WiE            | general       | 11P    |
| 12. Kl. WiE        | general       | 12Kl   |

---

*Zuletzt aktualisiert: August 2026 · Gymnasium Grootmoor Hamburg · Philipp Tran-Huynh*
