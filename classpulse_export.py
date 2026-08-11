#!/usr/bin/env python3
"""ClassPulse PDF v3 — farbenblind-freundlich: Text + Farbe"""

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

COURSE_NAME = "8a Englisch"
TEACHER     = "Philipp Tran-Huynh"
HALF_YEAR   = "Schuljahr 2026/27 · Halbjahr 1"
EXPORT_DATE = datetime.date.today().strftime("%-d. %B %Y")

FS_CRITERIA = [
    ("Beteiligung",    "Engagement"),
    ("Beiträge",       "Engagement"),
    ("HA & Heft",      "Arbeitsverhalten"),
    ("Verantwortung",  "Arbeitsverhalten"),
    ("Vokabeln/Gram.", "Sprache"),
    ("Sprachfluss",    "Sprache"),
    ("Fremdsprache",   "Sprache"),
    ("Tests",          "Sprache"),
]

STUDENTS = [
    {
        "name": "Ahuja, Priya",
        "observations": {
            "Beteiligung":    (8,1), "Beiträge":       (6,2),
            "HA & Heft":      (9,0), "Verantwortung":  (7,1),
            "Vokabeln/Gram.": (5,3), "Sprachfluss":    (6,2),
            "Fremdsprache":   (8,1), "Tests":          (4,1),
        },
        "hw_pct": 94, "absent": 1,
        "notes": [
            ("2026-09-14", "Sehr starke Beteiligung in der Gruppenarbeit."),
            ("2026-10-02", "Spricht konsequent Englisch, auch wenn es schwierig wird."),
        ],
        "trend": "stark",
    },
    {
        "name": "Bekele, Samuel",
        "observations": {
            "Beteiligung":    (3,5), "Beiträge":       (2,4),
            "HA & Heft":      (4,3), "Verantwortung":  (2,5),
            "Vokabeln/Gram.": (3,4), "Sprachfluss":    (2,5),
            "Fremdsprache":   (1,6), "Tests":          (0,3),
        },
        "hw_pct": 51, "absent": 4,
        "notes": [
            ("2026-09-22", "Wechselt häufig ins Deutsche, mehrfach angesprochen."),
            ("2026-10-15", "HA dreimal nicht dabei — Gespräch geführt."),
        ],
        "trend": "schwach",
    },
    {
        "name": "Chen, Mei-Lin",
        "observations": {
            "Beteiligung":    (6,2), "Beiträge":       (5,1),
            "HA & Heft":      (8,0), "Verantwortung":  (6,1),
            "Vokabeln/Gram.": (7,1), "Sprachfluss":    (5,2),
            "Fremdsprache":   (7,0), "Tests":          (3,0),
        },
        "hw_pct": 100, "absent": 0,
        "notes": [("2026-10-08", "Exzellente Vorbereitung, HA immer vollständig.")],
        "trend": "stark",
    },
    {
        "name": "Döring, Luca",
        "observations": {
            "Beteiligung":    (4,3), "Beiträge":       (4,2),
            "HA & Heft":      (5,2), "Verantwortung":  (4,2),
            "Vokabeln/Gram.": (4,3), "Sprachfluss":    (3,3),
            "Fremdsprache":   (4,2), "Tests":          (2,1),
        },
        "hw_pct": 78, "absent": 2, "notes": [], "trend": "mittel",
    },
    {
        "name": "Eriksen, Sofie",
        "observations": {
            "Beteiligung":    (7,1), "Beiträge":       (6,1),
            "HA & Heft":      (7,1), "Verantwortung":  (7,0),
            "Vokabeln/Gram.": (6,1), "Sprachfluss":    (7,0),
            "Fremdsprache":   (8,0), "Tests":          (3,0),
        },
        "hw_pct": 92, "absent": 1,
        "notes": [("2026-09-30", "Sehr flüssiges Englisch, native-level Aussprache.")],
        "trend": "stark",
    },
]

def make_styles():
    return {
        "page_title":    ParagraphStyle("pt",  fontName="Montserrat-Bold",    fontSize=18, textColor=PRUSSIAN, spaceAfter=2*mm, leading=22),
        "page_subtitle": ParagraphStyle("ps",  fontName="Montserrat",         fontSize=10, textColor=GREY_TEXT, spaceAfter=5*mm, leading=14),
        "section_lbl":   ParagraphStyle("sl",  fontName="Montserrat-Bold",    fontSize=9,  textColor=TEAL, spaceAfter=3*mm, leading=11),
        "table_header":  ParagraphStyle("th",  fontName="Montserrat-Bold",    fontSize=8,  textColor=colors.white, leading=10),
        "table_cell":    ParagraphStyle("tc",  fontName="Montserrat",         fontSize=8.5,textColor=BLACK, leading=12),
        "table_dim":     ParagraphStyle("td",  fontName="Montserrat",         fontSize=8,  textColor=GREY_TEXT, leading=11),
        "student_name":  ParagraphStyle("sn",  fontName="Montserrat-Bold",    fontSize=14, textColor=PRUSSIAN, spaceAfter=1*mm, leading=17),
        "student_meta":  ParagraphStyle("sm",  fontName="Montserrat",         fontSize=9,  textColor=GREY_TEXT, spaceAfter=5*mm, leading=12),
        "area_label":    ParagraphStyle("al",  fontName="Montserrat-Bold",    fontSize=8,  textColor=TEAL, spaceAfter=2*mm, leading=10),
        "crit_name":     ParagraphStyle("cn",  fontName="Montserrat-SemiBold",fontSize=9,  textColor=BLACK, leading=12),
        "note_text":     ParagraphStyle("nt",  fontName="Montserrat-Italic",  fontSize=8.5,textColor=BLACK, leading=12),
        "note_date":     ParagraphStyle("nd",  fontName="Montserrat",         fontSize=7.5,textColor=GREY_TEXT, leading=10, alignment=2),
        "footer":        ParagraphStyle("ft",  fontName="Montserrat",         fontSize=7.5,textColor=GREY_TEXT, leading=10),
        "disclaimer":    ParagraphStyle("di",  fontName="Montserrat-Italic",  fontSize=7.5,textColor=GREY_TEXT, leading=10, spaceAfter=2*mm),
    }

def calc_tendency(pos, neg):
    total = pos + neg
    if total == 0:
        return "–",                  "—",          GREY_TEXT, GREY_LIGHT
    ratio = pos / total
    if ratio >= 0.70:
        return "↑ über Erwartung",   "überwiegend positiv",  GREEN,  GREEN_LIGHT
    elif ratio >= 0.45:
        return "→ entspricht Erw.",  "ausgeglichen",          AMBER,  AMBER_LIGHT
    else:
        return "↓ unter Erwartung",  "überwiegend schwach",  RED,    RED_LIGHT

def overall_trend_info(st):
    if st["trend"] == "stark":
        return "↑ über Erwartung",  GREEN,  GREEN_LIGHT
    if st["trend"] == "schwach":
        return "↓ unter Erwartung", RED,    RED_LIGHT
    return "→ entspricht Erw.",     AMBER,  AMBER_LIGHT

# ── KLASSENLISTE ─────────────────────────────────────────────────────────────

def num_cell_with_label(pos, neg, styles):
    """Zahl + Tendenz-Label in einer Zelle — farbenblind-freundlich"""
    total = pos + neg
    if total == 0:
        return Paragraph("–", styles["table_dim"])
    ratio = pos / total
    if ratio >= 0.70:
        symbol, tc = "↑", GREEN
    elif ratio >= 0.45:
        symbol, tc = "→", AMBER
    else:
        symbol, tc = "↓", RED
    hex_tc = tc.hexval()[2:]
    # Zahl in schwarz, Symbol farbig darunter
    return Paragraph(
        f'+{pos} /−{neg}<br/><font color="#{hex_tc}" size="7">{symbol}</font>',
        styles["table_cell"]
    )

def build_overview(styles):
    story = []
    story.append(Paragraph("ClassPulse", styles["page_title"]))
    story.append(Paragraph(f"{COURSE_NAME} · {HALF_YEAR} · Lehrkraft: {TEACHER}", styles["page_subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRUSSIAN, spaceAfter=4*mm))
    story.append(Paragraph("KLASSENLISTE — INTERNER ÜBERBLICK", styles["section_lbl"]))

    cw = [42*mm, 19*mm, 19*mm, 19*mm, 19*mm, 19*mm, 16*mm, 22*mm]
    hdr = [
        Paragraph("Name",          styles["table_header"]),
        Paragraph("Beteiligung",   styles["table_header"]),
        Paragraph("Beiträge",      styles["table_header"]),
        Paragraph("HA & Heft",     styles["table_header"]),
        Paragraph("Vokabeln",      styles["table_header"]),
        Paragraph("Fremdsprache",  styles["table_header"]),
        Paragraph("HA-Quote",      styles["table_header"]),
        Paragraph("Gesamt",        styles["table_header"]),
    ]
    rows = [hdr]

    for i, st in enumerate(STUDENTS):
        obs = st["observations"]
        otlabel, otc, _ = overall_trend_info(st)
        hex_otc = otc.hexval()[2:]
        rows.append([
            Paragraph(st["name"], styles["table_cell"]),
            num_cell_with_label(*obs.get("Beteiligung",    (0,0)), styles),
            num_cell_with_label(*obs.get("Beiträge",       (0,0)), styles),
            num_cell_with_label(*obs.get("HA & Heft",      (0,0)), styles),
            num_cell_with_label(*obs.get("Vokabeln/Gram.", (0,0)), styles),
            num_cell_with_label(*obs.get("Fremdsprache",   (0,0)), styles),
            Paragraph(f'{st["hw_pct"]}%', styles["table_cell"]),
            Paragraph(f'<font color="#{hex_otc}"><b>{otlabel}</b></font>', styles["table_cell"]),
        ])

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
        *[("BACKGROUND",  (0,i+1),(-1,i+1), GREY_LIGHT if i%2==0 else colors.white)
          for i in range(len(STUDENTS))],
    ]))
    story.append(t)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f"Nur für interne Verwendung · Export: {EXPORT_DATE} · ClassPulse Participation Tracker",
        styles["footer"]))
    return story

# ── DETAILSEITEN ─────────────────────────────────────────────────────────────

def build_detail(st, styles):
    story = []
    story.append(PageBreak())

    otlabel, otc, otbg = overall_trend_info(st)
    hex_otc = otc.hexval()[2:]

    hdr = Table([[
        Paragraph(st["name"], styles["student_name"]),
        Paragraph(f'<font color="#{hex_otc}"><b>{otlabel}</b></font>',
                  ParagraphStyle("oh", fontName="Montserrat-Bold", fontSize=11,
                                 textColor=otc, leading=14, alignment=2)),
    ]], colWidths=[110*mm, 65*mm])
    hdr.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "BOTTOM"),
        ("LINEBELOW",     (0,0),(-1,-1), 1.5, PRUSSIAN),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph(
        f"{COURSE_NAME} · {HALF_YEAR} · Fehlzeiten: {st['absent']} Std. · HA-Quote: {st['hw_pct']}%",
        styles["student_meta"]))

    # Criteria by area
    areas = {}
    for crit, area in FS_CRITERIA:
        areas.setdefault(area, []).append(crit)

    for area, crits in areas.items():
        story.append(Paragraph(area.upper(), styles["area_label"]))
        crit_cells = []
        for crit in crits:
            pos, neg = st["observations"].get(crit, (0,0))
            tend_short, tend_long, tc, bg = calc_tendency(pos, neg)
            hex_tc = tc.hexval()[2:]

            # Kachel: Name links, Tendenz rechts (Text + Symbol, kein reines Farbsignal)
            cell = Table([[
                Paragraph(crit, styles["crit_name"]),
                Paragraph(
                    f'<font color="#{hex_tc}"><b>{tend_short}</b></font><br/>'
                    f'<font color="#555555" size="7">{tend_long}</font>',
                    ParagraphStyle("tv", fontName="Montserrat-Bold", fontSize=8.5,
                                   textColor=tc, leading=12, alignment=2)),
            ]], colWidths=[42*mm, 40*mm])
            cell.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), bg),
                ("LINEBEFORE",    (0,0),(0,-1),  3, tc),
                ("TOPPADDING",    (0,0),(-1,-1), 6),
                ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                ("LEFTPADDING",   (0,0),(-1,-1), 7),
                ("RIGHTPADDING",  (0,0),(-1,-1), 7),
                ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ]))
            crit_cells.append(cell)

        for i in range(0, len(crit_cells), 2):
            right = crit_cells[i+1] if i+1 < len(crit_cells) else ""
            pair = Table([[crit_cells[i], right]], colWidths=[87*mm, 87*mm])
            pair.setStyle(TableStyle([
                ("LEFTPADDING",   (0,0),(-1,-1), 0),
                ("RIGHTPADDING",  (0,0),(-1,-1), 3),
                ("TOPPADDING",    (0,0),(-1,-1), 0),
                ("BOTTOMPADDING", (0,0),(-1,-1), 2),
                ("VALIGN",        (0,0),(-1,-1), "TOP"),
            ]))
            story.append(pair)
        story.append(Spacer(1, 3*mm))

    # Notes
    if st["notes"]:
        story.append(HRFlowable(width="100%", thickness=0.5, color=GREY_TEXT, spaceAfter=3*mm))
        story.append(Paragraph("BEOBACHTUNGEN & NOTIZEN", styles["area_label"]))
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

    story.append(Spacer(1, 5*mm))
    story.append(HRFlowable(width="100%", thickness=0.3, color=GREY_TEXT, spaceAfter=2*mm))
    story.append(Paragraph(
        "Die Einschätzungen basieren auf pädagogischen Beobachtungen im Unterricht. "
        "Über die Gewichtung der Kriterien entscheidet die Lehrkraft in pädagogischer Verantwortung (Grootmoor-Bogen).",
        styles["disclaimer"]))
    story.append(Paragraph(
        f"ClassPulse · {COURSE_NAME} · Export {EXPORT_DATE} · Lehrkraft: {TEACHER}",
        styles["footer"]))
    return story

def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=f"ClassPulse — {COURSE_NAME}", author=TEACHER)
    styles = make_styles()
    story  = build_overview(styles)
    for st in STUDENTS:
        story += build_detail(st, styles)
    doc.build(story)
    print(f"✓ {path}")

build_pdf("/home/claude/classpulse_v3.pdf")
