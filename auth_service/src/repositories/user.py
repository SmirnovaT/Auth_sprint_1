from fastapi import HTTPException
from sqlalchemy import select

from src.db import models
from src.db.models import Role, User
from src.repositories.base import BaseRepository
from src.schemas.user import UserInDB, UserInDBWRole


class UserRepository(BaseRepository):
    """Репозиторий для взаимодействия с моделью User"""

    model = models.User

    async def create_user(self, user: User) -> UserInDB:
        """Создание пользователя"""

        return await self.create(user)

    async def update_user_role(self, login: str, role_id: str) -> UserInDBWRole:
        """Изменение роли пользователя"""

        user_to_update = await self.db.scalar(
            select(User).where(self.model.login == login)
        )
        if not user_to_update:
            raise HTTPException(
                status_code=404, detail=f"Пользователя с login '{login}' не существует"
            )

        role = await self.db.scalar(select(Role).where(Role.id == role_id))
        if not role:
            raise HTTPException(
                status_code=404, detail=f"Роли с id '{role_id}' не существует"
            )

        user_to_update.role_id = role_id
        updated_user = await self.update(user_to_update)

        return updated_user

    async def remove_user_role(self, login: str, role_id: str) -> None:
        """Удаление роли у пользователя"""

        user_to_role_delete = await self.db.scalar(
            select(User).where(self.model.login == login)
        )
        if not user_to_role_delete:
            raise HTTPException(
                status_code=404, detail=f"Пользователя с login '{login}' не существует"
            )

        role = await self.db.scalar(select(Role).where(Role.id == role_id))
        if not role:
            raise HTTPException(
                status_code=404, detail=f"Роли с id '{role_id}' не существует"
            )

        user_to_role_delete.role_id = None
        await self.update(user_to_role_delete)

    async def get_users(self) -> UserInDB:
        """Получение всех пользователей"""

        return await self.get(self.model)

    async def get_user_by_login(self, login: str) -> UserInDB:
        """Получение пользователя по логину"""

        users =  await self.get(self.model)
        return users[0]
