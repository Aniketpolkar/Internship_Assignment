import requests
import uuid

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def call(self, method: str, params: dict):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()

        data = response.json()
        if "error" in data:
            raise RuntimeError(data["error"])

        return data["result"]
