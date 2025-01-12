from pydantic import BaseModel

class Config(BaseModel):
    config_id: int = 1
    calories: float = 99.00
    fat: float = 99.00
    protein: float = 99.00

class ConfigDTO(BaseModel):
    caloriesPerDay: float = 99.1
    fatPerDay: float = 99.1
    proteinPerDay: float = 99.1