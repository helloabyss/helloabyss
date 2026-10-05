"""Dispute lifecycle: deadlines, the e-OSCAR loop and escalation.

  consumer dispute -> bureau (§ 611) -> ACDV to furnisher within 5 business days (§ 611(a)(2))
  -> furnisher investigates (§ 623(b)) -> response code -> bureau updates file
  -> results to consumer within 5 business days of completion (§ 611(a)(6))
  -> verified?  -> MOV request (§ 611(a)(7)) + direct furnisher dispute (§ 623(a)(8))
  -> no reply?  -> failure-to-reinvestigate notice + CFPB complaint
  -> deleted?   -> watch for reinsertion (§ 611(a)(5)(B)); request § 611(d) notices
"""

from datetime import date, timedelta

from .models import parse_date

# Disputes are counted from RECEIPT. When only the mailing date is known, assume this
# many days in the mail (certified mail return receipts give the real date).
ASSUMED_MAIL_DAYS = 5


def _nth_weekday(year, month, weekday, n):
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year, month, weekday):
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def federal_holidays(year):
    fixed = [date(year, 1, 1), date(year, 6, 19), date(year, 7, 4), date(year, 11, 11), date(year, 12, 25)]
    observed = []
    for d in fixed:
        observed.append(d - timedelta(days=1) if d.weekday() == 5 else d + timedelta(days=1) if d.weekday() == 6 else d)
    return set(observed) | {
        _nth_weekday(year, 1, 0, 3), _nth_weekday(year, 2, 0, 3), _last_weekday(year, 5, 0),
        _nth_weekday(year, 9, 0, 1), _nth_weekday(year, 10, 0, 2), _nth_weekday(year, 11, 3, 4),
    }


def add_business_days(d, n):
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in federal_holidays(d.year):
            n -= 1
    return d


def received_date(dispute):
    r = parse_date(dispute.get("received_date"))
    if r:
        return r, True
    s = parse_date(dispute.get("sent_date"))
    return (s + timedelta(days=ASSUMED_MAIL_DAYS), False) if s else (None, False)


def deadline(dispute):
    """Return (deadline_date, rule_text) for a dispute record."""
    rec, _ = received_date(dispute)
    if not rec:
        return None, "not sent yet"
    kind = dispute["letter_type"]
    if kind in ("bureau_dispute", "reinsertion_challenge", "furnisher_direct", "failure_to_respond"):
        days = 45 if dispute.get("after_free_annual_disclosure") else 30
        if dispute.get("supplemented_on"):
            days += 15
        return rec + timedelta(days=days), f"{days} days from receipt (§ 1681i(a)(1)" + \
            (", § 1681j(a)(3)" if days >= 45 else "") + ")"
    if kind == "mov_request":
        return rec + timedelta(days=15), "15 days from request (§ 1681i(a)(7))"
    if kind == "identity_theft_block":
        return add_business_days(rec, 4), "4 business days (§ 1681c-2(a))"
    if kind == "debt_validation":
        return None, "collector must stop collecting until it mails verification (§ 1692g(b)); no fixed deadline"
    return None, "no statutory response deadline"


def next_actions(case):
    """Walk every dispute record and say what to do next."""
    today = case.today
    out = []
    for d in case.disputes:
        due, rule = deadline(d)
        status = d.get("status", "draft")
        rec, actual = received_date(d)
        label = f"{d['id']} ({d['letter_type']} -> {d['target']})"
        if status == "draft":
            out.append((label, "Print, sign and send by certified mail with return receipt. Record sent_date."))
            continue
        if status == "sent":
            if due and today > due:
                late = (today - due).days
                out.append((label, f"OVERDUE by {late} day(s); deadline was {due} [{rule}]. "
                                   "Send a failure_to_respond notice and file a CFPB complaint "
                                   "(consumerfinance.gov/complaint). Under § 1681i(a)(5)(A) unverified "
                                   "information must be deleted."
                                   + ("" if actual else " Deadline is estimated: record received_date from the return receipt.")))
            elif due:
                out.append((label, f"Waiting. Response due {due} [{rule}]"
                                   + ("" if actual else " (estimated; add received_date)") + "."))
            else:
                out.append((label, f"Waiting. {rule}."))
            continue
        for item in d.get("results", []):
            key, outcome = item["account_key"], item["outcome"]
            if outcome == "verified":
                steps = []
                if d["letter_type"] in ("bureau_dispute", "reinsertion_challenge"):
                    steps.append("send mov_request to the bureau (§ 1681i(a)(6)(B)(iii), (a)(7))")
                    steps.append("send furnisher_direct dispute with your documents (§ 1681s-2(a)(8))")
                    steps.append("consider a § 1681i(b) statement of dispute")
                if d["letter_type"] == "furnisher_direct":
                    steps.append("re-dispute with the bureau only if you have NEW information (repeat "
                                 "disputes without it can be treated as frivolous)")
                steps.append("file a CFPB complaint; consult an FCRA attorney (§ 1681s-2(b) claims "
                             "arise only after a bureau dispute; 2-year limit, § 1681p)")
                out.append((f"{label} :: {key}", "VERIFIED. Next: " + "; ".join(steps) + "."))
            elif outcome == "deleted":
                out.append((f"{label} :: {key}", "DELETED. Pull a fresh report in 30-60 days to watch for "
                                                 "reinsertion; optionally send deletion_notification (§ 1681i(d))."))
            elif outcome == "modified":
                out.append((f"{label} :: {key}", "MODIFIED. Add the updated report to the case file and "
                                                 "re-run the audit."))
            elif outcome == "frivolous":
                out.append((f"{label} :: {key}", "Rejected as frivolous/irrelevant. The notice must say what "
                                                 "information is missing (§ 1681i(a)(3)(B)). Supply it and resend."))
    return out
