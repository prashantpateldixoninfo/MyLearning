from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
db = client["ping_app"]
collection = db["ping_results"]

def insert_ping(record):
    collection.insert_one(record)

def fetch_history():
    return list(collection.find({}, {"_id": 0}))
