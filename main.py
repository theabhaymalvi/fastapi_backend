from fastapi import FastAPI
from routes import users, tasks
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

# DB CONNECTION
conn = MongoClient(os.environ.get("DB_URL"))
if conn:
    print(conn)
db = conn['taskify']

# if "users" not in db.list_collection_names():
#     db.create_collection("users")

# if "tasks" not in db.list_collection_names():
#     db.create_collection("tasks")

# users_collection = db['users']
# tasks_collection = db['tasks']
#-----------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/')
def home():
    return {"data": 'Welcome to the page'}

app.include_router(users.router, prefix="/users")
app.include_router(tasks.router, prefix="/tasks")
