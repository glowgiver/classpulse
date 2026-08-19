#!/usr/bin/env python3
"""
ClassPulse — Student Info Sheet, one PDF per course

For the start of the school year: a one-page, bilingual (EN/DE) sheet per
course that tells students transparently how their participation grade comes
about — what's observed, how often, the course's actual weighting, and how
tests/homework/materials factor in as a capped correction. Meant to be
uploaded (IServ) or presented on the first lesson of each course.

Criteria and weighting mirror COURSES_META / FREMDSPRACHEN_CRITERIA /
GENERAL_CRITERIA in index.html and the correction logic in
classpulse_export.py — keep the three in sync when either changes.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

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

TEACHER = "Philipp Tran-Huynh"

# ── KURSE — Spiegel von COURSES_META in index.html. subject_en/subject_de nur
#    zur Anzeige; "PGW" bleibt an Stellen, wo die Fachkonferenz Geschichte/PGW
#    diesen Namen selbst benutzt (Jg9/11P Social Studies). ───────────────────
COURSES = [
    # name,                  criteriaType,      mitarbeit, notenformat,     subject_en,                          subject_de
    ("8a Englisch",          "fremdsprachen",   60,        "drittelnoten",  "English (Class 8a)",                "Englisch (8a)"),
    ("Jg8 History",          "general",         60,        "drittelnoten",  "History (Year 8)",                  "Geschichte (Jg. 8)"),
    ("Jg9 Social Studies",   "general",         70,        "drittelnoten",  "Social Studies / PGW (Year 9, bilingual)", "Gesellschaft / PGW (Jg. 9, bilingual)"),
    ("11P Social Studies",   "general",         60,        "punkte",        "Social Studies / PGW (11P)",        "Gesellschaft / PGW (11P)"),
    ("Jg10 Social Studies",  "general",         60,        "drittelnoten",  "Social Studies / PGW (Year 10)",    "Gesellschaft / PGW (Jg. 10)"),
    ("Jg10 History",         "general",         60,        "drittelnoten",  "History (Year 10)",                 "Geschichte (Jg. 10)"),
    ("12. Kl. Englisch",     "fremdsprachen",   60,        "punkte",        "English (12th Grade)",              "Englisch (12. Kl.)"),
    ("11P WiE",              "general",         60,        "punkte",        "Business & Economics (11P)",        "WiE (11P)"),
    ("12. Kl. WiE",          "general",         60,        "punkte",        "Business & Economics (12th Grade)", "WiE (12. Kl.)"),
]

# ── KRITERIEN — EN/DE-Kurzform, Spiegel von FREMDSPRACHEN_CRITERIA /
#    GENERAL_CRITERIA (index.html). Reihenfolge egal, hier zur Übersicht
#    nach Bogen-Bereich sortiert. ─────────────────────────────────────────────
FREMDSPRACHEN_CRITERIA = [
    ("Contributions in class",               "Beiträge im Unterricht"),
    ("Building arguments",                   "Argumente aufbauen"),
    ("Reflection",                           "Reflexion"),
    ("Working with texts & materials",       "Umgang mit Texten & Material"),
    ("Planning your work",                   "Arbeitsplanung"),
    ("Vocabulary & grammar",                 "Vokabeln & Grammatik"),
    ("Fluency & use of the target language", "Sprachfluss & Zielsprache"),
    ("Responding to others",                 "Auf andere eingehen"),
    ("Active participation",                 "Beteiligung"),
]
GENERAL_CRITERIA = [
    ("Factually correct contributions", "Sachlich richtige Beiträge"),
    ("Building arguments",              "Argumente aufbauen"),
    ("Reflection",                      "Reflexion"),
    ("Working with texts & materials",  "Umgang mit Bezugstexten & Material"),
    ("Planning your work",              "Arbeitsplanung"),
    ("Subject-specific language",       "Fachsprache"),
    ("Language correctness",            "Sprachrichtigkeit"),
    ("Responding to others",            "Auf andere eingehen"),
]

def criteria_for(criteria_type):
    return FREMDSPRACHEN_CRITERIA if criteria_type == "fremdsprachen" else GENERAL_CRITERIA

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
    content = [
        [Paragraph("How is your participation graded?", styles["hero_title"]),],
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
    rows = []
    for i in range(0, len(criteria), 2):
        left_en, left_de = criteria[i]
        right_en, right_de = criteria[i+1] if i+1 < len(criteria) else ("", "")

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
        Table([[Paragraph(label_en, styles["body_en"])], [Paragraph(label_de, styles["body_de"])]], colWidths=[w1]),
        Table([[Paragraph(value_en, styles["body_en"])], [Paragraph(value_de, styles["body_de"])]], colWidths=[w2]),
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

def info_rows_for(mitarbeit, notenformat):
    written_pct = 100 - mitarbeit
    grade_en = "grade points, 0–15" if notenformat == "punkte" else "grades, 1–6"
    grade_de = "Notenpunkten, 0–15" if notenformat == "punkte" else "Noten, 1–6"
    return [
        ("How often",    "Wie oft",
         "I observe students systematically throughout the semester — every student is observed regularly, across different lesson types and phases.",
         "Ich beobachte Schüler/innen systematisch über das Halbjahr — jede/r wird regelmäßig in verschiedenen Unterrichtssituationen beobachtet."),
        ("Rating",       "Bewertung",
         "Each observation is rated + (positive) or − (needs improvement). No intermediate steps.",
         "Jede Beobachtung wird mit + (positiv) oder − (Verbesserungsbedarf) bewertet. Keine Zwischenstufen."),
        ("When",         "Wann",
         "Participation grades are given per semester (Halbjahr). One bad day does not decide your grade — a grade only forms once enough observations have built up.",
         "Mitarbeitsnoten werden pro Halbjahr vergeben. Ein einzelner schlechter Tag entscheidet nicht — eine Note bildet sich erst, wenn genug Beobachtungen vorliegen."),
        ("Weighting",    "Gewichtung",
         f"{mitarbeit}% oral participation (sonstige Leistungen) · {written_pct}% written work (Klausuren / Tests)",
         f"{mitarbeit}% mündliche Mitarbeit (sonstige Leistungen) · {written_pct}% schriftliche Leistungen"),
        ("Tests & preparation", "Tests & Vorbereitung",
         "Vocabulary tests or exams, missing homework, or repeatedly missing materials can shift your grade by at most one step — never more, and only once there's a real pattern, not from a single bad day.",
         "Vokabeltests/Klausuren, fehlende Hausaufgaben oder wiederholt fehlendes Material können deine Note um höchstens eine Stufe verschieben — nie mehr, und nur bei einem echten Muster, nicht bei einem einzelnen schlechten Tag."),
        ("Your grade",   "Deine Note",
         f"Your grade reflects a consistent pattern over the semester, expressed in {grade_en} — not a single moment.",
         f"Deine Note spiegelt ein konsistentes Muster über das Halbjahr wider, in {grade_de} — nicht einzelne Momente."),
    ]

def slug(name):
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-")

def build_sheet(output_path, subject_en, subject_de, criteria, mitarbeit, notenformat, teacher=TEACHER):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=14*mm, bottomMargin=14*mm,
    )
    styles = make_styles()
    story  = []

    story.append(hero_block(styles, subject_en, subject_de, teacher))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("WHAT I OBSERVE · WAS ICH BEOBACHTE", styles["section_label"]))
    for row in criteria_table(criteria, styles):
        story.append(row)
    story.append(Spacer(1, 4*mm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DDDDDD"), spaceAfter=4*mm))

    story.append(Paragraph("HOW IT WORKS · WIE ES FUNKTIONIERT", styles["section_label"]))
    for en_label, de_label, en_val, de_val in info_rows_for(mitarbeit, notenformat):
        story.append(info_row(en_label, de_label, en_val, de_val, styles))
        story.append(Spacer(1, 3*mm))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DDDDDD"), spaceAfter=3*mm))

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

    story.append(Paragraph(
        f"Gymnasium Grootmoor Hamburg · {teacher} · ClassPulse Participation System · {subject_en}",
        styles["footer"]
    ))

    doc.build(story)
    print(f"✓ {output_path}")

if __name__ == "__main__":
    for name, criteria_type, mitarbeit, notenformat, subject_en, subject_de in COURSES:
        build_sheet(
            f"/home/claude/ClassPulse_InfoSheet_{slug(name)}.pdf",
            subject_en, subject_de,
            criteria_for(criteria_type),
            mitarbeit, notenformat,
        )
