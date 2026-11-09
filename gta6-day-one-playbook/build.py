"""Build GUIDE.md -> Day-One-Playbook.pdf (channel palette: near-black, white, one red)."""
import markdown, pathlib, subprocess
src = pathlib.Path(__file__).with_name("GUIDE.md").read_text()
body = markdown.markdown(src, extensions=["tables"])
body = body.replace("[ ]", "☐")
css = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: 'Helvetica Neue', Arial, sans-serif; color:#111; font-size:10.5pt; line-height:1.5; }
h1 { font-size:34pt; letter-spacing:-1px; margin:0; text-transform:uppercase; font-weight:900; }
h1 + h3 { color:#C8102E; margin-top:4px; }
h2 { border-top:4px solid #111; padding-top:8px; margin-top:28px; text-transform:uppercase;
     font-size:15pt; break-after:avoid; }
h2::before { content:''; display:inline-block; width:10px; height:10px; background:#C8102E; margin-right:8px; }
h3 { break-after:avoid; }
table { border-collapse:collapse; width:100%; margin:10px 0; font-size:9.5pt; break-inside:avoid; }
th { background:#111; color:#fff; text-align:left; padding:6px; }
td { border-bottom:1px solid #ccc; padding:6px; vertical-align:top; }
blockquote { border-left:4px solid #C8102E; margin:12px 0; padding:4px 12px; background:#f3f3f3; }
code { background:#eee; padding:1px 4px; }
strong { color:#000; }
hr { border:0; }
"""
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
out = pathlib.Path(__file__).with_name("Day-One-Playbook.html"); out.write_text(html)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{out}');await p.pdf({{path:'{out.with_suffix('.pdf')}',format:'A4',printBackground:true,
displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:7pt;width:100%;text-align:center;color:#777">Unofficial guide. Not affiliated with Rockstar Games or Take-Two Interactive · <span class=pageNumber></span></div>',
margin:{{top:'18mm',bottom:'18mm',left:'16mm',right:'16mm'}}}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print("built", out.with_suffix('.pdf'))
