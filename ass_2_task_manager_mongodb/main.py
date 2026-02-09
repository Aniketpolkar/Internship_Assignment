from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from routes import authRoute
from routes import taskRoute
from config.database import get_database
from models.schemas import (
    UserCreate, UserResponse,Token,
    TaskCreate, TaskResponse,TaskUpdate
)
from auth.auth import (
    hash_password, verify_password,
    create_access_token, get_current_user, get_current_user_ws
)
from routes.websocket import manager

app = FastAPI()
app.include_router(authRoute.router)
app.include_router(taskRoute.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    current_user = await get_current_user_ws(token)
    if not current_user:
        await websocket.close(code=1008)
        return

    user_id = str(current_user["_id"])
    await manager.connect(websocket, user_id)

    try:
        while True:
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)