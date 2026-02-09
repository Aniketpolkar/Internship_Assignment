from passlib.context import CryptContext
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(db, user):
    user_dict = {
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "full_name": user.full_name
    }
    result = await db.users.insert_one(user_dict)
    return str(result.inserted_id)

async def get_user_by_email(db, email: str):
    return await db.users.find_one({"email": email})
