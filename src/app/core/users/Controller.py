from .model import User
from prisma.errors import RecordNotFoundError
from datetime import datetime
from ...Utils.auth import encryptPassword
from ...Config.db import conn
import json

class UserController:
    @staticmethod
    async def get_all()-> list[User]:
        try:
            users: list[User] = await conn.prisma.user.find_many()
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
# "birth_date": json.dumps(data.birth_date, default=UserController._serialize_datetime)
            user_data = {"email":data.email, "last_name":data.last_name, "name":data.name, "password":encryptPassword(data.password)}
            user_post = await conn.prisma.user.create(user_data)
        except Exception as e:
            print(e)
            return False
        else:
            return user_data
            
    @staticmethod
    async def update(data: User) -> None:
        try:
            user_exists = await UserController.get_user(data.user_id)

            if user_exists == []:
                raise RecordNotFoundError(data, message="User does not exists")
            else:
                user_post = await conn.prisma.user.create({"birth_date": data.birth_date, "email": data.email, "last_name": data.last_name, "name": data.name, "password": encryptPassword(data.password)})
        except Exception as e:
            print(e)
            return False
        else:
            return user_post

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