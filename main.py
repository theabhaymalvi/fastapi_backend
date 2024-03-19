from fastapi import FastAPI
from routes import users, tasks
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")
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
