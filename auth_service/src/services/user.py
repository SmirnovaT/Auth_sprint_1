from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.postgres import get_session
from src.schemas.user import UserCreate, UserInDB
from src.repositories.user import UserRepository


class UserService:
    """Сервис для взаимодействия с моделью User"""

    def __init__(
        self,
        db: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(),
    ):
        self.repository = repository
        self.db = db

    async def register(self, user_create: UserCreate) -> UserInDB:
        """Регистрация пользователя"""

        user_dto = jsonable_encoder(user_create)
        user = User(**user_dto)
        return await self.repository.create_user(user)

    async def get_user(self, login):
        """Получение всех ролей, заведенных в сервисе"""

        user = await self.repository.get_user(login)
        return user