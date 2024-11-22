from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    name: str
    last_name: str
    email: str
    password: str
    # birth_date: datetime

class User_payload(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    birth_date: datetime