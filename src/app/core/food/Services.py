from .model import Food, FoodDTO
from prisma.errors import RecordNotFoundError
from ...Utils.errors import FoodDoesExistsError, FoodDoesNotExistsError
from ...Config.db import conn
import tensorflow as tf
from tensorflow import convert_to_tensor, Tensor 
from tensorflow.keras import models #type:ignore
import pandas as pd
import numpy as np
import cv2

class FoodService:
    @staticmethod
    async def get_all() -> list[Food]:
        try:
            food: list[Food] = await conn.prisma.food.find_many()
        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return food

    @staticmethod
    async def get_food(id: int) -> Food:
        try:
            food: Food = await conn.prisma.food.find_many(where={"id": id})

            if food == []:
                raise FoodDoesNotExistsError()

            role = role[0]
        except FoodDoesNotExistsError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return role

    @staticmethod
    async def get_food_by_name(name: str) -> Food: # service to use for the image
        try:
            foods: list[Food] = await conn.prisma.food.find_many(where={"name": name})
            
            if foods == []:
                return foods

            food = foods[0]
        except Exception as e:
            print(e)
            return False
        else:
            return food

    @staticmethod
    async def get_food_by_image(img) -> Food: # service to use for the image
        try:
            img = cv2.resize(img, (100, 100))
            ds_img = convert_to_tensor(list(map(FoodService._toFloat, img)), tf.Float32)

            df_labels = pd.read_csv("../../../dataset/vista_minable/meta/labels.csv")
            df_labels.index = range(1, len(df_labels) + 1)
            foodName = df_labels.iloc[FoodService._model(ds=ds_img)].values[0]

            food: Food = await FoodService.get_food_by_name(foodName)
        except Exception as e:
            print(e)
            return False
        else:
            return food
        
    @staticmethod
    async def create(data: FoodDTO) -> Food | bool | int:
        try:
            if await FoodService.get_role_by_name(data.name) != []:
                raise FoodDoesExistsError()

            role_post = await conn.prisma.user.create(data=data)
        except FoodDoesExistsError:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return role_post
            
    @staticmethod
    async def update(data: FoodDTO, id: int) -> None:
        try:
            food_exists = await FoodService.get_role(id)

            if food_exists == []:
                raise FoodDoesNotExistsError()


            food_update = await conn.prisma.food.update(data=data, where={"id":id})
        except FoodDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return food_update

    @staticmethod
    async def delete(id: int) -> None:
        try:
            role_exists = await FoodService.get_food(id)

            if role_exists == []:
                raise FoodDoesNotExistsError()
            else:
                role_deleted = await conn.prisma.food.delete(where={"id":id})
        except FoodDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return role_deleted

    @staticmethod
    def _toFloat(img):
        return img/255.

    @staticmethod
    def _model(ds: Tensor):
        m = models.load_model("../../Utils/trainnedModel/nutricionAIModel.h5")
        prediction = m.predict(ds)
        return np.argmax(prediction[0])