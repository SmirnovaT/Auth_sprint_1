from src.db import models
from src.db.models import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserInDB


class UserRepository(BaseRepository):
    """Репозиторий для взаимодействия с моделью User"""

    model = models.User

    async def create_user(self, user: User) -> UserInDB:
        """Создание пользователя"""

        return await self.create(user)

    async def get_users(self) -> UserInDB:
        """Получение всех пользователей"""

        return await self.get(self.model)

    async def get_user_by_login(self, login: str) -> UserInDB:
        """Получение пользователя по логину"""

        users =  await self.get(self.model)
        return users[0]
