"""Letter planning and rendering.

plan_letters() decides which letters a case needs and refuses any dispute item that has
no factual basis. render() turns a planned letter into plain text ready to print and sign.
"""

from collections import defaultdict
from dataclasses import dataclass, field

from .evidence import letter_ready
from .law import LAWS
from .metro2 import DISPUTE_CATEGORIES
from .models import EVIDENCE_TYPES, norm_furnisher

# Mailing addresses from the bureaus' published dispute pages, checked October 2026.
# Re-check before mailing; bureaus change P.O. boxes.
BUREAU_ADDRESSES = {
    "equifax": ("Equifax Information Services LLC", "P.O. Box 740256", "Atlanta, GA 30374-0256"),
    "experian": ("Experian", "P.O. Box 4500", "Allen, TX 75013"),
    "transunion": ("TransUnion Consumer Solutions", "P.O. Box 2000", "Chester, PA 19016-2000"),
    "innovis": ("Innovis Consumer Assistance", "[CONFIRM P.O. BOX AT innovis.com BEFORE MAILING]", ""),
}

TITLES = {
    "bureau_dispute": "Request for reinvestigation under 15 U.S.C. § 1681i",
    "identity_theft_block": "Request to block identity theft information under 15 U.S.C. § 1681c-2",
    "reinsertion_challenge": "Reinserted information: 15 U.S.C. § 1681i(a)(5)(B)",
    "furnisher_direct": "Direct dispute under 15 U.S.C. § 1681s-2(a)(8) and 12 C.F.R. § 1022.43",
    "furnisher_identity_theft": "Identity theft notice under 15 U.S.C. § 1681s-2(a)(6)",
    "collector_dispute": "Dispute of debt and credit reporting: 15 U.S.C. §§ 1692g, 1692e(8)",
    "mov_request": "Request for description of reinvestigation procedure: 15 U.S.C. § 1681i(a)(7)",
    "failure_to_respond": "Reinvestigation not completed within the statutory period",
}


@dataclass
class Letter:
    letter_type: str
    target: str
    recipient: tuple
    findings: list
    enclosures: list = field(default_factory=list)
    missing_documents: list = field(default_factory=list)
    context: dict = field(default_factory=dict)

    @property
    def ready(self):
        return not self.missing_documents


def _repeat_block(case, finding, target):
    """§ 1681i(a)(3) / § 1022.43(f): a dispute already answered 'verified' may not be resent
    to the same party unless it carries new information."""
    for d in case.disputes:
        if d.get("target") != target:
            continue
        for item in d.get("results", []):
            if item.get("account_key") == finding.account_key and item.get("outcome") == "verified":
                if not set(finding.evidence_ids) - set(item.get("evidence_ids", [])):
                    return (f"{target}: already disputed in {d['id']} and verified; resending without new "
                            "evidence risks a frivolous determination. Escalate instead (see `track`).")
    return ""


def plan_letters(case, findings, include_direct=False):
    blocked = []
    usable = []
    for f in findings:
        if not f.disputable:
            blocked.append((f, f.blocked_reason or "not disputable"))
            continue
        if not f.facts or not f.laws:
            blocked.append((f, "no factual basis or legal citation"))
            continue
        usable.append(f)

    letters = []
    per_bureau = defaultdict(list)
    for f in usable:
        for b in f.bureaus:
            reason = _repeat_block(case, f, b)
            if reason:
                blocked.append((f, reason))
            else:
                per_bureau[b].append(f)

    for bureau, fs in sorted(per_bureau.items()):
        theft = [f for f in fs if f.category == "FRAUD"]
        reins = [f for f in fs if f.rule == "REINSERTED"]
        normal = [f for f in fs if f not in theft and f not in reins]
        addr = BUREAU_ADDRESSES[bureau]
        for kind, group in (("identity_theft_block", theft), ("reinsertion_challenge", reins),
                            ("bureau_dispute", normal)):
            if group:
                letters.append(Letter(kind, bureau, addr, group))

    # Furnisher letters: identity theft notices always; direct disputes on request or after
    # a bureau dispute came back verified.
    verified_keys = {i["account_key"] for d in case.disputes for i in d.get("results", [])
                     if i.get("outcome") == "verified"}
    per_furnisher = defaultdict(list)
    for f in usable:
        if _repeat_block(case, f, norm_furnisher(f.furnisher)):
            blocked.append((f, _repeat_block(case, f, norm_furnisher(f.furnisher))))
            continue
        if f.account_key and f.category not in ("INQUIRY", "PERSONAL_INFO") and f.rule != "OBSOLETE-BK":
            per_furnisher[norm_furnisher(f.furnisher)].append(f)
    for fk, fs in sorted(per_furnisher.items()):
        name = fs[0].furnisher
        addr = case.furnisher_addresses.get(name) or case.furnisher_addresses.get(fk)
        recipient = (name, *(addr.split("\n") if addr else
                             ["[Address the furnisher designates for disputes: see your statements, its "
                              "website, or the bureau results letter]"]))
        theft = _dedupe([f for f in fs if f.category == "FRAUD"])
        if theft:
            letters.append(Letter("furnisher_identity_theft", fk, recipient, theft))
        collection = [f for f in fs if f.category != "FRAUD" and _is_collection(case, f)]
        if collection:
            letters.append(Letter("collector_dispute", fk, recipient, _dedupe(collection)))
        direct = _dedupe([f for f in fs if f.category != "FRAUD" and not _is_collection(case, f)
                          and (include_direct or f.account_key in verified_keys)])
        if direct:
            letters.append(Letter("furnisher_direct", fk, recipient, direct))

    # MOV requests and failure-to-respond notices come from the dispute history.
    from .pipeline import deadline
    for d in case.disputes:
        if d.get("letter_type") not in ("bureau_dispute", "reinsertion_challenge") or d["target"] not in BUREAU_ADDRESSES:
            continue
        ver = [i for i in d.get("results", []) if i.get("outcome") == "verified"]
        if ver and not any(x.get("letter_type") == "mov_request" and x.get("parent") == d["id"] for x in case.disputes):
            letters.append(Letter("mov_request", d["target"], BUREAU_ADDRESSES[d["target"]], [],
                                  context={"parent": d, "items": ver}))
        due, _ = deadline(d)
        if d.get("status") == "sent" and due and case.today > due:
            letters.append(Letter("failure_to_respond", d["target"], BUREAU_ADDRESSES[d["target"]], [],
                                  context={"parent": d, "due": due}))

    for L in letters:
        L.missing_documents = letter_ready(case, L.letter_type)
        ids = {i for f in L.findings for i in f.evidence_ids}
        ev = case.evidence_by_id()
        L.enclosures = [e for e in case.evidence if e.type in ("government_id", "proof_of_address")
                        and L.letter_type not in ("collector_dispute",)]
        L.enclosures += [ev[i] for i in sorted(ids) if ev[i] not in L.enclosures]
        if L.letter_type in ("identity_theft_block", "furnisher_identity_theft"):
            L.enclosures += [e for e in case.evidence if e.type in ("ftc_identity_theft_report", "police_report")
                             and e not in L.enclosures]
        if L.letter_type in ("mov_request", "failure_to_respond"):
            L.enclosures += [e for e in case.evidence if e.type in ("bureau_results", "mail_receipt")
                             and e not in L.enclosures]
    return letters, blocked


def _dedupe(fs):
    seen, out = set(), []
    for f in fs:
        k = id(f)
        if k not in seen:
            seen.add(k)
            out.append(f)
    return out


def _is_collection(case, f):
    return any(t.is_collection for t in case.tradelines() if t.account_key == f.account_key)


# ------------------------------------------------------------------ rendering
def _cites(keys):
    return "; ".join(LAWS[k].cite for k in keys if k in LAWS)


def _header(case, L):
    c = case.consumer
    lines = [c.full_name, c.current_address.line1]
    if c.current_address.line2:
        lines.append(c.current_address.line2)
    lines += [f"{c.current_address.city}, {c.current_address.state} {c.current_address.zip}", "",
              f"{case.today:%B} {case.today.day}, {case.today.year}", "", "SENT BY CERTIFIED MAIL, RETURN RECEIPT REQUESTED", ""]
    lines += [x for x in L.recipient if x] + [""]
    lines += [f"Re: {TITLES[L.letter_type]}",
              f"    Consumer: {c.full_name} | Date of birth: {c.date_of_birth} | SSN: XXX-XX-{c.ssn_last4}"]
    if c.prior_addresses:
        lines.append(f"    Prior address: {c.prior_addresses[0].one_line()}")
    return lines + [""]


def _items(L, with_bureau=False):
    """One numbered item per account, so each account maps to a single ACDV with a
    clear primary issue rather than several fragmented ones."""
    groups = defaultdict(list)
    for f in L.findings:
        groups[f.account_label or f.furnisher].append(f)
    out = []
    for n, (label, fs) in enumerate(groups.items(), 1):
        bureaus = sorted({b for f in fs for b in f.bureaus})
        out.append(f"{n}. {label}" + (f" (reported by {', '.join(b.title() for b in bureaus)})" if with_bureau else ""))
        facts, laws = [], []
        for f in fs:
            out.append(f"   Issue: {f.title}. [{DISPUTE_CATEGORIES[f.category]['label']}]")
            facts += [x for x in f.facts if x not in facts]
            laws += [k for k in f.laws if k not in laws]
        out += [f"   - {fact}" for fact in facts]
        out.append(f"   Legal basis: {_cites(laws)}")
        remedies = []
        for f in fs:
            if f.remedy not in remedies:
                remedies.append(f.remedy)
        out.append(f"   Requested action: {'; '.join(remedies)}.")
        out.append("")
    return out


def _enclosures(L):
    if not L.enclosures:
        return []
    out = ["Enclosures:"]
    for e in L.enclosures:
        out.append(f"  - {EVIDENCE_TYPES[e.type]}: {e.description}")
    return out + [""]


def _sign(case):
    return ["Sincerely,", "", "", "______________________________", case.consumer.full_name, ""]


def render(case, L):
    c = case.consumer
    out = _header(case, L)
    t = L.letter_type
    if t == "bureau_dispute":
        out += [f"I dispute the completeness and accuracy of the items listed below in my "
                f"{L.target.title()} credit file. Each item states what is wrong and why. Please conduct a "
                "reasonable reinvestigation under 15 U.S.C. § 1681i(a)(1), forward all relevant information "
                "I have provided, including the enclosed documents, to each furnisher under § 1681i(a)(2), "
                "and consider it under § 1681i(a)(4). Information that is inaccurate, incomplete or cannot "
                "be verified must be deleted or modified under § 1681i(a)(5)(A).", ""]
        out += _items(L)
        out += ["Please send me written results under § 1681i(a)(6), including a free copy of my report if "
                "it changes. If any item is verified, I ask for a description of the procedure used to "
                "determine its accuracy, including the furnisher's name, address and telephone number, under "
                "§ 1681i(a)(6)(B)(iii) and (a)(7).", ""]
    elif t == "identity_theft_block":
        out += ["I am a victim of identity theft. Under 15 U.S.C. § 1681c-2(a), please block the information "
                f"listed below from my {L.target.title()} file within four business days and notify each "
                "furnisher under § 1681c-2(b). Enclosed are proof of my identity and a copy of my identity "
                "theft report.", ""]
        out += _items(L)
        out += ["Statement under § 1681c-2(a)(4): The information listed above does not relate to any "
                "transaction that I made or authorized.", "",
                "Please also confirm whether a fraud alert is on my file (15 U.S.C. § 1681c-1). I request an "
                "extended fraud alert if my enclosed identity theft report supports one.", ""]
    elif t == "reinsertion_challenge":
        out += ["The information below was deleted from my file after a previous dispute and has been "
                "reinserted. Under 15 U.S.C. § 1681i(a)(5)(B), reinsertion requires the furnisher's "
                "certification that the information is complete and accurate, and written notice to me "
                "within five business days. I did not receive that notice.", ""]
        out += _items(L)
        out += ["Please provide the furnisher's certification and the date of notice to me, or delete the "
                "information.", ""]
    elif t == "furnisher_direct":
        out += ["I dispute the accuracy of information you furnish to consumer reporting agencies about the "
                "account(s) below. Under 15 U.S.C. § 1681s-2(a)(8) and 12 C.F.R. § 1022.43, please investigate, "
                "review the enclosed documents, and report your results to me. While the dispute is open, you "
                "may not report this information without noting that I dispute it (§ 1681s-2(a)(3)).", ""]
        out += _items(L, with_bureau=True)
        out += ["If your investigation finds the information inaccurate, please notify every consumer "
                "reporting agency you furnished it to and correct it (§ 1681s-2(a)(2)).", ""]
    elif t == "furnisher_identity_theft":
        out += ["I am a victim of identity theft. The account(s) below were opened or used without my "
                "authorization. Enclosed is my identity theft report. Under 15 U.S.C. § 1681s-2(a)(6)(B), "
                "you may not furnish this information to any consumer reporting agency unless you later "
                "know or are informed by me that it is correct.", ""]
        out += _items(L, with_bureau=True)
        out += ["Please also send me copies of the application and business transaction records for these "
                "accounts, which I am entitled to receive as an identity theft victim under 15 U.S.C. § 1681g(e).", ""]
    elif t == "collector_dispute":
        out += ["I dispute the debt(s) listed below and how you report them.", "",
                "If I am within the validation period stated in your validation notice, this is my written "
                "dispute under 15 U.S.C. § 1692g(b): please stop collection until you mail me verification "
                "of the debt and the name and address of the original creditor.", "",
                "Whether or not the validation period has passed, under 15 U.S.C. § 1692e(8) you may not "
                "communicate credit information you know or should know is false, including failing to "
                "report that this debt is disputed.", ""]
        out += _items(L, with_bureau=True)
    elif t == "mov_request":
        d = L.context["parent"]
        out += [f"On {d.get('sent_date', '[date]')} I disputed items in my file. Your results letter dated "
                f"{d.get('result_date', '[date]')} said the following were verified:", ""]
        for i in L.context["items"]:
            out.append(f"  - {i.get('label', i['account_key'])}")
        out += ["", "Under 15 U.S.C. § 1681i(a)(7), please send me within 15 days a description of the "
                "procedure you used to determine the accuracy and completeness of each item, including the "
                "business name, address and telephone number of each furnisher you contacted. Please also "
                "tell me whether the documents I enclosed with my dispute were forwarded to the furnisher "
                "under § 1681i(a)(2).", ""]
    elif t == "failure_to_respond":
        d, due = L.context["parent"], L.context["due"]
        out += [f"I sent a dispute on {d.get('sent_date', '[date]')}, received by you on "
                f"{d.get('received_date') or '[date from return receipt]'}. The reinvestigation period under "
                f"15 U.S.C. § 1681i(a)(1) ended on {due:%B} {due.day}, {due.year}. I have not received results.", "",
                "Information that is not verified within the reinvestigation period must be deleted under "
                "§ 1681i(a)(5)(A). Please delete the disputed items and send me an updated report. I am "
                "filing a complaint with the Consumer Financial Protection Bureau.", ""]
    out += _sign(case) + _enclosures(L)
    return "\n".join(out)
