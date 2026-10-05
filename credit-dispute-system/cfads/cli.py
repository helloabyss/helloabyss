import argparse
import json
import os
import re
import sys

from .audit import run_audit
from .ingest import load_case, parse_report_text, pdf_text
from .law import LAWS
from .letters import TITLES, plan_letters, render
from .pipeline import next_actions
from .report import audit_text


def cmd_audit(a):
    case = load_case(a.case)
    findings = run_audit(case)
    if a.json:
        print(json.dumps([f.to_dict() for f in findings], indent=2))
    else:
        print(audit_text(case, findings, a.include_direct))


def cmd_letters(a):
    case = load_case(a.case)
    letters, blocked = plan_letters(case, run_audit(case), a.include_direct)
    os.makedirs(a.out, exist_ok=True)
    for n, L in enumerate(letters, 1):
        name = re.sub(r"[^a-z0-9]+", "-", f"{n:02d}-{L.letter_type}-{L.target}".lower()).strip("-")
        path = os.path.join(a.out, name + ".txt")
        with open(path, "w") as fh:
            fh.write(render(case, L))
        state = "ready" if L.ready else "NOT READY, missing " + ", ".join(L.missing_documents)
        print(f"wrote {path}  ({state})")
    for f, why in blocked:
        print(f"skipped {f.id} {f.title}: {why}", file=sys.stderr)


def cmd_track(a):
    case = load_case(a.case)
    for lbl, msg in next_actions(case) or [("-", "No disputes recorded in the case file yet.")]:
        print(f"{lbl}\n  {msg}")


def cmd_parse_pdf(a):
    print(json.dumps(parse_report_text(pdf_text(a.pdf), a.bureau.lower()), indent=2))


def cmd_laws(a):
    for law in LAWS.values():
        print(f"{law.cite} — {law.short}  [verified: {law.verified}]\n  {law.rule}")
        if law.correction:
            print(f"  NOTE: {law.correction}")
        if law.private_action:
            print(f"  Private action: {law.private_action}")
        print()


def cmd_web(a):
    from .web import serve
    serve(a.port)


def main(argv=None):
    p = argparse.ArgumentParser(prog="cfads", description="Credit file audit & dispute automation")
    sub = p.add_subparsers(required=True)
    s = sub.add_parser("audit", help="Run the audit and print findings")
    s.add_argument("case")
    s.add_argument("--json", action="store_true")
    s.add_argument("--include-direct", action="store_true", help="Also plan direct furnisher disputes now")
    s.set_defaults(fn=cmd_audit)
    s = sub.add_parser("letters", help="Generate dispute letters")
    s.add_argument("case")
    s.add_argument("--out", default="letters")
    s.add_argument("--include-direct", action="store_true")
    s.set_defaults(fn=cmd_letters)
    s = sub.add_parser("track", help="Deadlines and next steps for sent disputes")
    s.add_argument("case")
    s.set_defaults(fn=cmd_track)
    s = sub.add_parser("parse-pdf", help="Draft tradelines from a report PDF (review before use)")
    s.add_argument("pdf")
    s.add_argument("--bureau", required=True, choices=["equifax", "experian", "transunion", "innovis"])
    s.set_defaults(fn=cmd_parse_pdf)
    s = sub.add_parser("laws", help="Print the legal knowledge base")
    s.set_defaults(fn=cmd_laws)
    s = sub.add_parser("web", help="Run the local web app")
    s.add_argument("--port", type=int, default=8765)
    s.set_defaults(fn=cmd_web)
    a = p.parse_args(argv)
    a.fn(a)
