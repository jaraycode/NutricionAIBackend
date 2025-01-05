from pydantic import BaseModel

class Role(BaseModel):
    id: int
    name: str = "admin"

class RoleDTO(BaseModel):
    name: str = "admin"