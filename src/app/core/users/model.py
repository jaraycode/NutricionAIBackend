from pydantic import BaseModel
from ..config.model import Config, ConfigDTO
from prisma.enums import Role



class User(BaseModel):
    user_id: int
    name: str = "Jonas"
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"
    role: Role = Role.USER
    config: Config = Config(config_id=1, calories=99.00, fat=99.00, protein=99.00)

class UserDTO(BaseModel):
    name: str = "Jonas"
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"
    role: Role = Role.USER
    config: ConfigDTO = ConfigDTO(calories=99.00, fat=99.00, protein=99.00)