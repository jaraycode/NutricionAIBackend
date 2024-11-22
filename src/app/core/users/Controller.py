from .model import User
from prisma.errors import RecordNotFoundError
from datetime import datetime, date
from ...Utils.auth import encryptPassword
from ...Utils.errors import UserDoesExistsError, UserDoesNotExistsError
from ...Config.db import conn
import json

class UserController:
    @staticmethod
    async def get_all()-> list[User]:
        try:
            users: list[User] = await conn.prisma.user.find_many()
            for user in users:
                user.birth_date = user.birth_date.strftime("%Y-%m-%d")
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
            user: User = await conn.prisma.user.find_many(where={"user_id": id})
            # print(user[0])
            if user == []:
                raise UserDoesNotExistsError()

            user = user[0]
            user.birth_date = user.birth_date.strftime("%Y-%m-%d")
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
            user: User = await conn.prisma.user.find_many(where={"email": email})[0]
            user.birth_date = user.birth_date.strftime("%Y-%m-%d")
        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return user
        
    @staticmethod
    async def create(data: User) -> None:
        try:
            if await UserController.get_user_by_email(data.email) != []:
                raise UserDoesExistsError()

            user_data = {"email":data.email, "last_name":data.last_name, "name":data.name,"birth_date":datetime.strptime(data.birth_date.strftime("%Y-%m-%d"), "%Y-%m-%d"), "password":encryptPassword(data.password)}

            user_post = await conn.prisma.user.create(user_data)
        except UserDoesExistsError:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return user_post
            
    @staticmethod
    async def update(data: User, id: int) -> None:
        try:
            if await UserController.get_user(id) == []:
                raise RecordNotFoundError(data, message=f"User by id {id} is not found")
            user_data = {"email":data.email, "last_name":data.last_name, "name":data.name,"birth_date":datetime.strptime(data.birth_date.strftime("%Y-%m-%d"), "%Y-%m-%d"), "password":encryptPassword(data.password)}

            user_update = await conn.prisma.user.update(data=user_data)
        except RecordNotFoundError as e:
            print(e)
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return user_update

    @staticmethod
    async def delete(id: int) -> None:
        try:
            user_exists = await UserController.get_user(id)

            if user_exists == []:
                raise RecordNotFoundError(message=f"User with id:{id}, does not exists")
            else:
                # user_post = await conn.prisma.user.create({"birth_date": data.birth_date, "email": data.email, "last_name": data.last_name, "name": data.name, "password": encryptPassword(data.password)})
                pass
        except:
            pass
        else:
            # return user_post
            pass

    @staticmethod
    def _serialize_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()