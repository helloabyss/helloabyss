"""Report ingestion: JSON case files and best-effort PDF text extraction.

Bureau PDF layouts differ and change often, so PDF parsing only produces a DRAFT list of
tradelines. Every value must be checked against the PDF before running the audit; a wrong
date parsed from a PDF would produce a wrong dispute.
"""

import json
import re
import shutil
import subprocess

from .models import CaseFile


def load_case(path):
    with open(path) as fh:
        return CaseFile.from_dict(json.load(fh))


def pdf_text(path):
    try:
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    except ImportError:
        pass
    if shutil.which("pdftotext"):
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                              text=True, check=True).stdout
    raise RuntimeError("Install pypdf (pip install pypdf) or poppler-utils (pdftotext) to read PDFs")


FIELD_PATTERNS = {
    "furnisher": r"(?:account name|creditor name|company name|creditor)\s*:?\s*(.+)",
    "account_number": r"account (?:number|#)\s*:?\s*([\dXx*\- ]{4,})",
    "account_type": r"(?:account type|type)\s*:?\s*(.+)",
    "date_opened": r"(?:date opened|opened)\s*:?\s*([\d/\-]+)",
    "date_of_first_delinquency": r"(?:date of first delinquency|first delinquency|dofd)\s*:?\s*([\d/\-]+)",
    "date_last_payment": r"(?:date of last payment|last payment(?: date)?)\s*:?\s*([\d/\-]+)",
    "date_reported": r"(?:date reported|reported|date updated|last reported)\s*:?\s*([\d/\-]+)",
    "date_closed": r"(?:date closed|closed)\s*:?\s*([\d/\-]+)",
    "balance": r"(?:balance|current balance)\s*:?\s*\$?([\d,\.]+)",
    "credit_limit": r"(?:credit limit|limit)\s*:?\s*\$?([\d,\.]+)",
    "high_credit": r"(?:high credit|high balance|original amount)\s*:?\s*\$?([\d,\.]+)",
    "past_due": r"(?:amount past due|past due)\s*:?\s*\$?([\d,\.]+)",
    "status_text": r"(?:status|account status|pay status)\s*:?\s*(.+)",
    "original_creditor": r"original creditor\s*:?\s*(.+)",
}
BLOCK_START = re.compile(r"^\s*(?:account name|creditor name|company name)\s*:", re.I | re.M)


def _norm_date(v):
    m = re.match(r"(\d{1,2})/(\d{4})$", v)
    if m:
        return f"{m.group(2)}-{int(m.group(1)):02d}"
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", v)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    return v


def parse_report_text(text, bureau):
    starts = [m.start() for m in BLOCK_START.finditer(text)]
    blocks = [text[a:b] for a, b in zip(starts, starts[1:] + [len(text)])]
    lines = []
    for blk in blocks:
        t = {}
        for fld, pat in FIELD_PATTERNS.items():
            m = re.search(pat, blk, re.I)
            if m:
                v = m.group(1).strip().split("  ")[0]
                t[fld] = _norm_date(v) if fld.startswith("date") else v
        if t.get("furnisher"):
            st = t.get("status_text", "").lower()
            t["is_collection"] = "collection" in st or bool(t.get("original_creditor"))
            t.setdefault("account_number", "UNKNOWN")
            lines.append(t)
    return {"bureau": bureau, "report_date": "", "tradelines": lines,
            "_warning": "DRAFT from PDF text. Check every value against the report, add status_code "
                        "(Metro 2) where known, then move this into the case file."}
