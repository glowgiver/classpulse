# ClassPulse — Participation Tracker

PWA für Mitarbeitsbeobachtung im Unterricht.
Gymnasium Grootmoor Hamburg · Philipp Tran-Huynh

**Live:** https://glowgiver.github.io/classpulse/
**Repo:** https://github.com/glowgiver/classpulse

---

## Dateien in diesem Ordner

### App (werden auf GitHub Pages deployed)

| Datei | Zweck |
|-------|-------|
| `index.html` | Die komplette App — React via CDN, alles inline, kein Build-Schritt |
| `manifest.json` | PWA-Metadaten (Name, Icons, Theme) |
| `sw.js` | Service Worker — Offline-Cache |
| `icon-192.png` | Homescreen-Icon klein |
| `icon-512.png` | Homescreen-Icon groß |

### Export-Tools (laufen lokal, nicht deployed)

| Datei | Zweck |
|-------|-------|
| `classpulse_export.py` | Generiert Klassenliste + Schüler-Detailseiten als PDF aus JSON-Backup |
| `classpulse_infosheet.py` | Generiert die Info-Sheets für Schüler (EN + General Version) |
| `CLASSPULSE_PDF_RULES.md` | Design-Dokumentation: Farben, Fonts, Layout-Regeln, Kriterien-Definitionen |

---

## Lokales Setup

### Voraussetzungen

```bash
# Python-Pakete
pip3 install reportlab

# Montserrat Font (macOS via Homebrew)
brew install --cask font-montserrat

# ODER manuell von Google Fonts herunterladen und installieren
```

**Wichtig:** Die Python-Scripts erwarten Montserrat unter einem Systempfad.
Auf macOS muss der `FONT_DIR` in beiden `.py` Dateien angepasst werden:

```python
# Aktuell (Linux):
FONT_DIR = "/usr/share/fonts/truetype/montserrat/"

# macOS nach brew install:
FONT_DIR = "/Users/DEINNAME/Library/Fonts/"
```

### App lokal testen

```bash
# Lokalen Server starten (Service Worker braucht http://, nicht file://)
python3 -m http.server 8080

# Browser öffnen:
# http://localhost:8080
```

### PDFs generieren

```bash
# Info-Sheets für Schüler (2 PDFs: English + General)
python3 classpulse_infosheet.py

# Schüler-Reports aus JSON-Backup
# (Script erwartet aktuell Beispieldaten — muss angepasst werden
#  um echtes Backup einzulesen)
python3 classpulse_export.py
```

---

## Deployment

Änderungen an `index.html`, `manifest.json`, `sw.js` oder Icons:

```bash
git add .
git commit -m "Beschreibung der Änderung"
git push
```

GitHub Pages deployed automatisch nach ~30 Sekunden.

**Wichtig bei Service-Worker-Änderungen:** `CACHE_NAME` in `sw.js` hochzählen
(`classpulse-v1` → `classpulse-v2`), sonst laden Nutzer die alte Version aus dem Cache.

---

## Workflow: Quartalsfeedback

1. In der App: **Mehr → Backup herunterladen** (.json)
2. `classpulse_export.py` anpassen um das Backup einzulesen
3. `python3 classpulse_export.py` ausführen
4. PDFs an IServ Aufgabenmodul anhängen (Einzelfeedback pro Schüler)

---

## Architektur-Entscheidungen

**Warum React via CDN statt Build-Setup:**
Kein Node.js, kein npm, kein Build-Schritt. Eine Datei die überall läuft.
Trade-off: Babel-Kompilierung im Browser (~200KB Overhead beim ersten Laden,
danach gecacht).

**Warum localStorage statt Server:**
Kein Backend, kein Login, kein Datenschutz-Problem. Schülerdaten verlassen
das Gerät nie. Trade-off: Daten sind gerätgebunden, JSON-Backup ist Pflicht.

**Warum PDFs nicht in der App:**
Browser können keine PDFs mit eigenem Font und komplexem Layout erzeugen.
ReportLab läuft lokal — dafür ist die Qualität deutlich besser.

---

## Pädagogische Regeln (nicht ändern ohne Grund)

- **Notenvorschlag ab 6 Einträgen / 3 verschiedenen Tagen** — ein einzelner
  Tag darf keine Note bestimmen (pädagogisch + rechtlich)
- **Nur + und −** — keine 5-Stufen-Skala im Unterricht. Die Feinabstufung
  passiert am Halbjahresende durch die Lehrkraft, nicht in der Stunde
- **Farbenblind-freundlich** — immer Text + Farbe, nie Farbe als einziges Signal
- **Keine Popups** — Hinweise nur passiv im Schülerdetail
- **Detailseiten ohne Zahlen** — Schüler-PDFs zeigen nur Tendenzen
  ("über Erwartung"), keine Zählwerte. Zahlen nur in der internen Klassenliste

---

## Bewertungsbögen

Zwei Systeme, automatisch zugeordnet:

**Fremdsprachen-Bogen** (8a Englisch, 12. Kl. Englisch) — 8 Kriterien
**Allgemeiner Grootmoor-Bogen** (alle anderen) — 8 Kriterien (3 Inhalt / 2 Fachmethoden / 3 Sprache)

Details in `CLASSPULSE_PDF_RULES.md`.

---

*Stand: August 2026*
