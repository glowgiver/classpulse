# Class Pulse — Projektanleitung für Claude Code

> Diese Datei wird von Claude Code automatisch als Projekt-Kontext geladen
> (reservierter Dateiname — nicht umbenennen).

Participation-Tracker-App für den Schulalltag (Klassenbuch, Anwesenheit,
Verspätung, Noten/Bögen-PDF-Export). Eine einzige Single-Page-App
(`index.html`) + Python-Exportskripte, kein separates Backend/Engine.

## 🧭 Eine Session, kein Zwei-Buckets-System

Anders als Teaching Hub oder Real Estate hat Class Pulse **keine** natürliche
Trennung zwischen "kleiner wiederkehrender Fix" und "großes neues Feature" —
fast jede Änderung ist Feature-Arbeit oder ein Bugfix an derselben
`index.html`, und beides läuft gemischt und fortlaufend (siehe Git-Log: Fix
und Feature wechseln sich Commit für Commit ab). Eine Workshop/Wegwerf-
Trennung würde hier künstliche Entscheidungen erzwingen ("ist das jetzt groß
genug für eine neue Session?") statt Entscheidungen zu sparen.

**Deshalb: genau eine durchgehende Session, die offen bleibt, solange die App
aktiv weiterentwickelt wird.**

| | **Class Pulse: App-Entwicklung** (gepinnt, dauerhaft) |
|---|---|
| **Wofür** | Alles: Bugfixes, neue Features, PDF-Export-Anpassungen, Kursverwaltung, UI-Fixes — die gesamte laufende App-Arbeit |
| **Modell** | Sonnet 5, Effort **hoch** (echte Code-Arbeit, kein Admin) |
| **Wie benannt** | bleibt immer gleich |
| **Danach** | bleibt offen, wird **nicht archiviert**, solange die App aktiv ist |

**Nur für kategorisch anderes** (z. B. eine reine Datenmigration, ein Audit,
das nichts mit App-Weiterentwicklung zu tun hat) lohnt sich eine separate,
einmalige Session — das ist die Ausnahme, nicht die Regel.

### `/compact` — ein Auslöser

Ein Feature/Fix ist fertig und das nächste Thema hat inhaltlich nichts damit
zu tun (z. B. Noten-Feature fertig → als Nächstes PDF-Export) → `/compact`.
Nicht mitten in einer zusammenhängenden Änderung. Vergessen ist unkritisch —
Kompaktierung passiert sonst irgendwann von selbst.

## Projektstruktur

```
index.html                        Die App (Single-Page, alles drin)
sw.js                              Service Worker (Cache-Version bei jedem Release bumpen)
manifest.json, icon-*.png          PWA-Assets
classpulse_export.py               PDF/Noten-Export-Logik
classpulse_infosheet.py            Info-Sheet-Export
CLASSPULSE_PDF_RULES.md            Vorgaben für den PDF-Export (Bögen, Notenpunkte)
README.md                          Projekt-Doku
ClassPulse_Backup_*.json           Automatische Backups (nicht committen/löschen)
*Kursliste.pdf                     Ausgangsdaten pro Kurs
```
