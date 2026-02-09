import os

MCP_CONTEXT_SERVER_URL = os.getenv(
    "MCP_CONTEXT_SERVER_URL",
    "http://localhost:3333"
)

# Gmail calendar MCP server URL
MCP_GMAIL_SERVER_URL = os.getenv(
    "MCP_GMAIL_SERVER_URL",
    "http://localhost:4444"
)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "aniketpolkar@gmail.com"
SMTP_PASSWORD = "eqwpjetnjefvltpk"

# SMTP_USERNAME = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")