from .model import LogInDTO, LogInResponse
from ..users.model import UserDTO, User
from ..users.Services import UserService # type: ignore
from ...Utils.auth import generateJWToken, validatePassword

class LoginService:
    @staticmethod
    async def logIn(data: LogInDTO):
        try:
            user_retrived = await UserService.get_user_by_email(email=data.email) 
            
            if user_retrived == []:
                return 1
                
            if not validatePassword(data.password, user_retrived.password):
                return 2

        except Exception as e:
            print(e)
            return False
        else:
            return LogInResponse(email=user_retrived.email, token=generateJWToken(user_retrived.email))

    @staticmethod
    async def register(data: UserDTO) -> User | bool | int:
        return UserService.create(data)