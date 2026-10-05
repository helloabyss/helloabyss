"""Audit engine: runs every rule over a case file and returns findings.

Two kinds of finding:
  basis="report_data"  - provable from the reports themselves (a copy of the report is
                          the evidence). Always disputable.
  basis="assertion"    - depends on a fact the consumer states. Disputable only when the
                          evidence in evidence.REQUIRED_FOR_ASSERTION is attached.
Findings with severity "review" are signals for the consumer to check; they are never
turned into disputes on their own, because the system can't know they're wrong.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

from . import metro2
from .evidence import supporting_evidence
from .models import norm_furnisher, norm_name, parse_date

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "review": 4}
BALANCE_TOLERANCE = 1.00


@dataclass
class Finding:
    rule: str
    category: str
    severity: str
    title: str
    facts: list
    laws: list
    remedy: str
    bureaus: list
    account_key: str = ""
    furnisher: str = ""
    account_label: str = ""
    basis: str = "report_data"
    assertion_id: str = ""
    evidence_ids: list = field(default_factory=list)
    disputable: bool = True
    blocked_reason: str = ""
    id: str = ""

    def to_dict(self):
        return dict(self.__dict__)


def add_years(d, years):
    try:
        return d.replace(year=d.year + years)
    except ValueError:  # 29 Feb
        return d.replace(year=d.year + years, day=28)


def month_index(d):
    return d.year * 12 + d.month - 1


def obsolescence_date(dofd):
    """§ 1681c(a)(4) and (c): 180 days from commencement of delinquency, then 7 years."""
    return add_years(dofd + timedelta(days=180), 7)


def _long(d):
    return f"{d:%B} {d.day}, {d.year}"


def _fmt(v):
    return "not reported" if v in (None, "") else (f"${v:,.2f}" if isinstance(v, float) else str(v))


class Auditor:
    def __init__(self, case):
        self.case = case
        self.today = case.today
        self.findings = []
        self.by_account = defaultdict(list)
        for t in case.tradelines():
            self.by_account[t.account_key].append(t)

    def add(self, **kw):
        self.findings.append(Finding(**kw))

    def run(self):
        for rule in (self.cross_bureau, self.obsolete, self.dofd_rules, self.internal_contradictions,
                     self.collection_rules, self.inquiries, self.personal_info, self.bankruptcy,
                     self.reinsertion, self.assertions):
            rule()
        self.findings.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.account_key, f.rule))
        for i, f in enumerate(self.findings, 1):
            f.id = f"F{i:03d}"
        return self.findings

    # ---- A. Cross-bureau inconsistencies --------------------------------------------
    def cross_bureau(self):
        for key, lines in self.by_account.items():
            if len({t.bureau for t in lines}) < 2:
                continue
            t0 = lines[0]
            for fld, cat, label in (("date_opened", "DATES", "Date opened"),
                                    ("date_of_first_delinquency", "REAGING", "Date of first delinquency"),
                                    ("credit_limit", "BALANCE", "Credit limit"),
                                    ("high_credit", "BALANCE", "High credit"),
                                    ("original_creditor", "OWNERSHIP", "Original creditor")):
                vals = {t.bureau: getattr(t, fld) for t in lines if getattr(t, fld) not in (None, "")}
                if fld.startswith("date"):
                    vals = {b: v[:7] for b, v in vals.items()}
                if fld == "original_creditor":
                    vals = {b: norm_furnisher(v) for b, v in vals.items()}
                if len(set(vals.values())) > 1:
                    sev = "critical" if fld == "date_of_first_delinquency" else "medium"
                    self.add(rule="XB-FIELD-MISMATCH", category=cat, severity=sev,
                             title=f"{label} reported differently across bureaus",
                             facts=[f"{b.title()} reports {label.lower()} as {_fmt(v)}." for b, v in vals.items()]
                                   + ["The same account can have only one true value for this field."],
                             laws=["FCRA_607B", "FCRA_623A1", "FCRA_611A1"] + (["FCRA_605C", "FCRA_623A5"] if sev == "critical" else []),
                             remedy="Correct to the accurate value or delete as unverifiable",
                             bureaus=sorted(vals), account_key=key, furnisher=t0.furnisher,
                             account_label=t0.label)
            # Balances / status legitimately move month to month: compare only same-month reports.
            by_month = defaultdict(list)
            for t in lines:
                if t.date_reported:
                    by_month[t.date_reported[:7]].append(t)
            for month, group in by_month.items():
                if len({t.bureau for t in group}) < 2:
                    continue
                bals = {t.bureau: t.balance for t in group if t.balance is not None}
                if bals and max(bals.values()) - min(bals.values()) > BALANCE_TOLERANCE:
                    self.add(rule="XB-BALANCE", category="BALANCE", severity="medium",
                             title=f"Different balances reported for the same month ({month})",
                             facts=[f"{b.title()}: balance {_fmt(v)} as of {month}." for b, v in bals.items()],
                             laws=["FCRA_607B", "FCRA_623A1", "FCRA_611A1"],
                             remedy="Correct the balance or delete as unverifiable",
                             bureaus=sorted(bals), account_key=key, furnisher=t0.furnisher,
                             account_label=t0.label)
                derog = {t.bureau: t.status_code in metro2.DEROGATORY_STATUSES for t in group if t.status_code}
                if len(set(derog.values())) > 1:
                    self.add(rule="XB-STATUS", category="STATUS", severity="high",
                             title=f"Account status conflicts across bureaus ({month})",
                             facts=[f"{t.bureau.title()}: status {t.status_code} "
                                    f"({metro2.ACCOUNT_STATUS.get(t.status_code, t.status_text)})." for t in group if t.status_code],
                             laws=["FCRA_607B", "FCRA_623A1", "FCRA_611A1"],
                             remedy="Correct the status to the accurate one or delete",
                             bureaus=sorted(derog), account_key=key, furnisher=t0.furnisher,
                             account_label=t0.label)

    # ---- B. Obsolete information -------------------------------------------------------
    def obsolete(self):
        for t in self.case.tradelines():
            dofd = t.d("date_of_first_delinquency")
            if not dofd or t.status_code not in metro2.DEROGATORY_STATUSES and not t.is_collection:
                continue
            purge = obsolescence_date(dofd)
            if purge <= self.today:
                self.add(rule="OBSOLETE-7YR", category="REAGING", severity="critical",
                         title="Negative account is past the 7-year reporting limit",
                         facts=[f"Reported date of first delinquency: {dofd:%B %Y}.",
                                f"Under § 1681c(c) the reporting period ended on {_long(purge)} "
                                f"(DOFD + 180 days + 7 years).",
                                f"It is still being reported as of {_long(self.today)}."],
                         laws=["FCRA_605A", "FCRA_605C", "FCRA_607B"],
                         remedy="Delete the account as obsolete",
                         bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                         account_label=t.label)
        for r in self.case.reports:
            for p in r.public_records:
                filed = parse_date(p.filed_date)
                if p.type.lower() == "bankruptcy" and filed and add_years(filed, 10) <= self.today:
                    self.add(rule="OBSOLETE-BK", category="BANKRUPTCY", severity="critical",
                             title="Bankruptcy is past the 10-year reporting limit",
                             facts=[f"Bankruptcy (Chapter {p.chapter or '?'}) order for relief dated {_long(filed)}.",
                                    f"The 10-year limit ended on {_long(add_years(filed, 10))}."],
                             laws=["FCRA_605A"], remedy="Delete the public record as obsolete",
                             bureaus=[r.bureau], furnisher=p.court or "Public record",
                             account_label=f"Bankruptcy {p.case_number}".strip())

    # ---- C. DOFD / re-aging ---------------------------------------------------------------
    def dofd_rules(self):
        lines = self.case.tradelines()
        for t in lines:
            derog = t.status_code in {"97", "93", "64", "62"} or t.is_collection
            if derog and not t.date_of_first_delinquency:
                self.add(rule="DOFD-MISSING", category="DATES", severity="high",
                         title="Collection or charge-off reported without a date of first delinquency",
                         facts=[f"Status: {metro2.ACCOUNT_STATUS.get(t.status_code, t.status_text or 'collection')}.",
                                "No date of first delinquency is shown, so the 7-year removal date can't be checked."],
                         laws=["FCRA_623A5", "FCRA_605C", "FCRA_607B"],
                         remedy="Report the accurate DOFD or delete as incomplete and unverifiable",
                         bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                         account_label=t.label)
            self._history_vs_dofd(t)
        # Collection DOFD later than the original creditor's DOFD = re-aging.
        for c in [t for t in lines if t.is_collection and t.original_creditor and t.date_of_first_delinquency]:
            oc_name = norm_furnisher(c.original_creditor)
            # Compare against the earliest DOFD any bureau reports for the original creditor.
            for o in sorted(lines, key=lambda t: t.date_of_first_delinquency or "9999"):
                if o.is_collection or not o.date_of_first_delinquency:
                    continue
                on = norm_furnisher(o.furnisher)
                if not oc_name or not on or (oc_name not in on and on not in oc_name):
                    continue
                cd, od = c.d("date_of_first_delinquency"), o.d("date_of_first_delinquency")
                if month_index(cd) > month_index(od):
                    self.add(rule="REAGED-COLLECTION", category="REAGING", severity="critical",
                             title="Collection account appears re-aged",
                             facts=[f"Original creditor {o.furnisher} reports DOFD {od:%B %Y} ({o.bureau.title()}).",
                                    f"Collector {c.furnisher} reports DOFD {cd:%B %Y} ({c.bureau.title()}).",
                                    "A sale or transfer doesn't restart the § 1681c(c) clock; the collector must "
                                    "carry the original DOFD.",
                                    f"The correct removal date is {obsolescence_date(od):%B %Y}, not "
                                    f"{obsolescence_date(cd):%B %Y}."],
                             laws=["FCRA_605C", "FCRA_623A5", "FCRA_623A1", "FDCPA_807_8", "FCRA_607B"],
                             remedy="Correct DOFD to the original delinquency date (delete if that makes it obsolete)",
                             bureaus=[c.bureau], account_key=c.account_key,
                             furnisher=c.furnisher, account_label=c.label)
                break  # only the earliest original-creditor DOFD matters

    def _history_vs_dofd(self, t):
        """Payment history (most recent month first) showing the delinquency streak began
        before the reported DOFD."""
        dofd, start = t.d("date_of_first_delinquency"), t.d("payment_history_start")
        hist = (t.payment_history or "").upper()
        if not (dofd and start and hist):
            return
        # Walk back from the most recent month to the start of the current delinquency streak.
        streak_start = None
        for i, ch in enumerate(hist):
            if ch in metro2.LATE_MARKS:
                streak_start = i
            elif streak_start is not None:
                break
        if streak_start is None:
            return
        first_late = month_index(start) - streak_start
        if month_index(dofd) - first_late >= 2:
            y, m = divmod(first_late, 12)
            self.add(rule="REAGED-HISTORY", category="REAGING", severity="critical",
                     title="Reported DOFD is later than the payment history shows",
                     facts=[f"Payment history shows the delinquency began around {date(y, m + 1, 1):%B %Y}.",
                            f"Reported date of first delinquency is {dofd:%B %Y}.",
                            "A later DOFD extends the 7-year reporting period."],
                     laws=["FCRA_605C", "FCRA_623A5", "FCRA_623A1", "FCRA_607B"],
                     remedy="Correct the DOFD to match the payment history",
                     bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                     account_label=t.label)

    # ---- D. Internal contradictions -------------------------------------------------------
    def internal_contradictions(self):
        for t in self.case.tradelines():
            hist = (t.payment_history or "").upper()
            common = dict(bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                          account_label=t.label)
            if t.status_code in metro2.PAID_STATUSES and (t.balance or 0) > BALANCE_TOLERANCE:
                self.add(rule="PAID-WITH-BALANCE", category="BALANCE", severity="high",
                         title="Account reported as paid but still shows a balance",
                         facts=[f"Status {t.status_code}: {metro2.ACCOUNT_STATUS[t.status_code]}.",
                                f"Balance reported: {_fmt(t.balance)}."],
                         laws=["FCRA_607B", "FCRA_623A1"], remedy="Report a $0 balance", **common)
            if t.past_due is not None and t.balance is not None and t.past_due - t.balance > BALANCE_TOLERANCE:
                self.add(rule="PASTDUE-GT-BALANCE", category="BALANCE", severity="medium",
                         title="Past-due amount exceeds the balance",
                         facts=[f"Past due {_fmt(t.past_due)} vs balance {_fmt(t.balance)}."],
                         laws=["FCRA_607B", "FCRA_623A1"], remedy="Correct the amounts", **common)
            if t.status_code == "11" and hist[:1] in metro2.LATE_MARKS:
                self.add(rule="STATUS-HISTORY", category="PAYMENT_HISTORY", severity="medium",
                         title="Status says current but the latest month shows late",
                         facts=[f"Status 11 (current); most recent payment history month is "
                                f"'{hist[0]}' ({metro2.PAYMENT_HISTORY.get(hist[0])})."],
                         laws=["FCRA_607B", "FCRA_623A1"], remedy="Correct the inconsistent field", **common)
            if t.status_code == "05" and (t.balance or 0) > BALANCE_TOLERANCE:
                self.add(rule="TRANSFERRED-BALANCE", category="OWNERSHIP", severity="high",
                         title="Transferred/sold account still reports a balance",
                         facts=["Status 05 means the account was transferred; the transferor no longer "
                                "owns the debt.", f"Balance still reported: {_fmt(t.balance)}."],
                         laws=["FCRA_607B", "FCRA_623A1"], remedy="Report a $0 balance", **common)
            if t.past_due and t.date_closed and t.status_code in metro2.PAID_STATUSES:
                self.add(rule="CLOSED-PASTDUE", category="BALANCE", severity="medium",
                         title="Closed, paid account still shows an amount past due",
                         facts=[f"Closed {t.date_closed}, status {t.status_code}, past due {_fmt(t.past_due)}."],
                         laws=["FCRA_607B", "FCRA_623A1"], remedy="Report $0 past due", **common)

    # ---- E. Collections ------------------------------------------------------------------
    def collection_rules(self):
        lines = self.case.tradelines()
        for c in [t for t in lines if t.is_collection]:
            common = dict(bureaus=[c.bureau], account_key=c.account_key, furnisher=c.furnisher,
                          account_label=c.label)
            if c.is_medical and (c.status_code in metro2.PAID_STATUSES or (c.balance or 0) == 0 or (c.balance or 0) < 500):
                self.add(rule="MEDICAL-POLICY", category="STATUS", severity="medium",
                         title="Medical collection the nationwide bureaus say they no longer report",
                         facts=[f"Medical collection, balance {_fmt(c.balance)}, status "
                                f"{metro2.ACCOUNT_STATUS.get(c.status_code, c.status_text)}.",
                                "Equifax, Experian and TransUnion policy excludes paid medical collections "
                                "and those under $500. This is bureau policy, not a statute."],
                         laws=["POLICY_MEDICAL"], remedy="Delete under the bureau's medical debt policy", **common)
            # Original creditor and collector both carrying a balance for the same debt.
            if c.original_creditor:
                ocn = norm_furnisher(c.original_creditor)
                for o in lines:
                    on = norm_furnisher(o.furnisher)
                    if (o.bureau == c.bureau and not o.is_collection and ocn and on
                            and (ocn in on or on in ocn) and (o.balance or 0) > BALANCE_TOLERANCE
                            and (c.balance or 0) > BALANCE_TOLERANCE and o.status_code in {"97", "05", "93"}):
                        self.add(rule="DOUBLE-BALANCE", category="OWNERSHIP", severity="high",
                                 title="Same debt carries a balance under both original creditor and collector",
                                 facts=[f"{o.furnisher} ({o.status_text or o.status_code}) reports {_fmt(o.balance)}.",
                                        f"{c.furnisher} (collector for {c.original_creditor}) reports {_fmt(c.balance)}.",
                                        "Once a debt is sold, only the current owner may report a balance. "
                                        "Confirm the debt was sold, not just placed for collection."],
                                 laws=["FCRA_607B", "FCRA_623A1"],
                                 remedy="Original creditor to report $0 balance (sold/transferred)",
                                 bureaus=[c.bureau], account_key=o.account_key, furnisher=o.furnisher,
                                 account_label=o.label)

    # ---- F. Inquiries ---------------------------------------------------------------------
    def inquiries(self):
        not_mine = {norm_furnisher(a.furnisher) for a in self.case.assertions if a.type == "not_my_inquiry"}
        for r in self.case.reports:
            for q in r.inquiries:
                d = parse_date(q.date)
                if q.kind == "hard" and d and add_years(d, 2) <= self.today:
                    self.add(rule="INQUIRY-AGED", category="INQUIRY", severity="low",
                             title="Hard inquiry older than 2 years",
                             facts=[f"Inquiry by {q.creditor} on {_long(d)}.",
                                    "Bureaus remove hard inquiries after about 2 years by policy. "
                                    "The FCRA sets no inquiry limit, so this is a policy request."],
                             laws=["POLICY_INQUIRY"], remedy="Remove under bureau retention policy",
                             bureaus=[r.bureau], furnisher=q.creditor, account_label=f"Inquiry {q.creditor}")
                if q.kind == "hard" and norm_furnisher(q.creditor) in not_mine:
                    pass  # handled by assertions()

    # ---- G. Personal information --------------------------------------------------------
    def personal_info(self):
        c = self.case.consumer
        names, addrs = c.known_names(), c.known_addresses()
        for r in self.case.reports:
            odd_names = [n for n in r.names if norm_name(n) not in names]
            odd_addrs = [a for a in r.addresses if not isinstance(a, str) and a.norm() not in addrs]
            odd_ssn = [s for s in r.ssn_variations if s[-4:] != c.ssn_last4]
            odd_dob = [d for d in r.dates_of_birth if d != c.date_of_birth]
            items = ([f"Name variation: {n}" for n in odd_names] + [f"Address: {a.one_line()}" for a in odd_addrs]
                     + [f"SSN variation ending {s[-4:]}" for s in odd_ssn] + [f"Date of birth: {d}" for d in odd_dob])
            if items:
                sev = "high" if odd_ssn or odd_dob else "review"
                self.add(rule="PII-MISMATCH", category="PERSONAL_INFO", severity=sev,
                         title="Personal information on file that doesn't match the consumer",
                         facts=items + ["Unknown identifiers can indicate a mixed file or identity theft."],
                         laws=["FCRA_607B", "FCRA_611A1", "FCRA_609"],
                         remedy="Remove identifiers that don't belong to the consumer",
                         bureaus=[r.bureau], furnisher=r.bureau.title(), account_label="Personal information",
                         basis="report_data" if sev == "high" else "assertion",
                         disputable=sev == "high",
                         blocked_reason="" if sev == "high" else
                         "Confirm these aren't old or misspelled versions of your own details, then add a "
                         "personal_info_wrong assertion")

    # ---- H. Bankruptcy ----------------------------------------------------------------------
    def bankruptcy(self):
        bks = [p for r in self.case.reports for p in r.public_records
               if p.type.lower() == "bankruptcy" and p.discharged_date]
        for p in bks:
            filed = parse_date(p.filed_date)
            for t in self.case.tradelines():
                opened = t.d("date_opened")
                if opened and filed and opened < filed and ((t.balance or 0) > 0 or (t.past_due or 0) > 0) \
                        and "bankrupt" not in (t.remarks + t.status_text).lower():
                    self.add(rule="BK-NOT-REFLECTED", category="BANKRUPTCY", severity="review",
                             title="Pre-bankruptcy account still shows a balance after discharge",
                             facts=[f"Bankruptcy filed {_long(filed)}, discharged {p.discharged_date}.",
                                   f"Account opened {opened:%B %Y} still reports balance {_fmt(t.balance)}, "
                                   f"past due {_fmt(t.past_due)}, with no bankruptcy notation."],
                             laws=["FCRA_607B", "FCRA_623A1"],
                             remedy="If the debt was discharged: report $0 balance, 'included in bankruptcy'",
                             bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                             account_label=t.label, basis="assertion", disputable=False,
                             blocked_reason="Check your schedules. If listed and discharged, add an "
                                            "included_in_bankruptcy assertion with the discharge order")

    # ---- I. Reinsertion -------------------------------------------------------------------
    def reinsertion(self):
        deleted = {}
        for d in self.case.disputes:
            for item in d.get("results", []):
                if item.get("outcome") == "deleted":
                    deleted[(d["target"], item["account_key"])] = d.get("result_date", "")
        for t in self.case.tradelines():
            when = deleted.get((t.bureau, t.account_key))
            if when is not None:
                self.add(rule="REINSERTED", category="STATUS", severity="critical",
                         title="Previously deleted account has reappeared",
                         facts=[f"{t.bureau.title()} deleted this account after a dispute (result dated {when or 'on file'}).",
                                "It is reporting again. Reinsertion requires the furnisher's certification of "
                                "accuracy and written notice to you within 5 business days."],
                         laws=["FCRA_611A5B", "FCRA_607B"],
                         remedy="Produce the certification and reinsertion notice, or delete",
                         bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                         account_label=t.label)

    # ---- J. Consumer assertions -----------------------------------------------------------
    def _lines_for(self, a):
        if a.account_key and a.account_key in self.by_account:
            lines = self.by_account[a.account_key]
        else:
            fn = norm_furnisher(a.furnisher)
            lines = [t for t in self.case.tradelines() if fn and fn in norm_furnisher(t.furnisher)]
        if a.bureaus:
            lines = [t for t in lines if t.bureau in a.bureaus]
        return lines

    def assertions(self):
        for a in self.case.assertions:
            ok, attached, reason = supporting_evidence(self.case, a)
            spec = ASSERTION_RULES.get(a.type, ("STATUS",))
            if a.type == "not_my_inquiry":
                hits = [(r.bureau, q) for r in self.case.reports for q in r.inquiries
                        if norm_furnisher(a.furnisher) in norm_furnisher(q.creditor)
                        and (not a.bureaus or r.bureau in a.bureaus)]
                for bureau, q in hits:
                    self.add(rule="ASSERT-INQUIRY", category="INQUIRY", severity="medium",
                             title=f"Unauthorized inquiry: {q.creditor}",
                             facts=[f"Hard inquiry by {q.creditor} on {q.date}.", a.statement,
                                    "A report may be obtained only for a permissible purpose under § 1681b."],
                             laws=["FCRA_607B", "FCRA_611A1"], remedy="Delete the inquiry",
                             bureaus=[bureau], furnisher=q.creditor, account_label=f"Inquiry {q.creditor}",
                             basis="assertion", assertion_id=a.id,
                             evidence_ids=[e.id for e in attached])
                continue
            if a.type == "personal_info_wrong":
                self.add(rule="ASSERT-PII", category="PERSONAL_INFO", severity="medium",
                         title="Personal information that isn't the consumer's",
                         facts=[a.statement], laws=["FCRA_607B", "FCRA_611A1"],
                         remedy="Remove the listed identifiers", bureaus=a.bureaus or [r.bureau for r in self.case.reports],
                         account_label="Personal information", basis="assertion", assertion_id=a.id)
                continue
            lines = self._lines_for(a)
            if not lines:
                self.add(rule="ASSERT-NO-MATCH", category=spec[0], severity="review",
                         title=f"Assertion {a.id} doesn't match any reported account",
                         facts=[a.statement, f"Looked for account_key={a.account_key!r} furnisher={a.furnisher!r}."],
                         laws=[], remedy="Fix the account_key or furnisher name in the assertion",
                         bureaus=a.bureaus, basis="assertion", assertion_id=a.id, disputable=False,
                         blocked_reason="No matching account")
                continue
            if a.type == "disputed_directly":
                self._dispute_flag(a, lines, ok, attached, reason)
                continue
            for t in lines:
                facts = [a.statement] + [f"{k.replace('_', ' ').title()}: {v}" for k, v in a.details.items()]
                facts.append(f"{t.bureau.title()} currently reports: status "
                             f"{metro2.ACCOUNT_STATUS.get(t.status_code, t.status_text) or 'n/a'}, "
                             f"balance {_fmt(t.balance)}, DOFD {_fmt(t.date_of_first_delinquency)}.")
                self.add(rule=f"ASSERT-{a.type.upper()}", category=spec[0], severity=spec[1],
                         title=spec[2], facts=facts, laws=list(spec[3]), remedy=spec[4],
                         bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                         account_label=t.label, basis="assertion", assertion_id=a.id,
                         evidence_ids=[e.id for e in attached], disputable=ok, blocked_reason=reason if not ok else "")

    def _dispute_flag(self, a, lines, ok, attached, reason):
        disputed_on = parse_date(a.details.get("date_sent") or a.details.get("date_received"))
        for t in lines:
            reported = t.d("date_reported")
            if disputed_on and reported and reported > disputed_on + timedelta(days=30) \
                    and t.compliance_condition.upper() not in metro2.DISPUTE_FLAGS:
                laws = ["FCRA_623A3", "FCRA_607B"] + (["FDCPA_807_8"] if t.is_collection else [])
                self.add(rule="MISSING-XB", category="STATUS", severity="high",
                         title="Directly disputed account not marked as disputed",
                         facts=[a.statement, f"Dispute sent {_long(disputed_on)}.",
                                f"{t.bureau.title()} report dated {_long(reported)} shows compliance "
                                f"condition '{t.compliance_condition or 'blank'}', not XB (disputed)."],
                         laws=laws, remedy="Mark the account as disputed by the consumer",
                         bureaus=[t.bureau], account_key=t.account_key, furnisher=t.furnisher,
                         account_label=t.label, basis="assertion", assertion_id=a.id,
                         evidence_ids=[e.id for e in attached], disputable=ok,
                         blocked_reason=reason if not ok else "")


# assertion type -> (category, severity, title, laws, remedy)
ASSERTION_RULES = {
    "not_mine": ("IDENTITY", "critical", "Account doesn't belong to the consumer",
                 ("FCRA_607B", "FCRA_611A1", "FCRA_611A5A", "FCRA_623B"), "Delete the account"),
    "identity_theft": ("FRAUD", "critical", "Account resulted from identity theft",
                       ("FCRA_605B", "FCRA_623A6", "FCRA_611A5A"), "Block the account under § 605B"),
    "paid": ("BALANCE", "high", "Paid account reported with a balance or unpaid status",
             ("FCRA_607B", "FCRA_623A1", "FCRA_611A1", "FCRA_623B"), "Report as paid with a $0 balance"),
    "settled": ("BALANCE", "high", "Settled account still reported with a balance",
                ("FCRA_607B", "FCRA_623A1", "FCRA_611A1", "FCRA_623B"), "Report as settled with a $0 balance"),
    "never_late": ("PAYMENT_HISTORY", "high", "Late payments reported for months paid on time",
                   ("FCRA_607B", "FCRA_623A1", "FCRA_611A1", "FCRA_623B"), "Remove the late marks for the listed months"),
    "closed_by_consumer": ("STATUS", "low", "Account not shown as closed at consumer's request",
                           ("FCRA_607B", "FCRA_623A1"), "Report as closed at the consumer's request"),
    "included_in_bankruptcy": ("BANKRUPTCY", "high", "Discharged debt not reported as included in bankruptcy",
                               ("FCRA_607B", "FCRA_623A1", "FCRA_611A1", "FCRA_623B"),
                               "Report $0 balance, included in bankruptcy"),
    "wrong_dofd": ("REAGING", "critical", "Date of first delinquency is wrong",
                   ("FCRA_605C", "FCRA_623A5", "FCRA_607B", "FCRA_611A1"),
                   "Correct the DOFD (delete if that makes it obsolete)"),
    "wrong_balance": ("BALANCE", "medium", "Balance or credit limit is wrong",
                      ("FCRA_607B", "FCRA_623A1", "FCRA_611A1"), "Correct the balance/limit"),
    "authorized_user_only": ("IDENTITY", "medium", "Consumer was only an authorized user",
                             ("FCRA_607B", "FCRA_611A1"), "Report ECOA code 3 (authorized user) or remove"),
}


def run_audit(case):
    return Auditor(case).run()
