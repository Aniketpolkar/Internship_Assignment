from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "task_manager"

client = AsyncIOMotorClient(MONGODB_URI)
database = client[DATABASE_NAME]

def get_database():
    return database

