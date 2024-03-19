from pymongo import MongoClient
import os
# from dotenv import dotenv_values

# config = dotenv_values('.env')

conn = MongoClient(os.environ.get("DB_URL"))
if conn:
    print(conn)
db = conn['fastapi']

users_collection = db['users']
tasks_collection = db['tasks']