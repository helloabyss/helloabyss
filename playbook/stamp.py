"""Stamp running feet onto the built PDF.

Chromium's own header/footer reserves a band at the bottom of every sheet --
including the zero-margin pages -- which clips the full-bleed cover and part
dividers. So the feet are added here instead, and skipped on any page whose
top-left pixel is dark (i.e. a full-bleed page).
"""
import base64, io, re, sys
import pymupdf

PDF   = "dist/The-Faceless-Channel-Playbook.pdf"
FONTS = "src/fonts.css"
TITLE = "The Faceless Channel Playbook"

def serif_regular() -> bytes:
    css = open(FONTS).read()
    m = re.search(
        r"font-family:'Source Serif 4';font-style:normal;font-weight:400;"
        r"font-display:block;src:url\(data:font/ttf;base64,([^)]+)\)", css)
    if not m:
        sys.exit("Source Serif 4 regular not found in fonts.css")
    return base64.b64decode(m.group(1))

def is_full_bleed(page) -> bool:
    pix = page.get_pixmap(clip=pymupdf.Rect(2, 2, 6, 6))
    r, g, b = pix.pixel(0, 0)[:3]
    return (r + g + b) / 3 < 110

def main():
    doc = pymupdf.open(PDF)
    font = serif_regular()
    y = 792 - 44            # 44pt up from the foot of a US Letter sheet
    left, right = 68.4, 612 - 68.4
    stamped = 0
    for i, page in enumerate(doc):
        if is_full_bleed(page):
            continue
        page.insert_font(fontname="SS4", fontbuffer=font)
        page.insert_text((left, y), TITLE.upper(), fontname="SS4",
                         fontsize=6.6, color=(0.55, 0.55, 0.57),
                         render_mode=0, fill_opacity=1)
        num = str(i + 1)
        w = pymupdf.get_text_length(num, fontsize=8.5, fontname="helv")
        page.insert_text((right - w, y), num, fontname="SS4",
                         fontsize=8.5, color=(0.55, 0.55, 0.57))
        stamped += 1
    doc.saveIncr()
    print(f"stamped running feet on {stamped} of {doc.page_count} pages")

if __name__ == "__main__":
    main()
