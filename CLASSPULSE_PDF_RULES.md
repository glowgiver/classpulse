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

## Kurz vorm Quartal — so machst du's

Wenn's soweit ist und die Kinder ihre Noteneinschätzung bekommen sollen:

1. **Aktuelles Backup holen.** In der App: Mehr → „Backup herunterladen" —
   den frischesten Stand, damit alles bis heute drin ist.
2. **Falls vorhanden: Selbsteinschätzungen bereithalten.** Wenn Schüler
   schon über IServ eingeschätzt haben, kurze Liste Name → Wert parat halten
   (muss nicht formatiert sein, reicht als Stichpunkte).
3. **Claude-Chat öffnen, beide Dateien hochladen** — `ClassPulse_Backup_DATUM.json`
   + diese Datei hier.
4. **Auftrag geben**, z.B.: „Erstell mir die ClassPulse PDF-Exports aus
   diesem Backup für Jg8 History." (Pro Kurs einzeln — mehrere Kurse einfach
   nacheinander fragen.)
5. **Vorschau-Tabelle anschauen — noch kein PDF.** Claude zeigt erstmal nur
   Name, anwesende Stunden, rechnerischer Vorschlag pro Schüler. Kein Bogen existiert noch.
6. **Abweichungen und Selbsteinschätzungen durchgeben**, direkt im Chat, z.B.:
   „Fenja auf Punkte 13 setzen, ihre Selbsteinschätzung war 11. Rest passt so."
   Wer nicht erwähnt wird, bekommt den Rechenwert.
7. **PDF generieren lassen und herunterladen.** Erst jetzt entstehen die
   fertigen Bögen — Klassenliste intern (zeigt Rechenwert *und* Anpassung),
   plus eine fertige Seite pro Schüler (nur das Endergebnis, sauber).
8. **Austeilen bzw. weiterschicken** — Papier oder digital über IServ.

---

## Workflow

1. In der App: **Mehr → Backup herunterladen** (.json Datei)
2. Claude Momentum-Chat öffnen
3. Beide Dateien hochladen: `ClassPulse_Backup_DATUM.json` + `CLASSPULSE_PDF_RULES.md`
4. Schreiben: „Erstell mir die ClassPulse PDF-Exports aus diesem Backup"
5. **Claude zeigt zuerst eine Vorschau-Tabelle** (`preview_grades()`) — Name,
   anwesende Stunden, rechnerischer Vorschlag pro Schüler. **Noch keine PDF, noch keine
   Bögen.**
6. Philipp sieht sich das an und sagt, wo er pädagogisch abweicht (`override_grade`)
   und, falls schon bekannt (z.B. von IServ), die Selbsteinschätzung der Schüler
   (`student_grade`) — beides pro Schüler in `STUDENTS` im Skript.
7. Erst danach: Claude generiert die finalen Bögen — Klassenliste (intern,
   zeigt Rechenwert *und* Anpassung nebeneinander) + eine Bogen-Seite pro
   Schüler (zeigt nur das Endergebnis, sauber, ohne Rechenweg)
8. PDF herunterladen — fertig für Zeugniskonferenz oder Elterngespräch

**Schritt 5–6 nie überspringen** — sonst steht auf jedem Bogen „Über die
Gewichtung der Kriterien entscheidet die Lehrkraft in pädagogischer
Verantwortung", aber niemand hatte je die Gelegenheit, das auch zu tun.

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
  die aus dem Stunden-Score dieses Bereichs folgt (siehe Skala unten);
  zu wenige Beobachtungen im Bereich → kein Kreuz, keine Spalte hervorgehoben
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

Derselbe Stunden-Score wie beim Notenvorschlag (siehe unten), nur auf die
Kriterien dieses Bereichs eingeschränkt: eine anwesende Stunde ohne Eintrag *in
diesem Bereich* zählt neutral (0,5). Dieselben Schwellen (80/65/50/40%), nur ohne
die unterste 25%-Trennung, weil der Bogen 5 statt 6 Stufen hat. Neutral landet
damit in „weitgehend", der Mitte.

**Ein Kreuz gibt es erst ab 6 anwesenden Stunden UND 4 echten Beobachtungen in
diesem Bereich** — sonst stünde auf dem Bogen ein Kreuz, das nur aus neutralen
Stunden besteht, also aus nichts, was tatsächlich beobachtet wurde.

| Voraussetzung                          | Score im Bereich | Spalte                     |
|-----------------------------------------|------------------|----------------------------|
| < 6 Stunden oder < 4 Beob. im Bereich   | —                | kein Kreuz                 |
| erfüllt                                 | ≥ 80%            | in besonderem Maße         |
| erfüllt                                 | ≥ 65%            | umfassend                  |
| erfüllt                                 | ≥ 50%            | weitgehend                 |
| erfüllt                                 | ≥ 40%            | in Grundzügen              |
| erfüllt                                 | < 40%            | nicht oder nur in Ansätzen |

Sowohl die 5er-Skala als auch die Mindestmenge (4) sind eigenständige Cutoffs
(nicht mit Philipp einzeln durchgesprochen) — beim ersten Einsatz gegenprüfen,
ob sie zur tatsächlichen Einschätzung passen.

---

## Notenvorschlag-Logik

Nur anzeigen ab: **6 anwesenden Stunden**

**Einheit ist die anwesende Stunde, nicht der Eintrag.** Beobachtungen sind
Momentaufnahmen: Eingetragen wird, was auffällt. Eine Stunde ohne Eintrag heißt
„unauffällig", nicht „unbekannt", und zählt deshalb neutral.

**Stand 2026-09-17 umgestellt.** Vorher wurde pro Eintrag gezählt (+ / alle
Einträge). Stunden ohne Eintrag fielen dabei einfach heraus. Selbst nach dem
Verschärfen der Schwellen am 2026-09-10 lag die Median-Ratio bei 1,00, 97 % der
Schüler mit Vorschlag standen in den zwei besten Bändern, und die Hälfte hatte
kein einziges „−". Grund: Ein „−" ist eine aktive Entscheidung, nichts
einzutragen kostete nichts. An Schwellen zu drehen hilft dagegen nicht.

**Score pro Schüler** = Durchschnitt über alle Einträge plus die neutralen Stunden:

| Was                            | zählt als                                  |
|--------------------------------|--------------------------------------------|
| jedes „+"                      | 1                                          |
| jedes „−"                      | 0                                          |
| anwesende Stunde ohne Eintrag  | ein Eintrag mit 0,5 (neutral)              |
| mehr als 3 Einträge in einer Stunde | zählen zusammen wie 3, im selben +/−-Verhältnis |

Rechnung: (Summe der gewichteten Einträge + 0,5 × Stunden ohne Eintrag) /
(Anzahl gewichteter Einträge + Stunden ohne Eintrag).

**Stand 2026-09-17, zweite Anpassung:** Zuerst zählte jede Stunde nur einmal, egal
wie viele „+" darin standen. Dann kam z.B. jemand mit +7 −0 in 2 von 7 Stunden
nur auf „3". Philipp sah sie eher bei „2". Jetzt zählen mehrere Einträge stärker.
Die Grenze von 3 pro Stunde verhindert, dass eine einzelne Stunde die
unauffälligen Stunden einfach überstimmt. `note` und `skip` sind keine Bewertungen.

**So zählst du die Stunden aus dem Backup** (exakt wie `getLessonStats` in
`index.html`):
1. Stattgefundene Stunden eines Kurses = alle Daten, für die es einen Schlüssel
   `DATUM_Kursname` in `absences`, `materials`, `topics`, `homework`,
   `homeworkAssigned` oder `lateArrivals` gibt, plus alle Daten mit einer
   Beobachtung (`observations`) in diesem Kurs.
2. Pro Schüler: Stunden, an denen seine ID in `absences[DATUM_Kurs]` steht,
   fallen weg.
3. Tage in `remoteDays` (Fernunterricht) zählen nur, wenn der Schüler an dem Tag
   eine Bewertung hat. Wer nicht im Raum sein konnte, war nicht „unauffällig".
4. Ergebnis → `lessons_present`. Die Stunden mit Bewertung → `rated_lessons`,
   eine Liste mit `{kriterium: (+, −)}` pro Stunde.

**Basis-Band** aus dem Score (Drittelnoten-Kurse zeigen „Note",
Oberstufen-Kurse mit `notenformat: "punkte"` zeigen „Punkte"):

| Score       | Note    | Punkte  | Label                         |
|-------------|---------|---------|-------------------------------|
| ≥ 80%       | 1–2     | 12–15   | sehr gut / gut                |
| ≥ 65%       | 2–3     | 9–11    | gut / befriedigend            |
| ≥ 50%       | 3       | 7–8     | befriedigend                  |
| ≥ 40%       | 3–4     | 5–6     | befriedigend / ausreichend    |
| ≥ 25%       | 4–5     | 2–4     | ausreichend / mangelhaft      |
| < 25%       | 5–6     | 0–1     | mangelhaft / ungenügend       |

Ein Schüler ganz ohne Einträge landet also bei 50 % = „3". Das ist gewollt:
unauffällig heißt befriedigend. Wer darüber liegen soll, braucht regelmäßig „+".
Wer nie mitmacht, obwohl er angesprochen wird, bekommt dafür ein „−".
Mit den Daten vom 2026-09-17 hatten erst 30 Schüler 6 anwesende Stunden (fast
alle 8a Englisch). Verteilung von „1–2" bis „5–6": 5 / 5 / 13 / 5 / 2 / 0. Vorher
waren es 21 / 13 / 1 / 0 / 0 / 0. Dass sich so viele bei „3" sammeln, liegt an den
wenigen Stunden bisher. Nach ein paar Wochen mehr Daten die Schwellen noch einmal
gegenprüfen.

**Korrektur** — Vokabeltests, HA-Quote, Material-Quote verschieben das Basis-Band
danach um maximal ±1 Zeile insgesamt (Effekte werden addiert, dann gedeckelt —
ein gutes Ergebnis in einer Spur kann ein schlechtes in einer anderen ausgleichen):

| Faktor          | Schwelle (ab Mindestmenge)                          | Wirkung        |
|------------------|------------------------------------------------------|----------------|
| Tests            | ab 2 Tests: Ø ≤2,0 (bzw. ≥11 Punkte)                 | +1 Zeile hoch  |
| Tests            | ab 2 Tests: Ø ≥4,0 (bzw. ≤5 Punkte)                  | +1 Zeile runter|
| HA-Quote         | ab 6 Kontrollen: < 80%                                | +1 Zeile runter|
| Material-Quote   | ab 8 Kontrollen: < 85%                                | +1 Zeile runter|

Ein „Material fehlte"-Eintrag lässt sich nachträglich entschuldigen (Klassenbuch →
Tag antippen → „Mat. entschuldigen?"), z.B. wenn Tage später eine plausible
Begründung kommt. Entschuldigte Einträge zählen weder für noch gegen die
Material-Quote — sie fallen aus Zähler und Nenner raus, statt als „hier"
mitgezählt zu werden.

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
