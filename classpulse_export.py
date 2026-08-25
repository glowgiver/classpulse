#!/usr/bin/env python3
"""ClassPulse PDF v4 — reproduziert den echten Grootmoor-Bogen

Seite 1 (intern) bleibt eine ClassPulse-eigene Klassenliste — die geht nie an
Schüler raus, muss also nicht am Schulformular hängen.

Ab Seite 2: eine Seite pro Schüler, die das Original-Blatt „Bewertung von
Leistungen in der laufenden Unterrichtsarbeit" nachbildet — FACH/NAME
vorausgefüllt, dieselben drei Tabellen (Inhalt / Fachmethoden / Sprache und
Kommunikation) mit denselben fünf Spalten und denselben Aufzählungspunkten
wie das Original. ClassPulse trägt nur EIN Kreuz pro Zeile ein (Lehrkraft-
Einschätzung, aus den Beobachtungen aggregiert) und die Note der Lehrkraft
unten rechts. Die Schülerzeile und „Meine Noteneinschätzung" bleiben leer —
das ist Selbsteinschätzung, die kreuzt der Schüler von Hand an.

Das Blatt gilt jetzt auch für Fremdsprachenkurse (nicht nur Allgemein) — die
9 ClassPulse-Kriterien pro Kurstyp sind darauf gemappt (bogenBereich), aber
nur zur internen Berechnung. Gedruckt werden IMMER die Original-Bullets, weil
das Blatt für jedes Fach dasselbe ist.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

FONT_DIR = "/usr/share/fonts/truetype/montserrat/"
pdfmetrics.registerFont(TTFont("Montserrat",          FONT_DIR + "Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Bold",     FONT_DIR + "Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-SemiBold", FONT_DIR + "Montserrat-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Italic",   FONT_DIR + "Montserrat-Italic.ttf"))

PRUSSIAN    = colors.HexColor("#023A5D")
TEAL        = colors.HexColor("#1B5E79")
TEAL_LIGHT  = colors.HexColor("#E8F2F5")
DARK_HEADER = colors.HexColor("#44546A")
GREY_LIGHT  = colors.HexColor("#F5F5F5")
GREY_TEXT   = colors.HexColor("#555555")
BLACK       = colors.HexColor("#111111")
GREEN       = colors.HexColor("#2D7A4F")
GREEN_LIGHT = colors.HexColor("#E8F5EE")
RED         = colors.HexColor("#B03A2E")
RED_LIGHT   = colors.HexColor("#FDECEA")
AMBER       = colors.HexColor("#8B6914")
AMBER_LIGHT = colors.HexColor("#FEF9E7")

# ── KONTEXT — bei jedem Export durch die echten Werte aus dem Backup und aus
#    COURSES_META (index.html) ersetzen ──────────────────────────────────────
COURSE_NAME   = "8a Englisch"
CRITERIA_TYPE = "fremdsprachen"        # "fremdsprachen" oder "general"
NOTENFORMAT   = "drittelnoten"         # "drittelnoten" oder "punkte" (Oberstufe)
MITARBEIT_PCT = 60                     # siehe COURSES_META
TEACHER       = "Philipp Tran-Huynh"
HALF_YEAR     = "Schuljahr 2026/27 · Halbjahr 1"
EXPORT_DATE   = datetime.date.today().strftime("%-d. %B %Y")

# ── KRITERIEN — Spiegel von FREMDSPRACHEN_CRITERIA / GENERAL_CRITERIA in
#    index.html. bogenBereich=None heißt: eigene Beobachtung, kein Platz auf
#    dem Original-Blatt (nur fs1 Beteiligung). (id, short, bogenBereich) ──
FREMDSPRACHEN_CRITERIA = [
    ("fs2",  "Beiträge",               "Inhalt"),
    ("fs10", "Argumente",              "Inhalt"),
    ("fs11", "Reflexion",              "Inhalt"),
    ("fs12", "Bezugstexte",            "Fachmethoden"),
    ("fs13", "Arbeitsplanung",         "Fachmethoden"),
    ("fs5",  "Vokabeln/Gram.",         "Sprache & Komm."),
    ("fs9",  "Sprachfluss & Zielspr.", "Sprache & Komm."),
    ("fs14", "Auf andere eingehen",    "Sprache & Komm."),
    ("fs1",  "Beteiligung",            None),
]
GENERAL_CRITERIA = [
    ("gi1", "Sachlich richtig",    "Inhalt"),
    ("gi2", "Argumente",           "Inhalt"),
    ("gi3", "Reflexion",           "Inhalt"),
    ("gm1", "Bezugstexte",         "Fachmethoden"),
    ("gm2", "Arbeitsplanung",      "Fachmethoden"),
    ("gs1", "Fachsprache",         "Sprache & Komm."),
    ("gs2", "Sprachrichtigkeit",   "Sprache & Komm."),
    ("gs3", "Auf andere eingehen", "Sprache & Komm."),
]

def criteria_for(criteria_type):
    return FREMDSPRACHEN_CRITERIA if criteria_type == "fremdsprachen" else GENERAL_CRITERIA

BEREICHE = ["Inhalt", "Fachmethoden", "Sprache & Komm."]

# ── ORIGINAL-TEXT DES GROOTMOOR-BOGENS — wortgleich, weil das Blatt für jedes
#    Fach dasselbe ist. Nicht aus den ClassPulse-Kriterien ableiten. ─────────
SHEET_TITLE = "Bewertung von Leistungen in der laufenden Unterrichtsarbeit"
SHEET_INTRO = (
    "Die folgende Übersicht führt Kriterien auf, die für die Bewertung von Leistungen verwendet werden. "
    "Bewertet werden mündliche, schriftliche und praktische Leistungen, die z.B. in Unterrichtsgesprächen, "
    "bei Präsentationen, in Einzelarbeit oder in kooperativen Phasen erbracht werden.<br/>"
    "Es kann vorkommen, dass nicht alle Kriterien zum erteilten Unterricht passen. Über die Gewichtung der "
    "Kriterien entscheidet die Lehrkraft in pädagogischer Verantwortung."
)
SHEET_ROW_LABEL = "Meine Leistungen erfüllen die Anforderungen …"
SHEET_COLUMNS   = ["nicht oder nur\nin Ansätzen", "in Grundzügen", "weitgehend", "umfassend", "in besonderem\nMaße"]
SHEET_FOOTNOTE  = "Ergänzend kann es in einzelnen Fächern weitere fachbezogene Kriterien geben."

SHEET_BULLETS = {
    "Inhalt": [
        "Meine Beiträge und Arbeitsergebnisse passen zur Aufgabe, tragen zur Lösung bei und sind sachlich richtig.",
        "Meine Beiträge /Argumente bauen sinnvoll aufeinander auf und erschließen viele Seiten eines Problems.",
        "Ich verstehe die Inhalte des Unterrichts ganz genau und stelle sie verständlich dar.",
        "Ich nutze Vorwissen aus Schule und Alltag, setze es sinnvoll mit anderem in Verbindung und nutze es, "
        "um Neues zu erschließen.",
        "Ich nutze eigenständige, kreative Lösungswege und komme zu eigenen Lösungen.",
        "Ich reflektiere Ergebnisse kritisch und kann sie im Sachzusammenhang einordnen und deuten.",
        "Ich stelle mich auch schwierigen Aufgaben.",
        "Ich entwickle weiterführende Fragestellungen.",
    ],
    "Fachmethoden": [
        "Ich gehe mit Bezugstexten, Medien und Material angemessen und sinnvoll um.",
        "Ich verwende Fachmethoden angemessen.",
        "Ich wähle Werkzeuge situationsgerecht aus und nutze sie sicher.",
        "Ich kann meine Arbeit sinnvoll planen, einteilen und durchführen.",
    ],
    "Sprache & Komm.": [
        "Ich drücke mich treffend und differenziert aus und verwende die Fachsprache richtig.",
        "Meine Beiträge sind sprachlich richtig.",
        "Wenn ich mit anderen spreche, bleibe ich beim Thema, damit wir gemeinsam zu einem guten Ergebnis kommen.",
        "Meine Beiträge sind sinnvoll gegliedert und bauen aufeinander auf.",
        "Ich berücksichtige die Beiträge von Mitschülerinnen und Mitschülern.",
        "Ich stoße Arbeitsprozesse in Gruppen an und bringe die Arbeit in der Gruppe voran.",
        "Ich bringe geeignete eigene Arbeitsergebnisse in den Arbeitsprozess der Gruppe ein.",
    ],
}

# ── SKALA (5 Spalten des Original-Blatts) — dieselben Schwellen wie der
#    Notenvorschlag in der App (80/60/45/30%), nur ohne die unterste 15%-
#    Trennung, weil hier nur 5 statt 6 Stufen zur Verfügung stehen.
#    BEREICH_MIN_OBS: ohne Mindestmenge könnte ein einzelnes "+" am zweiten
#    Schultag schon "in besonderem Maße" auslösen — dieselbe Sorte Fehler,
#    vor der MIN_ENTRIES/MIN_DAYS beim Notenvorschlag schon schützt, hier nur
#    pro Bereich statt für den ganzen Kurs. 4 ist eine eigene Setzung (nicht
#    mit Philipp einzeln abgestimmt) — bei Bedarf anpassen. ──────────────────
BEREICH_MIN_OBS = 4

def scale_index(pos, neg):
    total = pos + neg
    if total < BEREICH_MIN_OBS:
        return None
    ratio = pos / total
    if ratio >= 0.80: return 4
    if ratio >= 0.60: return 3
    if ratio >= 0.45: return 2
    if ratio >= 0.30: return 1
    return 0

# ── NOTENVORSCHLAG — exakter Spiegel von getGradeProposal in index.html,
#    inklusive der gedeckelten Tests/HA-Quote/Material-Quote-Korrektur. ──────
GRADE_BANDS_NOTEN = [
    ("1–2",  "sehr gut / gut"),
    ("2–3",  "gut / befriedigend"),
    ("3",    "befriedigend"),
    ("3–4",  "befriedigend / ausreichend"),
    ("4–5",  "ausreichend / mangelhaft"),
    ("5–6",  "mangelhaft / ungenügend"),
]
GRADE_BANDS_PUNKTE = [
    ("12–15", "sehr gut / gut"),
    ("9–11",  "gut / befriedigend"),
    ("7–8",   "befriedigend"),
    ("5–6",   "befriedigend / ausreichend"),
    ("2–4",   "ausreichend / mangelhaft"),
    ("0–1",   "mangelhaft / ungenügend"),
]
MIN_ENTRIES, MIN_DAYS = 6, 3

# Notenpunkte werden am Ende als eine Zahl ins Zeugnis eingetragen, nicht als
# Band — anders als Drittelnoten, wo "2+/2/2−" die Bandbreite schon ausdrückt.
# Rein interpolierte Zusatzangabe, NUR für notenformat "punkte": innerhalb des
# angezeigten Bands (nach Korrektur!) wird die Ratio auf die Punktspanne des
# Bands abgebildet — nicht das Basis-Band, damit die Zahl nie außerhalb dessen
# liegt, was tatsächlich gedruckt steht. (ratio_lo, ratio_hi, punkte_lo, punkte_hi),
# dieselbe Reihenfolge wie GRADE_BANDS_PUNKTE/base_band_index.
PUNKTE_INTERP_BOUNDS = [
    (0.80, 1.00, 12, 15),
    (0.60, 0.80,  9, 11),
    (0.45, 0.60,  7,  8),
    (0.30, 0.45,  5,  6),
    (0.15, 0.30,  2,  4),
    (0.00, 0.15,  0,  1),
]

def interpolate_punkte(ratio, band_idx):
    lo_r, hi_r, lo_p, hi_p = PUNKTE_INTERP_BOUNDS[band_idx]
    r = min(max(ratio, lo_r), hi_r)
    return round(lo_p + (r - lo_r) / (hi_r - lo_r) * (hi_p - lo_p))

def base_band_index(ratio):
    if ratio >= 0.80: return 0
    if ratio >= 0.60: return 1
    if ratio >= 0.45: return 2
    if ratio >= 0.30: return 3
    if ratio >= 0.15: return 4
    return 5

def test_delta(avg, notenformat):
    if avg is None: return 0
    if notenformat == "punkte":
        if avg >= 11: return -1
        if avg <= 5:  return 1
        return 0
    if avg <= 2.0: return -1
    if avg >= 4.0: return 1
    return 0

def hw_delta(quote):
    return 1 if (quote is not None and quote < 0.80) else 0

def material_delta(quote):
    return 1 if (quote is not None and quote < 0.85) else 0

def grade_proposal(entry_count, day_count, ratio, notenformat, test_avg=None, hw_quote=None, mat_quote=None):
    """None, wenn die Mindestmenge (6 Einträge / 3 Tage) noch nicht erreicht ist."""
    if entry_count < MIN_ENTRIES or day_count < MIN_DAYS:
        return None
    bands = GRADE_BANDS_PUNKTE if notenformat == "punkte" else GRADE_BANDS_NOTEN
    base_idx = base_band_index(ratio)
    net = max(-1, min(1, test_delta(test_avg, notenformat) + hw_delta(hw_quote) + material_delta(mat_quote)))
    final_idx = max(0, min(5, base_idx + net))
    punkte_exact = interpolate_punkte(ratio, final_idx) if notenformat == "punkte" else None
    return {"grade": bands[final_idx][0], "label": bands[final_idx][1],
            "base_grade": bands[base_idx][0], "corrected": final_idx != base_idx,
            "punkte_exact": punkte_exact}

def score_label(notenformat):
    return "Punkte" if notenformat == "punkte" else "Note"

# ── STICHPROBEN-DATEN — bei jedem Export durch die echten Beobachtungen aus
#    dem Backup ersetzen (Kriterien-IDs siehe FREMDSPRACHEN_CRITERIA oben).
#    hw_quote/material_quote/test_avg: None lassen, wenn die jeweilige
#    Mindestmenge (6 / 8 / 2) noch nicht erreicht ist. ───────────────────────
STUDENTS = [
    {
        "name": "Ahuja, Priya",
        "observations": {
            "fs1":(8,1), "fs2":(6,2), "fs10":(7,1), "fs11":(5,2),
            "fs12":(6,1), "fs13":(7,0), "fs5":(5,3), "fs9":(6,2), "fs14":(7,1),
        },
        "hw_quote": 0.94, "material_quote": 0.97, "test_avg": 1.7, "absent": 1,
        "notes": [
            ("2026-09-14", "Sehr starke Beteiligung in der Gruppenarbeit."),
            ("2026-10-02", "Spricht konsequent Englisch, auch wenn es schwierig wird."),
        ],
    },
    {
        "name": "Bekele, Samuel",
        "observations": {
            "fs1":(3,5), "fs2":(2,4), "fs10":(2,3), "fs11":(1,4),
            "fs12":(3,3), "fs13":(2,4), "fs5":(3,4), "fs9":(1,5), "fs14":(2,4),
        },
        "hw_quote": 0.51, "material_quote": 0.68, "test_avg": 4.3, "absent": 4,
        "notes": [
            ("2026-09-22", "Wechselt häufig ins Deutsche, mehrfach angesprochen."),
            ("2026-10-15", "HA dreimal nicht dabei — Gespräch geführt."),
        ],
    },
    {
        "name": "Chen, Mei-Lin",
        "observations": {
            "fs1":(6,2), "fs2":(5,1), "fs10":(6,1), "fs11":(4,2),
            "fs12":(6,0), "fs13":(5,1), "fs5":(7,1), "fs9":(5,2), "fs14":(6,1),
        },
        "hw_quote": 1.00, "material_quote": 1.00, "test_avg": 1.3, "absent": 0,
        "notes": [("2026-10-08", "Exzellente Vorbereitung, HA immer vollständig.")],
    },
]

def make_styles():
    return {
        "page_title":    ParagraphStyle("pt",  fontName="Montserrat-Bold",    fontSize=18, textColor=PRUSSIAN, spaceAfter=2*mm, leading=22),
        "page_subtitle": ParagraphStyle("ps",  fontName="Montserrat",         fontSize=10, textColor=GREY_TEXT, spaceAfter=5*mm, leading=14),
        "section_lbl":   ParagraphStyle("sl",  fontName="Montserrat-Bold",    fontSize=9,  textColor=TEAL, spaceAfter=3*mm, leading=11),
        "table_header":  ParagraphStyle("th",  fontName="Montserrat-Bold",    fontSize=8,  textColor=colors.white, leading=10),
        "table_header_sm": ParagraphStyle("ths", fontName="Montserrat-Bold",  fontSize=6.7,textColor=colors.white, leading=8, alignment=1),
        "table_cell":    ParagraphStyle("tc",  fontName="Montserrat",         fontSize=8.5,textColor=BLACK, leading=12),
        "table_dim":     ParagraphStyle("td",  fontName="Montserrat",         fontSize=8,  textColor=GREY_TEXT, leading=11),
        "student_name":  ParagraphStyle("sn",  fontName="Montserrat-Bold",    fontSize=14, textColor=PRUSSIAN, spaceAfter=1*mm, leading=17),
        "student_meta":  ParagraphStyle("sm",  fontName="Montserrat",         fontSize=9,  textColor=GREY_TEXT, spaceAfter=5*mm, leading=12),
        "area_label":    ParagraphStyle("al",  fontName="Montserrat-Bold",    fontSize=9,  textColor=TEAL, spaceAfter=2*mm, spaceBefore=4*mm, leading=11),
        "crit_name":     ParagraphStyle("cn",  fontName="Montserrat-SemiBold",fontSize=9,  textColor=BLACK, leading=12),
        "note_text":     ParagraphStyle("nt",  fontName="Montserrat-Italic",  fontSize=8.5,textColor=BLACK, leading=12),
        "note_date":     ParagraphStyle("nd",  fontName="Montserrat",         fontSize=7.5,textColor=GREY_TEXT, leading=10, alignment=2),
        "footer":        ParagraphStyle("ft",  fontName="Montserrat",         fontSize=7.5,textColor=GREY_TEXT, leading=10),
        "disclaimer":    ParagraphStyle("di",  fontName="Montserrat-Italic",  fontSize=7.5,textColor=GREY_TEXT, leading=10, spaceAfter=2*mm),
        # Original-Blatt
        "sheet_header":  ParagraphStyle("sh",  fontName="Montserrat",         fontSize=10, textColor=BLACK, leading=13),
        "sheet_title":   ParagraphStyle("st",  fontName="Montserrat-Bold",    fontSize=14, textColor=PRUSSIAN, spaceBefore=3*mm, spaceAfter=3*mm, leading=17),
        "sheet_intro":   ParagraphStyle("si",  fontName="Montserrat",         fontSize=8.3,textColor=BLACK, leading=11.5, spaceAfter=3*mm),
        "sheet_row":     ParagraphStyle("sr",  fontName="Montserrat",         fontSize=8,  textColor=BLACK, leading=11),
        "bullet":        ParagraphStyle("bl",  fontName="Montserrat-Italic",  fontSize=8,  textColor=BLACK, leading=11.5, leftIndent=3*mm, spaceAfter=1*mm),
        "footnote":      ParagraphStyle("fn",  fontName="Montserrat-Italic",  fontSize=8,  textColor=GREY_TEXT, spaceBefore=2*mm, spaceAfter=3*mm),
        "footer_box":    ParagraphStyle("fb",  fontName="Montserrat-SemiBold",fontSize=9.5,textColor=BLACK, leading=13),
    }

def obs_ratio(observations):
    """Gesamt-Ratio über alle Kriterien eines Schülers (für den Notenvorschlag)."""
    pos = sum(p for p, n in observations.values())
    neg = sum(n for p, n in observations.values())
    return pos, neg

def section_counts(observations, criteria, bereich):
    pos = neg = 0
    for cid, short, b in criteria:
        if b != bereich:
            continue
        p, n = observations.get(cid, (0, 0))
        pos += p
        neg += n
    return pos, neg

def other_criteria(criteria):
    """Kriterien ohne bogenBereich — eigene Beobachtung, kein Platz auf dem Blatt."""
    return [(cid, short) for cid, short, b in criteria if b is None]

def cell_tendency(pos, neg):
    total = pos + neg
    if total == 0:
        return "–", GREY_TEXT
    ratio = pos / total
    if ratio >= 0.70: return "überwiegend positiv", GREEN
    if ratio >= 0.45: return "ausgeglichen",         AMBER
    return "überwiegend schwach", RED

# ── SEITE 1 — INTERNE KLASSENLISTE (nicht Teil des Original-Blatts) ─────────

def build_overview(styles, criteria):
    story = []
    story.append(Paragraph("ClassPulse", styles["page_title"]))
    story.append(Paragraph(f"{COURSE_NAME} · {HALF_YEAR} · Lehrkraft: {TEACHER}", styles["page_subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRUSSIAN, spaceAfter=4*mm))
    story.append(Paragraph("KLASSENLISTE — INTERNER ÜBERBLICK", styles["section_lbl"]))
    story.append(Paragraph(
        "Bereichsspalten entsprechen den drei Tabellen des Original-Bogens — dieselbe "
        "Aggregation, die auch die Schüler-Seiten hier hinten füllt.",
        styles["table_dim"]))
    story.append(Spacer(1, 2*mm))

    cw = [36*mm, 24*mm, 29*mm, 26*mm, 19*mm, 19*mm, 19*mm]
    hdr = [Paragraph(t, styles["table_header"]) for t in
           ["Name", "Inhalt", "Fachmethoden", "Sprache & Komm.", "HA-Quote", "Material", "Gesamt"]]
    rows = [hdr]

    for st in STUDENTS:
        obs = st["observations"]
        pos, neg = obs_ratio(obs)
        total = pos + neg
        days = MIN_DAYS  # Stichprobendaten haben kein Datum je Eintrag — echte Exporte zählen Tage.
        entry_count = total
        ratio = pos / total if total else 0
        proposal = grade_proposal(entry_count, days, ratio, NOTENFORMAT,
                                   st.get("test_avg"), st.get("hw_quote"), st.get("material_quote"))
        if proposal:
            gesamt = f"{score_label(NOTENFORMAT)} {proposal['grade']}"
            if proposal["punkte_exact"] is not None:
                gesamt += f" ({proposal['punkte_exact']})"
        else:
            gesamt = "—"
        # Anders als auf der Schülerseite bleibt hier sichtbar, WENN pädagogisch
        # angepasst wurde — diese Seite geht nie an Schüler raus, ist also der
        # richtige Ort für den Rechenweg, nicht nur das Ergebnis.
        if st.get("override_grade"):
            gesamt = f"{st['override_grade']} (Vorschlag: {gesamt})" if proposal else st["override_grade"]
        gesamt_color = PRUSSIAN if (proposal or st.get("override_grade")) else GREY_TEXT

        cells = [Paragraph(st["name"], styles["table_cell"])]
        for bereich in BEREICHE:
            p, n = section_counts(obs, criteria, bereich)
            label, tc = cell_tendency(p, n)
            hex_tc = tc.hexval()[2:]
            cells.append(Paragraph(f'+{p}/−{n}<br/><font color="#{hex_tc}" size="7">{label}</font>', styles["table_cell"]))
        cells.append(Paragraph(f'{round(st["hw_quote"]*100)}%' if st.get("hw_quote") is not None else "–", styles["table_cell"]))
        cells.append(Paragraph(f'{round(st["material_quote"]*100)}%' if st.get("material_quote") is not None else "–", styles["table_cell"]))
        hex_g = gesamt_color.hexval()[2:]
        cells.append(Paragraph(f'<font color="#{hex_g}"><b>{gesamt}</b></font>', styles["table_cell"]))
        rows.append(cells)

    t = Table(rows, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  DARK_HEADER),
        ("LINEBELOW",     (0,0),(-1,0),  1.5, PRUSSIAN),
        ("LINEBEFORE",    (0,0),(0,-1),  3,   PRUSSIAN),
        ("GRID",          (0,0),(-1,-1), 0.3, colors.HexColor("#DDDDDD")),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        *[("BACKGROUND",  (0,i+1),(-1,i+1), GREY_LIGHT if i % 2 == 0 else colors.white)
          for i in range(len(STUDENTS))],
    ]))
    story.append(t)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f"Nur für interne Verwendung · Export: {EXPORT_DATE} · ClassPulse Participation Tracker",
        styles["footer"]))
    return story

# ── SEITEN 2+ — REPRODUKTION DES ORIGINAL-BOGENS, EINE SEITE PRO SCHÜLER ────

def build_official_sheet(st, criteria, styles):
    story = [PageBreak()]

    hdr = Table([[
        Paragraph(f"FACH: <u>{COURSE_NAME}</u>", styles["sheet_header"]),
        Paragraph(f"NAME: <u>{st['name']}</u>",  styles["sheet_header"]),
    ]], colWidths=[85*mm, 90*mm])
    hdr.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(hdr)
    story.append(Paragraph(SHEET_TITLE, styles["sheet_title"]))
    story.append(Paragraph(SHEET_INTRO, styles["sheet_intro"]))

    for bereich in BEREICHE:
        story.append(Paragraph(bereich.upper() if bereich != "Sprache & Komm."
                                else "SPRACHE UND KOMMUNIKATION", styles["area_label"]))

        pos, neg = section_counts(st["observations"], criteria, bereich)
        idx = scale_index(pos, neg)

        col_w = [58*mm] + [23.4*mm]*5
        header_row = [Paragraph("Einschätzung der <b>Schülerin</b>/des <b>Schülers</b>", styles["table_header_sm"])] + \
                     [Paragraph(c, styles["table_header_sm"]) for c in SHEET_COLUMNS]
        rating_row = [Paragraph(SHEET_ROW_LABEL, styles["sheet_row"])] + \
                     [Paragraph("✕" if idx == i else "", styles["table_cell"]) for i in range(5)]
        t = Table([header_row, rating_row], colWidths=col_w)
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),  DARK_HEADER),
            ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#BBBBBB")),
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 3),
            ("RIGHTPADDING",  (0,0),(-1,-1), 3),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("ALIGN",         (1,0),(-1,-1), "CENTER"),
            *([("BACKGROUND", (idx+1,1),(idx+1,1), TEAL_LIGHT)] if idx is not None else []),
        ]))
        story.append(t)
        story.append(Spacer(1, 1.5*mm))
        for b in SHEET_BULLETS[bereich]:
            story.append(Paragraph(f"•  {b}", styles["bullet"]))

    story.append(Paragraph(SHEET_FOOTNOTE, styles["footnote"]))

    others = other_criteria(criteria)
    if others:
        lines = []
        for cid, short in others:
            p, n = st["observations"].get(cid, (0, 0))
            label, tc = cell_tendency(p, n)
            hex_tc = tc.hexval()[2:]
            lines.append(f'{short}: <font color="#{hex_tc}"><b>{label}</b></font>')
        story.append(Paragraph(
            "<i>Zusätzlich beobachtet, nicht Teil dieses Bogens:</i> " + " · ".join(lines),
            styles["table_dim"]))
        story.append(Spacer(1, 2*mm))

    pos, neg = obs_ratio(st["observations"])
    total = pos + neg
    ratio = pos / total if total else 0
    proposal = grade_proposal(total, MIN_DAYS, ratio, NOTENFORMAT,
                               st.get("test_avg"), st.get("hw_quote"), st.get("material_quote"))
    # override_grade: das PÄDAGOGISCH entschiedene Ergebnis, nachdem die
    # Lehrkraft die rechnerischen Vorschläge (siehe preview_grades()) gesehen
    # und ggf. angepasst hat. Wenn gesetzt, geht es 1:1 auf den Bogen — der
    # Rechenweg bleibt nur in der internen Klassenliste sichtbar, nicht hier,
    # weil die Schülerseite ohnehin nur "die Einschätzung der Lehrkraft" zeigt,
    # nicht wie sie zustande kam.
    if st.get("override_grade"):
        lehrkraft_note = st["override_grade"]
    elif proposal:
        # Nur "Punkte 12–15" zu drucken sagt niemandem etwas, der die Skala nicht
        # auswendig kennt — das Wort dazu (aus GRADE_BANDS_*) gehört mit drauf.
        lehrkraft_note = f"{score_label(NOTENFORMAT)} {proposal['grade']} ({proposal['label']})"
        # Nur bei Notenpunkten: Notenpunkte werden am Ende als eine Zahl ins
        # Zeugnis eingetragen, deshalb zusätzlich ein rechnerischer Einzelwert
        # innerhalb des Bands — bei Drittelnoten gibt es diese Erwartung nicht.
        if proposal["punkte_exact"] is not None:
            lehrkraft_note += f" · rechnerisch: {proposal['punkte_exact']}"
    else:
        lehrkraft_note = "noch nicht möglich"

    # student_grade: Selbsteinschätzung, z.B. digital über IServ eingesammelt
    # und hier übertragen — dann muss die Zeile nicht mehr per Hand ausgefüllt
    # werden. Leer gelassen bleibt sie eine echte Linie zum Selbst-Ausfüllen.
    student_line = f"Meine Noteneinschätzung: {st['student_grade']}" if st.get("student_grade") \
        else "Meine Noteneinschätzung: ____________"

    footer = Table([[
        Paragraph(student_line, styles["footer_box"]),
        Paragraph(f"Note der Lehrkraft: {lehrkraft_note}", styles["footer_box"]),
    ]], colWidths=[85*mm, 90*mm])
    footer.setStyle(TableStyle([
        ("BOX",           (0,0),(-1,-1), 0.6, colors.HexColor("#999999")),
        ("LINEAFTER",     (0,0),(0,-1),  0.6, colors.HexColor("#999999")),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(Spacer(1, 3*mm))
    story.append(footer)

    if st["notes"]:
        story.append(Spacer(1, 4*mm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=GREY_TEXT, spaceAfter=3*mm))
        story.append(Paragraph("BEOBACHTUNGEN & NOTIZEN (für das Gespräch, nicht auf dem Original-Bogen)", styles["area_label"]))
        for date, note in st["notes"]:
            nb = Table([[
                Paragraph(f"→ {note}", styles["note_text"]),
                Paragraph(date, styles["note_date"]),
            ]], colWidths=[125*mm, 40*mm])
            nb.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), TEAL_LIGHT),
                ("LINEBEFORE",    (0,0),(0,-1),  3, TEAL),
                ("TOPPADDING",    (0,0),(-1,-1), 5),
                ("BOTTOMPADDING", (0,0),(-1,-1), 5),
                ("LEFTPADDING",   (0,0),(-1,-1), 7),
                ("RIGHTPADDING",  (0,0),(-1,-1), 7),
                ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ]))
            story.append(nb)
            story.append(Spacer(1, 1.5*mm))

    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.3, color=GREY_TEXT, spaceAfter=2*mm))
    story.append(Paragraph(
        f"ClassPulse · {COURSE_NAME} · Export {EXPORT_DATE} · Lehrkraft: {TEACHER} · "
        f"Zählt {MITARBEIT_PCT}% der Gesamtnote",
        styles["footer"]))
    return story

def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=f"ClassPulse — {COURSE_NAME}", author=TEACHER)
    styles = make_styles()
    criteria = criteria_for(CRITERIA_TYPE)
    story = build_overview(styles, criteria)
    for st in STUDENTS:
        story += build_official_sheet(st, criteria, styles)
    doc.build(story)
    print(f"✓ {path}")

# ── VORSCHAU — vor build_pdf() aufrufen, NICHT überspringen ─────────────────
# Zeigt, was jeder Schüler rechnerisch bekäme, BEVOR die Bögen als PDF
# entstehen — der Moment, in dem die Lehrkraft laut eigener Ansage auf dem
# Bogen ("Über die Gewichtung entscheidet die Lehrkraft in pädagogischer
# Verantwortung") auch tatsächlich etwas entscheiden kann, statt dass der
# Satz nur so dasteht. Zwei Felder pro Schüler in STUDENTS nehmen das Ergebnis
# dieser Kontrolle auf:
#   "override_grade": pädagogisch angepasstes Ergebnis, z.B. "Punkte 13"
#                      oder "Note 2–3" — überschreibt den Rechenwert 1:1 auf
#                      dem Bogen; leer/weggelassen = Rechenwert wird gedruckt.
#   "student_grade":  Selbsteinschätzung der Schülerin/des Schülers, falls
#                      schon bekannt (z.B. von IServ übertragen) — füllt die
#                      "Meine Noteneinschätzung"-Zeile; leer = Zeile bleibt
#                      blanko zum Selbst-Ausfüllen von Hand.
def preview_grades(students, notenformat, criteria_type_label=""):
    print(f"\n── Vorschau {criteria_type_label} ──".rstrip())
    for st in students:
        pos, neg = obs_ratio(st["observations"])
        total = pos + neg
        ratio = pos / total if total else 0
        proposal = grade_proposal(total, MIN_DAYS, ratio, notenformat,
                                   st.get("test_avg"), st.get("hw_quote"), st.get("material_quote"))
        if proposal:
            rechnerisch = f"{score_label(notenformat)} {proposal['grade']} ({proposal['label']})"
            if proposal["punkte_exact"] is not None:
                rechnerisch += f" [{proposal['punkte_exact']}]"
        else:
            rechnerisch = "noch nicht möglich"
        override = f"  →  ÜBERSCHRIEBEN MIT: {st['override_grade']}" if st.get("override_grade") else ""
        selbst = f"  ·  Selbsteinschätzung: {st['student_grade']}" if st.get("student_grade") else ""
        print(f"{st['name']:<28} {total:>2} Einträge   {rechnerisch}{override}{selbst}")
    print()

if __name__ == "__main__":
    preview_grades(STUDENTS, NOTENFORMAT)
    build_pdf("/home/claude/classpulse_v4.pdf")
