from .model import Role, RoleDTO
from prisma.errors import RecordNotFoundError
from ...Utils.errors import RoleDoesExistsError, RoleDoesNotExistsError
from ...Config.db import conn

class RoleService:
    @staticmethod
    async def get_all() -> list[Role]:
        try:
            roles: list[Role] = await conn.prisma.role.find_many()
        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return roles

    @staticmethod
    async def get_role(id: int) -> Role:
        try:
            role: Role = await conn.prisma.role.find_many(where={"id": id})

            if role == []:
                raise RoleDoesNotExistsError()

            role = role[0]
        except RoleDoesNotExistsError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return role

    @staticmethod
    async def get_role_by_name(name: str) -> Role:
        try:
            roles: Role = await conn.prisma.role.find_many(where={"name": name})
            
            if roles == []:
                return roles

            role = roles[0]
        except Exception as e:
            print(e)
            return False
        else:
            return role
        
    @staticmethod
    async def create(data: RoleDTO) -> Role | bool | int:
        try:
            if await RoleService.get_role_by_name(data.name) != []:
                raise RoleDoesExistsError()

            role_post = await conn.prisma.user.create(data=data)
        except RoleDoesExistsError:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return role_post
            
    @staticmethod
    async def update(data: RoleDTO, id: int) -> None:
        try:
            role_exists = await RoleService.get_role(id)

            if role_exists == []:
                raise RoleDoesNotExistsError()


            role_update = await conn.prisma.role.update(data=data, where={"id":id})
        except RoleDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return role_update

    @staticmethod
    async def delete(id: int) -> None:
        try:
            role_exists = await RoleService.get_role(id)

            if role_exists == []:
                raise RoleDoesNotExistsError()
            else:
                role_deleted = await conn.prisma.role.delete(where={"id":id})
        except RoleDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return role_deleted