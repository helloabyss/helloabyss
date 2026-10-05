"""Legal knowledge base.

Every finding and letter cites entries from LAWS by key. Each entry records what the
provision actually requires and, where the commonly repeated version is wrong, a
`correction` note. `verified` records how the entry was checked:

  "statute"   - checked against statutory text (govinfo / state code)
  "secondary" - checked against reputable secondary sources only
  "unverified"- from domain knowledge; confirm before relying on it
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Law:
    key: str
    cite: str
    short: str
    rule: str
    verified: str = "statute"
    correction: str = ""
    private_action: str = ""
    tags: tuple = field(default_factory=tuple)


_L = [
    # ---------------- FCRA: bureau duties ----------------
    Law("FCRA_607B", "15 U.S.C. § 1681e(b) (FCRA § 607(b))", "Maximum possible accuracy",
        "A consumer reporting agency preparing a report must follow reasonable procedures "
        "to assure maximum possible accuracy of the information about the consumer.",
        private_action="§§ 1681n (willful) / 1681o (negligent)"),
    Law("FCRA_611A1", "15 U.S.C. § 1681i(a)(1) (FCRA § 611(a)(1))", "30-day reinvestigation",
        "If a consumer disputes the completeness or accuracy of an item, the CRA must conduct a "
        "reasonable reinvestigation free of charge and record the status or delete the item "
        "within 30 days of receiving the dispute. Extendable by up to 15 days if the consumer "
        "supplies additional relevant information during the 30 days (§ 1681i(a)(1)(B)). "
        "For disputes following a free annual disclosure under § 1681j(a), the period is 45 days "
        "(§ 1681j(a)(3)).",
        correction="The 45-day period comes from § 1681j(a)(3), not § 1681i itself.",
        private_action="§§ 1681n / 1681o"),
    Law("FCRA_611A2", "15 U.S.C. § 1681i(a)(2)", "Notice to furnisher",
        "Within 5 business days of receiving a dispute the CRA must notify the furnisher and "
        "include all relevant information it received from the consumer.",
        tags=("eoscar",)),
    Law("FCRA_611A3", "15 U.S.C. § 1681i(a)(3)", "Frivolous / irrelevant disputes",
        "A CRA may decline to reinvestigate a dispute it reasonably determines is frivolous or "
        "irrelevant, including for lack of sufficient information to investigate. It must notify "
        "the consumer within 5 business days and say what information is needed. "
        "This system refuses to generate any dispute without a factual basis.",
        tags=("guardrail",)),
    Law("FCRA_611A4", "15 U.S.C. § 1681i(a)(4)", "Consider consumer information",
        "In the reinvestigation the CRA must review and consider all relevant information "
        "submitted by the consumer."),
    Law("FCRA_611A5A", "15 U.S.C. § 1681i(a)(5)(A)", "Delete or modify",
        "If disputed information is found inaccurate or incomplete or cannot be verified, the CRA "
        "must promptly delete or modify it and notify the furnisher."),
    Law("FCRA_611A5B", "15 U.S.C. § 1681i(a)(5)(B)", "Reinsertion",
        "Deleted information may not be reinserted unless the furnisher certifies it is complete "
        "and accurate, and the CRA must notify the consumer in writing within 5 business days of "
        "reinsertion, including the furnisher's name, address and phone if reasonably available.",
        correction="Reinsertion is governed by § 1681i(a)(5)(B), not § 1681i(d). Section 1681i(d) "
                   "concerns notifying prior report recipients of a deletion at the consumer's request."),
    Law("FCRA_611A6", "15 U.S.C. § 1681i(a)(6)", "Results notice",
        "The CRA must give the consumer written results within 5 business days of completing the "
        "reinvestigation, including notice that the consumer may request a description of the "
        "procedure used to determine accuracy, including the furnisher's business name, address "
        "and phone if reasonably available (§ 1681i(a)(6)(B)(iii))."),
    Law("FCRA_611A7", "15 U.S.C. § 1681i(a)(7)", "Method of verification",
        "On request, the CRA must provide the description of the reinvestigation procedure "
        "within 15 days of the request.", tags=("mov",)),
    Law("FCRA_611B", "15 U.S.C. § 1681i(b)-(c)", "Statement of dispute",
        "If a reinvestigation doesn't resolve the dispute, the consumer may file a brief statement, "
        "and later reports must note that the item is disputed."),
    Law("FCRA_611D", "15 U.S.C. § 1681i(d)", "Notice of deletion to recipients",
        "After a deletion or a statement of dispute, the CRA must, at the consumer's request, "
        "notify anyone named by the consumer who received a report in the last 2 years for "
        "employment purposes or 6 months for any other purpose."),
    # ---------------- FCRA: obsolescence ----------------
    Law("FCRA_605A", "15 U.S.C. § 1681c(a) (FCRA § 605(a))", "Obsolete information",
        "A CRA may not report bankruptcy cases more than 10 years old (from the date of entry of "
        "the order for relief); accounts placed for collection or charged off, and any other adverse "
        "item, more than 7 years old.",
        correction="The FCRA sets no 2-year limit for inquiries. Bureaus remove hard inquiries after "
                   "about 2 years as a matter of policy; § 1681b(c)(3) and § 1681g(a)(3) set related "
                   "1-year/2-year windows for disclosing who requested reports. An inquiry older than "
                   "2 years is a policy-deletion request, not a statutory violation."),
    Law("FCRA_605C", "15 U.S.C. § 1681c(c)", "When the 7-year clock starts",
        "For delinquent accounts placed for collection, charged off or subjected to similar action, "
        "the 7-year period starts after the 180-day period beginning on the commencement of the "
        "delinquency that immediately preceded the collection or charge-off. Practical rule: "
        "removal date = DOFD + 180 days + 7 years. A sale or transfer to a debt buyer does not "
        "restart the clock.", tags=("dofd",)),
    Law("FCRA_605B_EXEMPT", "15 U.S.C. § 1681c(b)", "Obsolescence exemptions",
        "The time limits don't apply to reports used for credit or life insurance of $150,000 or "
        "more, or employment at a salary of $75,000 or more."),
    Law("FCRA_605G", "15 U.S.C. § 1681c(g)", "Truncation (FACTA)",
        "Printed electronic card receipts may show no more than the last 5 digits of the card "
        "number and no expiration date.", tags=("facta",)),
    # ---------------- FCRA: disclosure, ID theft ----------------
    Law("FCRA_609", "15 U.S.C. § 1681g (FCRA § 609)", "File disclosure",
        "On request and proper identification, a CRA must disclose all information in the "
        "consumer's file, the sources of the information, and recipients of reports (1 year; "
        "2 years for employment). The consumer may request SSN truncation on the disclosure.",
        correction="§ 609 is a disclosure right. It does NOT require a bureau to produce the "
                   "original signed contract, and § 609 letters demanding that are not a basis for deletion."),
    Law("FCRA_605B", "15 U.S.C. § 1681c-2 (FCRA § 605B)", "Identity theft block",
        "A CRA must block information the consumer identifies as resulting from identity theft "
        "within 4 business days of receiving: (1) appropriate proof of identity, (2) a copy of an "
        "identity theft report, (3) identification of the information, and (4) a statement that "
        "it doesn't relate to any transaction by the consumer. It must notify the furnisher. "
        "The CRA may decline or rescind a block made in error or based on a material "
        "misrepresentation.", tags=("idtheft",)),
    Law("FCRA_605A_ALERT", "15 U.S.C. § 1681c-1", "Fraud alerts and security freezes",
        "Initial fraud alert lasts 1 year; extended alert 7 years (requires an identity theft "
        "report); active-duty alert 1 year. Security freezes are free (§ 1681c-1(i)). The bureau "
        "contacted must notify the other nationwide bureaus.",
        verified="secondary", tags=("facta",),
        correction="Initial alerts were 90 days before the 2018 Economic Growth, Regulatory Relief, "
                   "and Consumer Protection Act extended them to 1 year."),
    Law("FCRA_612", "15 U.S.C. § 1681j", "Free disclosures",
        "Free annual disclosure from each nationwide CRA. The three nationwide bureaus also offer "
        "free weekly online reports through AnnualCreditReport.com (voluntary practice).",
        verified="secondary"),
    Law("FCRA_615", "15 U.S.C. § 1681m", "Adverse action / risk-based pricing",
        "A user taking adverse action based on a report must give notice naming the CRA and the "
        "consumer's right to a free report within 60 days and to dispute. Risk-based pricing "
        "notices are required under § 1681m(h)."),
    # ---------------- FCRA: furnisher duties ----------------
    Law("FCRA_623A1", "15 U.S.C. § 1681s-2(a)(1)", "Duty not to furnish inaccurate info",
        "A furnisher may not report information it knows or has reasonable cause to believe is "
        "inaccurate.",
        private_action="None. § 1681s-2(c)-(d) bar private suits for § 1681s-2(a); enforcement is "
                       "by regulators. Use it in letters to put the furnisher on notice, not as a lawsuit basis."),
    Law("FCRA_623A3", "15 U.S.C. § 1681s-2(a)(3)", "Report the dispute",
        "If a consumer disputes information directly with a furnisher, the furnisher may not report "
        "it to any CRA without noting that it is disputed (Metro 2 compliance condition code XB).",
        private_action="None (see § 1681s-2(c)-(d))."),
    Law("FCRA_623A5", "15 U.S.C. § 1681s-2(a)(5)", "Report the date of delinquency",
        "A furnisher reporting a delinquent account placed for collection or charged off must report "
        "the month and year the delinquency began, within 90 days of reporting the action.",
        tags=("dofd",), private_action="None (see § 1681s-2(c)-(d))."),
    Law("FCRA_623A6", "15 U.S.C. § 1681s-2(a)(6)", "Identity theft notices to furnisher",
        "On receiving an identity theft report at its designated address, a furnisher may not "
        "furnish the information to a CRA unless it subsequently knows or is informed the "
        "information is correct.", tags=("idtheft",)),
    Law("FCRA_623A8", "15 U.S.C. § 1681s-2(a)(8); 12 C.F.R. § 1022.43 (Reg V)", "Direct disputes",
        "A furnisher must investigate a dispute sent directly to it at its designated address if the "
        "dispute identifies the account, states the specific information disputed and the basis, and "
        "includes supporting documentation (12 C.F.R. § 1022.43(d)). It must complete the "
        "investigation within the § 1681i(a)(1) time period and report results to the consumer. It may "
        "treat a dispute as frivolous under § 1022.43(f), including disputes from credit repair "
        "templates or substantially the same as a prior dispute without new information.",
        tags=("guardrail",)),
    Law("FCRA_623B", "15 U.S.C. § 1681s-2(b)", "Investigating bureau-forwarded disputes",
        "After notice of a dispute from a CRA (the ACDV), the furnisher must investigate, review all "
        "relevant information the CRA provided, report results to the CRA, and correct, delete or "
        "block information that is inaccurate, incomplete or cannot be verified.",
        private_action="Yes: §§ 1681n / 1681o, but only after the consumer disputed through a CRA.",
        tags=("eoscar",)),
    Law("FCRA_616_617", "15 U.S.C. §§ 1681n, 1681o, 1681p", "Remedies and limitations",
        "Willful noncompliance: actual or statutory damages $100-$1,000, punitive damages, fees. "
        "Negligent: actual damages and fees. Suit must be filed within 2 years of discovering the "
        "violation and no later than 5 years after it occurred."),
    # ---------------- FDCPA ----------------
    Law("FDCPA_809", "15 U.S.C. § 1692g; 12 C.F.R. § 1006.34 (Reg F)", "Debt validation",
        "A debt collector must send a validation notice. If the consumer disputes in writing within "
        "the 30-day validation period (Reg F defines its end date), the collector must stop "
        "collecting until it mails verification of the debt or the original creditor's name and "
        "address.",
        correction="Validation rights apply to third-party debt collectors under the FDCPA, not "
                   "original creditors, and are timely only within the validation period."),
    Law("FDCPA_807_8", "15 U.S.C. § 1692e(8)", "False credit information",
        "A debt collector may not communicate credit information it knows or should know is "
        "false, including failing to communicate that a disputed debt is disputed.",
        private_action="Yes: § 1692k (actual damages, up to $1,000 statutory, fees; 1-year limit)."),
    Law("FDCPA_1006_30", "12 C.F.R. § 1006.30(a) (Reg F)", "No passive collection",
        "A debt collector may not furnish information about a debt to a CRA before communicating "
        "with the consumer about the debt.", verified="secondary"),
    # ---------------- Policy rules (not statute) ----------------
    Law("POLICY_INQUIRY", "Nationwide CRA policy", "Inquiry retention",
        "Hard inquiries are typically displayed for 2 years. Not a statutory limit.",
        verified="secondary", tags=("policy",)),
    Law("POLICY_MEDICAL", "Nationwide CRA policy (2022-2023)", "Medical collections",
        "Equifax, Experian and TransUnion voluntarily stopped reporting paid medical collections, "
        "medical collections under $500, and medical collections less than one year old. The CFPB's "
        "January 2025 medical debt rule was vacated by the E.D. Tex. in July 2025 and is not in force.",
        verified="secondary", tags=("policy",)),
    Law("POLICY_EOSCAR", "CDIA e-OSCAR / Metro 2 (CRRG)", "Industry dispute pipeline",
        "Bureaus convert disputes into ACDVs carrying one or two dispute codes plus a short free-form "
        "line, and route them to furnishers through e-OSCAR. Supporting documents may be attached "
        "as images. Furnishers respond with a response code and corrected Metro 2 fields.",
        verified="secondary", tags=("eoscar",)),
]

LAWS = {law.key: law for law in _L}


def cite(*keys):
    """Return citation strings for law keys, failing loudly on unknown keys."""
    return [LAWS[k].cite for k in keys]
