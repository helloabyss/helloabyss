"""Professional tier: firms (consumer-law attorneys, credit repair businesses) manage many
clients on a monthly subscription.

The firm is the party that contracts with its client, so the CROA rights statement and
contract name the firm, and the CLIENT signs them through a private link. Letters for a
client are released only after the client's 3-business-day cancellation period ends,
whatever the firm's billing arrangement with that client.
"""

import io
import re
import secrets
from datetime import datetime

from flask import abort, flash, g, redirect, render_template, request, send_file, url_for
from werkzeug.security import generate_password_hash

from . import croa, mailer, store
from .pdf import text_to_pdf


def register_pro_routes(app):
    from .app import (build_case, case_progress, company_for, get_case, login_required, make_token,
                      price_for, send_verification, sign_acknowledgment, sign_agreement)

    def pro_required(fn):
        import functools

        @functools.wraps(fn)
        @login_required
        def wrapper(*a, **kw):
            if not g.user["org_id"]:
                abort(403)
            g.org = store.db().execute("SELECT * FROM orgs WHERE id=?", (g.user["org_id"],)).fetchone()
            return fn(*a, **kw)
        return wrapper

    @app.get("/pro")
    def pro_home():
        return render_template("pro_home.html")

    @app.route("/pro/register", methods=["GET", "POST"])
    def pro_register():
        if request.method == "POST":
            f = {k: request.form.get(k, "").strip() for k in ("firm", "address", "email", "password")}
            f["email"] = f["email"].lower()
            if not (f["firm"] and len(f["address"]) > 10):
                flash("Enter your firm's legal name and full business address. They appear on client contracts.")
            elif not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", f["email"]) or len(f["password"]) < 10:
                flash("Enter a valid email and a password of at least 10 characters.")
            elif store.db().execute("SELECT 1 FROM users WHERE email=?", (f["email"],)).fetchone():
                flash("That email already has an account.")
            else:
                cur = store.db().execute("INSERT INTO orgs (name, address, created_at) VALUES (?,?,?)",
                                         (f["firm"], f["address"], store.now()))
                org_id = cur.lastrowid
                cur = store.db().execute("INSERT INTO users (email, pw_hash, role, org_id, created_at, email_verified)"
                                         " VALUES (?,?,?,?,?,?)", (f["email"], generate_password_hash(f["password"]),
                                                                    "pro_admin", org_id, store.now(),
                                                                    1 if app.config["DEMO_MODE"] else 0))
                store.db().commit()
                from flask import session
                session.clear()
                session["uid"] = cur.lastrowid
                send_verification(cur.lastrowid, f["email"])
                flash("Firm account created. Check your email to confirm your address.")
                return redirect(url_for("pro_dashboard"))
        return render_template("pro_register.html")

    @app.get("/pro/dashboard")
    @pro_required
    def pro_dashboard():
        cases = store.db().execute("SELECT id, title, client_name, status, updated_at FROM cases WHERE org_id=?"
                                   " ORDER BY id DESC", (g.org["id"],)).fetchall()
        team = store.db().execute("SELECT email, role, email_verified FROM users WHERE org_id=? ORDER BY id",
                                  (g.org["id"],)).fetchall()
        return render_template("pro_dashboard.html", org=g.org, cases=cases, team=team)

    @app.post("/pro/subscribe")
    @pro_required
    def pro_subscribe():
        if g.user["role"] != "pro_admin":
            abort(403)
        if app.config["STRIPE_SECRET_KEY"] and app.config["STRIPE_PRO_PRICE_ID"]:
            import stripe
            stripe.api_key = app.config["STRIPE_SECRET_KEY"]
            s = stripe.checkout.Session.create(
                mode="subscription", customer_email=g.user["email"], metadata={"org_id": str(g.org["id"])},
                subscription_data={"metadata": {"org_id": str(g.org["id"])}},
                line_items=[{"price": app.config["STRIPE_PRO_PRICE_ID"], "quantity": 1}],
                success_url=app.config["BASE_URL"] + url_for("pro_dashboard"),
                cancel_url=app.config["BASE_URL"] + url_for("pro_dashboard"))
            return redirect(s.url, code=303)
        if app.config["DEV_PAYMENTS"]:
            store.db().execute("UPDATE orgs SET sub_status='active' WHERE id=?", (g.org["id"],))
            store.db().commit()
            flash("Subscription active (development mode).")
            return redirect(url_for("pro_dashboard"))
        abort(503, "Payments are not configured.")

    @app.post("/pro/billing")
    @pro_required
    def pro_billing():
        if g.user["role"] != "pro_admin" or not g.org["stripe_customer"]:
            abort(403)
        import stripe
        stripe.api_key = app.config["STRIPE_SECRET_KEY"]
        s = stripe.billing_portal.Session.create(customer=g.org["stripe_customer"],
                                                 return_url=app.config["BASE_URL"] + url_for("pro_dashboard"))
        return redirect(s.url, code=303)

    @app.post("/pro/invite")
    @pro_required
    def pro_invite():
        if g.user["role"] != "pro_admin":
            abort(403)
        email = request.form.get("email", "").strip().lower()
        if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Enter a valid email.")
        elif store.db().execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            flash("That email already has an account.")
        else:
            pw_hash = generate_password_hash(secrets.token_urlsafe(24))
            cur = store.db().execute("INSERT INTO users (email, pw_hash, role, org_id, created_at) VALUES (?,?,?,?,?)",
                                     (email, pw_hash, "pro_staff", g.org["id"], store.now()))
            store.db().commit()
            tok = make_token("reset", [cur.lastrowid, pw_hash[-12:]])
            mailer.send(email, f"You've been added to {g.org['name']}",
                        f"{g.user['email']} added you to {g.org['name']}. Set your password here (valid 1 hour; "
                        f"use 'Forgot password' for a new link):\n\n{app.config['BASE_URL']}"
                        f"{url_for('reset_password', token=tok)}")
            flash(f"Invitation sent to {email}.")
        return redirect(url_for("pro_dashboard"))

    @app.post("/pro/case/new")
    @pro_required
    def pro_case_new():
        if not g.user["email_verified"]:
            flash("Confirm your email address before adding clients.")
            return redirect(url_for("pro_dashboard"))
        name = request.form.get("client_name", "").strip()
        email = request.form.get("client_email", "").strip().lower()
        try:
            price = round(float(request.form.get("client_price", "0") or 0) * 100)
        except ValueError:
            price = -1
        if not name or not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", email) or price < 0:
            flash("Enter the client's name, email, and what you charge them (0 if nothing).")
            return redirect(url_for("pro_dashboard"))
        cur = store.db().execute(
            "INSERT INTO cases (user_id, org_id, title, client_name, client_email, client_price_cents, data,"
            " created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (g.user["id"], g.org["id"], name[:80], name[:80], email, price, store.enc(store.empty_case()),
             store.now(), store.now()))
        store.db().commit()
        return redirect(url_for("case_about", case_id=cur.lastrowid))

    @app.route("/pro/case/<int:case_id>/signing", methods=["GET", "POST"])
    @pro_required
    def pro_signing(case_id):
        row, data = get_case(case_id)
        case, p = case_progress(case_id, data, row)
        link = None
        if request.method == "POST":
            if not p["ready_to_agree"]:
                flash("Finish the case (documents, reports, statements) before sending it for signature.")
            else:
                token = row["sign_token"] or secrets.token_urlsafe(32)
                store.db().execute("UPDATE cases SET sign_token=? WHERE id=?", (token, case_id))
                store.db().commit()
                url = app.config["BASE_URL"] + url_for("client_sign", token=token)
                mailer.send(row["client_email"], f"{g.org['name']}: please review and sign",
                            f"{g.org['name']} has prepared your credit dispute file. Before any work is "
                            f"delivered, federal law requires you to receive a statement of your rights and to "
                            f"sign an agreement you can cancel within 3 business days.\n\nReview and sign here:\n{url}")
                flash(f"Signing link sent to {row['client_email']}.")
            return redirect(url_for("pro_signing", case_id=case_id))
        if row["sign_token"]:
            link = app.config["BASE_URL"] + url_for("client_sign", token=row["sign_token"])
        return render_template("pro_signing.html", row=row, p=p, link=link, org=g.org)

    # ---- client side (no account needed; the private link is the credential)
    def _client_case(token):
        if not token or len(token) < 20:
            abort(404)
        row = store.db().execute("SELECT * FROM cases WHERE sign_token=?", (token,)).fetchone()
        if not row:
            abort(404)
        data = store.dec(row["data"])
        case, p = case_progress(row["id"], data, row)
        return row, case, p

    @app.route("/sign/<token>", methods=["GET", "POST"])
    def client_sign(token):
        row, case, p = _client_case(token)
        acked = store.db().execute("SELECT 1 FROM acknowledgments WHERE case_id=? AND user_email=?",
                                   (row["id"], row["client_email"])).fetchone()
        if request.method == "POST":
            step = request.form.get("step")
            name = request.form.get("signature", "").strip()
            if step == "ack" and request.form.get("ack"):
                err = sign_acknowledgment(row, case, name, row["client_email"], request.remote_addr)
            elif step == "agree" and acked and request.form.get("agree") and not p["signed"]:
                err = sign_agreement(row, case, name, request.remote_addr)
            elif step == "cancel" and p["signed"] and not p["cancel_period_over"]:
                store.db().execute("UPDATE agreements SET cancelled_at=? WHERE id=?", (store.now(), p["agreement"]["id"]))
                store.db().commit()
                mailer.send(row["client_email"], "Your agreement is cancelled",
                            f"You cancelled your agreement with {company_for(row)['name']}. You owe nothing.")
                err = None
            else:
                err = "Tick the box and type your full name."
            if err:
                flash(err)
            return redirect(url_for("client_sign", token=token))
        company = company_for(row)
        return render_template("sign.html", row=row, p=p, acked=acked, token=token, company=company,
                               disclosure=croa.DISCLOSURE,
                               contract=croa.contract_text(company, case.consumer.full_name, price_for(row), firm=True),
                               notice=croa.cancellation_notice(company, datetime.now()))

    @app.get("/sign/<token>/agreement.pdf")
    def client_agreement_pdf(token):
        row, case, p = _client_case(token)
        if not p["agreement"]:
            abort(404)
        ag = p["agreement"]
        body = f"{ag['contract_text']}\n\nSigned electronically by {ag['signed_name']} on {ag['signed_at']}."
        return send_file(io.BytesIO(text_to_pdf(body, "Agreement")), mimetype="application/pdf",
                         as_attachment=True, download_name="agreement.pdf")

    @app.get("/sign/<token>/rights.pdf")
    def client_rights_pdf(token):
        _client_case(token)
        return send_file(io.BytesIO(text_to_pdf(croa.DISCLOSURE, croa.DISCLOSURE_TITLE)), mimetype="application/pdf",
                         as_attachment=True, download_name="consumer-credit-file-rights.pdf")
