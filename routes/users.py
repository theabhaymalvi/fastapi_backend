from fastapi import APIRouter, HTTPException
from models import User
from db_connection import users_collection
from jose import jwt
import json
from bson import json_util
from passlib.context import CryptContext

SECRET_KEY = "cba13e8e0379de60466cfda50921e93a0ef229c4027b72af9b0efb33d4553909"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

router = APIRouter()

@router.get("/")
def users():
    return {"users": 'Abhay'}

@router.post("/register")
def register(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User is already registered")
    
    new_user = {
        'name': user.name,
        'email': user.email,
        'password': get_password_hash(user.password)
    }

    result = users_collection.insert_one(new_user)
    # when dict object is passed to insert in db, mongodb adds _id to document if not present
    # so we can pass dummy _id already in document also
    # new_user has _id of ObjectId type which is not json serializable, so remove _id before encoding json
    # or use json_util dumps to convert
    # insert_one returns InsertOneResult(ObjectId('65f7c4589a70e7db4b42e816'), acknowledged=True) as output
    # new_user = json.loads(json_util.dumps(new_user))
    new_user["_id"] = str(new_user["_id"])
    # new_user.pop('_id', None)
    encoded_jwt = None
    if result:
        encoded_jwt = jwt.encode(new_user, SECRET_KEY, algorithm=ALGORITHM)
    return {"authToken": encoded_jwt}

@router.post("/login")
def login(user: dict):
    try:
        result = users_collection.find_one({"email": user["email"]})

        if not result:
            raise HTTPException(status_code=400, detail="Please enter correct email address")
        
        password_match = verify_password(user["password"], result['password'])

        if not password_match:
            raise HTTPException(status_code=400, detail="Please enter correct password")
        
        result["_id"] = str(result["_id"])

        auth_token = jwt.encode(result, SECRET_KEY, algorithm=ALGORITHM)

        return {"authToken": auth_token}
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
