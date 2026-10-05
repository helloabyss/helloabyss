"""SQLite storage. Case data and uploaded documents are encrypted at rest with Fernet.

Signed CROA acknowledgments live in their own table and survive case deletion, because
§ 1679c(c) requires keeping them for 2 years.
"""

import json
import sqlite3
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, pw_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'consumer', org_id INTEGER, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS cases (
  id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
  title TEXT NOT NULL, data BLOB NOT NULL, status TEXT NOT NULL DEFAULT 'draft',
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY, case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  filename TEXT NOT NULL, mime TEXT NOT NULL, blob BLOB NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS acknowledgments (
  id INTEGER PRIMARY KEY, user_email TEXT NOT NULL, case_id INTEGER, signed_name TEXT NOT NULL,
  disclosure_sha256 TEXT NOT NULL, signed_at TEXT NOT NULL, ip TEXT, retain_until TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS agreements (
  id INTEGER PRIMARY KEY, case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  signed_name TEXT NOT NULL, signed_at TEXT NOT NULL, ip TEXT, contract_text TEXT NOT NULL,
  price_cents INTEGER NOT NULL, cancel_deadline TEXT NOT NULL, cancelled_at TEXT);
CREATE TABLE IF NOT EXISTS orgs (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, address TEXT NOT NULL,
  sub_status TEXT NOT NULL DEFAULT 'inactive', stripe_customer TEXT, stripe_subscription TEXT,
  created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS login_attempts (key TEXT NOT NULL, ts REAL NOT NULL);
CREATE INDEX IF NOT EXISTS login_attempts_key ON login_attempts(key);
CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY, case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  provider_ref TEXT, amount_cents INTEGER NOT NULL, status TEXT NOT NULL, paid_at TEXT);
"""


def now():
    return datetime.now().replace(microsecond=0).isoformat()


def db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_=None):
    d = g.pop("db", None)
    if d is not None:
        d.close()


# Columns added after the first release. init_db() adds any that are missing.
MIGRATIONS = {
    "users": {"email_verified": "INTEGER NOT NULL DEFAULT 0"},
    "cases": {"org_id": "INTEGER", "client_name": "TEXT", "client_email": "TEXT",
              "client_price_cents": "INTEGER", "sign_token": "TEXT"},
}


def init_db():
    db().executescript(SCHEMA)
    for table, cols in MIGRATIONS.items():
        have = {r["name"] for r in db().execute(f"PRAGMA table_info({table})")}
        for col, decl in cols.items():
            if col not in have:
                db().execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
    db().commit()


# ---- login throttling
MAX_FAILURES, WINDOW_SECONDS = 5, 15 * 60


def too_many_failures(*keys):
    cutoff = datetime.now().timestamp() - WINDOW_SECONDS
    db().execute("DELETE FROM login_attempts WHERE ts < ?", (cutoff,))
    return any(db().execute("SELECT COUNT(*) FROM login_attempts WHERE key=?", (k,)).fetchone()[0] >= MAX_FAILURES
               for k in keys)


def record_failure(*keys):
    for k in keys:
        db().execute("INSERT INTO login_attempts (key, ts) VALUES (?, ?)", (k, datetime.now().timestamp()))
    db().commit()


def clear_failures(*keys):
    for k in keys:
        db().execute("DELETE FROM login_attempts WHERE key=?", (k,))
    db().commit()


def _f():
    return Fernet(current_app.config["DATA_KEY"])


def enc(obj):
    return _f().encrypt(json.dumps(obj).encode())


def dec(blob):
    return json.loads(_f().decrypt(blob))


def enc_bytes(b):
    return _f().encrypt(b)


def dec_bytes(b):
    return _f().decrypt(b)


def empty_case():
    return {"consumer": None, "reports": [], "evidence": [], "assertions": [], "disputes": [],
            "furnisher_addresses": {}}


def load_case(case_id, user):
    """A case is visible to its creator, or to any member of the firm that owns it."""
    row = db().execute("SELECT * FROM cases WHERE id=? AND (user_id=? OR (org_id IS NOT NULL AND org_id=?))",
                       (case_id, user["id"], user["org_id"] or -1)).fetchone()
    return (row, dec(row["data"])) if row else (None, None)


def save_case(case_id, data, status=None):
    if status:
        db().execute("UPDATE cases SET data=?, status=?, updated_at=? WHERE id=?", (enc(data), status, now(), case_id))
    else:
        db().execute("UPDATE cases SET data=?, updated_at=? WHERE id=?", (enc(data), now(), case_id))
    db().commit()


def record_acknowledgment(email, case_id, name, sha, ip, years):
    signed = datetime.now()
    db().execute("INSERT INTO acknowledgments (user_email, case_id, signed_name, disclosure_sha256, signed_at, ip,"
                 " retain_until) VALUES (?,?,?,?,?,?,?)",
                 (email, case_id, name, sha, signed.isoformat(timespec="seconds"), ip,
                  (signed + timedelta(days=365 * years + 1)).date().isoformat()))
    db().commit()


def purge_expired_acknowledgments():
    db().execute("DELETE FROM acknowledgments WHERE retain_until < ?", (datetime.now().date().isoformat(),))
    db().commit()
