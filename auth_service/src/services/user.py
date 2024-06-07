from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.core.config import settings
from src.db.models import User
from src.db.postgres import get_session
from src.db.cache import AsyncCacheService
from src.schemas.user import UserCreate, UserInDB, UserInDBWRole
from src.repositories.user import UserRepository
from src.utils.jwt import validate_token, create_access_and_refresh_tokens


class UserService:
    """Сервис для взаимодействия с моделью User"""

    def __init__(
        self,
        cache: AsyncCacheService = Depends(AsyncCacheService),
        db: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(),
    ):
        self.cache = cache
        self.repository = repository
        self.db = db

    async def register(self, user_create: UserCreate) -> UserInDB:
        """Регистрация пользователя"""

        user_dto = jsonable_encoder(user_create)
        user = User(**user_dto)
        return await self.repository.create_user(user)

    async def change_user_role(self, login: str, role_id: str) -> UserInDBWRole:
        """Изменение роли пользователя"""

        return await self.repository.update_user_role(login, role_id)

    async def remove_user_role(self, login: str, role_id: str) -> None:
        """Удаление роли у пользователя"""

        return await self.repository.remove_user_role(login, role_id)

    async def refresh_token(self, request: Request) -> JSONResponse:
        """Обновление токенов по рефреш токену"""

        refresh_token = request.cookies.get("refresh_token")

        decoded_refresh_token = await validate_token(refresh_token)

        user_role = decoded_refresh_token.get("user_role")
        user_login = decoded_refresh_token.get("user_login")

        encoded_access_token, encoded_refresh_token = (
            await create_access_and_refresh_tokens(user_login, user_role)
        )

        request.cookies["refresh_token"] = encoded_refresh_token
        request.cookies["access_token"] = encoded_access_token

        await self.cache.create_or_update_token(
            user_login, settings.cache_expire_in_seconds, encoded_refresh_token
        )

        return JSONResponse(content={"message": "Токен обновлен"})
