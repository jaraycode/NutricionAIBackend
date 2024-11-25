from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    name: str = "Jonas"
    last_name: str = "Aray"
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"
    birth_date: datetime = datetime.now()

class UserDTO(BaseModel):
    name: str = "Jonas"
    last_name: str = "Aray"
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"
    birth_date: datetime = datetime.now()