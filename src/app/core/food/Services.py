from .model import Food, FoodDTO, FoodFromModel
from prisma.errors import RecordNotFoundError
from ...Utils.errors import FoodDoesExistsError, FoodDoesNotExistsError
from ...Config.db import conn
import tensorflow as tf
from tensorflow import convert_to_tensor, Tensor 
from tensorflow.keras import models #type:ignore
import tensorflow as tf
import pandas as pd
import numpy as np
import cv2, os

MODEL = "src/model/my_model.keras"
model = models.load_model(os.path.join(MODEL))


class FoodService:
    LABELS = "dataset/vista_minable/meta"

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
    async def get_food_by_image(img) -> FoodFromModel: # service to use for the image
        try:
            img = cv2.resize(img, (100, 100))
            img = img.reshape((1,100,100,3))
            img = list(map(FoodService._toFloat, img))
            ds_img = convert_to_tensor(img, tf.float32)

            df_labels = pd.read_csv(os.path.join(FoodService.LABELS, "labels.csv"))
            df_labels.index = range(1, len(df_labels) + 1)
            response = FoodService._model(ds=ds_img)
            foodName = df_labels.iloc[response].values[0]

            print(foodName)
            food: FoodFromModel = FoodFromModel(name=foodName)

            # food: Food = await FoodService.get_food_by_name(foodName)
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
        prediction = model.predict(ds)
        return np.argmax(prediction[0])