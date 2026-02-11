from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pydantic import EmailStr
import bcrypt
import os
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# DB
client = MongoClient(os.getenv("MONGO_URI"))
db = client.auth_db
users = db.users
events = db.login_events

# LLM
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --------- Models ---------
class LoginRequest(BaseModel):
    email: str
    password: str
    ip: str
    device_hash: str

# --------- Register Model ---------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
# --------- Agents ---------

def identity_risk_agent(user, device_hash):
    if device_hash not in user.get("known_devices", []):
        return 40
    return 5

def threat_agent(ip):
    # placeholder logic (replace with real intel feed)
    if ip.startswith("192."):
        return 10
    return 30

def llm_reasoning_agent(identity_risk, threat_risk):
    prompt = f"""
You are a security reasoning agent.
Return JSON only.

Identity risk: {identity_risk}
Threat risk: {threat_risk}

Decide recommended_action from:
ALLOW, REQUIRE_MFA, BLOCK
"""

    completion = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return completion.choices[0].message.content

# --------- Policy Engine ---------

def enforce_policy(identity_risk, threat_risk):
    total = identity_risk + threat_risk
    if total >= 80:
        return "BLOCK"
    elif total >= 40:
        return "REQUIRE_MFA"
    return "ALLOW"

# --------- Register Endpoint ---------
@app.post("/register")
def register(req: RegisterRequest):
    if users.find_one({"email": req.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    password_hash = bcrypt.hashpw(
        req.password.encode(),
        bcrypt.gensalt()
    )

    users.insert_one({
        "email": req.email,
        "password_hash": password_hash,
        "known_devices": [],
        "last_login": None,
        "created_at": datetime.utcnow()
    })

    return {"status": "registered successfully"}

# --------- Login Endpoint ---------

@app.post("/login")
def login(req: LoginRequest):
    user = users.find_one({"email": req.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(req.password.encode(), user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    identity_risk = identity_risk_agent(user, req.device_hash)
    threat_risk = threat_agent(req.ip)

    llm_advice = llm_reasoning_agent(identity_risk, threat_risk)
    decision = enforce_policy(identity_risk, threat_risk)

    events.insert_one({
        "user_id": user["_id"],
        "ip": req.ip,
        "device_hash": req.device_hash,
        "risk_score": identity_risk + threat_risk,
        "decision": decision,
        "llm_advice": llm_advice,
        "timestamp": datetime.utcnow()
    })

    return {
        "decision": decision,
        "risk_score": identity_risk + threat_risk
    }

