"""Thumbnails for the DCA video. 1280x720, channel palette, real NVDA data.
Figures trace to research/2026-09-28-dca.md."""
import math
INK, PAPER, RED, MUTED = "#0B0B0C", "#F5F5F3", "#D42A2A", "#6E6E6E"
NVDA = [2.67, 4.84, 3.34, 5.88, 13.05, 29.41, 14.61, 49.52, 134.29, 186.27, 225.07]  # YE2016..2025, then 2026-09-25

def nvda_line(x0, x1, y0, y1):
    lo, hi = math.log(2.2), math.log(260)
    n = len(NVDA) - 1
    pts = [(x0 + (x1-x0)*i/n, y1 - (y1-y0)*(math.log(p)-lo)/(hi-lo)) for i, p in enumerate(NVDA)]
    path = " ".join(f"{'M' if i==0 else 'L'} {x:.1f} {y:.1f}" for i,(x,y) in enumerate(pts))
    return pts, path

HEAD = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:720px;overflow:hidden;background:{INK}}}
body{{font-family:"Liberation Sans","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;position:relative}}
.abs{{position:absolute}}
</style></head><body>"""

def thumb_a():
    # keep the whole line in the right half, clear of the headline and the red tag
    pts, path = nvda_line(760, 1215, 90, 470)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>' for x,y in pts[:-1])
    ex, ey = pts[-1]
    grid = "".join(f'<line x1="740" x2="1240" y1="{y}" y2="{y}" stroke="{PAPER}" stroke-opacity=".06" stroke-width="2"/>' for y in (150,310,470))
    return HEAD + f"""
<svg class="abs" width="1280" height="720" style="left:0;top:0">
  <defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{INK}"/><stop offset=".55" stop-color="{INK}" stop-opacity="0"/></linearGradient></defs>
  {grid}
  <path d="{path}" fill="none" stroke="{RED}" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/>
  {dots}
  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="22" fill="{RED}" stroke="{PAPER}" stroke-width="6"/>
  
</svg>
<div class="abs" style="left:64px;top:70px;color:{PAPER};font-size:50px;font-weight:800;letter-spacing:.01em;line-height:1.1">$500 A MONTH<br>INTO NVIDIA</div>
<div class="abs" style="left:52px;top:218px;color:{PAPER};font-size:250px;font-weight:900;letter-spacing:-.05em;line-height:1">$1.7M</div>
<div class="abs" style="left:64px;top:500px;background:{RED};color:{PAPER};font-size:62px;font-weight:900;letter-spacing:.01em;padding:10px 26px 14px">BUT THERE'S A CATCH</div>
<div class="abs" style="left:66px;top:630px;color:{MUTED};font-size:28px;font-weight:700;letter-spacing:.18em">10 YEARS · REAL PRICES</div>
</body></html>"""

def thumb_b():
    maxw = 820
    rows = [("DRIP-FEED (DCA)", 191, PAPER, INK), ("ALL AT ONCE", 398, RED, PAPER)]
    bars = ""
    for i,(lbl,v,fill,txt) in enumerate(rows):
        top = 330 + i*170; w = maxw*v/398
        bars += (f'<div class="abs" style="left:64px;top:{top}px;color:{MUTED};font-size:34px;font-weight:800;letter-spacing:.14em">{lbl}</div>'
                 f'<div class="abs" style="left:64px;top:{top+46}px;width:{w:.0f}px;height:92px;background:{fill}"></div>'
                 f'<div class="abs" style="left:{64+w+24:.0f}px;top:{top+48}px;color:{fill};font-size:84px;font-weight:900;letter-spacing:-.03em">${v}K</div>')
    return HEAD + f"""
<div class="abs" style="left:64px;top:62px;color:{PAPER};font-size:44px;font-weight:800;letter-spacing:.02em">SAME $60,000 IN QQQ</div>
<div class="abs" style="left:58px;top:118px;color:{PAPER};font-size:160px;font-weight:900;letter-spacing:-.045em;line-height:1">DCA LOST?</div>
{bars}
</body></html>"""

open("thumb_A.html","w").write(thumb_a())
open("thumb_B.html","w").write(thumb_b())
print("written thumb_A.html, thumb_B.html")
