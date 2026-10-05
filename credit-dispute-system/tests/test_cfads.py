import copy
import json
import os
import unittest
from datetime import date

from cfads.audit import obsolescence_date, run_audit
from cfads.letters import plan_letters, render
from cfads.models import CaseFile, infer_status_code
from cfads.pipeline import add_business_days, deadline, next_actions

HERE = os.path.dirname(__file__)
with open(os.path.join(HERE, "..", "examples", "sample_case.json")) as fh:
    SAMPLE = json.load(fh)


def case(mutate=None):
    d = copy.deepcopy(SAMPLE)
    if mutate:
        mutate(d)
    return CaseFile.from_dict(d)


def rules(findings):
    return {f.rule for f in findings}


class LawMath(unittest.TestCase):
    def test_obsolescence_is_dofd_plus_180_days_plus_7_years(self):
        self.assertEqual(obsolescence_date(date(2018, 9, 1)), date(2026, 2, 28))

    def test_business_days_skip_weekends_and_holidays(self):
        # Thu 2026-12-24 + 4 business days skips Christmas (Fri) and the weekend.
        self.assertEqual(add_business_days(date(2026, 12, 24), 4), date(2026, 12, 31))

    def test_reinvestigation_deadlines(self):
        self.assertEqual(deadline({"letter_type": "bureau_dispute", "received_date": "2026-08-20"})[0], date(2026, 9, 19))
        self.assertEqual(deadline({"letter_type": "bureau_dispute", "received_date": "2026-08-20",
                                   "after_free_annual_disclosure": True})[0], date(2026, 10, 4))
        self.assertEqual(deadline({"letter_type": "mov_request", "received_date": "2026-08-20"})[0], date(2026, 9, 4))

    def test_status_inference(self):
        self.assertEqual(infer_status_code("Paid charge-off"), "64")
        self.assertEqual(infer_status_code("Charged off"), "97")
        self.assertEqual(infer_status_code("Pays as agreed"), "11")


class Audit(unittest.TestCase):
    def setUp(self):
        self.f = run_audit(case())

    def test_expected_rules_fire(self):
        for r in ("OBSOLETE-7YR", "REAGED-COLLECTION", "REAGED-HISTORY", "XB-FIELD-MISMATCH", "XB-BALANCE",
                  "PAID-WITH-BALANCE", "DOUBLE-BALANCE", "MISSING-XB", "MEDICAL-POLICY", "INQUIRY-AGED",
                  "PII-MISMATCH", "ASSERT-IDENTITY_THEFT", "ASSERT-INQUIRY"):
            self.assertIn(r, rules(self.f), r)

    def test_every_disputable_finding_has_facts_and_law(self):
        for f in self.f:
            if f.disputable:
                self.assertTrue(f.facts and f.laws, f.id)

    def test_balance_mismatch_only_compared_within_same_month(self):
        def m(d):
            d["reports"][1]["tradelines"][0]["date_reported"] = "2026-07"
        self.assertNotIn("XB-BALANCE", rules(run_audit(case(m))))

    def test_collection_not_flagged_when_dofd_matches_original_creditor(self):
        def m(d):
            for r in d["reports"]:
                for t in r["tradelines"]:
                    if t["furnisher"].startswith("Midland"):
                        t["date_of_first_delinquency"] = "2018-11"
        self.assertNotIn("REAGED-COLLECTION", rules(run_audit(case(m))))


class Guardrails(unittest.TestCase):
    def test_assertion_without_evidence_is_not_disputed(self):
        f = next(x for x in run_audit(case()) if x.rule == "ASSERT-NEVER_LATE")
        self.assertFalse(f.disputable)
        letters, blocked = plan_letters(case(), run_audit(case()))
        self.assertIn(f.title, [b[0].title for b in blocked])
        self.assertFalse(any(f.title == g.title for L in letters for g in L.findings))

    def test_repeat_dispute_after_verified_is_blocked_for_that_bureau_only(self):
        c = case()
        letters, blocked = plan_letters(c, run_audit(c))
        eq = next(L for L in letters if L.letter_type == "bureau_dispute" and L.target == "equifax")
        ex = next(L for L in letters if L.letter_type == "bureau_dispute" and L.target == "experian")
        self.assertFalse(any(f.account_key == "capone-1234" for f in eq.findings))
        self.assertTrue(any(f.account_key == "capone-1234" for f in ex.findings))

    def test_new_evidence_lifts_repeat_block(self):
        def m(d):
            d["evidence"].append({"id": "E9", "type": "account_statement", "description": "Capital One statement Sept 2026"})
            d["assertions"].append({"id": "A9", "type": "wrong_balance", "account_key": "capone-1234",
                                    "bureaus": ["equifax"], "evidence_ids": ["E9"],
                                    "statement": "My September 2026 statement shows a balance of $1,200 and limit of $2,500."})
        c = case(m)
        letters, _ = plan_letters(c, run_audit(c))
        eq = next(L for L in letters if L.letter_type == "bureau_dispute" and L.target == "equifax")
        self.assertTrue(any(f.assertion_id == "A9" for f in eq.findings))

    def test_identity_theft_block_requires_report(self):
        def m(d):
            d["evidence"] = [e for e in d["evidence"] if e["type"] != "ftc_identity_theft_report"]
            d["assertions"][0]["evidence_ids"] = []
        c = case(m)
        theft = next(f for f in run_audit(c) if f.rule == "ASSERT-IDENTITY_THEFT")
        self.assertFalse(theft.disputable)

    def test_missing_identity_documents_mark_letters_not_ready(self):
        c = case(lambda d: d.update(evidence=[e for e in d["evidence"] if e["type"] != "proof_of_address"]))
        letters, _ = plan_letters(c, run_audit(c))
        self.assertFalse(next(L for L in letters if L.letter_type == "bureau_dispute").ready)

    def test_bad_input_rejected(self):
        with self.assertRaises(ValueError):
            case(lambda d: d["assertions"].append({"id": "X", "type": "not_mine", "statement": "no"}))
        with self.assertRaises(ValueError):
            case(lambda d: d["evidence"].append({"id": "X", "type": "selfie", "description": "x"}))


class Letters(unittest.TestCase):
    def test_letters_render_with_citations_and_no_full_ssn(self):
        c = case()
        letters, _ = plan_letters(c, run_audit(c))
        kinds = {L.letter_type for L in letters}
        self.assertTrue({"bureau_dispute", "identity_theft_block", "mov_request", "failure_to_respond",
                         "collector_dispute", "furnisher_identity_theft"} <= kinds)
        for L in letters:
            text = render(c, L)
            self.assertIn("XXX-XX-4321", text)
            self.assertIn("U.S.C.", text)

    def test_tracker_flags_overdue_dispute(self):
        msgs = " ".join(m for _, m in next_actions(case()))
        self.assertIn("OVERDUE", msgs)
        self.assertIn("VERIFIED", msgs)


if __name__ == "__main__":
    unittest.main()


class PdfText(unittest.TestCase):
    def test_parse_report_text_drafts_tradelines(self):
        from cfads.ingest import parse_report_text
        text = ("Account Name: MIDLAND CREDIT MGMT\nAccount Number: 7788XXXX\nOriginal Creditor: SYNCHRONY BANK\n"
                "Date Opened: 09/2019\nBalance: $2,450\nStatus: Collection account\n"
                "Account Name: CAPITAL ONE\nAccount Number: XXXX1234\nBalance: $1,200\nStatus: Pays as agreed\n")
        r = parse_report_text(text, "experian")
        self.assertEqual(len(r["tradelines"]), 2)
        self.assertTrue(r["tradelines"][0]["is_collection"])
        self.assertEqual(r["tradelines"][0]["date_opened"], "2019-09")
