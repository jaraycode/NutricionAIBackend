from typing import Optional, TypeVar
from pydantic import BaseModel
from enum import Enum
T = TypeVar("T")

class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None

class Role(Enum):
    ADMIN = "ADMIN"
    USER = "USER"