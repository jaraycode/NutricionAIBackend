from pydantic import BaseModel

class Food(BaseModel):
    id: int
    user_id: int = 1
    name: str = "pollo"
    foodGr: float = 100.00
    calories: float = 100.00
    fat: float = 100.00
    protein: float = 100.00
    description: str | None = None

class FoodDTO(BaseModel):
    user_id: int = 1
    name: str = "pollo"
    foodGr: float = 100.00
    calories: float = 100.00
    fat: float = 100.00
    protein: float = 100.00
    description: str | None = None


class FoodFromModel(BaseModel):
    name: str = "pollo"