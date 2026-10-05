"""Outbound email. Uses SMTP when SMTP_HOST is set; otherwise logs the message (development)
and, under testing, keeps it in app.config["OUTBOX"] so tests can follow links."""

import smtplib
from email.message import EmailMessage

from flask import current_app


def send(to, subject, body):
    cfg = current_app.config
    if cfg.get("TESTING"):
        cfg.setdefault("OUTBOX", []).append({"to": to, "subject": subject, "body": body})
        return
    if not cfg.get("SMTP_HOST"):
        current_app.logger.warning("Email not configured. To %s: %s\n%s", to, subject, body)
        return
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = cfg["MAIL_FROM"], to, subject
    msg.set_content(body)
    with smtplib.SMTP(cfg["SMTP_HOST"], int(cfg.get("SMTP_PORT", 587))) as s:
        s.starttls()
        if cfg.get("SMTP_USER"):
            s.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
        s.send_message(msg)
