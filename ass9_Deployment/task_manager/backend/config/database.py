# config/database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI not set")

DATABASE_NAME = "task_manager"

client = AsyncIOMotorClient(MONGODB_URI)
database = client[DATABASE_NAME]

async def check_mongo_connection():
    try:
        await client.admin.command("ping")
        # Avoid emojis for Windows console compatibility
        print("MongoDB Atlas connected successfully")
    except Exception as e:
        print("MongoDB connection failed")
        raise e

def get_database():
    return database
