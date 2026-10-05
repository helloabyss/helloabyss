"""Plain-text audit report shared by the CLI and web app."""

from . import DISCLAIMER
from .evidence import evidence_report
from .law import LAWS
from .letters import plan_letters
from .metro2 import DISPUTE_CATEGORIES
from .pipeline import next_actions
from .states import state_notes


def audit_text(case, findings, include_direct=False):
    out = [f"CREDIT FILE AUDIT: {case.consumer.full_name}  (as of {case.today})", DISCLAIMER, ""]
    missing, problems = evidence_report(case)
    out.append("IDENTITY DOCUMENTS")
    out += [f"  MISSING: {m}" for m in missing] or ["  Government ID and proof of address present."]
    out += [f"  CHECK: {p}" for p in problems]
    out.append("")
    out.append(f"FINDINGS ({len(findings)})")
    for f in findings:
        flag = "" if f.disputable else "  [NOT DISPUTED: " + f.blocked_reason + "]"
        out.append(f"{f.id} [{f.severity.upper()}] {f.title}{flag}")
        out.append(f"     {f.account_label or f.furnisher} | bureaus: {', '.join(f.bureaus)} | "
                   f"category: {DISPUTE_CATEGORIES[f.category]['label']} | basis: {f.basis}")
        for fact in f.facts:
            out.append(f"     - {fact}")
        if f.laws:
            out.append("     Law: " + "; ".join(LAWS[k].cite for k in f.laws))
        out.append(f"     Remedy: {f.remedy}")
    letters, blocked = plan_letters(case, findings, include_direct)
    out += ["", f"LETTERS PLANNED ({len(letters)})"]
    for L in letters:
        status = "READY" if L.ready else "NEEDS: " + ", ".join(L.missing_documents)
        n = len(L.findings) or len(L.context.get("items", [])) or 1
        out.append(f"  {L.letter_type} -> {L.target}: {n} item(s) [{status}]")
    if blocked:
        out += ["", "NOT DISPUTED to the recipient shown (guardrails: factual basis, evidence, no repeat disputes)"]
        out += [f"  {f.id} {f.title}: {why}" for f, why in blocked]
    acts = next_actions(case)
    if acts:
        out += ["", "DISPUTE TRACKER"] + [f"  {lbl}: {msg}" for lbl, msg in acts]
    out += ["", "STATE LAW", "  " + state_notes(case.consumer.state)]
    return "\n".join(out)
