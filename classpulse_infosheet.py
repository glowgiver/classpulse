#!/usr/bin/env python3
"""
ClassPulse — Student Info Sheet
Bilingual (EN/DE), two versions: English courses + General courses
One page each, Montserrat, Prussian/Teal design
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "/usr/share/fonts/truetype/montserrat/"
pdfmetrics.registerFont(TTFont("Montserrat",         FONT_DIR + "Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Bold",    FONT_DIR + "Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-SemiBold",FONT_DIR + "Montserrat-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Italic",  FONT_DIR + "Montserrat-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Montserrat-Light",   FONT_DIR + "Montserrat-Light.ttf"))

PRUSSIAN    = colors.HexColor("#023A5D")
TEAL        = colors.HexColor("#1B5E79")
TEAL_LIGHT  = colors.HexColor("#E8F2F5")
DARK_HEADER = colors.HexColor("#44546A")
GREY_LIGHT  = colors.HexColor("#F5F5F5")
GREY_TEXT   = colors.HexColor("#555555")
BLACK       = colors.HexColor("#111111")
WHITE       = colors.white

def make_styles():
    return {
        "hero_title": ParagraphStyle("ht",
            fontName="Montserrat-Bold", fontSize=22,
            textColor=WHITE, leading=26, spaceAfter=2*mm),
        "hero_sub": ParagraphStyle("hs",
            fontName="Montserrat-Light", fontSize=11,
            textColor=colors.HexColor("#B0C8D8"), leading=15),
        "section_label": ParagraphStyle("sl",
            fontName="Montserrat-Bold", fontSize=8,
            textColor=TEAL, leading=10, spaceAfter=2*mm,
            spaceBefore=5*mm),
        "body_en": ParagraphStyle("be",
            fontName="Montserrat-SemiBold", fontSize=10.5,
            textColor=BLACK, leading=15, spaceAfter=1*mm),
        "body_de": ParagraphStyle("bd",
            fontName="Montserrat-Italic", fontSize=9,
            textColor=GREY_TEXT, leading=13, spaceAfter=3*mm),
        "crit_en": ParagraphStyle("ce",
            fontName="Montserrat-SemiBold", fontSize=9.5,
            textColor=BLACK, leading=13),
        "crit_de": ParagraphStyle("cd",
            fontName="Montserrat-Italic", fontSize=8,
            textColor=GREY_TEXT, leading=11),
        "footer": ParagraphStyle("ft",
            fontName="Montserrat", fontSize=7.5,
            textColor=GREY_TEXT, leading=10, alignment=1),
        "note": ParagraphStyle("nt",
            fontName="Montserrat-Italic", fontSize=8.5,
            textColor=GREY_TEXT, leading=12),
    }

def hero_block(styles, subject_en, subject_de, teacher):
    """Dark header banner with title"""
    content = [
        [Paragraph(f"How is your participation graded?", styles["hero_title"]),],
        [Paragraph(f"Wie wird deine Mitarbeit bewertet? · {subject_en} / {subject_de}", styles["hero_sub"]),],
    ]
    t = Table(content, colWidths=[174*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), PRUSSIAN),
        ("TOPPADDING",    (0,0), (-1,-1), 6*mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5*mm),
        ("LEFTPADDING",   (0,0), (-1,-1), 7*mm),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7*mm),
        ("LINEBEFORE",    (0,0), (0,-1),  6, TEAL),
    ]))
    return t

def criteria_table(criteria, styles):
    """2-column grid of criteria"""
    rows = []
    for i in range(0, len(criteria), 2):
        left_en, left_de = criteria[i]
        if i+1 < len(criteria):
            right_en, right_de = criteria[i+1]
        else:
            right_en, right_de = "", ""

        def cell(en, de):
            if not en: return ""
            inner = Table([
                [Paragraph(en, styles["crit_en"])],
                [Paragraph(de, styles["crit_de"])],
            ], colWidths=[80*mm])
            inner.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), TEAL_LIGHT),
                ("TOPPADDING",    (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("LEFTPADDING",   (0,0), (-1,-1), 6),
                ("RIGHTPADDING",  (0,0), (-1,-1), 4),
                ("LINEBEFORE",    (0,0), (0,-1),  3, TEAL),
            ]))
            return inner

        row = Table([[cell(left_en, left_de), cell(right_en, right_de)]],
                    colWidths=[87*mm, 87*mm])
        row.setStyle(TableStyle([
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 3),
            ("TOPPADDING",    (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        rows.append(row)
    return rows

def info_row(label_en, label_de, value_en, value_de, styles, w1=55*mm, w2=119*mm):
    t = Table([[
        Table([
            [Paragraph(label_en, styles["body_en"])],
            [Paragraph(label_de, styles["body_de"])],
        ], colWidths=[w1]),
        Table([
            [Paragraph(value_en, styles["body_en"])],
            [Paragraph(value_de, styles["body_de"])],
        ], colWidths=[w2]),
    ]], colWidths=[w1, w2])
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LINEBEFORE",    (0,0), (0,-1),  3, PRUSSIAN),
        ("LEFTPADDING",   (0,0), (0,-1),  6),
    ]))
    return t

# ── VERSION 1: ENGLISH COURSES ───────────────────────────────────────────────

FS_CRITERIA = [
    ("Active participation",         "Aktive Beteiligung am Unterricht"),
    ("Quality of contributions",     "Inhaltliche Qualität der Beiträge"),
    ("Homework & materials",         "Hausaufgaben & Heftführung"),
    ("Responsibility for learning",  "Eigenverantwortung für den Lernprozess"),
    ("Vocabulary & grammar",         "Vokabeln & Grammatik"),
    ("Fluency & pronunciation",      "Sprachfluss & Aussprache"),
    ("Use of English",               "Durchgängiger Gebrauch der Fremdsprache"),
    ("Tests (trend only)",           "Tests (nur Tendenz +/−)"),
]

# ── VERSION 2: GENERAL COURSES ───────────────────────────────────────────────

GEN_CRITERIA = [
    ("Factually correct contributions", "Sachlich richtige Beiträge"),
    ("Building arguments",              "Aufbauende Argumentation"),
    ("Reflection & critical thinking",  "Reflexion & kritisches Denken"),
    ("Working with sources & media",    "Umgang mit Texten & Medien"),
    ("Work organisation",               "Arbeitsplanung & -durchführung"),
    ("Subject-specific language",       "Fachsprache & Ausdrucksvermögen"),
    ("Language correctness",            "Sprachliche Richtigkeit"),
    ("Responding to others",            "Eingehen auf Mitschüler/innen"),
]

def build_sheet(output_path, subject_en, subject_de, criteria, teacher="Tran-Huynh"):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=14*mm, bottomMargin=14*mm,
    )
    styles = make_styles()
    story  = []

    # Hero
    story.append(hero_block(styles, subject_en, subject_de, teacher))
    story.append(Spacer(1, 5*mm))

    # What I observe
    story.append(Paragraph("WHAT I OBSERVE · WAS ICH BEOBACHTE", styles["section_label"]))
    for row in criteria_table(criteria, styles):
        story.append(row)
    story.append(Spacer(1, 4*mm))

    story.append(HRFlowable(width="100%", thickness=0.5,
                            color=colors.HexColor("#DDDDDD"), spaceAfter=4*mm))

    # How it works
    story.append(Paragraph("HOW IT WORKS · WIE ES FUNKTIONIERT", styles["section_label"]))

    infos = [
        ("How often",    "Wie oft",
         "I observe students systematically throughout the semester — every student is observed regularly, across different lesson types and phases.",
         "Ich beobachte Schüler/innen systematisch über das Halbjahr — jede/r wird regelmäßig in verschiedenen Unterrichtssituationen beobachtet."),
        ("Rating",       "Bewertung",
         "Each observation is rated + (positive) or − (needs improvement). No intermediate steps.",
         "Jede Beobachtung wird mit + (positiv) oder − (Verbesserungsbedarf) bewertet. Keine Zwischenstufen."),
        ("When",         "Wann",
         "Participation grades are given per semester (Halbjahr). One bad day does not decide your grade.",
         "Mitarbeitsnoten werden pro Halbjahr vergeben. Ein einzelner schlechter Tag entscheidet nicht."),
        ("Weighting",    "Gewichtung",
         "60% oral participation (sonstige Leistungen) · 40% written work (Klausuren / Tests)",
         "60% mündliche Mitarbeit (sonstige Leistungen) · 40% schriftliche Leistungen"),
        ("Your grade",   "Deine Note",
         "Your grade reflects a consistent pattern over the semester — not a single moment. Homework and test results are indicators, not separate sub-grades that are calculated into a formula.",
         "Deine Note spiegelt ein konsistentes Muster über das Halbjahr wider — nicht einzelne Momente. Hausaufgaben und Testergebnisse sind Indikatoren, keine eigenständigen Teilnoten die mechanisch verrechnet werden."),
    ]

    for en_label, de_label, en_val, de_val in infos:
        story.append(info_row(
            f"{en_label}", f"{de_label}",
            en_val, de_val, styles
        ))
        story.append(Spacer(1, 3*mm))

    story.append(HRFlowable(width="100%", thickness=0.5,
                            color=colors.HexColor("#DDDDDD"), spaceAfter=3*mm))

    # Note
    story.append(Paragraph(
        "Questions? Talk to me — I'm happy to explain your current standing at any time. · "
        "Fragen? Sprich mich an — ich erkläre dir deinen aktuellen Stand jederzeit gerne.",
        styles["note"]
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Quarterly feedback: You will receive your individual participation update via IServ (Aufgabenmodul) — "
        "only you can see your own feedback. · "
        "Quartalsfeedback: Du erhältst deinen individuellen Zwischenstand per IServ (Aufgabenmodul) — "
        "nur du siehst dein eigenes Feedback.",
        styles["note"]
    ))
    story.append(Spacer(1, 3*mm))

    # Footer
    story.append(Paragraph(
        f"Gymnasium Grootmoor Hamburg · {teacher} · ClassPulse Participation System · {subject_en}",
        styles["footer"]
    ))

    doc.build(story)
    print(f"✓ {output_path}")

build_sheet(
    "/home/claude/ClassPulse_InfoSheet_English.pdf",
    "English", "Englisch",
    FS_CRITERIA
)
build_sheet(
    "/home/claude/ClassPulse_InfoSheet_General.pdf",
    "History / Social Studies / WiE", "Geschichte / Gesellschaft / WiE",
    GEN_CRITERIA
)
