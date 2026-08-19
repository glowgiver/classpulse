#!/usr/bin/env python3
"""
ClassPulse — Student Info Sheet (one universal PDF, all courses)

One bilingual (EN/DE) page, handed out at the start of any course, that
explains transparently how participation is graded — what's observed, how
often, and how tests/homework/materials factor in. Deliberately course-
agnostic: the three observation areas (Inhalt / Fachmethoden / Sprache und
Kommunikation) are the same across every course, mirroring the official
Grootmoor sheet ("Bewertung von Leistungen in der laufenden
Unterrichtsarbeit") students also receive each Halbjahr.

What this sheet does NOT print: weighting (%), and whether the course uses
Noten or Notenpunkte — those genuinely differ per course (see COURSES_META
in index.html) and are said out loud when handing this out, not printed.
That's the whole point of keeping this to one file instead of nine.
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
GREY_TEXT   = colors.HexColor("#555555")
BLACK       = colors.HexColor("#111111")
WHITE       = colors.white

TEACHER = "Philipp Tran-Huynh"

# ── WAS ICH BEOBACHTE — dieselben drei Bereiche wie der offizielle Grootmoor-
#    Bogen, kurz gefasst statt aller 19 Original-Bullets (die stehen wortgleich
#    auf dem Bogen selbst, siehe classpulse_export.py). Bewusst fachneutral,
#    damit ein Blatt für Fremdsprachen wie Allgemein passt. ─────────────────
AREAS = [
    ("Content", "Inhalt", [
        ("My contributions fit the task and are factually correct.",
         "Meine Beiträge passen zur Aufgabe und sind sachlich richtig."),
        ("I reflect critically on results and place them in context.",
         "Ich reflektiere Ergebnisse kritisch und ordne sie ein."),
    ]),
    ("Methods", "Fachmethoden", [
        ("I use texts, media and materials appropriately.",
         "Ich gehe mit Texten, Medien und Material angemessen um."),
        ("I plan and carry out my work sensibly.",
         "Ich plane und führe meine Arbeit sinnvoll durch."),
    ]),
    ("Language & Communication", "Sprache und Kommunikation", [
        ("I express myself clearly and stay on topic.",
         "Ich drücke mich klar aus und bleibe beim Thema."),
        ("I take my classmates' contributions into account.",
         "Ich berücksichtige die Beiträge meiner Mitschüler/innen."),
    ]),
]

INFO_ROWS = [
    ("How often",    "Wie oft",
     "I observe students systematically throughout the semester — every student is observed regularly, across different lesson types and phases.",
     "Ich beobachte Schüler/innen systematisch über das Halbjahr — jede/r wird regelmäßig in verschiedenen Unterrichtssituationen beobachtet."),
    ("Rating",       "Bewertung",
     "Each observation is rated + (positive) or − (needs improvement). No intermediate steps.",
     "Jede Beobachtung wird mit + (positiv) oder − (Verbesserungsbedarf) bewertet. Keine Zwischenstufen."),
    ("When",         "Wann",
     "Participation grades are given per semester (Halbjahr). One bad day does not decide your grade — a grade only forms once enough observations have built up.",
     "Mitarbeitsnoten werden pro Halbjahr vergeben. Ein einzelner schlechter Tag entscheidet nicht — eine Note bildet sich erst, wenn genug Beobachtungen vorliegen."),
    ("Tests & preparation", "Tests & Vorbereitung",
     "Vocabulary tests or exams, missing homework, or repeatedly missing materials can shift your grade by at most one step — never more, and only once there's a real pattern, not from a single bad day.",
     "Vokabeltests/Klausuren, fehlende Hausaufgaben oder wiederholt fehlendes Material können deine Note um höchstens eine Stufe verschieben — nie mehr, und nur bei einem echten Muster, nicht bei einem einzelnen schlechten Tag."),
    ("Your grade",   "Deine Note",
     "Your grade combines this participation assessment with written work (Klausuren/Tests) — I'll tell you the exact weighting and grading scale (Noten or Notenpunkte) for this course.",
     "Deine Note setzt sich aus dieser Mitarbeitsbewertung und schriftlichen Leistungen (Klausuren/Tests) zusammen — die genaue Gewichtung und Notenskala (Noten oder Notenpunkte) für diesen Kurs sage ich dir mündlich."),
]

def make_styles():
    return {
        "hero_title": ParagraphStyle("ht", fontName="Montserrat-Bold", fontSize=22,
            textColor=WHITE, leading=26, spaceAfter=2*mm),
        "hero_sub": ParagraphStyle("hs", fontName="Montserrat-Light", fontSize=11,
            textColor=colors.HexColor("#B0C8D8"), leading=15),
        "section_label": ParagraphStyle("sl", fontName="Montserrat-Bold", fontSize=8,
            textColor=TEAL, leading=10, spaceAfter=2*mm, spaceBefore=5*mm),
        "area_label": ParagraphStyle("al", fontName="Montserrat-Bold", fontSize=9.5,
            textColor=PRUSSIAN, leading=12, spaceBefore=3*mm, spaceAfter=1.5*mm),
        "bullet_en": ParagraphStyle("be", fontName="Montserrat-SemiBold", fontSize=9.5,
            textColor=BLACK, leading=13, leftIndent=3*mm),
        "bullet_de": ParagraphStyle("bd", fontName="Montserrat-Italic", fontSize=8.5,
            textColor=GREY_TEXT, leading=11.5, leftIndent=3*mm, spaceAfter=1.5*mm),
        "body_en": ParagraphStyle("boe", fontName="Montserrat-SemiBold", fontSize=10.5,
            textColor=BLACK, leading=15, spaceAfter=1*mm),
        "body_de": ParagraphStyle("bod", fontName="Montserrat-Italic", fontSize=9,
            textColor=GREY_TEXT, leading=13, spaceAfter=3*mm),
        "footer": ParagraphStyle("ft", fontName="Montserrat", fontSize=7.5,
            textColor=GREY_TEXT, leading=10, alignment=1),
        "note": ParagraphStyle("nt", fontName="Montserrat-Italic", fontSize=8.5,
            textColor=GREY_TEXT, leading=12),
    }

def hero_block(styles):
    content = [
        [Paragraph("How is your participation graded?", styles["hero_title"]),],
        [Paragraph("Wie wird deine Mitarbeit bewertet? · Gymnasium Grootmoor · ClassPulse", styles["hero_sub"]),],
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

def build_sheet(output_path, teacher=TEACHER):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=14*mm, bottomMargin=14*mm,
    )
    styles = make_styles()
    story  = []

    story.append(hero_block(styles))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("WHAT I OBSERVE · WAS ICH BEOBACHTE", styles["section_label"]))
    story.append(Paragraph(
        "Same three areas as the official Grootmoor assessment sheet you'll also receive each Halbjahr — this "
        "is just the short version. · Dieselben drei Bereiche wie der offizielle Grootmoor-Bogen, den du auch "
        "jedes Halbjahr bekommst — hier nur die Kurzfassung.",
        styles["note"]))
    for area_en, area_de, bullets in AREAS:
        story.append(Paragraph(f"{area_en.upper()} · {area_de.upper()}", styles["area_label"]))
        for en, de in bullets:
            story.append(Paragraph(f"•  {en}", styles["bullet_en"]))
            story.append(Paragraph(de, styles["bullet_de"]))

    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DDDDDD"), spaceAfter=4*mm))

    story.append(Paragraph("HOW IT WORKS · WIE ES FUNKTIONIERT", styles["section_label"]))
    for en_label, de_label, en_val, de_val in INFO_ROWS:
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
        f"Gymnasium Grootmoor Hamburg · {teacher} · ClassPulse Participation System",
        styles["footer"]
    ))

    doc.build(story)
    print(f"✓ {output_path}")

if __name__ == "__main__":
    build_sheet("/home/claude/ClassPulse_InfoSheet.pdf")
