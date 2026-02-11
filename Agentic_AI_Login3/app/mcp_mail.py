import smtplib
import os
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, formatdate, make_msgid
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

if not SMTP_USER or not SMTP_PASS:
    raise ValueError("SMTP_USER and SMTP_PASS must be set in .env file")

def send_otp(email: str, otp: str):
    # Use MIMEMultipart("alternative") for better compatibility
    msg = MIMEMultipart("alternative")
    
    # Subject: Concise and professional
    msg["Subject"] = "Your Verification Code"
    
    # From: Using the actual sender name if possible, or a generic but authentic name
    msg["From"] = formataddr(("Security Team", SMTP_USER))
    msg["To"] = email
    msg["Reply-To"] = SMTP_USER
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    
    # Content: Simplified and centered on the OTP
    text = (
        f"Hello,\n\n"
        f"Your verification code is: {otp}\n\n"
        f"Please enter this code on the registration page to verify your account.\n"
        f"This code will expire soon. If you didn't request this, please ignore this email.\n"
    )
    
    html = f"""
    <html>
      <body style="font-family: sans-serif; text-align: center; padding: 20px;">
        <div style="max-width: 400px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
          <h2 style="color: #333;">Verify your email address</h2>
          <p>Hello,</p>
          <p>Thanks for signing up! Use the code below to verify your email address:</p>
          <h1 style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; letter-spacing: 5px; color: #007bff;">{otp}</h1>
          <p style="font-size: 0.9em; color: #666;">Enter this code to complete your registration.</p>
          <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
          <p style="font-size: 0.8em; color: #999;">If you didn't create an account, you can safely ignore this email.</p>
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        print(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            # Explicitly pass from and to addresses
            s.send_message(msg, from_addr=SMTP_USER, to_addrs=[email])
        print(f"OTP successfully sent to {email}")
    except smtplib.SMTPAuthenticationError:
        print(f"SMTP Authentication failed for {SMTP_USER}. Check app password.")
        raise
    except smtplib.SMTPException as e:
        print(f"SMTP error sending OTP to {email}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error sending OTP to {email}: {e}")
        raise
