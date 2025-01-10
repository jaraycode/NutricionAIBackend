from pydantic import BaseModel

class Food(BaseModel):
    id: int
    name: str = "pollo"
    foodGr: float = 100.00
    calories: float = 100.00

class FoodDTO(BaseModel):
    name: str = "pollo"
    foodGr: float = 100.00
    calories: float = 100.00


class FoodFromModel(BaseModel):
    name: str = "pollo"