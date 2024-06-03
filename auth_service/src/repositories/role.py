from fastapi import HTTPException
from sqlalchemy import select

from src.db import models
from src.db.models import Role
from src.repositories.base import BaseRepository
from src.schemas.role import RoleGeneral


class RoleRepository(BaseRepository):
    """Репозиторий для взаимодействия с моделью Role"""

    model = models.Role

    async def get_roles(self) -> list[RoleGeneral]:
        """Получение всех ролей"""

        return await self.get(self.model)

    async def create_role(self, role_name: str) -> RoleGeneral:
        """Создание роли"""

        role_already_exist = await self.db.scalar(
            select(Role).where(self.model.name == role_name)
        )
        if role_already_exist:
            raise HTTPException(
                status_code=409, detail=f"Роль с названием '{role_name}' уже существует"
            )

        created_role = await self.create(Role(name=role_name))

        return created_role

    async def remove_role(self, role_name: str) -> None:
        """Удаление роли"""

        role_to_delete = await self.db.scalar(
            select(Role).where(self.model.name == role_name)
        )
        if not role_to_delete:
            raise HTTPException(
                status_code=409, detail=f"Роли с названием '{role_name}' не существует"
            )

        await self.delete(role_to_delete)

