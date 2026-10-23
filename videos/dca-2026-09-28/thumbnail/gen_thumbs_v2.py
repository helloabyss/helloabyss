"""Colourful thumbnails (v2) for the DCA video, at the user's direction.
1280x720. Figures trace to research/2026-09-28-dca.md. Tickers as text, no company logos."""
import math
NVDA = [2.67, 4.84, 3.34, 5.88, 13.05, 29.41, 14.61, 49.52, 134.29, 186.27, 225.07]
GREEN, BLUE, GOLD1, GOLD2, HOT, YEL = "#23E57F", "#34A7FF", "#FFE56B", "#FF9F1C", "#FF2E63", "#FFD60A"

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Anton;src:url(fonts/anton-latin-400-normal.woff2)}
@font-face{font-family:Inter;font-weight:800;src:url(fonts/inter-latin-800-normal.woff2)}
@font-face{font-family:Inter;font-weight:900;src:url(fonts/inter-latin-900-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;overflow:hidden}
body{position:relative;font-family:Inter,sans-serif}
.abs{position:absolute}
.anton{font-family:Anton,Impact,sans-serif;font-weight:400;line-height:1}
.gold{background:linear-gradient(180deg,%s 0%%,%s 100%%);-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 6px 0 #5a2a00) drop-shadow(0 14px 22px rgba(0,0,0,.65))}
.pill{display:inline-block;border-radius:22px;padding:4px 30px 10px;color:#fff;letter-spacing:.02em;
  box-shadow:0 10px 30px rgba(0,0,0,.45), inset 0 -8px 0 rgba(0,0,0,.18)}
.sticker{color:#fff;font-weight:900;letter-spacing:.01em;box-shadow:0 12px 30px rgba(0,0,0,.5)}
</style></head><body>""" % (GOLD1, GOLD2)

def nvda_path(x0,x1,y0,y1):
    lo,hi=math.log(2.2),math.log(260); n=len(NVDA)-1
    pts=[(x0+(x1-x0)*i/n, y1-(y1-y0)*(math.log(p)-lo)/(hi-lo)) for i,p in enumerate(NVDA)]
    d=" ".join(f"{'M' if i==0 else 'L'} {x:.1f} {y:.1f}" for i,(x,y) in enumerate(pts))
    return pts,d

def arrow(x,y,s,color,rot):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-60 18 L20 18 L20 44 L78 0 L20 -44 L20 -18 L-60 -18 Z" fill="{color}" stroke="#0b1030" stroke-width="6" stroke-linejoin="round"/></g>')

def thumb_a():
    pts,d = nvda_path(700,1215,120,520)
    area = d + f" L {pts[-1][0]:.1f} 640 L {pts[0][0]:.1f} 640 Z"
    ex,ey = pts[-1]
    return HEAD + f"""
<div class="abs" style="inset:0;background:radial-gradient(1100px 700px at 78% 30%,#3b1d8f 0%,#1a0f4d 45%,#070a1f 100%)"></div>
<svg class="abs" width="1280" height="720" style="left:0;top:0">
 <defs>
  <linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".55"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 </defs>
 {''.join(f'<line x1="660" x2="1280" y1="{y}" y2="{y}" stroke="#fff" stroke-opacity=".07" stroke-width="2"/>' for y in (160,300,440,580))}
 <path d="{area}" fill="url(#ar)"/>
 <path d="{d}" fill="none" stroke="{GREEN}" stroke-width="13" stroke-linejoin="round" stroke-linecap="round" filter="url(#glow)"/>
 {''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#fff"/>' for x,y in pts[:-1])}
 {arrow(ex-6, ey-18, 1.05, GREEN, -52)}
</svg>
<div class="abs sticker" style="left:52px;top:40px;background:{YEL};color:#111;font-size:40px;padding:8px 22px 10px;border-radius:12px;transform:rotate(-2deg)">$500/MONTH · 10 YEARS</div>
<div class="abs" style="left:52px;top:150px;display:flex;align-items:center;gap:26px">
  <span class="pill anton" style="background:linear-gradient(180deg,#39f08f,#0fae5a);font-size:96px">NVDA</span>
  <span class="anton gold" style="font-size:190px">$1.7M</span>
</div>
<div class="abs" style="left:52px;top:390px;display:flex;align-items:center;gap:26px">
  <span class="pill anton" style="background:linear-gradient(180deg,#5cbcff,#1473e6);font-size:96px">QQQ</span>
  <span class="anton gold" style="font-size:150px">$191K</span>
</div>
<div class="abs" style="left:58px;top:600px;color:#cfd3ff;font-size:30px;font-weight:800;letter-spacing:.06em">FROM $60K INVESTED EACH</div>
<div class="abs sticker" style="right:40px;bottom:46px;background:{HOT};font-size:58px;padding:8px 26px 12px;border-radius:14px;transform:rotate(-6deg);border:5px solid #fff">THE CATCH?</div>
</body></html>"""

def thumb_b():
    return HEAD + f"""
<div class="abs" style="inset:0;background:linear-gradient(180deg,#0a2a18,#04140c)"></div>
<div class="abs" style="inset:0;background:linear-gradient(180deg,#0b1e46,#050b1f);clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)"></div>
<div class="abs" style="inset:0;background:radial-gradient(520px 420px at 24% 48%,rgba(35,229,127,.40),transparent 70%),radial-gradient(520px 420px at 77% 48%,rgba(52,167,255,.42),transparent 70%)"></div>
<svg class="abs" width="1280" height="720" style="left:0;top:0"><line x1="742" y1="0" x2="538" y2="720" stroke="#fff" stroke-width="10"/></svg>
<div class="abs" style="left:0;top:34px;width:1280px;text-align:center">
  <span class="sticker" style="background:{YEL};color:#111;font-size:42px;padding:8px 26px 10px;border-radius:12px;display:inline-block">$500 A MONTH · 10 YEARS</span></div>
<div class="abs anton" style="left:70px;top:150px;font-size:210px;color:#fff;text-shadow:0 0 34px {GREEN},0 8px 0 #0a5a2e">NVDA</div>
<div class="abs anton gold" style="left:78px;top:420px;font-size:150px">$1.7M</div>
<div class="abs anton" style="right:90px;top:150px;font-size:210px;color:#fff;text-shadow:0 0 34px {BLUE},0 8px 0 #0b3f86">QQQ</div>
<div class="abs anton gold" style="right:92px;top:420px;font-size:150px">$191K</div>
<div class="abs" style="left:560px;top:278px;width:160px;height:160px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ff6a88,{HOT});border:7px solid #fff;
  display:flex;align-items:center;justify-content:center;box-shadow:0 14px 40px rgba(0,0,0,.6)"><span class="anton" style="font-size:84px;color:#fff">VS</span></div>
<div class="abs" style="left:0;bottom:30px;width:1280px;text-align:center;color:#e8ecff;font-size:32px;font-weight:900;letter-spacing:.08em;text-shadow:0 3px 10px #000">SAME $60,000 · WHICH ONE WON — AND WHAT'S THE CATCH?</div>
</body></html>"""

open("thumb_A2.html","w").write(thumb_a()); open("thumb_B2.html","w").write(thumb_b())
print("written v2")
