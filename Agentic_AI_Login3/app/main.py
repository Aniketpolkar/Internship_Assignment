from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field, validator
from pymongo import MongoClient
from passlib.context import CryptContext
import uuid
import re
import random
from app.mcp_mail import send_otp
from app.security_agent import security_agent

app = FastAPI()

# MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.auth_db
users = db.users

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Utilities
# -----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# -----------------------------
# Schemas
# -----------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @validator("password")
    def validate_password(cls, v: str):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class VerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=4, max_length=4)


# -----------------------------
# Routes
# -----------------------------
@app.post("/register")
def register(data: RegisterRequest, request: Request):
    client_ip = request.client.host
    
    # 1. Check access (Blocked IP)
    allowed, message = security_agent.check_access(client_ip)
    if not allowed:
        security_agent.log_activity(client_ip, data.email, "register", "blocked", message)
        raise HTTPException(403, message)

    if users.find_one({"email": data.email}):
        security_agent.log_activity(client_ip, data.email, "register", "fail", "Email already registered")
        raise HTTPException(409, "Email already registered")

    # Generate random 4-digit OTP
    otp = str(random.randint(1000, 9999))

    users.insert_one({
        "email": data.email,
        "password": hash_password(data.password),
        "verified": False,
        "otp": otp
    })

    send_otp(data.email, otp)
    security_agent.log_activity(client_ip, data.email, "register", "success")

    return {"status": "check email for 4-digit verification code"}

@app.post("/login")
def login(data: LoginRequest, request: Request):
    client_ip = request.client.host
    
    # 1. Check access (Blocked IP/Email)
    allowed, message = security_agent.check_access(client_ip, data.email)
    if not allowed:
        security_agent.log_activity(client_ip, data.email, "login", "blocked", message)
        raise HTTPException(403, message)

    user = users.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password"]):
        security_agent.log_activity(client_ip, data.email, "login", "fail", "Invalid credentials")
        raise HTTPException(401, "Invalid credentials")

    # Removed mandatory verification check for login as per user request
    security_agent.log_activity(client_ip, data.email, "login", "success")
    return {"status": "login success"}

@app.post("/verify")
def verify(data: VerifyRequest):
    user = users.find_one({"email": data.email, "otp": data.otp})
    if not user:
        raise HTTPException(400, "Invalid email or OTP")

    users.update_one(
        {"_id": user["_id"]},
        {"$set": {"verified": True}, "$unset": {"otp": ""}}
    )

    return {"status": "verified successfully"}
