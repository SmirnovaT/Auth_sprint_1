from pydantic import BaseModel


class RoleRead(BaseModel):
    name: str
