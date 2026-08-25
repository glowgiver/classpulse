# ClassPulse — PDF Export Rules

Dieses Dokument beschreibt das Design und den Workflow für den PDF-Export.
Bei der PDF-Generierung in Claude immer diese Datei + das JSON-Backup hochladen.

**Grundprinzip seit v4:** Die Schüler-Seiten sind keine ClassPulse-eigene Erfindung
mehr, sondern eine Reproduktion des echten Grootmoor-Bogens „Bewertung von
Leistungen in der laufenden Unterrichtsarbeit" — desselben Blatts, das die
Schüler in Papierform bekommen. ClassPulse trägt darauf nur die
Lehrkraft-Zeile ein (ein Kreuz pro Bereich, aggregiert aus den Beobachtungen)
und die Note der Lehrkraft unten rechts. Die Schülerzeile und „Meine
Noteneinschätzung" bleiben leer — das ist Selbsteinschätzung von Hand.
Das Blatt gilt für **alle** Kurstypen, auch Fremdsprachen (siehe unten).

---

## Workflow

1. In der App: **Mehr → Backup herunterladen** (.json Datei)
2. Claude Momentum-Chat öffnen
3. Beide Dateien hochladen: `ClassPulse_Backup_DATUM.json` + `CLASSPULSE_PDF_RULES.md`
4. Schreiben: „Erstell mir die ClassPulse PDF-Exports aus diesem Backup"
5. Claude generiert: Klassenliste (intern) + eine Bogen-Seite pro Schüler (für Gespräche)
6. PDF herunterladen — fertig für Zeugniskonferenz oder Elterngespräch

Der Python-Code für die Generierung liegt in `classpulse_export.py` im selben Repo —
das Skript enthält Stichprobendaten als Vorlage; Claude ersetzt sie beim Export
durch die echten Werte aus dem Backup.

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

## Seite 1 — Klassenliste (intern, nicht Teil des Original-Bogens)

- Überschrift: „ClassPulse" in PRUSSIAN, 18pt Bold
- Untertitel: Kursname · Halbjahr · Lehrkraft, 10pt GREY_TEXT
- Trennlinie: 1.5pt PRUSSIAN
- Label: „KLASSENLISTE — INTERNER ÜBERBLICK" in TEAL, 9pt Bold
- Fußzeile: „Nur für interne Verwendung"

**Tabelle** — Spalten: Name · Inhalt · Fachmethoden · Sprache & Komm. · HA-Quote ·
Material · Gesamt. Die drei Bereichsspalten sind dieselbe Aggregation, die auch
die Schüler-Seiten füllt (siehe unten) — kein eigenes Kriterien-Set mehr für
diese Seite.
- Header: DARK_HEADER Hintergrund, weiß, 8pt Bold
- Linke Border: 3pt PRUSSIAN auf Namensspalte
- Zeilen alternierend: GREY_LIGHT / weiß
- Bereichsspalten: Zahlen (+X/−Y) + Tendenz-Label (überwiegend positiv/ausgeglichen/
  überwiegend schwach) in Farbe
- Gesamt-Spalte: Notenvorschlag (Note/Punkte, siehe unten), PRUSSIAN wenn vorhanden

---

## Seiten 2+ — eine Seite pro Schüler = das Original-Blatt

**Das ist keine ClassPulse-Erfindung — das ist der Bogen, den die Schule vorgibt,
Wort für Wort.** Was ClassPulse ausfüllt: FACH, NAME, ein Kreuz pro Bereichs-Tabelle
(Lehrkraft-Zeile), „Note der Lehrkraft" unten rechts. Was leer bleibt: die
Schülerzeile jeder Tabelle und „Meine Noteneinschätzung" — das ist
Selbsteinschätzung, die füllt der Schüler von Hand aus.

**Kopf:**
- „FACH: [Kurs]" / „NAME: [Schüler]" nebeneinander, unterstrichen
- Titel „Bewertung von Leistungen in der laufenden Unterrichtsarbeit" — PRUSSIAN, 14pt Bold
- Intro-Absatz wortgleich vom Original (siehe `SHEET_INTRO` im Skript)

**Pro Bereich (Inhalt / Fachmethoden / Sprache und Kommunikation), in dieser Reihenfolge:**
- Bereichs-Label, TEAL, 9pt Bold, uppercase
- 5-Spalten-Tabelle, Kopfzeile DARK_HEADER: „nicht oder nur in Ansätzen" /
  „in Grundzügen" / „weitgehend" / „umfassend" / „in besonderem Maße"
- Zeile „Meine Leistungen erfüllen die Anforderungen …" — ein ✕ in der Spalte,
  die aus der Beobachtungs-Ratio dieses Bereichs folgt (siehe Skala unten);
  keine Beobachtung im Bereich → kein Kreuz, keine Spalte hervorgehoben
- Darunter die Original-Aufzählungspunkte dieses Bereichs, **wortgleich** —
  dieselben für jedes Fach, nicht aus den ClassPulse-Kriterien generiert
  (siehe `SHEET_BULLETS` im Skript für den exakten Text)

**Nach den drei Tabellen:**
- Fußnote wortgleich: „Ergänzend kann es in einzelnen Fächern weitere
  fachbezogene Kriterien geben."
- Bei Fremdsprachenkursen zusätzlich eine Zeile „Zusätzlich beobachtet, nicht Teil
  dieses Bogens: Beteiligung: [Tendenz]" — Beteiligung hat keinen Platz auf dem
  Bogen, zählt aber weiter in App und Notenvorschlag (siehe Kriterien unten)
- Fußzeilen-Box: „Meine Noteneinschätzung: ____________" (leer) |
  „Note der Lehrkraft: [Note/Punkte]" (aus dem Notenvorschlag, siehe unten)

**Notizen** (nur fürs Gespräch, nicht Teil des Original-Bogens — rutschen bei
Bedarf auf eine eigene Folgeseite, damit die Bogen-Seite selbst unverändert bleibt):
- Trennlinie 0.5pt GREY_TEXT
- Label: „BEOBACHTUNGEN & NOTIZEN (für das Gespräch, nicht auf dem Original-Bogen)"
- Pro Notiz: TEAL_LIGHT Hintergrund, 3pt TEAL linke Border
- Text links (Italic 8.5pt), Datum rechts (7.5pt GREY_TEXT)

**Fußzeile:**
„ClassPulse · Kursname · Export Datum · Lehrkraft: Name · Zählt X% der Gesamtnote"

---

## Kriterien → Bogen-Bereich (bogenBereich)

Die ClassPulse-Kriterien sind die tägliche Beobachtungseinheit; der Bogen kennt sie
nicht einzeln, nur die drei Bereiche. Jedes Kriterium hat ein `bogenBereich` (Spiegel
von `index.html`), nach dem die Beobachtungen für die Bereichs-Kreuze aggregiert werden.

### Fremdsprachen (Englisch: 8a Englisch, 12. Kl. Englisch) — 9 Kriterien

| ID   | Kurzname                | bogenBereich     |
|------|--------------------------|------------------|
| fs2  | Beiträge                 | Inhalt           |
| fs10 | Argumente                | Inhalt           |
| fs11 | Reflexion                | Inhalt           |
| fs12 | Bezugstexte              | Fachmethoden     |
| fs13 | Arbeitsplanung           | Fachmethoden     |
| fs5  | Vokabeln/Gram.           | Sprache & Komm.  |
| fs9  | Sprachfluss & Zielspr.   | Sprache & Komm.  |
| fs14 | Auf andere eingehen      | Sprache & Komm.  |
| fs1  | Beteiligung              | *(keiner)*       |

fs1 Beteiligung hat keinen `bogenBereich` — der Bogen hat dafür keine Spalte.
Zählt trotzdem im Notenvorschlag; auf der PDF-Seite als eigene Zeile unter dem
Bogen, klar getrennt.

Vokabeltests, HA-Quote und Material-Quote sind **keine Kriterien mehr** — sie
fließen als eigene, gedeckelte Korrektur in den Notenvorschlag ein (siehe unten),
nicht in die Bereichs-Kreuze.

### Allgemein (alle anderen Fächer) — 3/2/3, 8 Kriterien

| ID   | Kurzname            | bogenBereich       |
|------|---------------------|--------------------|
| gi1  | Sachlich richtig    | Inhalt             |
| gi2  | Argumente           | Inhalt             |
| gi3  | Reflexion           | Inhalt             |
| gm1  | Bezugstexte         | Fachmethoden       |
| gm2  | Arbeitsplanung      | Fachmethoden       |
| gs1  | Fachsprache         | Sprache & Komm.    |
| gs2  | Sprachrichtigkeit   | Sprache & Komm.    |
| gs3  | Auf andere eingehen | Sprache & Komm.    |

Hier ist `bogenBereich` identisch mit der App-eigenen `area` — beim
Allgemein-Set fielen beide schon immer zusammen.

---

## Skala der Bereichs-Kreuze (5 Spalten)

Dieselben Schwellen wie der Notenvorschlag (80/60/45/30%), nur ohne die unterste
15%-Trennung, weil der Bogen 5 statt 6 Stufen hat. **Erst ab 4 Beobachtungen in
diesem Bereich** — sonst könnte ein einzelnes "+" am zweiten Schultag schon
„in besonderem Maße" auslösen. Dieselbe Schutzlogik wie MIN_ENTRIES/MIN_DAYS
beim Notenvorschlag, hier nur pro Bereich statt für den ganzen Kurs (ein reiner
Mengen-Cutoff, kein Tage-Cutoff — die Kriterien-Daten tragen hier kein Datum):

| Beobachtungen im Bereich | Ratio +/(+−)              | Spalte                     |
|---------------------------|----------------------------|----------------------------|
| < 4                        | —                          | kein Kreuz                 |
| ≥ 4                        | ≥ 80%                      | in besonderem Maße         |
| ≥ 4                        | ≥ 60%                      | umfassend                  |
| ≥ 4                        | ≥ 45%                      | weitgehend                 |
| ≥ 4                        | ≥ 30%                      | in Grundzügen               |
| ≥ 4                        | < 30%                      | nicht oder nur in Ansätzen |

Sowohl die 5er-Skala als auch die Mindestmenge (4) sind eigenständige Cutoffs
(nicht mit Philipp einzeln durchgesprochen) — beim ersten Einsatz gegenprüfen,
ob sie zur tatsächlichen Einschätzung passen.

---

## Notenvorschlag-Logik

Nur anzeigen ab: **6 Einträge / 3 verschiedene Tage**

(6 statt 5: Bei genau 5 Einträgen liegt keine ganze Zahl von „+" im Band
45–60 %, die Note **3** wäre also im Moment der Freischaltung rechnerisch
unerreichbar. Ab 6 Einträgen ist jedes Notenband erreichbar.)

**Basis-Band** aus der Gesamt-Ratio über alle Kriterien (Drittelnoten-Kurse
zeigen „Note", Oberstufen-Kurse mit `notenformat: "punkte"` zeigen „Punkte"):

| Ratio +/(+−) | Note    | Punkte  | Label                         |
|-------------|---------|---------|-------------------------------|
| ≥ 80%       | 1–2     | 12–15   | sehr gut / gut                |
| ≥ 60%       | 2–3     | 9–11    | gut / befriedigend            |
| ≥ 45%       | 3       | 7–8     | befriedigend                  |
| ≥ 30%       | 3–4     | 5–6     | befriedigend / ausreichend    |
| ≥ 15%       | 4–5     | 2–4     | ausreichend / mangelhaft      |
| < 15%       | 5–6     | 0–1     | mangelhaft / ungenügend       |

**Korrektur** — Vokabeltests, HA-Quote, Material-Quote verschieben das Basis-Band
danach um maximal ±1 Zeile insgesamt (Effekte werden addiert, dann gedeckelt —
ein gutes Ergebnis in einer Spur kann ein schlechtes in einer anderen ausgleichen):

| Faktor          | Schwelle (ab Mindestmenge)                          | Wirkung        |
|------------------|------------------------------------------------------|----------------|
| Tests            | ab 2 Tests: Ø ≤2,0 (bzw. ≥11 Punkte)                 | +1 Zeile hoch  |
| Tests            | ab 2 Tests: Ø ≥4,0 (bzw. ≤5 Punkte)                  | +1 Zeile runter|
| HA-Quote         | ab 6 Kontrollen: < 80%                                | +1 Zeile runter|
| Material-Quote   | ab 8 Kontrollen: < 85%                                | +1 Zeile runter|

Disclaimer immer: „Pädagogische Einschätzung der Lehrkraft entscheidet."

---

## Kurse & Kalender (Schuljahr 2026/27)

`notenformat` bestimmt, ob der Export „Note" oder „Punkte" beschriftet und welche
Test-Schwellen gelten (siehe Notenvorschlag-Logik oben) — Spiegel von `COURSES_META`
in `index.html`.

| Kurs               | Typ           | Klasse | Notenformat   |
|--------------------|---------------|--------|---------------|
| 8a Englisch        | fremdsprachen | 8a     | drittelnoten  |
| Jg8 History        | general       | Jg8    | drittelnoten  |
| Jg9 Social Studies | general       | Jg9    | drittelnoten  |
| 11P Social Studies | general       | 11P    | punkte        |
| Jg10 Social Studies| general       | Jg10   | drittelnoten  |
| Jg10 History       | general       | Jg10   | drittelnoten  |
| 12. Kl. Englisch   | fremdsprachen | 12Kl   | punkte        |
| 11P WiE            | general       | 11P    | punkte        |
| 12. Kl. WiE        | general       | 12Kl   | punkte        |

---

*Zuletzt aktualisiert: August 2026 · Gymnasium Grootmoor Hamburg · Philipp Tran-Huynh*
