from .model import User, UserDTO
from ..config.Services import ConfigService
from prisma.errors import RecordNotFoundError
from datetime import datetime
from ...Utils.auth import encryptPassword
from ...Utils.errors import UserDoesExistsError, UserDoesNotExistsError
from ...Config.db import conn

class UserService:
    @staticmethod
    async def get_all() -> list[User]:
        try:
            users: list[User] = await conn.prisma.user.find_many(include={"Configuration":True})
        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return users

    @staticmethod
    async def get_user(id: int) -> User:
        try:
            user: User = await conn.prisma.user.find_many(where={"user_id": id}, include={"Configuration":True, "food":True})

            if user == []:
                raise UserDoesNotExistsError()

            user = user[0]
        except UserDoesNotExistsError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return user

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        try:
            users: User = await conn.prisma.user.find_many(where={"email": email}, include={"Configuration":True})
            
            if users == []:
                return users

            user = users[0]
        except Exception as e:
            print(e)
            return False
        else:
            return user
        
    @staticmethod
    async def create(data: UserDTO) -> User | bool | int:
        try:
            if await UserService.get_user_by_email(data.email) != []:
                raise UserDoesExistsError()
            
            config_created = await ConfigService.create(data=data.config)

            user_data= {"config_id":config_created.id, "name":data.name, "email":data.email, "password":encryptPassword(data.password), "role":data.role}            

            print(config_created)
            user_post = await conn.prisma.user.create(data=user_data)
        except UserDoesExistsError:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return user_post
            
    @staticmethod
    async def update(data: UserDTO, id: int) -> None:
        try:
            user_exists = await UserService.get_user(id)

            if user_exists == []:
                raise UserDoesNotExistsError()

            config_update = await ConfigService.update(data=data.config, id=user_exists.config_id)

            user_update = await conn.prisma.user.update(data={"name":data.name, "email":data.email, "password":user_exists.password, "role":user_exists.role}, where={"user_id":id})
        except UserDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return user_update

    @staticmethod
    async def delete(id: int) -> None:
        try:
            user_exists = await UserService.get_user(id)

            if user_exists == []:
                raise UserDoesNotExistsError()
            else:
                user_deleted = await conn.prisma.user.delete(where={"user_id":id})
        except UserDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return user_deleted