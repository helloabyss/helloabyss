"""Flask app: consumer self-service credit dispute letters.

Run locally:  DEV_PAYMENTS=1 flask --app webapp.app run
Config (environment variables):
  SECRET_KEY        session signing key (required in production)
  DATA_KEY          Fernet key for encrypting case data and documents (required in production)
  DATABASE          SQLite path (default instance/cfads.db)
  PRICE_CENTS       one-time price (default 4900)
  COMPANY_NAME / COMPANY_ADDRESS   shown on the contract and cancellation notice
  STRIPE_SECRET_KEY / STRIPE_WEBHOOK_SECRET   enable real payments
  DEV_PAYMENTS=1    mark cases paid without Stripe (local testing only)
  BASE_URL          public URL, used for Stripe redirects
"""

import functools
import io
import os
import re
import secrets
import zipfile
from datetime import datetime, timedelta

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template, request, send_file,
                   send_from_directory, session, url_for)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from cfads import DISCLAIMER
from cfads.audit import run_audit
from cfads.evidence import evidence_report
from cfads.law import LAWS
from cfads.letters import plan_letters, render
from cfads.metro2 import ACCOUNT_STATUS, DISPUTE_CATEGORIES
from cfads.models import ASSERTION_TYPES, BUREAUS, EVIDENCE_TYPES, CaseFile
from cfads.pipeline import deadline, next_actions
from cfads.report import audit_text
from cfads.states import state_notes

from . import croa, mailer, store
from .pdf import text_to_pdf

ALLOWED_UPLOADS = {".pdf": "application/pdf", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
ACCOUNT_FIELDS = ["furnisher", "account_number", "account_type", "status_text", "status_code", "date_opened",
                  "date_of_first_delinquency", "date_last_payment", "date_reported", "date_closed", "balance",
                  "credit_limit", "high_credit", "past_due", "original_creditor", "payment_history",
                  "payment_history_start", "compliance_condition", "remarks"]
LETTER_TYPES_TRACKED = ["bureau_dispute", "identity_theft_block", "reinsertion_challenge", "furnisher_direct",
                        "furnisher_identity_theft", "collector_dispute", "mov_request", "failure_to_respond"]


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATA_KEY=os.environ.get("DATA_KEY"),
        DATABASE=os.environ.get("DATABASE", os.path.join(app.instance_path, "cfads.db")),
        PRICE_CENTS=int(os.environ.get("PRICE_CENTS", "4900")),
        COMPANY={"name": os.environ.get("COMPANY_NAME", "[Your Company LLC]"),
                 "address": os.environ.get("COMPANY_ADDRESS", "[Company street address, City, ST ZIP]")},
        STRIPE_SECRET_KEY=os.environ.get("STRIPE_SECRET_KEY"),
        STRIPE_WEBHOOK_SECRET=os.environ.get("STRIPE_WEBHOOK_SECRET"),
        DEV_PAYMENTS=os.environ.get("DEV_PAYMENTS") == "1",
        BASE_URL=os.environ.get("BASE_URL", "http://127.0.0.1:5000"),
        STRIPE_PRO_PRICE_ID=os.environ.get("STRIPE_PRO_PRICE_ID"),
        SMTP_HOST=os.environ.get("SMTP_HOST"), SMTP_PORT=os.environ.get("SMTP_PORT", "587"),
        SMTP_USER=os.environ.get("SMTP_USER"), SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD"),
        MAIL_FROM=os.environ.get("MAIL_FROM", "no-reply@localhost"),
        PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
        # How the App Store / Google Play apps handle payment: "none" shows the website address as text
        # (safest for store review everywhere); "link" opens the website checkout in the phone's browser
        # (allowed by Apple in the US since 2025 - check current store rules before switching).
        NATIVE_PAYMENT_MODE=os.environ.get("NATIVE_PAYMENT_MODE", "none"),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("BASE_URL", "").startswith("https"),
    )
    if test_config:
        app.config.update(test_config)
    if not app.config["SECRET_KEY"] or not app.config["DATA_KEY"]:
        if not (app.debug or app.testing or app.config["DEV_PAYMENTS"]):
            raise RuntimeError("Set SECRET_KEY and DATA_KEY before running in production")
        key_file = os.path.join(app.instance_path, "dev-keys")
        if not os.path.exists(key_file):
            from cryptography.fernet import Fernet
            with open(key_file, "w") as fh:
                fh.write(secrets.token_hex(32) + "\n" + Fernet.generate_key().decode())
        sk, dk = open(key_file).read().split()
        app.config["SECRET_KEY"] = app.config["SECRET_KEY"] or sk
        app.config["DATA_KEY"] = app.config["DATA_KEY"] or dk

    if os.environ.get("TRUST_PROXY") == "1":
        # Behind Render/Fly/a load balancer: use the real client IP (for login throttling) and scheme.
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    app.teardown_appcontext(store.close_db)
    with app.app_context():
        store.init_db()
        store.purge_expired_acknowledgments()

    register_routes(app)
    from .pro import register_pro_routes
    register_pro_routes(app)
    return app


# ------------------------------------------------------------------ helpers
def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        if "uid" not in session:
            return redirect(url_for("login", next=request.path))
        g.user = store.db().execute("SELECT * FROM users WHERE id=?", (session["uid"],)).fetchone()
        if not g.user:
            session.clear()
            return redirect(url_for("login"))
        return fn(*a, **kw)
    return wrapper


def get_case(case_id):
    row, data = store.load_case(case_id, g.user)
    if not row:
        abort(404)
    return row, data


def build_case(data):
    if not data.get("consumer"):
        return None
    clean = {k: v for k, v in data.items()}
    return CaseFile.from_dict(clean)


def agreement_for(case_id):
    return store.db().execute("SELECT * FROM agreements WHERE case_id=? ORDER BY id DESC LIMIT 1",
                              (case_id,)).fetchone()


def paid(case_id):
    return store.db().execute("SELECT 1 FROM payments WHERE case_id=? AND status='paid'", (case_id,)).fetchone()


def org_active(org_id):
    row = store.db().execute("SELECT sub_status FROM orgs WHERE id=?", (org_id,)).fetchone()
    return bool(row and row["sub_status"] == "active")


# ---- signed tokens (email verification, password reset, client signing links)
def _ser(salt):
    from flask import current_app
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=salt)


def make_token(salt, payload):
    return _ser(salt).dumps(payload)


def read_token(salt, token, max_age):
    try:
        return _ser(salt).loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


def send_verification(user_id, email):
    from flask import current_app
    link = current_app.config["BASE_URL"] + url_for("verify_email", token=make_token("verify", user_id))
    mailer.send(email, "Confirm your email", f"Confirm your email address to continue:\n\n{link}\n\n"
                "The link works for 3 days. If you didn't create an account, ignore this email.")


def company_for(row):
    """The party providing the service: us for consumer cases, the firm for firm cases."""
    from flask import current_app
    if row["org_id"]:
        o = store.db().execute("SELECT name, address FROM orgs WHERE id=?", (row["org_id"],)).fetchone()
        return {"name": o["name"], "address": o["address"]}
    return current_app.config["COMPANY"]


def price_for(row):
    """Consumer cases pay our price; firm clients pay whatever the firm charges them."""
    from flask import current_app
    if row["org_id"]:
        return row["client_price_cents"] or 0
    return current_app.config["PRICE_CENTS"]


def sign_acknowledgment(row, case, name, email, ip):
    if name.lower() != case.consumer.full_name.lower():
        return "Type your full name exactly as it appears on the case."
    store.record_acknowledgment(email, row["id"], name, croa.DISCLOSURE_SHA256, ip, croa.RETENTION_YEARS)
    return None


def sign_agreement(row, case, name, ip):
    if name.lower() != case.consumer.full_name.lower():
        return "Type your full name exactly as it appears on the case."
    company, price, signed = company_for(row), price_for(row), datetime.now()
    text = croa.contract_text(company, case.consumer.full_name, price, signed, firm=bool(row["org_id"]))
    store.db().execute("INSERT INTO agreements (case_id, signed_name, signed_at, ip, contract_text,"
                       " price_cents, cancel_deadline) VALUES (?,?,?,?,?,?,?)",
                       (row["id"], name, signed.isoformat(timespec="seconds"), ip,
                        text + "\n\n" + croa.cancellation_notice(company, signed), price,
                        croa.cancellation_deadline(signed).isoformat()))
    store.db().commit()
    return None


def case_progress(case_id, data, row=None):
    """What's done, and what blocks the next step."""
    p = {"about": bool(data.get("consumer")),
         "documents": bool(data.get("evidence")),
         "reports": any(r.get("tradelines") for r in data.get("reports", [])),
         "statements": bool(data.get("assertions_reviewed"))}
    p["letters"], p["blocked"], p["missing_id"] = [], [], []
    case = None
    if p["about"]:
        try:
            case = build_case(data)
        except (ValueError, KeyError) as e:
            p["error"] = str(e)
    if case:
        findings = run_audit(case)
        letters, blocked = plan_letters(case, findings)
        p["findings"], p["letters"], p["blocked"] = findings, letters, blocked
        p["missing_id"], p["doc_problems"] = evidence_report(case)
    p["ready_to_agree"] = (p["about"] and p["reports"] and p["statements"] and not p["missing_id"]
                           and p["letters"] and all(L.ready for L in p["letters"]))
    ag = agreement_for(case_id)
    p["agreement"] = ag
    p["cancelled"] = bool(ag and ag["cancelled_at"])
    p["signed"] = bool(ag and not ag["cancelled_at"])
    p["cancel_period_over"] = bool(p["signed"] and datetime.now() > datetime.fromisoformat(ag["cancel_deadline"]))
    p["org_case"] = bool(row is not None and row["org_id"])
    if p["org_case"]:
        # Firm cases: the firm's subscription covers delivery, but the client's CROA
        # cancellation period must still have ended before letters are released.
        p["subscription"] = org_active(row["org_id"])
        p["paid"] = p["subscription"] and p["signed"] and p["cancel_period_over"] and p["ready_to_agree"]
        p["can_pay"] = False
    else:
        p["paid"] = bool(paid(case_id))
        p["can_pay"] = p["signed"] and p["cancel_period_over"] and p["ready_to_agree"] and not p["paid"]
    return case, p


def _clean_form(fields):
    return {f: request.form.get(f, "").strip() for f in fields}


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def parse_address(line):
    m = re.match(r"\s*(.+?),\s*(.+?),\s*([A-Za-z]{2})\s+(\d{5}(?:-\d{4})?)\s*$", line)
    if not m:
        return None
    return {"line1": m.group(1), "city": m.group(2), "state": m.group(3).upper(), "zip": m.group(4)}


def ensure_report(data, bureau):
    for r in data["reports"]:
        if r["bureau"] == bureau:
            return r
    r = {"bureau": bureau, "report_date": "", "names": [], "addresses": [], "ssn_variations": [],
         "dates_of_birth": [], "tradelines": [], "inquiries": []}
    data["reports"].append(r)
    return r


def letters_zip(case, letters, include_summary=True):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n, L in enumerate(letters, 1):
            name = _slug(f"{n:02d}-{L.letter_type}-{L.target}")
            z.writestr(name + ".pdf", text_to_pdf(render(case, L), title=name))
        if include_summary:
            steps = ["HOW TO SEND YOUR LETTERS", "",
                     "1. Read every letter. Change anything that isn't exactly true before you sign.",
                     "2. Sign each letter. Attach copies (never originals) of the documents listed under Enclosures.",
                     "3. Mail each letter by USPS Certified Mail with Return Receipt. Keep the receipts.",
                     "4. Log in and record the date you mailed each letter, then the delivery date from the green card.",
                     "   The app tracks each legal deadline and tells you what to send next.",
                     "5. Check the recipient addresses before mailing; bureaus occasionally change them.", "",
                     DISCLAIMER]
            z.writestr("00-how-to-send.pdf", text_to_pdf("\n".join(steps), "How to send"))
            z.writestr("audit-summary.pdf", text_to_pdf(audit_text(case, run_audit(case)), "Audit summary"))
    return buf.getvalue()


# ------------------------------------------------------------------ routes
def register_routes(app):
    app.jinja_env.globals.update(csrf_token=csrf_token, EVIDENCE_TYPES=EVIDENCE_TYPES, BUREAUS=BUREAUS,
                                 ASSERTION_TYPES=ASSERTION_TYPES, ACCOUNT_STATUS=ACCOUNT_STATUS,
                                 DISPUTE_CATEGORIES=DISPUTE_CATEGORIES, LAWS=LAWS, DISCLAIMER=DISCLAIMER,
                                 LETTER_TYPES_TRACKED=LETTER_TYPES_TRACKED)

    @app.before_request
    def detect_native():
        # The store apps add "CDLApp/" to their user agent (mobile/capacitor.config.json).
        g.native = "CDLApp/" in request.headers.get("User-Agent", "")

    @app.before_request
    def check_csrf():
        if request.method == "POST" and request.endpoint != "stripe_webhook":
            if not secrets.compare_digest(request.form.get("csrf", ""), session.get("csrf", "")):
                abort(400, "Form expired. Go back, reload the page and try again.")

    @app.after_request
    def headers(resp):
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "same-origin"
        resp.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
        return resp

    @app.get("/sw.js")
    def service_worker():
        resp = send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["Service-Worker-Allowed"] = "/"
        return resp

    @app.get("/manifest.webmanifest")
    def manifest():
        return send_from_directory(app.static_folder, "manifest.webmanifest", mimetype="application/manifest+json")

    @app.get("/offline")
    def offline():
        return render_template("offline.html")

    @app.get("/install")
    def install():
        return render_template("install.html")

    @app.get("/api/reminders")
    @login_required
    def api_reminders():
        """Upcoming dispute deadlines for on-device notifications. Notification text is generic on
        purpose: it shows on the lock screen, so it never names a creditor or bureau."""
        rows = store.db().execute("SELECT id, data FROM cases WHERE user_id=? OR (org_id IS NOT NULL AND org_id=?)",
                                  (g.user["id"], g.user["org_id"] or -1)).fetchall()
        out, now = [], datetime.now()
        for r in rows:
            for d in store.dec(r["data"]).get("disputes", []):
                if d.get("status") != "sent":
                    continue
                due, _ = deadline(d)
                if not due:
                    continue
                at = datetime.combine(due, datetime.min.time()).replace(hour=10)
                at = at + timedelta(days=1)  # morning after the deadline passes
                if at > now:
                    out.append({"id": r["id"] * 1000 + len(out) + 1, "at": at.isoformat(),
                                "title": "A dispute deadline has passed",
                                "body": "Open the app to see your next step."})
        return jsonify(reminders=out[:60])

    @app.get("/healthz")
    def healthz():
        store.db().execute("SELECT 1")
        return "ok"

    @app.get("/")
    def home():
        return render_template("home.html", price=app.config["PRICE_CENTS"])

    # ---- auth
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            pw = request.form.get("password", "")
            if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                flash("Enter a valid email address.")
            elif len(pw) < 10:
                flash("Use a password of at least 10 characters.")
            else:
                try:
                    cur = store.db().execute("INSERT INTO users (email, pw_hash, created_at) VALUES (?,?,?)",
                                             (email, generate_password_hash(pw), store.now()))
                    store.db().commit()
                    session.clear()
                    session["uid"] = cur.lastrowid
                    session.permanent = True
                    send_verification(cur.lastrowid, email)
                    flash("Check your email for a link to confirm your address.")
                    return redirect(url_for("dashboard"))
                except Exception:
                    flash("That email already has an account. Log in instead.")
        return render_template("auth.html", mode="register")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            keys = (f"email:{email}", f"ip:{request.remote_addr}")
            if store.too_many_failures(*keys):
                flash("Too many attempts. Wait 15 minutes, or reset your password.")
                return render_template("auth.html", mode="login"), 429
            row = store.db().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            if not (row and check_password_hash(row["pw_hash"], request.form.get("password", ""))):
                store.record_failure(*keys)
            else:
                store.clear_failures(*keys)
                session.clear()
                session["uid"] = row["id"]
                session.permanent = True
                nxt = request.args.get("next", "")
                return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else url_for("dashboard"))
            flash("Email or password is incorrect.")
        return render_template("auth.html", mode="login")

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    # ---- dashboard
    @app.get("/dashboard")
    @login_required
    def dashboard():
        if g.user["org_id"]:
            return redirect(url_for("pro_dashboard"))
        rows = store.db().execute("SELECT id, title, status, updated_at FROM cases WHERE user_id=? ORDER BY id DESC",
                                  (g.user["id"],)).fetchall()
        return render_template("dashboard.html", cases=rows)

    @app.post("/case/new")
    @login_required
    def case_new():
        title = request.form.get("title", "").strip() or "My credit dispute"
        cur = store.db().execute("INSERT INTO cases (user_id, title, data, created_at, updated_at) VALUES (?,?,?,?,?)",
                                 (g.user["id"], title[:80], store.enc(store.empty_case()), store.now(), store.now()))
        store.db().commit()
        return redirect(url_for("case_about", case_id=cur.lastrowid))

    @app.get("/case/<int:case_id>")
    @login_required
    def case_home(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        return render_template("case.html", row=row, p=p)

    # ---- step 1: about you
    @app.route("/case/<int:case_id>/about", methods=["GET", "POST"])
    @login_required
    def case_about(case_id):
        row, data = get_case(case_id)
        if request.method == "POST":
            f = _clean_form(["full_name", "aliases", "date_of_birth", "ssn_last4", "line1", "line2", "city",
                             "state", "zip", "prior", "phone"])
            errors = []
            if not re.match(r"^\d{4}$", f["ssn_last4"]):
                errors.append("Enter only the last 4 digits of your SSN.")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", f["date_of_birth"]):
                errors.append("Enter your date of birth.")
            if not (f["full_name"] and f["line1"] and f["city"] and re.match(r"^[A-Za-z]{2}$", f["state"])
                    and re.match(r"^\d{5}(-\d{4})?$", f["zip"])):
                errors.append("Enter your full name and complete current address.")
            prior = [parse_address(x) for x in f["prior"].splitlines() if x.strip()]
            if any(a is None for a in prior):
                errors.append("Write each prior address as: 12 Main St, City, ST 12345")
            if errors:
                for e in errors:
                    flash(e)
            else:
                data["consumer"] = {
                    "full_name": f["full_name"], "date_of_birth": f["date_of_birth"], "ssn_last4": f["ssn_last4"],
                    "aliases": [a.strip() for a in f["aliases"].split(",") if a.strip()],
                    "current_address": {"line1": f["line1"], "line2": f["line2"], "city": f["city"],
                                        "state": f["state"].upper(), "zip": f["zip"]},
                    "prior_addresses": prior, "phone": f["phone"], "email": g.user["email"]}
                store.save_case(case_id, data)
                return redirect(url_for("case_documents", case_id=case_id))
        return render_template("about.html", row=row, c=data.get("consumer") or {})

    # ---- step 2: documents
    @app.route("/case/<int:case_id>/documents", methods=["GET", "POST"])
    @login_required
    def case_documents(case_id):
        row, data = get_case(case_id)
        if request.method == "POST":
            up = request.files.get("file")
            if not (up and up.filename):
                up = request.files.get("photo")  # "Take a photo" on phones
            f = _clean_form(["type", "description", "issued_date", "expires_date", "name_on_document",
                             "address_on_document"])
            ext = os.path.splitext(up.filename or "")[1].lower() if up else ""
            if f["type"] not in EVIDENCE_TYPES:
                flash("Choose what kind of document this is.")
            elif ext not in ALLOWED_UPLOADS:
                flash("Upload a PDF, JPG or PNG file.")
            elif len(f["description"]) < 5:
                flash("Describe the document, e.g. 'Electric bill, September 2026'.")
            else:
                blob = up.read()
                cur = store.db().execute("INSERT INTO documents (case_id, filename, mime, blob, created_at) VALUES (?,?,?,?,?)",
                                         (case_id, os.path.basename(up.filename)[:120], ALLOWED_UPLOADS[ext],
                                          store.enc_bytes(blob), store.now()))
                store.db().commit()
                data["evidence"].append({"id": f"D{cur.lastrowid}", "file": str(cur.lastrowid), **f})
                store.save_case(case_id, data)
                flash("Document added.")
            return redirect(url_for("case_documents", case_id=case_id))
        problems = []
        if data.get("consumer"):
            try:
                missing, problems = evidence_report(build_case(data))
                problems = [f"Missing: {EVIDENCE_TYPES[m]}" for m in missing] + problems
            except ValueError as e:
                problems = [str(e)]
        return render_template("documents.html", row=row, evidence=data["evidence"], problems=problems)

    @app.get("/case/<int:case_id>/documents/<int:doc_id>")
    @login_required
    def case_document_download(case_id, doc_id):
        get_case(case_id)
        d = store.db().execute("SELECT * FROM documents WHERE id=? AND case_id=?", (doc_id, case_id)).fetchone()
        if not d:
            abort(404)
        return send_file(io.BytesIO(store.dec_bytes(d["blob"])), mimetype=d["mime"], as_attachment=True,
                         download_name=d["filename"])

    @app.post("/case/<int:case_id>/documents/<int:doc_id>/delete")
    @login_required
    def case_document_delete(case_id, doc_id):
        row, data = get_case(case_id)
        store.db().execute("DELETE FROM documents WHERE id=? AND case_id=?", (doc_id, case_id))
        store.db().commit()
        eid = f"D{doc_id}"
        data["evidence"] = [e for e in data["evidence"] if e["id"] != eid]
        for a in data.get("assertions", []):
            a["evidence_ids"] = [i for i in a.get("evidence_ids", []) if i != eid]
        store.save_case(case_id, data)
        return redirect(url_for("case_documents", case_id=case_id))

    # ---- step 3: reports
    @app.route("/case/<int:case_id>/reports", methods=["GET", "POST"])
    @login_required
    def case_reports(case_id):
        row, data = get_case(case_id)
        if request.method == "POST":
            kind = request.form.get("kind")
            bureau = request.form.get("bureau", "")
            if bureau not in BUREAUS:
                flash("Choose a credit bureau.")
                return redirect(url_for("case_reports", case_id=case_id))
            rep = ensure_report(data, bureau)
            if kind == "account":
                t = _clean_form(ACCOUNT_FIELDS)
                if not t["furnisher"] or not t["account_number"]:
                    flash("Enter at least the company name and account number as the report shows them.")
                    return redirect(url_for("case_reports", case_id=case_id))
                for fld in ("balance", "credit_limit", "high_credit", "past_due"):
                    t[fld] = re.sub(r"[^\d.]", "", t[fld]) or None
                for fld in [k for k in t if k.startswith("date") or k == "payment_history_start"]:
                    if t[fld] and not re.match(r"^\d{4}-\d{2}(-\d{2})?$", t[fld]):
                        flash(f"{fld.replace('_', ' ').title()}: use YYYY-MM or YYYY-MM-DD.")
                        return redirect(url_for("case_reports", case_id=case_id))
                nick = _slug(request.form.get("nickname", "")) or _slug(f"{t['furnisher']}-{t['account_number'][-4:]}")
                t.update(account_key=nick, is_collection=bool(request.form.get("is_collection")),
                         is_medical=bool(request.form.get("is_medical")))
                rep["tradelines"].append({k: v for k, v in t.items() if v not in ("", None) or k in ("is_collection", "is_medical")})
                flash(f"Added {t['furnisher']} to {bureau.title()}.")
            elif kind == "inquiry":
                f = _clean_form(["creditor", "date"])
                if f["creditor"] and re.match(r"^\d{4}-\d{2}-\d{2}$", f["date"]):
                    rep["inquiries"].append({"creditor": f["creditor"], "date": f["date"], "kind": "hard"})
                else:
                    flash("Enter the company name and inquiry date.")
            elif kind == "personal":
                f = _clean_form(["report_date", "names", "addresses", "ssns", "dobs"])
                rep["report_date"] = f["report_date"]
                rep["names"] = [x.strip() for x in f["names"].splitlines() if x.strip()]
                addrs = [parse_address(x) for x in f["addresses"].splitlines() if x.strip()]
                if any(a is None for a in addrs):
                    flash("Write each address as: 12 Main St, City, ST 12345")
                    return redirect(url_for("case_reports", case_id=case_id))
                rep["addresses"] = addrs
                rep["ssn_variations"] = [x.strip() for x in f["ssns"].splitlines() if x.strip()]
                rep["dates_of_birth"] = [x.strip() for x in f["dobs"].splitlines() if x.strip()]
            elif kind == "delete":
                idx = int(request.form.get("index", -1))
                coll = rep["inquiries"] if request.form.get("what") == "inquiry" else rep["tradelines"]
                if 0 <= idx < len(coll):
                    coll.pop(idx)
            store.save_case(case_id, data)
            return redirect(url_for("case_reports", case_id=case_id) + f"#{bureau}")
        keys = sorted({t.get("account_key") for r in data["reports"] for t in r["tradelines"]})
        return render_template("reports.html", row=row, reports={r["bureau"]: r for r in data["reports"]},
                               keys=keys, fields=ACCOUNT_FIELDS)

    # ---- step 4: your statements
    @app.route("/case/<int:case_id>/statements", methods=["GET", "POST"])
    @login_required
    def case_statements(case_id):
        row, data = get_case(case_id)
        accounts = {}
        for r in data["reports"]:
            for t in r["tradelines"]:
                a = accounts.setdefault(t["account_key"], {"label": f"{t['furnisher']} #{t['account_number']}",
                                                           "bureaus": [], "kind": "account"})
                a["bureaus"].append(r["bureau"])
            for q in r["inquiries"]:
                k = "inq-" + _slug(q["creditor"])
                a = accounts.setdefault(k, {"label": f"Inquiry: {q['creditor']}", "bureaus": [], "kind": "inquiry",
                                            "furnisher": q["creditor"]})
                a["bureaus"].append(r["bureau"])
        if request.method == "POST":
            new, n = [], 0
            for key, acc in accounts.items():
                typ = request.form.get(f"type__{key}", "")
                if not typ:
                    continue
                stmt = request.form.get(f"statement__{key}", "").strip()
                if len(stmt) < 15:
                    flash(f"{acc['label']}: describe the facts in a full sentence (what is wrong and how you know).")
                    return redirect(url_for("case_statements", case_id=case_id))
                n += 1
                a = {"id": f"A{n}", "type": typ, "statement": stmt,
                     "evidence_ids": request.form.getlist(f"evidence__{key}")}
                if acc["kind"] == "inquiry":
                    a["furnisher"] = acc["furnisher"]
                else:
                    a["account_key"] = key
                detail = request.form.get(f"detail__{key}", "").strip()
                if detail:
                    a["details"] = {"date_sent" if typ == "disputed_directly" else "note": detail}
                new.append(a)
            data["assertions"] = new
            data["assertions_reviewed"] = True
            store.save_case(case_id, data)
            return redirect(url_for("case_review", case_id=case_id))
        current = {a.get("account_key") or "inq-" + _slug(a.get("furnisher", "")): a for a in data.get("assertions", [])}
        return render_template("statements.html", row=row, accounts=accounts, current=current,
                               evidence=data["evidence"])

    # ---- step 5: review
    @app.get("/case/<int:case_id>/review")
    @login_required
    def case_review(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        return render_template("review.html", row=row, p=p,
                               state=state_notes(case.consumer.state) if case else "")

    # ---- step 6: disclosure (separate document) and agreement
    @app.route("/case/<int:case_id>/disclosure", methods=["GET", "POST"])
    @login_required
    def case_disclosure(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        if row["org_id"]:
            return redirect(url_for("pro_signing", case_id=case_id))
        if not p["ready_to_agree"]:
            flash("Finish the earlier steps first.")
            return redirect(url_for("case_review", case_id=case_id))
        if not g.user["email_verified"]:
            flash("Confirm your email address first (check your inbox, or resend from My cases).")
            return redirect(url_for("case_home", case_id=case_id))
        if request.method == "POST":
            err = None if request.form.get("ack") else "Tick the box to confirm you received the statement."
            err = err or sign_acknowledgment(row, case, request.form.get("signature", "").strip(),
                                             g.user["email"], request.remote_addr)
            if err:
                flash(err)
            else:
                return redirect(url_for("case_agreement", case_id=case_id))
        return render_template("disclosure.html", row=row, text=croa.DISCLOSURE)

    @app.route("/case/<int:case_id>/agreement", methods=["GET", "POST"])
    @login_required
    def case_agreement(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        acked = store.db().execute("SELECT 1 FROM acknowledgments WHERE case_id=? AND user_email=?",
                                   (case_id, g.user["email"])).fetchone()
        if not acked:
            return redirect(url_for("case_disclosure", case_id=case_id))
        if row["org_id"]:
            return redirect(url_for("pro_signing", case_id=case_id))
        company, price = company_for(row), price_for(row)
        if request.method == "POST" and not p["signed"]:
            err = None if request.form.get("agree") else "Tick the box to agree."
            err = err or sign_agreement(row, case, request.form.get("signature", "").strip(), request.remote_addr)
            if err:
                flash(err)
            else:
                flash("Agreement signed. Download your copy below.")
                return redirect(url_for("case_agreement", case_id=case_id))
        if p["signed"]:
            ag = p["agreement"]
            return render_template("agreement.html", row=row, p=p, contract=ag["contract_text"], signed=True)
        return render_template("agreement.html", row=row, p=p, signed=False,
                               contract=croa.contract_text(company, case.consumer.full_name, price, firm=bool(row["org_id"])),
                               notice=croa.cancellation_notice(company, datetime.now()))

    @app.get("/case/<int:case_id>/agreement.pdf")
    @login_required
    def case_agreement_pdf(case_id):
        get_case(case_id)
        ag = agreement_for(case_id)
        if not ag:
            abort(404)
        body = f"{ag['contract_text']}\n\nSigned electronically by {ag['signed_name']} on {ag['signed_at']}."
        return send_file(io.BytesIO(text_to_pdf(body, "Agreement")), mimetype="application/pdf",
                         as_attachment=True, download_name="agreement.pdf")

    @app.get("/case/<int:case_id>/disclosure.pdf")
    @login_required
    def case_disclosure_pdf(case_id):
        get_case(case_id)
        return send_file(io.BytesIO(text_to_pdf(croa.DISCLOSURE, croa.DISCLOSURE_TITLE)), mimetype="application/pdf",
                         as_attachment=True, download_name="consumer-credit-file-rights.pdf")

    @app.post("/case/<int:case_id>/cancel")
    @login_required
    def case_cancel(case_id):
        get_case(case_id)
        ag = agreement_for(case_id)
        if ag and not ag["cancelled_at"]:
            store.db().execute("UPDATE agreements SET cancelled_at=? WHERE id=?", (store.now(), ag["id"]))
            store.db().commit()
            flash("Your agreement is cancelled. You have not been charged.")
        return redirect(url_for("case_home", case_id=case_id))

    # ---- step 7: pay and download
    @app.post("/case/<int:case_id>/checkout")
    @login_required
    def case_checkout(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        if row["org_id"] or not p["can_pay"]:
            flash("Payment opens after your cancellation period ends and your letters are ready.")
            return redirect(url_for("case_home", case_id=case_id))
        price = p["agreement"]["price_cents"]
        if app.config["STRIPE_SECRET_KEY"]:
            import stripe
            stripe.api_key = app.config["STRIPE_SECRET_KEY"]
            s = stripe.checkout.Session.create(
                mode="payment", customer_email=g.user["email"], client_reference_id=str(case_id),
                metadata={"case_id": str(case_id)},
                line_items=[{"quantity": 1, "price_data": {"currency": "usd", "unit_amount": price,
                                                           "product_data": {"name": "Dispute letter package"}}}],
                success_url=f"{app.config['BASE_URL']}/case/{case_id}/paid?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{app.config['BASE_URL']}/case/{case_id}")
            return redirect(s.url, code=303)
        if app.config["DEV_PAYMENTS"]:
            _mark_paid(case_id, "dev", price)
            return redirect(url_for("case_home", case_id=case_id))
        abort(503, "Payments are not configured.")

    def _mark_paid(case_id, ref, amount):
        if not paid(case_id):
            store.db().execute("INSERT INTO payments (case_id, provider_ref, amount_cents, status, paid_at)"
                               " VALUES (?,?,?,?,?)", (case_id, ref, amount, "paid", store.now()))
            store.db().execute("UPDATE cases SET status='paid' WHERE id=?", (case_id,))
            store.db().commit()

    @app.get("/case/<int:case_id>/paid")
    @login_required
    def case_paid(case_id):
        get_case(case_id)
        import stripe
        stripe.api_key = app.config["STRIPE_SECRET_KEY"]
        s = stripe.checkout.Session.retrieve(request.args.get("session_id", ""))
        if s.payment_status == "paid" and s.metadata.get("case_id") == str(case_id):
            _mark_paid(case_id, s.id, s.amount_total)
            flash("Payment received. Your letters are ready to download.")
        return redirect(url_for("case_home", case_id=case_id))

    @app.post("/stripe/webhook")
    def stripe_webhook():
        import stripe
        try:
            ev = stripe.Webhook.construct_event(request.data, request.headers.get("Stripe-Signature", ""),
                                                app.config["STRIPE_WEBHOOK_SECRET"])
        except Exception:
            abort(400)
        obj = ev["data"]["object"]
        if ev["type"] == "checkout.session.completed":
            md = obj.get("metadata", {})
            if obj.get("payment_status") == "paid" and md.get("case_id"):
                _mark_paid(int(md["case_id"]), obj["id"], obj.get("amount_total") or 0)
            if md.get("org_id") and obj.get("subscription"):
                store.db().execute("UPDATE orgs SET sub_status='active', stripe_customer=?, stripe_subscription=?"
                                   " WHERE id=?", (obj.get("customer"), obj["subscription"], int(md["org_id"])))
                store.db().commit()
        elif ev["type"] in ("customer.subscription.updated", "customer.subscription.deleted"):
            status = "active" if obj.get("status") in ("active", "trialing") else "inactive"
            store.db().execute("UPDATE orgs SET sub_status=? WHERE stripe_subscription=?", (status, obj["id"]))
            store.db().commit()
        return "", 200

    @app.get("/case/<int:case_id>/letters.zip")
    @login_required
    def case_letters(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        if not p["paid"]:
            return "Payment required before download.", 402
        letters, _ = plan_letters(case, p["findings"])
        return send_file(io.BytesIO(letters_zip(case, letters)), mimetype="application/zip", as_attachment=True,
                         download_name="dispute-letters.zip")

    # ---- step 8: tracker
    @app.route("/case/<int:case_id>/tracker", methods=["GET", "POST"])
    @login_required
    def case_tracker(case_id):
        row, data = get_case(case_id)
        if request.method == "POST":
            f = _clean_form(["did", "letter_type", "target", "sent_date", "received_date", "result_date",
                             "outcome", "account_key"])
            if request.form.get("kind") == "new":
                if f["letter_type"] not in LETTER_TYPES_TRACKED or not f["target"] or not f["sent_date"]:
                    flash("Choose the letter type, recipient and mailing date.")
                else:
                    data["disputes"].append({"id": f"D{len(data['disputes']) + 1:03d}", "letter_type": f["letter_type"],
                                             "target": f["target"].lower(), "status": "sent",
                                             "sent_date": f["sent_date"], "received_date": f["received_date"]})
            else:
                d = next((d for d in data["disputes"] if d["id"] == f["did"]), None)
                if d:
                    if f["received_date"]:
                        d["received_date"] = f["received_date"]
                    if f["outcome"] and f["account_key"]:
                        d.setdefault("results", []).append({"account_key": f["account_key"], "outcome": f["outcome"]})
                        d["status"] = "answered"
                        d["result_date"] = f["result_date"] or datetime.now().date().isoformat()
            store.save_case(case_id, data)
            return redirect(url_for("case_tracker", case_id=case_id))
        case = build_case(data) if data.get("consumer") else None
        actions = next_actions(case) if case else []
        keys = sorted({t.get("account_key") for r in data["reports"] for t in r["tradelines"]})
        return render_template("tracker.html", row=row, disputes=data["disputes"], actions=actions, keys=keys,
                               paid=bool(paid(case_id)))

    # ---- deletion
    @app.post("/case/<int:case_id>/delete")
    @login_required
    def case_delete(case_id):
        get_case(case_id)
        store.db().execute("DELETE FROM cases WHERE id=?", (case_id,))
        store.db().commit()
        flash("Case and all its documents deleted. (Your signed rights acknowledgment is kept for 2 years as the law requires.)")
        return redirect(url_for("dashboard"))

    @app.post("/account/delete")
    @login_required
    def account_delete():
        uid, org = g.user["id"], g.user["org_id"]
        store.db().execute("DELETE FROM cases WHERE user_id=? AND org_id IS NULL", (uid,))
        if org:
            other = store.db().execute("SELECT MIN(id) FROM users WHERE org_id=? AND id<>?", (org, uid)).fetchone()[0]
            if other:  # firm cases stay with the firm
                store.db().execute("UPDATE cases SET user_id=? WHERE user_id=? AND org_id=?", (other, uid, org))
            else:      # last member: the firm and its cases go too
                store.db().execute("DELETE FROM cases WHERE org_id=?", (org,))
                store.db().execute("DELETE FROM orgs WHERE id=?", (org,))
        store.db().execute("DELETE FROM users WHERE id=?", (uid,))
        store.db().commit()
        session.clear()
        flash("Your account and all case data are deleted.")
        return redirect(url_for("home"))

    @app.get("/verify/<token>")
    def verify_email(token):
        uid = read_token("verify", token, 3 * 24 * 3600)
        if uid is None:
            flash("That confirmation link is invalid or expired. Log in and resend it.")
            return redirect(url_for("login"))
        store.db().execute("UPDATE users SET email_verified=1 WHERE id=?", (uid,))
        store.db().commit()
        flash("Email confirmed.")
        return redirect(url_for("dashboard") if session.get("uid") else url_for("login"))

    @app.post("/verify/resend")
    @login_required
    def verify_resend():
        if not g.user["email_verified"]:
            send_verification(g.user["id"], g.user["email"])
        flash("Confirmation email sent.")
        return redirect(url_for("dashboard"))

    @app.route("/forgot", methods=["GET", "POST"])
    def forgot():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            row = store.db().execute("SELECT id, pw_hash FROM users WHERE email=?", (email,)).fetchone()
            if row:
                # Binding the token to the current hash makes it single-use.
                tok = make_token("reset", [row["id"], row["pw_hash"][-12:]])
                mailer.send(email, "Reset your password",
                            f"Reset your password here (valid for 1 hour):\n\n{app.config['BASE_URL']}"
                            f"{url_for('reset_password', token=tok)}\n\nIf you didn't ask, ignore this email.")
            flash("If that email has an account, a reset link is on its way.")
            return redirect(url_for("login"))
        return render_template("auth.html", mode="forgot")

    @app.route("/reset/<token>", methods=["GET", "POST"])
    def reset_password(token):
        data = read_token("reset", token, 3600)
        row = data and store.db().execute("SELECT * FROM users WHERE id=?", (data[0],)).fetchone()
        if not row or row["pw_hash"][-12:] != data[1]:
            flash("That reset link is invalid, expired or already used.")
            return redirect(url_for("forgot"))
        if request.method == "POST":
            pw = request.form.get("password", "")
            if len(pw) < 10:
                flash("Use a password of at least 10 characters.")
            else:
                store.db().execute("UPDATE users SET pw_hash=?, email_verified=1 WHERE id=?",
                                   (generate_password_hash(pw), row["id"]))
                store.db().commit()
                store.clear_failures(f"email:{row['email']}")
                flash("Password changed. Log in with your new password.")
                return redirect(url_for("login"))
        return render_template("auth.html", mode="reset")

    @app.get("/privacy")
    def privacy():
        return render_template("privacy.html", company=app.config["COMPANY"])

    @app.get("/terms")
    def terms():
        return render_template("terms.html", company=app.config["COMPANY"])

    @app.get("/legal/rights")
    def legal_rights():
        return render_template("text.html", title=croa.DISCLOSURE_TITLE, text=croa.DISCLOSURE)
