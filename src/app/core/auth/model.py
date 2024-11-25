from pydantic import BaseModel

class LogInDTO(BaseModel):
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"