import datetime
from uuid import UUID

from pydantic import BaseModel


class RoleGeneral(BaseModel):
    id: UUID
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
