# from fastapi import FastAPI,APIRouter
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from config.database import get_database
# from models.schemas import (
#     UserCreate, UserResponse,Token
# )
# from routes.websocket import manager
# from auth.auth import (
#     hash_password, verify_password,
#     create_access_token
# )
# router = APIRouter()

# # ---------- REGISTER ----------
# @router.post("/register", response_model=UserResponse)
# async def register(user: UserCreate, db=Depends(get_database)):
#     existing = await db.users.find_one({"email": user.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     result = await db.users.insert_one({
#         "email": user.email,
#         "hashed_password": hash_password(user.password)
#     })

#     return {"id": str(result.inserted_id), "email": user.email}


# # ---------- LOGIN ----------
# @router.post("/login", response_model=Token)
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db=Depends(get_database)
# ):
#     user = await db.users.find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": str(user["_id"])})
#     return {"access_token": token, "token_type": "bearer"}

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config.database import get_database
from models.schemas import UserCreate, UserResponse, Token
from auth.auth import hash_password, verify_password, create_access_token

router = APIRouter()

# ---------- REGISTER ----------
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db=Depends(get_database)):
    print("hello")
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "email": user.email,
        "hashed_password": hash_password(user.password)
    }
    print(user.email)

    result = await db.users.insert_one(user_doc)

    return {
        "id": str(result.inserted_id),
        "email": user.email
    }


# ---------- LOGIN ----------
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_database)
):
    user = await db.users.find_one({"email": form_data.username})

    # 🔒 SAFE CHECK (prevents KeyError)
    if (
        not user
        or "hashed_password" not in user
        or not verify_password(form_data.password, user["hashed_password"])
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
