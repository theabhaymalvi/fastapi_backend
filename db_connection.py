from pymongo import MongoClient
import os

conn = MongoClient(os.environ.get("DB_URL"))
if conn:
    if "pool" not in conn.list_database_names():
        conn.create_database("pool")
    db = conn.get_database("pool")

    if "users" not in db.list_collection_names():
        db.create_collection("users")

    if "tasks" not in db.list_collection_names():
        db.create_collection("tasks")
        
    users_collection = db.get_collection("users")
    tasks_collection = db.get_collection("tasks")