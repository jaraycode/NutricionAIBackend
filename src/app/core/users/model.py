from pydantic import BaseModel
from datetime import datetime
from ..role.model import Role

class User(BaseModel):
    user_id: int
    name: str = "Jonas"
    last_name: str = "Aray"
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"
    birth_date: datetime | str = datetime.now()
    role: Role | None = None

class UserDTO(BaseModel):
    name: str = "Jonas"
    last_name: str = "Aray"
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"
    birth_date: datetime = datetime.now()
    role_id: int = 1