from mcp.client import MCPClient
from models import UserContext
from config import MCP_CONTEXT_SERVER_URL


class ContextClient:
    def __init__(self):
        self.client = MCPClient(MCP_CONTEXT_SERVER_URL)

    def get_user_context(self) -> UserContext:
        result = self.client.call(
            method="context.getUser",
            params={}
        )

        return UserContext(**result)
