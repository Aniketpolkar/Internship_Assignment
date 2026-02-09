import smtplib
from email.mime.text import MIMEText
from models import ScheduleSummary
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD


class EmailNotifier:
    def send_schedule_email(self, summary: ScheduleSummary):
        body_lines = ["Your upcoming schedule:\n"]

        for event in summary.events:
            body_lines.append(
                f"- {event.subject} | "
                f"{event.start.strftime('%Y-%m-%d %H:%M')} -> "
                f"{event.end.strftime('%H:%M')}"
            )

        body = "\n".join(body_lines)

        msg = MIMEText(body)
        msg["Subject"] = "Your Upcoming Schedule"
        msg["From"] = SMTP_USERNAME 
        msg["To"] = summary.email

        if not SMTP_USERNAME or not SMTP_PASSWORD:
            print("Warning: SMTP_USERNAME or SMTP_PASSWORD not set. Printing email to console instead:")
            print("=" * 40)
            print(f"Subject: {msg['Subject']}")
            print(f"From: {msg['From']}")
            print(f"To: {msg['To']}")
            print("\n" + body)
            print("=" * 40)
            return

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
                print(f"Email sent successfully to {summary.email}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            print("Printing email to console instead:")
            print("=" * 40)
            print(f"Subject: {msg['Subject']}")
            print(f"From: {msg['From']}")
            print(f"To: {msg['To']}")
            print("\n" + body)
            print("=" * 40)
