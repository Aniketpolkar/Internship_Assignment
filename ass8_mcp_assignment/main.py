from dotenv import load_dotenv

from mailer.notifier import EmailNotifier
from mcp.context_client import ContextClient
from mcp.gmail_client import GmailCalendarClient
from models import ScheduleSummary

load_dotenv()


def main():
    # Step 1: Fetch user context
    context_client = ContextClient()
    user = context_client.get_user_context()

    # Step 2: Fetch calendar events from Gmail calendar MCP server
    gmail_client = GmailCalendarClient()
    events = gmail_client.get_upcoming_events()

    
    # Step 3: Build summary
    summary = ScheduleSummary(email=user.email, events=events)
    # print(summary)

    # Step 4: Send email via Gmail SMTP
    notifier = EmailNotifier()
    notifier.send_schedule_email(summary)

    print("Schedule notification sent successfully.")


if __name__ == "__main__":
    main()
