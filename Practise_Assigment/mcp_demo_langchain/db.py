# db.py
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"  # or your Atlas URI
client = MongoClient(MONGO_URI)
db = client["travel"]
forts_collection = db["forts"]
