import time
import config

class AlertSystem:
    """
    Handles sending notifications to admins via Email, Telegram, and Webhooks.
    Currently runs in 'Simulation Mode' to demonstrate logic without needing real API keys.
    """
    
    @staticmethod
    def send_email(subject, body):
        # In a real app, you would use smtplib here.
        print(f"\n[📧 EMAIL ALERT] To: {config.ADMIN_EMAIL}")
        print(f"Subject: {subject}")
        print(f"Body: {body}\n")

    @staticmethod
    def send_telegram(message):
        # In a real app, we would use requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage"...)
        print(f"\n[📲 TELEGRAM ALERT] Chat ID: {config.TELEGRAM_CHAT_ID}")
        print(f"Message: {message}\n")

    @staticmethod
    def send_webhook(data):
        # In a real app, we would use requests.post(config.WEBHOOK_URL, json=data)
        print(f"\n[🌐 WEBHOOK TRIGGER] POST {config.WEBHOOK_URL}")
        print(f"Payload: {data}\n")

    @staticmethod
    def notify_admin(issue_type, message):
        """
        Facade function to send alerts to ALL channels at once.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] 🚨 {issue_type}: {message}"
        
        AlertSystem.send_email(f"CRITICAL: {issue_type}", formatted_msg)
        AlertSystem.send_telegram(formatted_msg)
        AlertSystem.send_webhook({"type": issue_type, "message": message, "ts": timestamp})