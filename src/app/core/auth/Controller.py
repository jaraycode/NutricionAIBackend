from .model import LogInDTO
from ..users.model import UserDTO, User
from ..users.Controller import UserController

class LoginController:
    @staticmethod
    async def logIn(data: LogInDTO):
        pass

    @staticmethod
    async def register(data: UserDTO) -> User | bool | int:
        return UserController.create(data)