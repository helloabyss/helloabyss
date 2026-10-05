import io
import re
import tempfile
import unittest
import zipfile

from cryptography.fernet import Fernet

from webapp import croa
from webapp.app import create_app


class WebFlow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db")
        self.app = create_app({"TESTING": True, "DATABASE": self.tmp.name, "SECRET_KEY": "t",
                               "DATA_KEY": Fernet.generate_key().decode(), "DEV_PAYMENTS": True,
                               "PRICE_CENTS": 4900})
        self.c = self.app.test_client()

    def csrf(self, path):
        html = self.c.get(path).get_data(as_text=True)
        return re.search(r'name="csrf" value="([^"]+)"', html).group(1)

    def post(self, path, data, files=None, page=None):
        data = dict(data, csrf=self.csrf(page or path))
        if files:
            data.update(files)
        return self.c.post(path, data=data, content_type="multipart/form-data" if files else None,
                           follow_redirects=True)

    def register(self, email="a@example.com", verify=True):
        r = self.post("/register", {"email": email, "password": "correct horse battery"})
        if verify:
            self.follow_mail(email, "/verify/")
        return r

    def follow_mail(self, to, path_part, visit=True):
        msg = [m for m in self.app.config.get("OUTBOX", []) if m["to"] == to][-1]
        url = re.search(r"https?://\S+", msg["body"]).group(0)
        path = "/" + url.split("://", 1)[1].split("/", 1)[1]
        self.assertIn(path_part, path)
        if visit:
            self.c.get(path)
        return path

    def new_case(self):
        self.post("/case/new", {"title": "Test"}, page="/dashboard")
        return 1

    def fill_case(self, cid):
        self.post(f"/case/{cid}/about", {"full_name": "Jordan A. Rivera", "aliases": "Jordan Rivera",
                                         "date_of_birth": "1988-04-17", "ssn_last4": "4321", "line1": "123 Example St",
                                         "city": "Sacramento", "state": "CA", "zip": "95814", "prior": ""})
        for typ, desc, extra in (("government_id", "CA driver license", {"expires_date": "2030-01-01"}),
                                 ("proof_of_address", "Electric bill", {"issued_date": __import__("datetime").date.today().isoformat()}),
                                 ("payment_proof", "Bank statement showing payoff", {})):
            r = self.post(f"/case/{cid}/documents", {"type": typ, "description": desc, **extra},
                          files={"file": (io.BytesIO(b"%PDF-1.4 test"), "doc.pdf")})
            self.assertIn("Document added", r.get_data(as_text=True))
        for b, bal in (("equifax", "1200"), ("experian", "1850")):
            self.post(f"/case/{cid}/reports", {"kind": "account", "bureau": b, "nickname": "capone", "furnisher": "Capital One",
                                               "account_number": "XXXX1234", "status_text": "Pays as agreed",
                                               "date_opened": "2017-06", "date_reported": "2026-09", "balance": bal})
        self.post(f"/case/{cid}/reports", {"kind": "account", "bureau": "equifax", "nickname": "westlake",
                                           "furnisher": "Westlake Financial", "account_number": "5501XXXX",
                                           "status_text": "Paid, closed", "date_reported": "2026-09", "balance": "450"})
        r = self.post(f"/case/{cid}/statements", {"type__westlake": "paid",
                                                  "statement__westlake": "I paid this loan in full on March 14, 2026.",
                                                  "evidence__westlake": "D3"})
        return r

    def test_full_flow_to_paid_download(self):
        self.register()
        cid = self.new_case()
        r = self.fill_case(cid)
        page = r.get_data(as_text=True)
        self.assertIn("Different balances reported", page)
        self.assertIn("Continue to agreement", page)
        # Payment is not possible before signing.
        r = self.post(f"/case/{cid}/checkout", {}, page=f"/case/{cid}")
        self.assertIn("Payment opens after", r.get_data(as_text=True))
        r = self.post(f"/case/{cid}/disclosure", {"ack": "1", "signature": "Jordan A. Rivera"})
        self.assertIn("SERVICE AGREEMENT", r.get_data(as_text=True))
        r = self.post(f"/case/{cid}/agreement", {"agree": "1", "signature": "Jordan A. Rivera"})
        self.assertIn("Signed", r.get_data(as_text=True))
        # Still inside the 3-business-day window: cannot pay.
        r = self.post(f"/case/{cid}/checkout", {}, page=f"/case/{cid}")
        self.assertIn("Payment opens after", r.get_data(as_text=True))
        self.assertEqual(self.c.get(f"/case/{cid}/letters.zip").status_code, 402)
        with self.app.app_context():
            from webapp import store
            store.db().execute("UPDATE agreements SET cancel_deadline='2000-01-01T00:00:00'")
            store.db().commit()
            ack = store.db().execute("SELECT * FROM acknowledgments").fetchone()
            self.assertEqual(ack["disclosure_sha256"], croa.DISCLOSURE_SHA256)
        self.post(f"/case/{cid}/checkout", {}, page=f"/case/{cid}")
        z = zipfile.ZipFile(io.BytesIO(self.c.get(f"/case/{cid}/letters.zip").data))
        names = z.namelist()
        self.assertIn("00-how-to-send.pdf", names)
        self.assertTrue(any("bureau-dispute-equifax" in n for n in names))
        self.assertTrue(z.read(names[0]).startswith(b"%PDF"))

    def test_cancel_within_window(self):
        self.register()
        cid = self.new_case()
        self.fill_case(cid)
        self.post(f"/case/{cid}/disclosure", {"ack": "1", "signature": "Jordan A. Rivera"})
        self.post(f"/case/{cid}/agreement", {"agree": "1", "signature": "Jordan A. Rivera"})
        r = self.post(f"/case/{cid}/cancel", {}, page=f"/case/{cid}")
        self.assertIn("cancelled", r.get_data(as_text=True))

    def test_agreement_requires_disclosure_first(self):
        self.register()
        cid = self.new_case()
        self.fill_case(cid)
        r = self.c.get(f"/case/{cid}/agreement")
        self.assertIn("/disclosure", r.headers["Location"])

    def test_other_users_cannot_see_case(self):
        self.register("a@example.com")
        cid = self.new_case()
        self.fill_case(cid)
        self.post("/logout", {}, page="/dashboard")
        self.register("b@example.com")
        self.assertEqual(self.c.get(f"/case/{cid}").status_code, 404)
        self.assertEqual(self.c.get(f"/case/{cid}/documents/1").status_code, 404)

    def test_csrf_required(self):
        self.register()
        self.assertEqual(self.c.post("/case/new", data={"title": "x"}).status_code, 400)

    def test_documents_encrypted_at_rest(self):
        self.register()
        cid = self.new_case()
        self.fill_case(cid)
        with self.app.app_context():
            from webapp import store
            blob = store.db().execute("SELECT blob FROM documents LIMIT 1").fetchone()["blob"]
            data = store.db().execute("SELECT data FROM cases").fetchone()["data"]
        self.assertNotIn(b"%PDF", blob)
        self.assertNotIn(b"Rivera", data)

    def test_unverified_email_cannot_sign(self):
        self.register(verify=False)
        cid = self.new_case()
        self.fill_case(cid)
        r = self.c.get(f"/case/{cid}/disclosure", follow_redirects=True)
        self.assertIn("Confirm your email", r.get_data(as_text=True))

    def test_login_throttled_after_repeated_failures(self):
        self.register()
        self.post("/logout", {}, page="/dashboard")
        for _ in range(5):
            self.post("/login", {"email": "a@example.com", "password": "wrong password"})
        r = self.post("/login", {"email": "a@example.com", "password": "correct horse battery"})
        self.assertIn("Too many attempts", r.get_data(as_text=True))

    def test_password_reset_is_single_use(self):
        self.register()
        self.post("/logout", {}, page="/dashboard")
        self.post("/forgot", {"email": "a@example.com"})
        path = self.follow_mail("a@example.com", "/reset/", visit=False)
        r = self.post(path, {"password": "a brand new password"})
        self.assertIn("Password changed", r.get_data(as_text=True))
        r = self.c.get(path, follow_redirects=True)
        self.assertIn("invalid, expired or already used", r.get_data(as_text=True))
        r = self.post("/login", {"email": "a@example.com", "password": "a brand new password"})
        self.assertIn("My cases", r.get_data(as_text=True))

    def test_disclosure_is_statutory_text(self):
        self.assertTrue(croa.DISCLOSURE.startswith("Consumer Credit File Rights Under State and Federal Law"))
        self.assertIn("within 3 business days from the date you signed it", croa.DISCLOSURE)
        self.assertTrue(croa.DISCLOSURE.rstrip().endswith("Washington, D.C. 20580"))


if __name__ == "__main__":
    unittest.main()


class FirmFlow(WebFlow):
    """Professional tier: firm staff build the case; the client signs through a private link."""

    def register_firm(self, email="pro@firm.com"):
        r = self.post("/pro/register", {"firm": "Rivera Law PLLC", "address": "100 Main St, Suite 2, Austin, TX 78701",
                                        "email": email, "password": "correct horse battery"})
        self.follow_mail(email, "/verify/")
        return r

    def firm_case(self):
        self.register_firm()
        self.post("/pro/case/new", {"client_name": "Jordan A. Rivera", "client_email": "client@example.com",
                                    "client_price": "300"}, page="/pro/dashboard")
        cid = 1
        self.fill_case(cid)
        return cid

    def test_full_firm_flow(self):
        cid = self.firm_case()
        # Staff can't sign for the client.
        self.assertIn("/signing", self.c.get(f"/case/{cid}/disclosure").headers["Location"])
        self.post(f"/pro/case/{cid}/signing", {})
        path = self.follow_mail("client@example.com", "/sign/", visit=False)
        client = self.app.test_client()
        page = client.get(path).get_data(as_text=True)
        self.assertIn("Consumer Credit File Rights", page)
        tok = re.search(r'name="csrf" value="([^"]+)"', page).group(1)
        client.post(path, data={"csrf": tok, "step": "ack", "ack": "1", "signature": "Jordan A. Rivera"})
        page = client.get(path).get_data(as_text=True)
        self.assertIn("Rivera Law PLLC", page)
        self.assertIn("$300.00", page)
        client.post(path, data={"csrf": tok, "step": "agree", "agree": "1", "signature": "Jordan A. Rivera"})
        self.assertIn("You can cancel without penalty", client.get(path).get_data(as_text=True))
        # Signed, but no subscription and still in the window: nothing released.
        self.assertEqual(self.c.get(f"/case/{cid}/letters.zip").status_code, 402)
        self.post("/pro/subscribe", {}, page="/pro/dashboard")
        self.assertEqual(self.c.get(f"/case/{cid}/letters.zip").status_code, 402)
        with self.app.app_context():
            from webapp import store
            store.db().execute("UPDATE agreements SET cancel_deadline='2000-01-01T00:00:00'")
            store.db().commit()
        r = self.c.get(f"/case/{cid}/letters.zip")
        self.assertEqual(r.status_code, 200)
        self.assertIn("00-how-to-send.pdf", zipfile.ZipFile(io.BytesIO(r.data)).namelist())

    def test_client_can_cancel(self):
        cid = self.firm_case()
        self.post(f"/pro/case/{cid}/signing", {})
        path = self.follow_mail("client@example.com", "/sign/", visit=False)
        client = self.app.test_client()
        tok = re.search(r'name="csrf" value="([^"]+)"', client.get(path).get_data(as_text=True)).group(1)
        client.post(path, data={"csrf": tok, "step": "ack", "ack": "1", "signature": "Jordan A. Rivera"})
        client.post(path, data={"csrf": tok, "step": "agree", "agree": "1", "signature": "Jordan A. Rivera"})
        client.post(path, data={"csrf": tok, "step": "cancel"})
        self.assertIn("You cancelled this agreement", client.get(path).get_data(as_text=True))

    def test_staff_invite_and_shared_access(self):
        cid = self.firm_case()
        self.post("/pro/invite", {"email": "staff@firm.com"}, page="/pro/dashboard")
        path = self.follow_mail("staff@firm.com", "/reset/", visit=False)
        self.post("/logout", {}, page="/pro/dashboard")
        self.post(path, {"password": "staff password 123"})
        self.post("/login", {"email": "staff@firm.com", "password": "staff password 123"})
        self.assertEqual(self.c.get(f"/case/{cid}").status_code, 200)

    def test_other_firm_cannot_see_case(self):
        cid = self.firm_case()
        self.post("/logout", {}, page="/pro/dashboard")
        self.register_firm("other@firm2.com")
        self.assertEqual(self.c.get(f"/case/{cid}").status_code, 404)
        self.assertEqual(self.c.get("/sign/not-a-real-token-at-all-xyz").status_code, 404)

    # The consumer-only tests inherited from WebFlow still run against a consumer account.


class PhoneApp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db")
        self.app = create_app({"TESTING": True, "DATABASE": self.tmp.name, "SECRET_KEY": "t",
                               "DATA_KEY": Fernet.generate_key().decode(), "DEV_PAYMENTS": True})
        self.c = self.app.test_client()

    def test_pwa_files_served(self):
        sw = self.c.get("/sw.js")
        self.assertEqual(sw.headers["Service-Worker-Allowed"], "/")
        self.assertIn(b"never cached", sw.data)
        m = self.c.get("/manifest.webmanifest")
        self.assertIn(b'"display": "standalone"', m.data)
        self.assertEqual(self.c.get("/static/icons/icon-512.png").status_code, 200)
        self.assertEqual(self.c.get("/offline").status_code, 200)
        self.assertIn(b"manifest.webmanifest", self.c.get("/").data)
        self.assertIn(b"Privacy policy", self.c.get("/privacy").data)
        self.assertIn(b"Terms of service", self.c.get("/terms").data)

    def test_native_app_hides_price_and_web_shows_it(self):
        self.assertIn(b"one time", self.c.get("/").data)
        self.assertNotIn(b"one time", self.c.get("/", headers={"User-Agent": "Mozilla/5.0 CDLApp/1"}).data)

    def test_reminders_require_login_and_are_generic(self):
        self.assertEqual(self.c.get("/api/reminders").status_code, 302)
        flow = WebFlow("test_full_flow_to_paid_download")
        flow.app, flow.c = self.app, self.c
        flow.register()
        cid = flow.new_case()
        flow.fill_case(cid)
        flow.post(f"/case/{cid}/tracker", {"kind": "new", "letter_type": "bureau_dispute", "target": "equifax",
                                           "sent_date": __import__("datetime").date.today().isoformat()})
        rem = self.c.get("/api/reminders").get_json()["reminders"]
        self.assertEqual(len(rem), 1)
        self.assertNotIn("equifax", str(rem).lower())


class DemoMode(unittest.TestCase):
    def test_demo_mode_banner_autoverify_and_no_wait(self):
        import os
        os.environ["DEMO_MODE"] = "1"
        try:
            tmp = tempfile.NamedTemporaryFile(suffix=".db")
            app = create_app({"TESTING": True, "DATABASE": tmp.name, "SECRET_KEY": "s", "DATA_KEY": None})
        finally:
            del os.environ["DEMO_MODE"]
        flow = WebFlow("test_full_flow_to_paid_download")
        flow.app, flow.c = app, app.test_client()
        self.assertIn(b"DEMO ONLY", flow.c.get("/").data)
        flow.register(verify=False)
        cid = flow.new_case()
        flow.fill_case(cid)
        flow.post(f"/case/{cid}/disclosure", {"ack": "1", "signature": "Jordan A. Rivera"})
        flow.post(f"/case/{cid}/agreement", {"agree": "1", "signature": "Jordan A. Rivera"})
        flow.post(f"/case/{cid}/checkout", {}, page=f"/case/{cid}")
        self.assertEqual(flow.c.get(f"/case/{cid}/letters.zip").status_code, 200)

    def test_demo_mode_refuses_live_stripe_keys(self):
        import os
        os.environ.update(DEMO_MODE="1", STRIPE_SECRET_KEY="sk_live_x")
        try:
            with self.assertRaises(RuntimeError):
                create_app({"TESTING": True, "DATABASE": ":memory:", "SECRET_KEY": "s"})
        finally:
            del os.environ["DEMO_MODE"], os.environ["STRIPE_SECRET_KEY"]
