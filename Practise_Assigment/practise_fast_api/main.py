from fastapi import FastAPI, Depends, HTTPException
from database import get_database
from datetime import datetime
from schemas import UserCreate, UserResponse
from crud import create_user, get_user_by_email
from schemas import TaskCreate, TaskResponse
app = FastAPI()

@app.get("/")
def greet():
    return "Hello world"


@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db=Depends(get_database)):
    task_dict = task.dict()
    task_dict["created_at"] = datetime.utcnow()

    result = await db.tasks.insert_one(task_dict)

    return {
        "id": str(result.inserted_id),
        **task_dict
    }


@app.post("/users", response_model=UserResponse)
async def register_user(user: UserCreate, db=Depends(get_database)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = await create_user(db, user)
    return {
        "id": user_id,
        "email": user.email,
        "full_name": user.full_name
    }
