from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    user_id: int
    name: str
    last_name: str
    email: str
    password: str
    birth_date: date