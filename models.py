from pydantic import BaseModel, Field, validator
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    password: str = Field(..., min_length=4, max_length=15)

class Task(BaseModel):
    userId: str
    title: str = Field(..., min_length=3, max_length=30)
    dueDate: Optional[str] = None
    dueTime: Optional[str] = None
    description: Optional[str] = None
    important: bool
    urgent: bool
    completed: Optional[bool] = False

@validator('title')
def title_length(cls, v):
    if len(v) < 3:
        raise ValueError('Title length must be at least 3')
    elif len(v) > 20:
        raise ValueError('Title length must be at most 20')
    return v