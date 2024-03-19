from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values('.env')

conn = MongoClient(config['DB_URL'])
db = conn['fastapi']

users_collection = db['users']
tasks_collection = db['tasks']