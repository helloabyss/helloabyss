# Credit File Audit & Dispute Automation System (CFADS)

Audits a consumer's credit reports against the FCRA, FDCPA and bureau policy, then writes
the dispute letters the findings support. It checks the consumer's ID, proof of address
and other evidence first, and it refuses to write any dispute that has no factual basis.

> Educational tool, not legal advice. It prepares disputes from the facts and documents
> you supply. You are responsible for their accuracy.

Pure Python 3.10+ standard library. Optional: `pypdf` or `pdftotext` for reading PDFs.

## Hosted web app (for customers)

`webapp/` is a self-service website: customers create an account, enter their details, upload ID,
proof of address and supporting documents, enter what their reports show, explain what's wrong,
review the audit, sign the CROA rights statement and contract, and, after the 3-business-day
cancellation period, pay once and download their letters as PDFs. A tracker records mailing dates
and results, counts the legal deadlines, and adds follow-up letters to the download.

```bash
pip install -r requirements.txt
DEV_PAYMENTS=1 flask --app webapp.app run      # local test; payments are simulated
```

Production: copy `.env.example`, fill in real keys, and run the Docker image (`docker build -t cfads .`)
behind HTTPS on any host (Render, Fly.io, Railway, a VPS). Mount `/data` on a persistent, backed-up disk.

**How the app follows the Credit Repair Organizations Act**

| Requirement | Where |
|---|---|
| § 1679c(a) rights statement, verbatim, before any contract | `webapp/croa.py` `DISCLOSURE`; step 6 |
| § 1679c(b) given as a separate document | its own page and PDF, signed before the contract appears |
| § 1679c(c) signed copy kept 2 years | `acknowledgments` table; survives case deletion; purged after 2 years |
| § 1679d contract terms, price, services, cancellation statement | `croa.contract_text` |
| § 1679e 3-business-day cancellation and notice form | `croa.cancellation_notice`; Cancel button |
| § 1679b(b) no payment before services fully performed | payment opens only when letters are ready and the cancellation period has ended |
| § 1679b(a) no false claims | no result promises anywhere; accurate items are never disputed |

**Before taking real customers:** have a consumer-finance lawyer confirm the items in
`croa.VERIFY_BEFORE_LAUNCH`, register in any state that requires credit services organizations to
register or post a bond, and publish a privacy policy and terms of service.

**Security:** case data and documents are encrypted at rest (Fernet, `DATA_KEY`); passwords are hashed;
every form has a CSRF token; users can only reach their own cases; users can delete cases or their
whole account. Still to do before launch: login rate limiting, email verification, password reset,
and off-site encrypted backups.

## Command-line quick start

```bash
python3 -m cfads audit examples/sample_case.json        # findings, planned letters, deadlines
python3 -m cfads letters examples/sample_case.json --out letters/
python3 -m cfads track examples/sample_case.json        # what's overdue and what to send next
python3 -m cfads web                                     # local web app at http://127.0.0.1:8765
python3 -m cfads parse-pdf report.pdf --bureau experian  # DRAFT tradelines from a PDF
python3 -m cfads laws                                    # the legal knowledge base
python3 -m unittest discover -s tests -t .
```

## How a case flows

1. **Collect.** Pull all three reports (AnnualCreditReport.com). Gather a government ID,
   proof of address dated within the last 90 days, and documents for each claim: an FTC
   Identity Theft Report, payment proof, a discharge order, and so on.
2. **Build the case file** (`examples/sample_case.json` shows every field):
   `consumer`, `reports` (tradelines, inquiries, public records, personal info as each
   bureau shows them), `evidence`, `assertions` (your factual statements, each linked to
   evidence) and `disputes` (history, filled in as you go).
3. **Audit.** The rule engine runs; see the table below.
4. **Letters.** Bureau disputes, § 605B identity theft blocks, furnisher and collector
   letters. Each letter is marked READY, or lists the documents it still needs.
5. **Send** by certified mail with return receipt. Record `sent_date`, then
   `received_date` from the green card.
6. **Track.** `track` computes each deadline and, from the outcome you record
   (`deleted` / `modified` / `verified` / `frivolous`), writes the next letter:
   a method-of-verification request, a direct furnisher dispute, a failure-to-respond notice,
   or a reinsertion challenge.

## Audit rules

| Rule | Detects | Main citations |
|---|---|---|
| XB-FIELD-MISMATCH | Date opened, DOFD, limit, high credit or original creditor differs between bureaus | § 1681e(b), § 1681s-2(a)(1) |
| XB-BALANCE / XB-STATUS | Balance or derogatory status differs **in the same reporting month** | § 1681e(b) |
| OBSOLETE-7YR / OBSOLETE-BK | Past DOFD + 180 days + 7 years; bankruptcy past 10 years | § 1681c(a), (c) |
| REAGED-COLLECTION | Collector's DOFD is later than the original creditor's | § 1681c(c), § 1681s-2(a)(5), § 1692e(8) |
| REAGED-HISTORY | DOFD is later than the delinquency the payment history shows | § 1681c(c), § 1681s-2(a)(5) |
| DOFD-MISSING | Collection or charge-off with no DOFD | § 1681s-2(a)(5) |
| PAID-WITH-BALANCE, PASTDUE-GT-BALANCE, STATUS-HISTORY, TRANSFERRED-BALANCE | Contradictions inside one tradeline | § 1681e(b), § 1681s-2(a)(1) |
| DOUBLE-BALANCE | Original creditor and collector both report a balance | § 1681e(b) |
| MISSING-XB | Disputed directly, still not flagged XB 30+ days later | § 1681s-2(a)(3), § 1692e(8) |
| REINSERTED | Deleted item has reappeared | § 1681i(a)(5)(B) |
| PII-MISMATCH | Unknown SSN, DOB, names or addresses | § 1681e(b) |
| MEDICAL-POLICY, INQUIRY-AGED | Bureau-policy deletions (labelled as policy, not law) | — |
| ASSERT-* | Your stated facts: not mine, identity theft, paid, never late, bankruptcy, wrong DOFD… | varies |

## Guardrails against frivolous disputes (§ 1681i(a)(3), 12 C.F.R. § 1022.43(f))

- Every disputed item carries specific facts and at least one citation.
- Claims that depend on your statement need the matching document
  (`evidence.REQUIRED_FOR_ASSERTION`). "Not mine" and "not my inquiry" need only your
  signed statement, because a negative can't be documented.
- Signals the system can't confirm (pre-bankruptcy balances, unfamiliar name spellings)
  are shown for review and never disputed on their own.
- An item a recipient already **verified** is not sent to that recipient again unless
  new evidence is attached. The tracker escalates instead.
- Letters are written from your facts, not boilerplate. Reg V lets furnishers ignore
  template disputes from credit repair organisations.

## Where the brief was wrong, and what the code does instead

| Brief said | Law actually says | Code |
|---|---|---|
| Reinsertion is § 1681i(d) | § 1681i(a)(5)(B). Subsection (d) covers notices to past report recipients | `FCRA_611A5B`, `FCRA_611D` |
| Inquiries: 2-year statutory limit | No FCRA limit. The 2 years is bureau policy | `INQUIRY-AGED` is labelled policy |
| 45 days with a free annual report is in § 1681i | It comes from § 1681j(a)(3) | `pipeline.deadline` |
| 7 years from DOFD | DOFD + 180 days + 7 years (§ 1681c(c)) | `obsolescence_date` |
| Furnisher duties in § 1681s-2(a) can be sued on | No private action for (a) (§ 1681s-2(c)-(d)); only (b), after a **bureau** dispute | Noted in the KB and the tracker |
| § 609 letters force deletion | § 609 gives a right to disclosure, not to the original contract | KB correction |

## Verification status (be honest about it)

- **Statutes:** FCRA and FDCPA sections are cited from the U.S. Code. § 1681c(c) and the
  CA CCRAA were re-checked against the code text and case law for this build.
- **e-OSCAR dispute codes:** CDIA publishes them only to members. The numbers in
  `metro2.DISPUTE_CATEGORIES` (001, 002, 006, 008, 010, 012, 019, 024, 031, 103, 104) come
  from secondary sources and are marked that way. **The engine's logic uses categories
  only**, so a wrong code number can't change which disputes get raised. Confirm the
  numbers against the current CDIA list before showing them to anyone.
- **Metro 2 / CRRG:** XB (disputed) and XH (dispute resolved) were confirmed from
  secondary sources. The other compliance-condition, status and field codes are marked
  `unverified` until checked against a licensed CRRG.
- **Bureau addresses:** Equifax, Experian and TransUnion were checked in October 2026.
  Sources disagreed on the Innovis P.O. box, so its letter carries a "confirm before
  mailing" placeholder.
- **Medical debt:** the CFPB's 2025 medical debt rule was vacated (E.D. Tex., July 2025).
  Only the bureaus' voluntary policy is encoded.

## State law

`cfads/states.py` currently encodes **California** only (CCRAA § 1785.25(a), which
carries a private right of action, and the Rosenthal Act). The brief's `[USER STATE]` was
never filled in. Add your state with verified citations before relying on state claims.

## If you offer this to other people

If you charge people to dispute their credit, the **Credit Repair Organizations Act**
(15 U.S.C. § 1679 et seq.) applies: no fees before the service is fully performed, a
written contract, a 3-day right to cancel, and required disclosures. Many states also
require registration or a bond. A free, self-service tool used by consumers themselves
avoids most of this; a paid service needs a lawyer's review first.

## Privacy

Case files hold DOBs, partial SSNs and ID scans. `.gitignore` excludes `cases/`,
`letters/` and `*.private.json`. Never commit real case files. The web app binds to
127.0.0.1 and writes nothing to disk.

## Layout

```
cfads/law.py       legal knowledge base, with verification status and corrections
cfads/metro2.py    Metro 2 status, payment history, CCC and ECOA codes; dispute categories
cfads/models.py    case-file schema (consumer, reports, evidence, assertions, disputes)
cfads/evidence.py  ID / address checks and evidence required for each claim and letter
cfads/audit.py     rule engine
cfads/letters.py   letter planning (guardrails) and rendering
cfads/pipeline.py  deadlines (business days, federal holidays) and escalation loop
cfads/states.py    state-law modules
cfads/ingest.py    JSON loading and draft PDF parsing
cfads/web.py       minimal local web app (no accounts)
webapp/            hosted customer app (Flask): accounts, intake, CROA flow, Stripe, PDFs, tracker
```
