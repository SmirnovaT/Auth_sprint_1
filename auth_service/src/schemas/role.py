import datetime
import uuid

from pydantic import BaseModel


class RoleGeneral(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime
    created_at: datetime.datetime
