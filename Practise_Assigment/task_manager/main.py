from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
from database import engine
from models import Base, User, Task
from schemas import UserCreate, TaskCreate, TaskResponse, Token
from auth import get_db, hash_password, verify_password, create_access_token, get_current_user
from websocket_manager import manager
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# -------- AUTH --------

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# -------- TASKS --------

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    new_task = Task(title=task.title, owner_id=user.id)
    db.add(new_task)
    db.commit()
    await manager.broadcast("New task added")
    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.owner_id == user.id).all()

@app.put("/tasks/{task_id}")
async def update_task(task_id: int,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id,
                                 Task.owner_id == user.id).first()
    task.completed = True
    db.commit()
    await manager.broadcast("Task updated")
    return {"message": "Task updated"}

# -------- WEBSOCKET --------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)
