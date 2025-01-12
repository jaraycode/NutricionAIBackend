from .model import Food, FoodDTO, FoodFromModel
from ..users.Services import UserService
from prisma.errors import RecordNotFoundError
from ...Utils.errors import FoodDoesExistsError, FoodDoesNotExistsError, UserDoesNotExistsError
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
            food: Food = await conn.prisma.food.find_many(where={"id": id}, include={"user": True})

            if food == []:
                raise FoodDoesNotExistsError()

            food = food[0]
        except FoodDoesNotExistsError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return food

    @staticmethod
    async def get_food_by_user_id(id: int) -> Food:
        try:
            food: Food = await conn.prisma.food.find_many(where={"user_id": id}, include={"user": True})

            if food == []:
                raise FoodDoesNotExistsError()

        except FoodDoesNotExistsError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return food

    @staticmethod
    async def get_food_by_name(name: str) -> Food:
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

            food: FoodFromModel = FoodFromModel(name=foodName)

        except Exception as e:
            print(e)
            return False
        else:
            return food
        
    @staticmethod
    async def create(data: FoodDTO) -> Food | bool | int:
        try:
            if await UserService.get_user(data.user_id) == []:
                raise UserDoesNotExistsError()

            food_post = await conn.prisma.food.create(data={"name": data.name, "calories": data.calories, "fat": data.fat, "protein":data.protein, "foodGr": data.foodGr, "user_id": data.user_id, "Description": data.description})
        except FoodDoesExistsError:
            return 1
        except UserDoesNotExistsError:
            return 2
        except Exception as e:
            print(e)
            return False
        else:
            return food_post
            
    @staticmethod
    async def update(data: FoodDTO, id: int) -> None:
        try:
            food_exists = await FoodService.get_food(id)

            if food_exists == []:
                raise FoodDoesNotExistsError()

            food_update = await conn.prisma.food.update(data={"name": data.name, "calories": data.calories, "fat": data.fat, "protein":data.protein, "foodGr": data.foodGr, "user_id": food_exists.user_id, "Description":data.description}, where={"id":id})
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
            food_exists = await FoodService.get_food(id)

            if food_exists == []:
                raise FoodDoesNotExistsError()
            else:
                food_deleted = await conn.prisma.food.delete(where={"id":id})
        except FoodDoesNotExistsError as e:
            return 1
        except Exception as e:
            print(e)
            return False
        else:
            return food_deleted

    @staticmethod
    def _toFloat(img):
        return img/255.

    @staticmethod
    def _model(ds: Tensor):
        prediction = model.predict(ds)
        return np.argmax(prediction[0])