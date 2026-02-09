from fastapi import APIRouter,FastAPI
from config.database import get_database
from models.schemas import (
  TaskCreate, TaskResponse,TaskUpdate
)

from routes.websocket import manager

from fastapi import FastAPI, Depends, HTTPException 
from datetime import datetime

from bson import ObjectId
from auth.auth import (
    hash_password, verify_password,
    create_access_token, get_current_user, get_current_user_ws
)
router = APIRouter(tags=["tasks"])

# # ---------- CREATE TASK (PROTECTED) ----------
@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate,current_user=Depends(get_current_user), db=Depends(get_database)):
    task_data = task.dict()
    task_data["user_id"] = current_user["_id"]
    task_data["created_at"] = datetime.utcnow()

    result = await db.tasks.insert_one(task_data)
    created_task = {
    "id": str(result.inserted_id),
    "title": task_data["title"],
    "description": task_data.get("description"),
    "completed": task_data.get("completed", False),
    "created_at": task_data["created_at"].isoformat()  # convert datetime to string
}
    await manager.broadcast_task_update(
    action="created",
    task_data=created_task,
    actor_id=str(current_user["_id"])
)
    return created_task

@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(db=Depends(get_database),current_user=Depends(get_current_user)):
    tasks = []
    
    async for task in db.tasks.find({"user_id": current_user["_id"]}):
        tasks.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task.get("description"),
            "completed": task["completed"],
            "created_at": task["created_at"]
        })
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    db=Depends(get_database),
    current_user=Depends(get_current_user)
):
    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # Find task owned by current user
    existing_task = await db.tasks.find_one({
        "_id": ObjectId(task_id),
        "user_id": current_user["_id"]
    })

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = {k: v for k, v in task.dict().items() if v is not None}

    if update_data:
        await db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )

    updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})

    task_response = {
    "id": str(updated_task["_id"]),
    "title": updated_task["title"],
    "description": updated_task.get("description"),
    "completed": updated_task["completed"],
    "created_at": updated_task["created_at"].isoformat()  # convert to string
}

    await manager.broadcast_task_update(
    action="updated",
    task_data=task_response,
    actor_id=str(current_user["_id"])
    )

    return task_response


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)
):
    # Validate ObjectId
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    # Find task owned by current user
    existing_task = await db.tasks.find_one({
        "_id": ObjectId(task_id),
        "user_id": current_user["_id"]
    })

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete the task
    await db.tasks.delete_one({"_id": ObjectId(task_id)})

    deleted_task = {
    "id": str(existing_task["_id"]),
    "title": existing_task["title"],
    "description": existing_task.get("description"),
    "completed": existing_task["completed"],
    "created_at": existing_task["created_at"].isoformat()  # convert to string
}

    await manager.broadcast_task_update(
    action="deleted",
    task_data=deleted_task,
    actor_id=str(current_user["_id"])
)

    return {"message": "Task deleted successfully"}