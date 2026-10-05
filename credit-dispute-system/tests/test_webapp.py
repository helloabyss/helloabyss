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

    def register(self, email="a@example.com"):
        return self.post("/register", {"email": email, "password": "correct horse battery"})

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

    def test_disclosure_is_statutory_text(self):
        self.assertTrue(croa.DISCLOSURE.startswith("Consumer Credit File Rights Under State and Federal Law"))
        self.assertIn("within 3 business days from the date you signed it", croa.DISCLOSURE)
        self.assertTrue(croa.DISCLOSURE.rstrip().endswith("Washington, D.C. 20580"))


if __name__ == "__main__":
    unittest.main()
