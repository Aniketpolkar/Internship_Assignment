from typing import List

from mcp.client import MCPClient
from models import CalendarEvent
from config import MCP_GMAIL_SERVER_URL


class GmailCalendarClient:
    def __init__(self):
        # Use the Gmail MCP server URL
        self.client = MCPClient(MCP_GMAIL_SERVER_URL)

    def get_upcoming_events(self, max_events: int = 5) -> List[CalendarEvent]:
        # Call the Gmail calendar RPC method exposed by gmail_mcp_server
        result = self.client.call(
            method="gmail.calendar.getUpcomingEvents",
            params={"limit": max_events},
        )

        return [CalendarEvent(**event) for event in result]
