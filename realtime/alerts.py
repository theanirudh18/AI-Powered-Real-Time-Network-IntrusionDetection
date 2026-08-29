"""
==========================================================
Email Alert System
Sends an email when a high-confidence attack is detected.
Includes a per-attack-type cooldown so repeated detections
of the same attack type don't flood the inbox.
==========================================================
"""

import os
import smtplib
import time
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
ALERT_RECEIVER_EMAIL = os.getenv("ALERT_RECEIVER_EMAIL")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Minimum seconds between two emails for the SAME attack label,
# so a repeated PortScan doesn't send 50 emails in a minute.
ALERT_COOLDOWN_SECONDS = 120

_last_alert_time = {}


def _cooldown_ok(label):

    now = time.time()

    last = _last_alert_time.get(label)

    if last is not None and (now - last) < ALERT_COOLDOWN_SECONDS:
        return False

    _last_alert_time[label] = now

    return True


def send_email_alert(result):
    """
    Fires an email alert for a single detection result dict.
    Expects keys: label, confidence, source_ip, destination_ip,
    and optionally: destination_port, top_features, ports_scanned.
    Silently does nothing if email isn't configured, and never
    raises — a failed alert should never crash detection.
    """

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD or not ALERT_RECEIVER_EMAIL:
        print("[Alert] Email not configured — skipping alert.")
        return

    if "paste_your" in EMAIL_APP_PASSWORD:
        print("[Alert] App password placeholder still in .env — skipping alert.")
        return

    label = result.get("label", "Unknown")

    if not _cooldown_ok(label):
        return

    subject = f"[IDS Alert] {label} detected"

    lines = [
        f"Attack Type      : {label}",
        f"Confidence       : {result.get('confidence')}%",
        f"Source IP        : {result.get('source_ip')}",
        f"Destination IP   : {result.get('destination_ip')}",
    ]

    if result.get("destination_port"):
        lines.append(f"Destination Port : {result.get('destination_port')}")

    if result.get("ports_scanned"):
        lines.append(f"Ports Scanned    : {result.get('ports_scanned')}")

    top_features = result.get("top_features")

    if top_features:
        lines.append("")
        lines.append("Top Contributing Features:")
        for f in top_features[:5]:
            lines.append(f"  - {f['feature']}: {f['weight']}%")

    lines.append("")
    lines.append("This is an automated alert from your AI-Powered Real-Time IDS.")

    body = "\n".join(lines)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ALERT_RECEIVER_EMAIL

    try:

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

            server.starttls()

            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)

            server.sendmail(
                EMAIL_ADDRESS,
                ALERT_RECEIVER_EMAIL,
                msg.as_string()
            )

        print(f"[Alert] Email sent for {label}")

    except Exception as e:

        print(f"[Alert Error] Failed to send email: {e}")
