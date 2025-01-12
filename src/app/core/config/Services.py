from .model import Config, ConfigDTO
from prisma.errors import RecordNotFoundError
from datetime import datetime
from ...Utils.auth import encryptPassword
from ...Utils.errors import ConfigDoesExistsError, ConfigDoesNotExistsError
from ...Config.db import conn
import json

class ConfigService:
    @staticmethod
    async def get_all() -> list[Config]:
        try:
            config: list[Config] = await conn.prisma.configuration.find_many()
        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return config

    @staticmethod
    async def get_config(id: int) -> Config:
        try:
            config: Config = await conn.prisma.configuration.find_many(where={"id": id})
            if config == []:
                raise ConfigDoesNotExistsError()

            config = config[0]
        except ConfigDoesNotExistsError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return config

    @staticmethod
    async def create(data: ConfigDTO) -> Config | bool | int:
        try:
            config_created = await conn.prisma.configuration.create(data={"proteinPerDay": data.proteinPerDay, "caloriesPerDay": data.caloriesPerDay, "fatPerDay":data.fatPerDay})
        except ConfigDoesExistsError:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return config_created
            
    @staticmethod
    async def update(data: ConfigDTO, id: int) -> None:
        try:
            config_exists = await ConfigService.get_config(id)

            if config_exists == []:
                raise ConfigDoesNotExistsError()

            print(data)
            config_updated = await conn.prisma.configuration.update(data={"proteinPerDay": data.proteinPerDay, "caloriesPerDay": data.caloriesPerDay, "fatPerDay":data.fatPerDay}, where={"id":id})
        except ConfigDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return config_updated

    @staticmethod
    async def delete(id: int) -> None:
        try:
            config_exists = await ConfigService.get_config(id)

            if config_exists == []:
                raise ConfigDoesNotExistsError()

            config_deleted = await conn.prisma.configuration.delete(where={"id":id})
        except ConfigDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return config_deleted
