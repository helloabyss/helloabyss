"""Evidence requirements and validation.

Identity documents establish who is disputing (bureaus may otherwise treat a letter as
suspicious or ask for more). Supporting documents give a dispute its factual basis, which
is what keeps it out of the frivolous bucket under § 1681i(a)(3) and 12 C.F.R. § 1022.43(f).
"""

from datetime import timedelta

from .models import EVIDENCE_TYPES, norm_name, parse_date

# Proof of address older than this is flagged. Bureaus don't publish a fixed limit;
# 90 days is a conservative working rule.
ADDRESS_PROOF_MAX_AGE_DAYS = 90

IDENTITY_PACKAGE = ("government_id", "proof_of_address")

# For each assertion type: alternatives, any one of which satisfies the requirement.
# An empty tuple means the consumer's signed statement is the evidence (you can't
# document a negative such as "this account isn't mine").
REQUIRED_FOR_ASSERTION = {
    "not_mine": (),
    "identity_theft": ("ftc_identity_theft_report", "police_report"),
    "paid": ("payment_proof", "paid_in_full_letter", "account_statement"),
    "settled": ("paid_in_full_letter", "payment_proof"),
    "never_late": ("payment_proof", "account_statement"),
    "closed_by_consumer": ("closure_confirmation", "account_statement"),
    "included_in_bankruptcy": ("bankruptcy_discharge",),
    "wrong_dofd": ("account_statement", "payment_proof", "credit_report"),
    "wrong_balance": ("account_statement", "payment_proof", "paid_in_full_letter"),
    "authorized_user_only": ("account_statement", "other"),
    "not_my_inquiry": (),
    "disputed_directly": ("mail_receipt",),
    "personal_info_wrong": (),
}

# An identity theft report is a report filed with a law enforcement agency; the FTC's
# IdentityTheft.gov report qualifies, as does a police report (12 C.F.R. § 1022.3(i)).
ID_THEFT_REPORT = ("ftc_identity_theft_report", "police_report")

# Requirements by letter type. Each entry must be present; a tuple entry is satisfied
# by any one of its alternatives.
REQUIRED_FOR_LETTER = {
    "bureau_dispute": IDENTITY_PACKAGE,
    "furnisher_direct": IDENTITY_PACKAGE,
    "mov_request": ("government_id", "proof_of_address", "bureau_results"),
    "identity_theft_block": ("government_id", "proof_of_address", ID_THEFT_REPORT),
    "furnisher_identity_theft": ("government_id", ID_THEFT_REPORT),
    "debt_validation": (),
    "collector_dispute": (),
    "reinsertion_challenge": ("government_id", "proof_of_address"),
    "failure_to_respond": ("government_id", "proof_of_address", "mail_receipt"),
    "deletion_notification": ("government_id",),
}


def check_identity_document(ev, consumer, today):
    problems = []
    if ev.name_on_document and norm_name(ev.name_on_document) not in consumer.known_names():
        problems.append(f"{ev.id}: name on document ({ev.name_on_document}) doesn't match "
                        f"{consumer.full_name} or a listed alias")
    if ev.type == "government_id" and ev.expires_date and parse_date(ev.expires_date) < today:
        problems.append(f"{ev.id}: ID expired on {ev.expires_date}")
    if ev.type == "proof_of_address":
        if ev.issued_date and today - parse_date(ev.issued_date) > timedelta(days=ADDRESS_PROOF_MAX_AGE_DAYS):
            problems.append(f"{ev.id}: proof of address dated {ev.issued_date} is more than "
                            f"{ADDRESS_PROOF_MAX_AGE_DAYS} days old; use a recent bill or statement")
        if not ev.issued_date:
            problems.append(f"{ev.id}: proof of address has no issue date; bureaus expect a recent document")
        if ev.address_on_document:
            want = consumer.current_address.line1.lower().split()[0]
            if want not in ev.address_on_document.lower():
                problems.append(f"{ev.id}: address on document doesn't match current address "
                                f"{consumer.current_address.one_line()}")
    return problems


def evidence_report(case):
    """Return (missing_identity_types, document_problems)."""
    today = case.today
    have = {e.type for e in case.evidence}
    missing = [t for t in IDENTITY_PACKAGE if t not in have]
    problems = []
    for e in case.evidence:
        if e.type in ("government_id", "proof_of_address", "ssn_proof"):
            problems += check_identity_document(e, case.consumer, today)
    return missing, problems


def supporting_evidence(case, assertion):
    """Return (ok, attached_evidence, reason) for an assertion's supporting documents."""
    by_id = case.evidence_by_id()
    attached = [by_id[i] for i in assertion.evidence_ids if i in by_id]
    unknown = [i for i in assertion.evidence_ids if i not in by_id]
    if unknown:
        return False, attached, f"evidence id(s) not found in case file: {unknown}"
    needed = REQUIRED_FOR_ASSERTION[assertion.type]
    if not needed:
        return True, attached, "consumer's signed statement is the evidence"
    if any(e.type in needed for e in attached):
        return True, attached, ""
    opts = " or ".join(EVIDENCE_TYPES[t] for t in needed)
    return False, attached, f"needs supporting document: {opts}"


def letter_ready(case, letter_type):
    have = {e.type for e in case.evidence}
    missing = []
    for req in REQUIRED_FOR_LETTER[letter_type]:
        alts = req if isinstance(req, tuple) else (req,)
        if not have.intersection(alts):
            missing.append(" or ".join(alts))
    return missing
