from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Role
from src.db.postgres import get_session
from src.repositories.base import BaseRepository
from src.schemas.role import RoleRead

PERMISSIONS = {
    "can_perform_roles": ["admin"],
}


class RoleService:
    """Имплементация класса для взаимодействия с ролями пользователей"""

    def __init__(
        self,
        db: AsyncSession = Depends(get_session),
        repository: BaseRepository = Depends(BaseRepository),
    ):
        self.repository = repository
        self.db = db

    async def create_role(self, role_name: str) -> RoleRead:
        """Создание новой роли"""

        role_already_exist = await self.db.scalar(
            select(Role).where(Role.name == role_name)
        )
        if role_already_exist:
            raise HTTPException(
                status_code=409, detail=f"Роль с названием '{role_name}' уже существует"
            )

        new_role = await self.repository.create(Role(name=role_name))

        return new_role
