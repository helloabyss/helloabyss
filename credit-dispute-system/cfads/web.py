"""Local web app (standard library only). Runs on 127.0.0.1; nothing leaves the machine.

Upload a case-file JSON, see the audit, and download each letter. The case file holds
identity data, so the server binds to localhost only and stores nothing on disk.
"""

import html
import io
import json
import re
import zipfile
from email.parser import BytesParser
from email.policy import default
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .audit import run_audit
from .letters import plan_letters, render
from .models import CaseFile
from .report import audit_text

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Credit Dispute Audit</title>
<style>
:root{{--bg:#fafaf9;--fg:#1c1917;--muted:#57534e;--line:#d6d3d1;--accent:#1d4ed8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1c1917;--fg:#f5f5f4;--muted:#a8a29e;--line:#44403c;--accent:#93c5fd}}}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif;margin:0;padding:24px 16px;max-width:960px;margin-inline:auto}}
h1{{font-size:1.4rem}} pre{{white-space:pre-wrap;border:1px solid var(--line);padding:12px;border-radius:6px;font-size:13px}}
.note{{color:var(--muted)}} button{{background:var(--accent);color:var(--bg);border:0;padding:8px 14px;border-radius:6px;font-weight:600;cursor:pointer}}
a{{color:var(--accent)}} .err{{color:#dc2626}}
</style></head><body>
<h1>Credit file audit &amp; dispute letters</h1>
<p class="note">Educational tool, not legal advice. Runs on your computer only. Build the case file
(reports, ID, proof of address, other evidence, your statements) as described in the README.</p>
<form method="post" action="/audit" enctype="multipart/form-data">
<input type="file" name="case" accept=".json" required> <label><input type="checkbox" name="direct"> include direct furnisher disputes</label>
<button>Run audit</button></form>
{body}
</body></html>"""


def _parse_form(handler):
    length = int(handler.headers.get("Content-Length", 0))
    raw = handler.rfile.read(length)
    msg = BytesParser(policy=default).parsebytes(
        b"Content-Type: " + handler.headers["Content-Type"].encode() + b"\r\n\r\n" + raw)
    out = {}
    for part in msg.iter_parts():
        out[part.get_param("name", header="content-disposition")] = part.get_payload(decode=True)
    return out


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype="text/html; charset=utf-8", extra=None):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(PAGE.format(body=""))

    def do_POST(self):
        try:
            form = _parse_form(self)
            case = CaseFile.from_dict(json.loads(form["case"]))
            direct = "direct" in form
            findings = run_audit(case)
            if self.path == "/letters.zip":
                letters, _ = plan_letters(case, findings, direct)
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w") as z:
                    for n, L in enumerate(letters, 1):
                        name = re.sub(r"[^a-z0-9]+", "-", f"{n:02d}-{L.letter_type}-{L.target}".lower())
                        z.writestr(name.strip("-") + ".txt", render(case, L))
                return self._send(buf.getvalue(), "application/zip",
                                  {"Content-Disposition": 'attachment; filename="dispute-letters.zip"'})
            raw = html.escape(form["case"].decode())
            body = (f"<pre>{html.escape(audit_text(case, findings, direct))}</pre>"
                    f'<form method="post" action="/letters.zip" enctype="multipart/form-data">'
                    f'<textarea name="case" hidden>{raw}</textarea>'
                    + ('<input type="hidden" name="direct" value="1">' if direct else "")
                    + "<button>Download letters (.zip)</button></form>")
        except Exception as e:  # show validation errors to the user
            body = f'<p class="err">Could not process the case file: {html.escape(str(e))}</p>'
        self._send(PAGE.format(body=body))


def serve(port=8765):
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Open http://127.0.0.1:{port}  (Ctrl+C to stop)")
    srv.serve_forever()
