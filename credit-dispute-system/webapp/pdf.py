"""Render plain-text letters to PDF (Letter size, 1-inch margins, wrapped Courier-free body)."""

import io
import textwrap

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

FONT, SIZE, LEADING, WIDTH_CHARS = "Helvetica", 10.5, 14, 92


def text_to_pdf(text, title="Letter"):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle(title)
    w, h = letter
    x, top, bottom = 72, h - 72, 72
    y = top
    c.setFont(FONT, SIZE)
    for para in text.split("\n"):
        indent = len(para) - len(para.lstrip(" "))
        lines = textwrap.wrap(para.strip(), WIDTH_CHARS - indent, subsequent_indent="  " if para.lstrip().startswith("-") else "") or [""]
        for ln in lines:
            if y < bottom:
                c.showPage()
                c.setFont(FONT, SIZE)
                y = top
            c.drawString(x + indent * 5, y, ln)
            y -= LEADING
    c.save()
    return buf.getvalue()
