import smtplib
import os
from pathlib import Path
from app.mcp_mail import send_otp

def test_otp_delivery(email: str):
    otp = "1234"
    try:
        print(f"Attempting to send OTP {otp} to {email}...")
        send_otp(email, otp)
        print(f"Success! Check logs for 'OTP successfully sent'.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    # Test with a dummy external email
    test_otp_delivery("test-external-recipient@example.com")
