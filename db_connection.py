from pymongo import MongoClient
import os

conn = MongoClient(os.environ.get("DB_URL"))
if conn:
    print(conn)

    db = conn.get_database("taskify")

    users_collection = db.get_collection("users")
    tasks_collection = db.get_collection("tasks")