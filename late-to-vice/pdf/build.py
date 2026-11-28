"""Build matching Late to Vice PDFs for every deliverable.

Usage (from repo root):  python3 late-to-vice/pdf/build.py
Writes HTML staging files to late-to-vice/pdf/_stage/ and PDFs to late-to-vice/pdf/.
Needs: python `markdown`, ffmpeg, node + playwright (see print.js).
"""
import json, re, subprocess, pathlib, markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent  # late-to-vice/
OUT = ROOT / "pdf"
STAGE = OUT / "_stage"
STAGE.mkdir(parents=True, exist_ok=True)

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,600;0,800;1,800;1,900&family=JetBrains+Mono:wght@500&display=swap">'

# Print overrides injected into the two web guides.
GUIDE_PRINT_CSS = """
<style>
@page { size: A4; margin: 0; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
nav.chap, body::before { display: none !important; }
.hero { padding-block: 28px 12px; }
section.guide { padding-block: 18px 4px; }
.card, tr, ol.flow li, .callout, .sec-head { break-inside: avoid; }
.table-wrap { overflow: visible; }
.subhead { break-after: avoid; }
.grid { grid-template-columns: repeat(2, 1fr) !important; }
footer { margin-top: 18px; padding-block: 18px; }
a { text-decoration: none; }
</style>
"""

# Shared brand sheet for documents built from Markdown.
DOC_CSS = """
<style>
@page { size: A4; margin: 0; }
:root { --night:#150a2e; --panel:#21123f; --line:#3a2763; --pink:#ff3fbf; --sun:#ffb347; --cyan:#1fd6ff; --text:#f6f1ff; --muted:#b7a9d6; }
* { box-sizing: border-box; }
html, body { margin:0; background: var(--night); color: var(--text); font-family: "Poppins", system-ui, sans-serif; font-size: 12.5px; line-height: 1.55; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { padding: 34px 44px 40px; }
header.brand { display:flex; align-items:center; gap:22px; padding-bottom:18px; border-bottom:1px solid var(--line); margin-bottom:18px; }
header.brand img.logo { width:120px; }
header.brand img.stk { width:62px; transform: rotate(-6deg); }
.eyebrow { font-family:"JetBrains Mono", monospace; font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--cyan); }
header.brand h1 { margin:.2rem 0 0; font-size:30px; font-weight:900; font-style:italic; line-height:1.05;
  background: linear-gradient(180deg, var(--sun), var(--pink)); -webkit-background-clip:text; background-clip:text; color:transparent; }
h1, h2, h3 { line-height:1.2; }
.md h1 { display:none; }
.md h2 { font-size:19px; font-weight:800; font-style:italic; color:var(--sun); margin:22px 0 8px; break-after: avoid; }
.md h3 { font-size:14px; color:var(--cyan); margin:16px 0 6px; break-after: avoid; }
.md p, .md li { color: var(--text); }
.md blockquote { margin: 10px 0; padding: 10px 14px; border-left:3px solid var(--pink); background:#2a1040; color:var(--text); border-radius:0 10px 10px 0; }
.md code { font-family:"JetBrains Mono", monospace; color:var(--sun); font-size:11px; }
.md table { width:100%; border-collapse:collapse; margin:8px 0 12px; font-size:11.5px; break-inside: avoid; }
.md th, .md td { text-align:left; padding:6px 9px; border-bottom:1px solid var(--line); vertical-align:top; }
.md th { font-family:"JetBrains Mono", monospace; font-size:9.5px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); background:var(--panel); }
.md ul, .md ol { padding-left: 20px; }
.md input[type=checkbox] { accent-color: var(--pink); }
.frames { display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin: 6px 0 4px; }
.frames figure { margin:0; break-inside: avoid; }
.frames img { width:100%; border-radius:8px; border:1px solid var(--line); display:block; }
.frames figcaption { font-family:"JetBrains Mono", monospace; font-size:9px; color:var(--muted); margin-top:4px; }
.cover-row { display:grid; grid-template-columns: 210px 1fr; gap:22px; align-items:start; margin-bottom:8px; }
.cover-row img { width:100%; border-radius:10px; border:1px solid var(--line); }
.meta { display:grid; gap:6px; }
.meta div { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:8px 12px; }
.meta b { color: var(--sun); font-weight:600; }
footer.doc { margin-top:20px; padding-top:12px; border-top:1px solid var(--line); font-size:10px; color:var(--muted); }
</style>
"""

def head(title):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>{FONTS}{DOC_CSS}</head><body><div class="page">'

def brand(eyebrow, title, assets):
    return (f'<header class="brand"><img class="logo" src="{assets}/gta6-logo-cutout.png" alt="">'
            f'<div><div class="eyebrow">{eyebrow}</div><h1>{title}</h1></div>'
            f'<img class="stk" src="{assets}/sticker-f.png" alt="" style="margin-left:auto"></header>')

FOOT = ('<footer class="doc">Late to Vice · @LateToVice · Unofficial fan material, not affiliated with Rockstar Games or Take-Two. '
        'Facts from launch-week community guides, checked 26 Nov 2026.</footer></div></body></html>')

def md(text):
    return '<div class="md">' + markdown.markdown(text, extensions=["tables", "fenced_code"]) + '</div>'

jobs = []
assets_rel = "../../assets"  # from pdf/_stage/

# 1-2. Web guides: copy with print CSS, rewrite asset paths.
for name, pdf in [("guides.html", "late-to-vice-field-guide-ch1-2.pdf"), ("road-ahead.html", "late-to-vice-road-ahead-ch3-5.pdf")]:
    src = (ROOT / name).read_text()
    src = src.replace('src="assets/', f'src="{assets_rel}/')
    html = '<!doctype html><html><head><meta charset="utf-8"></head><body>' + src + GUIDE_PRINT_CSS + '</body></html>'
    staged = STAGE / name
    staged.write_text(html)
    jobs.append({"html": str(staged), "pdf": str(OUT / pdf)})

# 3. Channel plan.
plan = (ROOT / "PLAN.md").read_text()
plan = re.sub(r"^> .*?(?:\n> .*?)*\n\n", "", plan, count=1, flags=re.M)
html = head("Late to Vice Channel Plan") + brand("Channel plan · weekly routine", "Late to Vice playbook", assets_rel) + md(plan) + FOOT
(STAGE / "plan.html").write_text(html)
jobs.append({"html": str(STAGE / "plan.html"), "pdf": str(OUT / "late-to-vice-channel-plan.pdf")})

# 4-6. One storyboard per TikTok: cover, scene frames, script.
videos = [
    ("tiktok-ch1-explainer", "late-to-vice-ch1.mp4", "TikTok 1 · storyboard", "Broke in Chapter 1?", "late-to-vice-tiktok-1-chapter-1.pdf"),
    ("tiktok-tips-explainer", "late-to-vice-tips.mp4", "TikTok 2 · storyboard", "Stuff GTA 6 never tells you", "late-to-vice-tiktok-2-tips.pdf"),
    ("tiktok-ch3-money", "late-to-vice-ch3-money.mp4", "TikTok 3 · storyboard", "Chapter 3 money math", "late-to-vice-tiktok-3-chapter-3-money.pdf"),
]
for folder, mp4, eyebrow, title, pdf in videos:
    d = ROOT / folder
    vhtml = (d / "video.html").read_text()
    scenes = [(float(a), float(b)) for a, b in re.findall(r'data-in="([\d.]+)" data-out="([\d.]+)"', vhtml)]
    frames_dir = STAGE / folder
    frames_dir.mkdir(exist_ok=True)
    figs = []
    for i, (a, b) in enumerate(scenes):
        t = max(a, b - 0.45)
        jpg = frames_dir / f"scene{i}.jpg"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(d / mp4),
                        "-frames:v", "1", "-vf", "scale=360:-1", "-q:v", "3", str(jpg)], check=True)
        figs.append(f'<figure><img src="{folder}/scene{i}.jpg" alt=""><figcaption>Scene {i+1} · {a:.1f}–{b:.1f}s</figcaption></figure>')
    dur = scenes[-1][1]
    script = (d / "SCRIPT.md").read_text()
    script = re.sub(r"^# .*\n", "", script, count=1)
    meta = (f'<div class="cover-row"><img src="../../{folder}/cover.jpg" alt="">'
            f'<div class="meta"><div><b>Length</b> · {dur:.1f}s, 1080×1920, 9:16</div>'
            f'<div><b>File</b> · <code>{folder}/{mp4}</code></div>'
            f'<div><b>Voice</b> · ElevenLabs "Liam – Energetic, Social Media Creator"</div>'
            f'<div><b>Cover</b> · frame at 3.0s (<code>cover.jpg</code>)</div></div></div>')
    html = (head(title) + brand(eyebrow, title, assets_rel) + meta +
            '<h2 style="font-size:19px;font-style:italic;color:#ffb347;margin:18px 0 8px">Scenes</h2>'
            f'<div class="frames">{"".join(figs)}</div>' + md(script) + FOOT)
    (STAGE / f"{folder}.html").write_text(html)
    jobs.append({"html": str(STAGE / f"{folder}.html"), "pdf": str(OUT / pdf)})

(STAGE / "jobs.json").write_text(json.dumps(jobs, indent=1))
subprocess.run(["node", str(OUT / "print.js"), str(STAGE / "jobs.json")], check=True)
