import threading
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def _send_telegram(message: str):
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            logger.warning("Telegram credentials not configured. Skipping telegram alert.")
            return

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            logger.info("Telegram alert sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")

    @staticmethod
    def _send_email(subject: str, body: str):
        if not all([settings.SMTP_SERVER, settings.SMTP_USER, settings.SMTP_PASS, settings.ALERT_EMAIL]):
            logger.warning("SMTP credentials not configured. Skipping email alert.")
            return

        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = settings.ALERT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg)
            server.quit()
            logger.info("Email alert sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send Email alert: {e}")

    @classmethod
    def dispatch_alert(cls, alert_type: str, severity: str, camera_id: str, description: str):
        """Dispatches an alert to all configured channels asynchronously."""
        # Only notify for high/critical priority
        if severity not in ['high', 'critical']:
            return

        subject = f"[{severity.upper()}] Sentinel AI Alert: {alert_type.replace('_', ' ').title()}"
        
        # HTML formatting
        body = f"""
        <b>🚨 SENTINEL AI ALERT 🚨</b><br><br>
        <b>Type:</b> {alert_type.replace('_', ' ').title()}<br>
        <b>Severity:</b> {severity.upper()}<br>
        <b>Camera ID:</b> {camera_id}<br>
        <b>Description:</b> {description}<br><br>
        <i>Please check the dashboard immediately.</i>
        """

        # Dispatch via threads to avoid blocking AI loop
        threading.Thread(target=cls._send_telegram, args=(body,), daemon=True).start()
        threading.Thread(target=cls._send_email, args=(subject, body), daemon=True).start()
