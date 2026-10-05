"""Case-file data model. A case file is one JSON document holding the consumer, their
reports, their evidence, their factual assertions and the dispute history."""

import re
from dataclasses import dataclass, field, fields, asdict
from datetime import date

BUREAUS = ("equifax", "experian", "transunion", "innovis")

EVIDENCE_TYPES = {
    "government_id": "Government-issued photo ID (driver's license, state ID, passport)",
    "ssn_proof": "Proof of SSN (SSA card, W-2, SSA-1099)",
    "proof_of_address": "Proof of current address (utility bill, bank or insurance statement, lease)",
    "ftc_identity_theft_report": "FTC Identity Theft Report from IdentityTheft.gov",
    "police_report": "Police report",
    "payment_proof": "Proof of payment (bank statement, cancelled check, receipt)",
    "paid_in_full_letter": "Paid-in-full or settlement letter from creditor/collector",
    "account_statement": "Account statement from the creditor",
    "bankruptcy_discharge": "Bankruptcy discharge order and schedules",
    "closure_confirmation": "Confirmation the consumer closed the account",
    "validation_notice": "Debt collector's validation notice",
    "bureau_results": "Bureau reinvestigation results letter",
    "mail_receipt": "Certified mail receipt / return receipt",
    "credit_report": "Copy of the credit report page showing the item",
    "other": "Other supporting document",
}


def parse_date(v):
    if v in (None, ""):
        return None
    if isinstance(v, date):
        return v
    s = str(v).strip()
    for pat, fmt in ((r"^\d{4}-\d{2}-\d{2}$", "ymd"), (r"^\d{4}-\d{2}$", "ym"),
                     (r"^\d{1,2}/\d{1,2}/\d{4}$", "mdy"), (r"^\d{1,2}/\d{4}$", "my")):
        if re.match(pat, s):
            p = re.split(r"[-/]", s)
            if fmt == "ymd":
                return date(int(p[0]), int(p[1]), int(p[2]))
            if fmt == "ym":
                return date(int(p[0]), int(p[1]), 1)
            if fmt == "mdy":
                return date(int(p[2]), int(p[0]), int(p[1]))
            return date(int(p[1]), int(p[0]), 1)
    raise ValueError(f"Unrecognised date: {v!r} (use YYYY-MM-DD, YYYY-MM, MM/DD/YYYY or MM/YYYY)")


def money(v):
    if v in (None, ""):
        return None
    return float(str(v).replace("$", "").replace(",", ""))


def _build(cls, data):
    names = {f.name for f in fields(cls)}
    unknown = set(data) - names
    if unknown:
        raise ValueError(f"{cls.__name__}: unknown field(s) {sorted(unknown)}")
    return cls(**data)


@dataclass
class Address:
    line1: str
    city: str
    state: str
    zip: str
    line2: str = ""

    def one_line(self):
        l2 = f" {self.line2}" if self.line2 else ""
        return f"{self.line1}{l2}, {self.city}, {self.state} {self.zip}"

    def norm(self):
        return re.sub(r"[^a-z0-9]", "", f"{self.line1}{self.zip[:5]}".lower())


@dataclass
class Consumer:
    full_name: str
    date_of_birth: str
    ssn_last4: str
    current_address: Address
    prior_addresses: list = field(default_factory=list)
    aliases: list = field(default_factory=list)
    phone: str = ""
    email: str = ""

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        d["current_address"] = Address(**d["current_address"])
        d["prior_addresses"] = [Address(**a) for a in d.get("prior_addresses", [])]
        return _build(cls, d)

    @property
    def state(self):
        return self.current_address.state.upper()

    def known_names(self):
        return {norm_name(n) for n in [self.full_name, *self.aliases]}

    def known_addresses(self):
        return {a.norm() for a in [self.current_address, *self.prior_addresses]}


def norm_name(n):
    return re.sub(r"[^a-z ]", "", n.lower()).strip()


def norm_furnisher(n):
    n = re.sub(r"[^a-z0-9 ]", " ", (n or "").lower())
    n = re.sub(r"\b(llc|inc|na|n a|bank|corp|co|the|financial|services|svcs)\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()


@dataclass
class Evidence:
    id: str
    type: str
    description: str
    file: str = ""
    issued_date: str = ""
    expires_date: str = ""
    name_on_document: str = ""
    address_on_document: str = ""
    related_accounts: list = field(default_factory=list)

    def __post_init__(self):
        if self.type not in EVIDENCE_TYPES:
            raise ValueError(f"Evidence {self.id}: unknown type {self.type!r}")


_STATUS_WORDS = [
    (r"paid.*charge.?off|charge.?off.*paid", "64"), (r"paid.*collection|collection.*paid", "62"),
    (r"charge.?off|charged off", "97"), (r"collection", "93"), (r"repossess", "96"),
    (r"foreclos", "94"), (r"surrender", "95"), (r"transferr|sold", "05"),
    (r"180", "84"), (r"150", "83"), (r"120", "82"), (r"\b90\b", "80"), (r"\b60\b", "78"),
    (r"\b30\b", "71"), (r"paid|closed|zero balance", "13"),
    (r"current|as agreed|never late|open", "11"),
]


def infer_status_code(text):
    """Best-effort Metro 2 status from a bureau's plain-English status. Returns '' if unsure."""
    t = text.lower()
    for pat, code in _STATUS_WORDS:
        if re.search(pat, t):
            return code
    return ""


@dataclass
class Tradeline:
    bureau: str
    furnisher: str
    account_number: str
    account_type: str = ""
    account_key: str = ""
    ecoa: str = "1"
    date_opened: str = ""
    date_closed: str = ""
    date_of_first_delinquency: str = ""
    date_last_payment: str = ""
    date_last_activity: str = ""
    date_reported: str = ""
    status_code: str = ""
    status_text: str = ""
    balance: float = None
    credit_limit: float = None
    high_credit: float = None
    past_due: float = None
    original_creditor: str = ""
    is_collection: bool = False
    is_medical: bool = False
    payment_history: str = ""
    payment_history_start: str = ""
    compliance_condition: str = ""
    remarks: str = ""

    def __post_init__(self):
        self.bureau = self.bureau.lower()
        for f in ("balance", "credit_limit", "high_credit", "past_due"):
            setattr(self, f, money(getattr(self, f)))
        if not self.account_key:
            self.account_key = self.derive_key()
        if not self.status_code and self.status_text:
            self.status_code = infer_status_code(self.status_text)

    def derive_key(self):
        digits = re.sub(r"\D", "", self.account_number)[-4:]
        opened = (self.date_opened or "")[:7]
        return f"{norm_furnisher(self.furnisher)}|{digits}|{opened}"

    @property
    def label(self):
        return f"{self.furnisher} #{self.account_number}"

    def d(self, name):
        return parse_date(getattr(self, name))


@dataclass
class Inquiry:
    bureau: str
    creditor: str
    date: str
    kind: str = "hard"


@dataclass
class PublicRecord:
    bureau: str
    type: str
    filed_date: str
    chapter: str = ""
    discharged_date: str = ""
    court: str = ""
    case_number: str = ""


@dataclass
class BureauReport:
    bureau: str
    report_date: str
    names: list = field(default_factory=list)
    addresses: list = field(default_factory=list)
    ssn_variations: list = field(default_factory=list)
    dates_of_birth: list = field(default_factory=list)
    employers: list = field(default_factory=list)
    tradelines: list = field(default_factory=list)
    inquiries: list = field(default_factory=list)
    public_records: list = field(default_factory=list)
    from_free_annual_disclosure: bool = False

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        b = d["bureau"].lower()
        if b not in BUREAUS:
            raise ValueError(f"Unknown bureau {b!r}")
        d["bureau"] = b
        d["addresses"] = [Address(**a) if isinstance(a, dict) else a for a in d.get("addresses", [])]
        d["tradelines"] = [_build(Tradeline, {"bureau": b, **t}) for t in d.get("tradelines", [])]
        d["inquiries"] = [_build(Inquiry, {"bureau": b, **i}) for i in d.get("inquiries", [])]
        d["public_records"] = [_build(PublicRecord, {"bureau": b, **p}) for p in d.get("public_records", [])]
        return _build(cls, d)


ASSERTION_TYPES = {
    "not_mine": "The account is not mine and I never authorized it (mixed file or unknown)",
    "identity_theft": "The account resulted from identity theft",
    "paid": "I paid this account (date/amount stated)",
    "settled": "I settled this account for less than the full balance",
    "never_late": "I was not late in the months stated",
    "closed_by_consumer": "I closed this account",
    "included_in_bankruptcy": "This debt was included in my bankruptcy",
    "wrong_dofd": "The date of first delinquency is wrong (actual date stated)",
    "wrong_balance": "The balance or limit is wrong (correct figure stated)",
    "authorized_user_only": "I was only an authorized user",
    "not_my_inquiry": "I did not apply for credit with this creditor",
    "disputed_directly": "I already disputed this directly with the furnisher/collector",
    "personal_info_wrong": "This name/address/SSN/DOB is not mine",
}


@dataclass
class Assertion:
    """A factual statement by the consumer about an item. Disputes built on assertions
    require the evidence listed in evidence.REQUIRED_FOR_ASSERTION."""
    id: str
    type: str
    statement: str
    account_key: str = ""
    furnisher: str = ""
    bureaus: list = field(default_factory=list)
    evidence_ids: list = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.type not in ASSERTION_TYPES:
            raise ValueError(f"Assertion {self.id}: unknown type {self.type!r}")
        if len(self.statement.strip()) < 15:
            raise ValueError(f"Assertion {self.id}: statement must describe the specific facts")


@dataclass
class CaseFile:
    consumer: Consumer
    reports: list
    evidence: list = field(default_factory=list)
    assertions: list = field(default_factory=list)
    disputes: list = field(default_factory=list)
    furnisher_addresses: dict = field(default_factory=dict)
    as_of: str = ""

    @classmethod
    def from_dict(cls, d):
        return cls(
            consumer=Consumer.from_dict(d["consumer"]),
            reports=[BureauReport.from_dict(r) for r in d.get("reports", [])],
            evidence=[_build(Evidence, e) for e in d.get("evidence", [])],
            assertions=[_build(Assertion, a) for a in d.get("assertions", [])],
            disputes=list(d.get("disputes", [])),
            furnisher_addresses=dict(d.get("furnisher_addresses", {})),
            as_of=d.get("as_of", ""),
        )

    def to_dict(self):
        return asdict(self)

    @property
    def today(self):
        return parse_date(self.as_of) or date.today()

    def tradelines(self):
        return [t for r in self.reports for t in r.tradelines]

    def evidence_by_id(self):
        return {e.id: e for e in self.evidence}

    def report_for(self, bureau):
        return next((r for r in self.reports if r.bureau == bureau), None)
