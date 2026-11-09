"""Build GUIDE.md -> Day-One-Playbook.pdf

Theme: Vice City at dusk. Sunset sky, striped sun, palm silhouettes, neon pink and teal on
deep night purple. All artwork is original CSS/SVG. No Rockstar logos, wordmark or key art.
"""
import markdown, pathlib, re, subprocess
from pypdf import PdfWriter

HERE = pathlib.Path(__file__).parent
src = (HERE / "GUIDE.md").read_text()

# Drop the markdown title block; the cover replaces it.
src = src.split("---", 1)[1]
body = markdown.markdown(src, extensions=["tables"])
body = body.replace("[ ]", '<span class="box"></span>')
for word, cls in (("CONFIRMED", "ok"), ("REPORTED", "rep"), ("RUMOUR", "rum")):
    body = re.sub(rf"(?<![\w-])(\*\*)?{word}\b", f'<span class="pill {cls}">{word}</span>', body)
# "Part N — Title" headings get a kicker line
body = re.sub(r"<h2>Part (\d+) — (.*?)</h2>",
              r'<h2><span class="kicker">PART \1</span>\2</h2>', body)

PALM = """<svg viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg"><g fill="#12051f">
<path d="M98 400 C 96 300, 104 220, 118 130 L 124 131 C 112 220, 106 300, 110 400 Z"/>
<path d="M120 130 C 80 100, 40 105, 5 140 C 45 115, 85 118, 120 136 Z"/>
<path d="M120 130 C 90 80, 50 60, 15 70 C 60 72, 95 100, 118 136 Z"/>
<path d="M120 130 C 125 80, 150 50, 190 45 C 160 65, 135 95, 124 136 Z"/>
<path d="M120 130 C 160 105, 190 115, 200 160 C 175 128, 150 125, 122 137 Z"/>
<path d="M120 130 C 110 90, 115 55, 130 25 C 125 60, 126 95, 124 134 Z"/>
<path d="M120 130 C 150 140, 165 170, 160 210 C 150 175, 138 155, 120 138 Z"/>
<path d="M120 130 C 90 145, 70 175, 72 215 C 85 180, 100 158, 121 139 Z"/></g></svg>"""

cover = f"""
<section class="cover">
  <div class="sky"></div>
  <div class="sun"></div>
  <div class="sea"></div>
  <div class="palm p1">{PALM}</div>
  <div class="palm p2">{PALM}</div>
  <div class="palm p3">{PALM}</div>
  <div class="cover-text">
    <div class="edition">EDITION 1.0 · PRE-LAUNCH · FACTS CHECKED 9 NOV 2026</div>
    <h1>THE<br>DAY ONE<br>PLAYBOOK</h1>
    <div class="sub">An unofficial launch guide for <b>Grand Theft Auto VI</b> players</div>
    <div class="tags"><span>Every claim labelled</span><span>Storage plan</span><span>Spoiler lockdown</span><span>Free updates</span></div>
  </div>
  <div class="cover-foot">Unofficial. Not made, endorsed or sponsored by Rockstar Games or Take-Two Interactive.</div>
</section>
"""

css = """
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;800&display=block');
@page { size: A4; margin: 16mm 15mm 18mm; }
:root { --night:#140a2b; --night2:#1f1040; --pink:#ff2d8a; --orange:#ff8a3d; --gold:#ffd166;
        --teal:#1ee3cf; --ink:#f4eefc; --mute:#b9a9d9; }
html { background: var(--night); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin:0; font-family: Inter, sans-serif; color: var(--ink); font-size:10.2pt; line-height:1.55; }

/* ---------- COVER ---------- */
.cover { position:relative; width:210mm; height:297mm; overflow:hidden; }
.sky { position:absolute; inset:0; background: linear-gradient(180deg,
        #0c0420 0%, #2a0f55 22%, #7a1e8c 40%, #ff2d8a 56%, #ff8a3d 66%, #ffd166 72%); }
.sun { position:absolute; left:50%; top:39%; width:120mm; height:120mm; transform:translateX(-50%);
       border-radius:50%; background: linear-gradient(180deg, #ffe08a 0%, #ff9d3d 45%, #ff2d8a 100%);
       -webkit-mask: repeating-linear-gradient(180deg, #000 0 9mm, transparent 9mm 11mm);
       mask: linear-gradient(#000 0 45%, transparent 45%),
             repeating-linear-gradient(180deg, #000 0 7mm, transparent 7mm 10mm); }
.sea { position:absolute; left:0; right:0; top:72%; bottom:0;
       background: repeating-linear-gradient(180deg, #170734 0 3mm, #241050 3mm 4mm),
                   #170734; }
.sea::before { content:''; position:absolute; left:30%; right:30%; top:0; height:40%;
       background: repeating-linear-gradient(180deg, rgba(255,140,80,.55) 0 1.2mm, transparent 1.2mm 4mm);
       filter: blur(.4px); }
.palm { position:absolute; bottom:24%; }
.palm svg { width:100%; height:100%; display:block; }
.p1 { left:-12mm; width:70mm; height:150mm; bottom:20%; }
.p2 { left:32mm; width:42mm; height:95mm; bottom:27%; transform:scaleX(-1); }
.p3 { right:-14mm; width:80mm; height:170mm; bottom:18%; transform:scaleX(-1); }
.cover-text { position:absolute; left:18mm; right:18mm; top:20mm; }
.edition { font-weight:800; letter-spacing:.25em; font-size:8pt; color: var(--teal); }
.cover h1 { font-family: Anton, Impact, sans-serif; font-weight:400; font-size:68pt; line-height:.92;
            margin:6mm 0 5mm; color:#fff; letter-spacing:.01em;
            text-shadow: 0 0 18px rgba(255,45,138,.75), 3px 3px 0 var(--pink); }
.sub { font-size:14pt; color:#fff; max-width:120mm; }
.tags { margin-top:6mm; display:flex; flex-wrap:wrap; gap:2.5mm; }
.tags span { border:1.5px solid var(--teal); color: var(--teal); border-radius:20px; padding:1mm 3.5mm;
             font-size:8.5pt; font-weight:800; text-transform:uppercase; letter-spacing:.06em;
             background: rgba(12,4,32,.55); }
.cover-foot { position:absolute; left:0; right:0; bottom:10mm; text-align:center; font-size:7.5pt; color: var(--mute); }

/* ---------- INTERIOR ---------- */
h2 { font-family: Anton, Impact, sans-serif; font-weight:400; font-size:26pt; line-height:1.05;
     margin: 0 0 4mm; break-before: page; text-transform:uppercase; letter-spacing:.01em; break-after:avoid;
     background: linear-gradient(90deg, var(--gold), var(--orange) 40%, var(--pink));
     -webkit-background-clip:text; background-clip:text; color:transparent; }
h2 .kicker { display:block; font-family:Inter, sans-serif; font-weight:800; font-size:8.5pt;
     letter-spacing:.3em; color: var(--teal); -webkit-text-fill-color: var(--teal); margin-bottom:1.5mm; }
h2::after { content:''; display:block; height:3px; margin-top:3mm; width:40mm;
     background: linear-gradient(90deg, var(--pink), var(--orange)); }
h3 { color: var(--teal); text-transform:uppercase; letter-spacing:.08em; font-size:10.5pt; break-after:avoid; }
strong, b { color:#fff; }
a { color: var(--teal); }
table { width:100%; border-collapse:separate; border-spacing:0; margin:4mm 0; font-size:9.3pt;
        break-inside:avoid; border-radius:8px; overflow:hidden; border:1px solid #3a2466; }
th { background: linear-gradient(90deg, var(--pink), var(--orange)); color:#fff; text-align:left;
     padding:2.4mm 3mm; font-weight:800; text-transform:uppercase; font-size:8pt; letter-spacing:.06em; }
td { padding:2.2mm 3mm; vertical-align:top; border-top:1px solid #33205c; }
tr:nth-child(even) td { background: var(--night2); }
.pill { display:inline-block; font-size:7pt; font-weight:800; letter-spacing:.08em; padding:.6mm 2.2mm;
        border-radius:20px; color:#120826; vertical-align:middle; }
.pill.ok { background: var(--teal); } .pill.rep { background: var(--gold); } .pill.rum { background: var(--pink); color:#fff; }
blockquote { margin:5mm 0; padding:3mm 5mm; border-left:4px solid var(--teal); background: var(--night2); border-radius:0 8px 8px 0; }
ul, ol { padding-left: 6mm; } li { margin: 1mm 0; }
li::marker { color: var(--pink); font-weight:800; }
code { background:#2c1756; color: var(--gold); padding:.3mm 1.5mm; border-radius:4px; font-size:9pt; }
.box { display:inline-block; width:3.2mm; height:3.2mm; border:1.5px solid var(--teal); border-radius:2px;
       margin-right:2mm; vertical-align:-.4mm; }
li:has(.box) { list-style:none; margin-left:-6mm; }
hr { border:0; height:1px; background: linear-gradient(90deg, transparent, #4a2d80, transparent); margin:8mm 0; }
em { color: var(--mute); }
"""

head = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>"
SCRATCH = HERE / ".build"; SCRATCH.mkdir(exist_ok=True)
(SCRATCH / "cover.html").write_text(head.replace("</style>", "@page{margin:0}</style>") + cover + "</body></html>")
html = head + body + "</body></html>"
out = HERE / "Day-One-Playbook.html"
out.write_text(head + cover + body + "</body></html>")  # browsable single-file version
(SCRATCH / "inner.html").write_text(html)

FOOT = ('<div style="font-size:7pt;width:100%;text-align:center;color:#b9a9d9;font-family:sans-serif">'
        'THE DAY ONE PLAYBOOK · Unofficial. Not affiliated with Rockstar Games or Take-Two Interactive'
        ' · <span class=pageNumber></span></div>')
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();
async function r(src,dst,opts){{const p=await b.newPage();await p.goto('file://'+src,{{waitUntil:'networkidle'}});
await p.evaluate(()=>document.fonts.ready);await p.pdf({{path:dst,format:'A4',printBackground:true,...opts}});await p.close();}}
await r('{SCRATCH/"cover.html"}','{SCRATCH/"cover.pdf"}',{{margin:{{top:0,bottom:0,left:0,right:0}}}});
await r('{SCRATCH/"inner.html"}','{SCRATCH/"inner.pdf"}',{{preferCSSPageSize:true,displayHeaderFooter:true,
headerTemplate:'<span></span>',footerTemplate:{FOOT!r}}});
await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
# Chromium leaves page margins unpainted: lay each interior page over a full-bleed night page.
from pypdf import PdfReader, PageObject, Transformation
w = PdfWriter()
w.append(str(SCRATCH / "cover.pdf"))
for pg in PdfReader(str(SCRATCH / "inner.pdf")).pages:
    bg = PageObject.create_blank_page(width=pg.mediabox.width, height=pg.mediabox.height)
    from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject
    stream = DecodedStreamObject(); stream.set_data(
        f"0.078 0.039 0.169 rg 0 0 {float(pg.mediabox.width)} {float(pg.mediabox.height)} re f".encode())
    bg[NameObject("/Contents")] = w._add_object(stream)
    bg.merge_page(pg)
    w.add_page(bg)
pdf = out.with_suffix(".pdf"); w.write(str(pdf))
print("built", pdf)
