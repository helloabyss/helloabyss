"""Shared design system for the Playbook guide series.

Every page is a fixed A4 artboard (<section class="page">) laid out by hand, so the PDF reads
like a designed magazine, not converted text. Theme: Vice City at dusk. All artwork is original
CSS/SVG. No Rockstar logos, wordmark, fonts or key art.

  render(pages_html, out_pdf, theme="night"|"day")
"""
import pathlib, subprocess

FONTS = ("https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;800"
         "&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=block")

PALM = """<svg viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax meet"><g fill="currentColor">
<path d="M98 400 C 96 300, 104 220, 118 130 L 124 131 C 112 220, 106 300, 110 400 Z"/>
<path d="M120 130 C 80 100, 40 105, 5 140 C 45 115, 85 118, 120 136 Z"/>
<path d="M120 130 C 90 80, 50 60, 15 70 C 60 72, 95 100, 118 136 Z"/>
<path d="M120 130 C 125 80, 150 50, 190 45 C 160 65, 135 95, 124 136 Z"/>
<path d="M120 130 C 160 105, 190 115, 200 160 C 175 128, 150 125, 122 137 Z"/>
<path d="M120 130 C 110 90, 115 55, 130 25 C 125 60, 126 95, 124 134 Z"/>
<path d="M120 130 C 150 140, 165 170, 160 210 C 150 175, 138 155, 120 138 Z"/>
<path d="M120 130 C 90 145, 70 175, 72 215 C 85 180, 100 158, 121 139 Z"/></g></svg>"""

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
:root { --pink:#ff2d8a; --orange:#ff8a3d; --gold:#ffc94d; --teal:#13d6c3; --violet:#7a2bd1;
        --night:#140a2b; --night2:#1f1040; --night3:#2b1757; --cream:#fff7ec; --sand:#ffe9d2; --ink:#1b1238; }
body { font-family: Inter, sans-serif; }

/* ---------- artboard ---------- */
.page { width:210mm; height:297mm; position:relative; overflow:hidden; page-break-after:always; break-after:page; }
.page:last-child { page-break-after:auto; }
.inner { position:absolute; left:16mm; right:16mm; top:20mm; bottom:20mm; }
.run { position:absolute; left:16mm; right:16mm; top:9mm; display:flex; justify-content:space-between;
       font-size:7pt; font-weight:800; letter-spacing:.22em; text-transform:uppercase; }
.foot { position:absolute; left:16mm; right:16mm; bottom:8mm; display:flex; justify-content:space-between;
        font-size:6.8pt; letter-spacing:.04em; }
.foot b { font-family:Anton, sans-serif; font-weight:400; font-size:11pt; letter-spacing:0; }

/* ---------- night theme (Day One) ---------- */
.night .page { background: var(--night); color:#efe8fb; font-size:9.6pt; line-height:1.5; }
.night .run { color: var(--teal); } .night .run span:last-child { color:#8c79b8; }
.night .foot { color:#8c79b8; } .night .foot b { color: var(--pink); }
.night strong, .night b { color:#fff; }

/* ---------- day theme (First-Timers) — large print, high contrast ---------- */
.day body, .day .page { font-family: 'Atkinson Hyperlegible', Inter, sans-serif; }
.day .page { background: var(--cream); color: var(--ink); font-size:13pt; line-height:1.5; }
.day .run { color: var(--pink); font-family: Inter, sans-serif; } .day .run span:last-child { color:#6b5f8a; }
.day .foot { color:#6b5f8a; font-family: Inter, sans-serif; } .day .foot b { color: var(--pink); }
.day .page::before { content:''; position:absolute; left:0; right:0; top:0; height:4mm;
        background: linear-gradient(90deg, var(--violet), var(--pink), var(--orange), var(--gold)); }

/* ---------- type ---------- */
.display { font-family: Anton, Impact, sans-serif; font-weight:400; text-transform:uppercase; line-height:.95; margin:0; letter-spacing:.005em; }
.grad { color: var(--gold); }   /* solid: background-clip:text leaves box artefacts in Chromium PDFs */
.day .grad { color: var(--pink); }
.kicker { font-family: Inter, sans-serif; font-weight:800; font-size:8pt; letter-spacing:.3em; text-transform:uppercase; color: var(--teal); }
.day .kicker { color: var(--pink); font-size:9.5pt; }
.lede { font-size:12pt; line-height:1.45; }
.day .lede { font-size:15pt; }
.mute { color:#a898cc; } .day .mute { color:#5d5280; }
p { margin: 0 0 3mm; }
h3 { font-family: Inter, sans-serif; font-weight:800; font-size:10pt; letter-spacing:.12em; text-transform:uppercase; margin:0 0 2.5mm; color: var(--teal); }
.day h3 { font-size:13pt; letter-spacing:.06em; color: var(--pink); }

/* part opener band */
.part { display:flex; align-items:flex-end; gap:5mm; margin-bottom:7mm; }
.part .num { font-family:Anton, sans-serif; font-size:84pt; line-height:.8; color:transparent;
             -webkit-text-stroke: 1.6px var(--pink); }
.day .part .num { -webkit-text-stroke: 2px var(--pink); }
.part .ttl .display { font-size:34pt; }
.part .ttl .kicker { display:block; margin-bottom:2mm; }

/* ---------- components ---------- */
.grid { display:grid; gap:4mm; } .g2 { grid-template-columns:1fr 1fr; } .g3 { grid-template-columns:1fr 1fr 1fr; }
.g4 { grid-template-columns:repeat(4,1fr); }
.card { border-radius:4mm; padding:5mm; background: var(--night2); border:1px solid #3a2470; position:relative; }
.day .card { background:#fff; border:1.5px solid #eadcf2; box-shadow: 0 1.5mm 0 #f1e3d3; }
.card.hot { background: linear-gradient(150deg, #3b1260, #6a1550 60%, #8a2a3a); border-color:#ff2d8a66; }
.day .card.hot { background: linear-gradient(150deg, #ffe3ef, #ffeedd); border-color:#ffb7d3; }
.card h4 { margin:0 0 2mm; font-family:Anton, sans-serif; font-weight:400; font-size:16pt; text-transform:uppercase; letter-spacing:.01em; }
.day .card h4 { font-size:18pt; }
.stat .big { font-family:Anton, sans-serif; font-size:40pt; line-height:1; }
.stat .lbl { font-size:8pt; font-weight:800; letter-spacing:.14em; text-transform:uppercase; margin-top:1.5mm; color:#c9b9ea; }

.pill { display:inline-block; font-family:Inter, sans-serif; font-size:6.8pt; font-weight:800; letter-spacing:.1em;
        padding:.7mm 2.3mm; border-radius:10mm; color:#120826; white-space:nowrap; vertical-align:middle; }
.ok { background: var(--teal); } .rep { background: var(--gold); } .rum { background: var(--pink); color:#fff; }

table.t { width:100%; border-collapse:separate; border-spacing:0; font-size:9pt; }
table.t th { text-align:left; font-size:7pt; letter-spacing:.14em; text-transform:uppercase; font-weight:800;
             color: var(--teal); padding:0 3mm 2mm; border-bottom:2px solid var(--pink); }
table.t td { padding:2.3mm 3mm; border-bottom:1px solid #33205c; vertical-align:top; }
table.t tr:nth-child(even) td { background:#1a0d36; }
table.t td:first-child { font-weight:700; color:#fff; width:30%; }
.day table.t { font-size:12pt; } .day table.t th { color: var(--pink); font-size:9pt; border-bottom-color: var(--ink); }
.day table.t td { border-bottom:1px solid #e9dccd; } .day table.t tr:nth-child(even) td { background:#fff; }
.day table.t td:first-child { color: var(--ink); }

.steps { counter-reset:s; display:grid; gap:3.2mm; }
.step { counter-increment:s; display:grid; grid-template-columns:11mm 1fr; gap:4mm; align-items:start; }
.step::before { content: counter(s, decimal-leading-zero); font-family:Anton, sans-serif; font-size:20pt; line-height:1;
        color: var(--pink); }
.day .step { grid-template-columns:14mm 1fr; } .day .step::before { font-size:26pt; }
.step b { display:block; font-size:10.5pt; margin-bottom:.5mm; } .day .step b { font-size:14pt; }

.check { list-style:none; margin:0; padding:0; } .check li { padding:2mm 0 2mm 9mm; position:relative; border-bottom:1px dashed #3a2470; }
.check li::before { content:''; position:absolute; left:0; top:2.3mm; width:5mm; height:5mm; border:2px solid var(--teal); border-radius:1.2mm; }
.day .check li { border-bottom-color:#e2d3c2; padding-left:11mm; } .day .check li::before { width:6.5mm; height:6.5mm; border-color: var(--pink); top:2mm; }

.callout { border-radius:4mm; padding:4.5mm 5mm 4.5mm 15mm; position:relative; background: var(--night3); }
.callout::before { content: attr(data-icon); position:absolute; left:4.5mm; top:4mm; font-family:Anton, sans-serif; font-size:18pt; line-height:1; color: var(--gold); }
.callout.warn { background: linear-gradient(120deg, #4a0f35, #3a1050); } .callout.warn::before { color: var(--pink); }
.day .callout { background: #efe6ff; } .day .callout::before { color: var(--violet); font-size:22pt; }
.day .callout.warn { background: #ffe4ee; } .day .callout.warn::before { color: var(--pink); }

.chip { display:inline-block; font-family: 'JetBrains Mono', monospace; font-size:8.5pt; padding:1.3mm 3mm; margin:0 1.5mm 2mm 0;
        border-radius:2mm; background:#2c1756; color: var(--gold); border:1px solid #4a2d80; }

.rule { height:2px; background: linear-gradient(90deg, var(--pink), var(--orange), transparent); margin:5mm 0; border:0; }

/* timeline */
.tl { position:relative; padding-left:30mm; }
.tl::before { content:''; position:absolute; left:23mm; top:2mm; bottom:2mm; width:2px; background: linear-gradient(var(--teal), var(--pink), var(--orange)); }
.tl .ev { position:relative; margin-bottom:5mm; }
.tl .ev .d { position:absolute; left:-30mm; width:20mm; text-align:right; font-family:Anton, sans-serif; font-size:14pt; line-height:1.05; text-transform:uppercase; }
.tl .ev .d small { display:block; font-family:Inter, sans-serif; font-size:6.8pt; letter-spacing:.18em; color: var(--teal); font-weight:800; }
.tl .ev::before { content:''; position:absolute; left:-8.6mm; top:1.6mm; width:4mm; height:4mm; border-radius:50%; background: var(--night); border:2px solid var(--pink); }
.tl .ev.key::before { background: var(--pink); box-shadow: 0 0 0 2mm #ff2d8a33; }
.tl .ev .body { background: var(--night2); border-radius:3mm; padding:3mm 4mm; border:1px solid #3a2470; }
.tl .ev.key .body { border-color: var(--pink); }

/* bar chart */
.bars .row { display:grid; grid-template-columns:36mm 1fr 18mm; gap:3mm; align-items:center; margin-bottom:2.6mm; font-size:8.6pt; }
.bars .track { height:7mm; background:#24134a; border-radius:1.5mm; position:relative; overflow:hidden; }
.bars .fill { position:absolute; left:0; top:0; bottom:0; border-radius:1.5mm; background:#3d2775; }
.bars .game { position:absolute; left:0; top:0; bottom:0; background: repeating-linear-gradient(135deg, var(--pink) 0 2mm, #d81b72 2mm 4mm); border-radius:1.5mm 0 0 1.5mm; }
.bars .row.risk .fill { background:#5a2140; }
.bars .v { font-family:Anton, sans-serif; font-size:12pt; text-align:right; }
.legend { display:flex; gap:6mm; font-size:7.5pt; color:#a898cc; margin-top:2mm; }
.legend i { display:inline-block; width:4mm; height:3mm; border-radius:.8mm; margin-right:1.5mm; vertical-align:-.3mm; }

/* toc */
.toc .row { display:grid; grid-template-columns:16mm 1fr 10mm; align-items:baseline; padding:3mm 0; border-bottom:1px solid #33205c; }
.toc .n { font-family:Anton, sans-serif; font-size:20pt; color: var(--pink); }
.toc .t { font-family:Anton, sans-serif; font-size:15pt; text-transform:uppercase; }
.toc .t small { display:block; font-family:Inter, sans-serif; font-size:8.5pt; text-transform:none; color:#a898cc; letter-spacing:0; }
.toc .p { font-family:Anton, sans-serif; font-size:13pt; text-align:right; color: var(--teal); }
.day .toc .row { border-bottom-color:#e2d3c2; padding:2.2mm 0; } .day .toc .t { font-size:17pt; } .day .toc .t small { font-family:'Atkinson Hyperlegible'; font-size:11pt; color:#5d5280; }
.day .toc .p { color: var(--violet); }

/* ---------- cover / sunset scene ---------- */
.scene { position:absolute; inset:0; overflow:hidden; }
.scene .sky { position:absolute; inset:0; }
.scene .sun { position:absolute; left:50%; transform:translateX(-50%); border-radius:50%;
       -webkit-mask: linear-gradient(#000 0 46%, transparent 46%), repeating-linear-gradient(180deg, #000 0 6.5mm, transparent 6.5mm 9.5mm);
       mask: linear-gradient(#000 0 46%, transparent 46%), repeating-linear-gradient(180deg, #000 0 6.5mm, transparent 6.5mm 9.5mm); }
.scene .sea { position:absolute; left:0; right:0; bottom:0; }
.scene .glint { position:absolute; left:28%; right:28%; top:0; height:45%;
       background: repeating-linear-gradient(180deg, rgba(255,150,90,.6) 0 1.1mm, transparent 1.1mm 4mm); }
.scene .palm { position:absolute; }
.scene .palm svg { width:100%; height:100%; display:block; }
.grain { position:absolute; inset:0; opacity:.13; mix-blend-mode:overlay;
         background-image: repeating-radial-gradient(circle at 17% 32%, #fff 0 .2px, transparent .6px 2px); }
"""


def scene(sky, sun, sea, horizon=70, sun_size=118, sun_top=40, palm_color="#12051f"):
    """A layered sunset. horizon/sun_top are % of the frame height."""
    return f"""<div class="scene">
  <div class="sky" style="background:{sky}"></div>
  <div class="sun" style="top:{sun_top}%;width:{sun_size}mm;height:{sun_size}mm;background:{sun}"></div>
  <div class="sea" style="top:{horizon}%;background:{sea}"><div class="glint"></div></div>
  <div class="palm" style="left:-14mm;width:72mm;height:155mm;bottom:{100-horizon-8}%;color:{palm_color}">{PALM}</div>
  <div class="palm" style="left:30mm;width:42mm;height:95mm;bottom:{100-horizon-3}%;transform:scaleX(-1);color:{palm_color}">{PALM}</div>
  <div class="palm" style="right:-16mm;width:84mm;height:178mm;bottom:{100-horizon-10}%;transform:scaleX(-1);color:{palm_color}">{PALM}</div>
  <div class="grain"></div>
</div>"""


def page(body, run_left="", run_right="", num=None, foot_note="Unofficial. Not affiliated with Rockstar Games or Take-Two Interactive.", style=""):
    foot = f'<div class="foot"><span>{foot_note}</span><b>{num:02d}</b></div>' if num else ""
    run = f'<div class="run"><span>{run_left}</span><span>{run_right}</span></div>' if run_left or run_right else ""
    return f'<section class="page" style="{style}">{run}<div class="inner">{body}</div>{foot}</section>'


def part(n, kicker, title):
    return (f'<div class="part"><div class="num">{n:02d}</div><div class="ttl"><span class="kicker">{kicker}</span>'
            f'<h2 class="display grad">{title}</h2></div></div>')


def render(pages, out_pdf, theme):
    out_pdf = pathlib.Path(out_pdf)
    html = (f"<!doctype html><html class='{theme}'><head><meta charset='utf-8'>"
            f"<link rel='stylesheet' href='{FONTS}'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>")
    src = out_pdf.with_suffix(".html")
    src.write_text(html)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{src}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);
const over=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((s,i)=>{{const r=s.getBoundingClientRect();
 const bad=[...s.querySelectorAll('.inner *')].some(e=>{{const q=e.getBoundingClientRect();return q.height&&q.bottom>r.bottom-(18*3.78);}});return bad?i+1:0;}}).filter(Boolean));
if(over.length)console.log('WARNING overflow on pages',over.join(','));
await p.pdf({{path:'{out_pdf}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)
    print("built", out_pdf)
