"""Regenerate the downloadable CV from _data/cv.yml: python scripts/export_cv.py."""

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
INK = colors.HexColor("#242735")
ACCENT = colors.HexColor("#66518b")
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.2, leading=12.2, textColor=INK, spaceAfter=3)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.6, leading=11, textColor=colors.HexColor("#5b5f6b"))
HEADING = ParagraphStyle("section", parent=BODY, fontSize=11, leading=14, textColor=ACCENT, spaceBefore=10, spaceAfter=6, keepWithNext=True)
TITLE = ParagraphStyle("name", parent=BODY, fontSize=25, leading=30, spaceAfter=5)


def clean(value):
    return escape(str(value)).replace("\u2013", "-").replace("\u2014", "-").replace("\u2011", "-")


def when(value):
    if not value:
        return ""
    value = str(value)
    if value.lower() in ("present", "now"):
        return "Present"
    try:
        return date.fromisoformat(value[:7] + "-01").strftime("%b %Y")
    except ValueError:
        return value


def export():
    cv = yaml.safe_load((ROOT / "_data/cv.yml").read_text(encoding="utf-8"))["cv"]
    output = ROOT / "assets/pdf/robert-dong-cv.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    story = [Paragraph(clean(cv["name"]), TITLE), Paragraph(clean(cv["label"]), BODY)]
    contacts = [cv.get("location", ""), cv.get("email", "")]
    story.append(Paragraph(" | ".join(clean(v) for v in contacts if v), SMALL))
    for social in cv.get("social_networks", []):
        if social["network"] == "LinkedIn":
            url = "https://www.linkedin.com/in/" + social["username"]
            story.append(Paragraph(f'<link href="{url}" color="#66518b">{url}</link>', SMALL))
    if cv.get("summary"):
        story.extend([Spacer(1, 8), Paragraph(clean(cv["summary"]), BODY)])
    for section, entries in cv["sections"].items():
        story.append(Paragraph(clean(section), HEADING))
        for item in entries:
            title = item.get("title") or item.get("position") or item.get("name") or item.get("institution") or item.get("label", "")
            start, end = when(item.get("start_date")), when(item.get("end_date"))
            if start and not end:
                end = "Present"
            dates = " - ".join(v for v in (start, end) if v) or when(item.get("date") or item.get("releaseDate"))
            row = Table([[Paragraph(f"<b>{clean(title)}</b>", BODY), Paragraph(clean(dates), ParagraphStyle("date", parent=SMALL, alignment=TA_RIGHT))]], colWidths=[385, 137])
            row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
            block = [row]
            secondary = [item.get("company"), item.get("awarder"), item.get("publisher")]
            if "studyType" in item:
                secondary.append(" ".join(str(item.get(k, "")) for k in ("studyType", "area")).strip())
            if any(secondary):
                block.append(Paragraph(" | ".join(clean(v) for v in secondary if v), SMALL))
            if item.get("authors"):
                block.append(Paragraph(", ".join(clean(v) for v in item["authors"]), SMALL))
            for key in ("summary", "keywords", "details"):
                if key == "summary" and section == "Publications":
                    continue
                if item.get(key):
                    block.append(Paragraph(clean(item[key]), BODY))
            for highlight in item.get("highlights", []):
                block.append(Paragraph(clean(highlight), ParagraphStyle("bullet", parent=BODY, leftIndent=10, firstLineIndent=-8), bulletText="-"))
            if item.get("url") and section == "Publications":
                block.append(Paragraph(f'<link href="{clean(item["url"])}" color="#66518b">View publication</link>', SMALL))
            story.extend([KeepTogether(block), Spacer(1, 3)])

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#757783"))
        canvas.drawString(45, 27, cv["name"])
        canvas.drawRightString(567, 27, str(doc.page))

    SimpleDocTemplate(str(output), pagesize=letter, leftMargin=45, rightMargin=45, topMargin=40, bottomMargin=45, title=f'{cv["name"]} - Curriculum vitae', author=cv["name"]).build(story, onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == "__main__":
    export()
