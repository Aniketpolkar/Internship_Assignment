from fastapi import WebSocket
from typing import Dict, List
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        # key = user_id, value = list of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)
        print(f"WS connected → user_id={user_id}")
        print("Active connections:", self.active_connections.keys())

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"WS disconnected → user_id={user_id}")
        print("Active connections:", self.active_connections.keys())

    async def broadcast_to_all(self, message: dict):
        # send to every connected WebSocket
        for user_id, connections in self.active_connections.items():
            for ws in connections:
                try:
                    await ws.send_text(json.dumps(message))
                except Exception as e:
                    print(f"Error sending WS message to {user_id}: {e}")

    async def broadcast_task_update(self, action: str, task_data: dict, actor_id: str):
        # build the message
        message = {
            "type": "task_update",
            "action": action,  # created | updated | deleted
            "task": task_data,
            "actor_id": actor_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        print(f"Broadcasting '{action}' to all users, actor_id={actor_id}")
        await self.broadcast_to_all(message)

# single instance
manager = ConnectionManager()
