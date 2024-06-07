from http import HTTPStatus

from fastapi import Depends, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.core.logger import auth_logger
from src.db.cache import AsyncCacheService
from src.db.models import User
from src.db.postgres import get_session
from src.schemas.user import UserCreate, UserInDB, UserInDBWRole, Login
from src.repositories.user import UserRepository
from src.utils.jwt import validate_token, create_access_and_refresh_tokens


class UserService:
    """Сервис для взаимодействия с моделью User"""

    def __init__(
        self,
        db: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(),
        cache: AsyncCacheService = Depends(AsyncCacheService),
    ):
        self.repository = repository
        self.db = db
        self.cache = cache

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

    async def refresh_token(
        self, refresh_token: str, response: Response
    ) -> JSONResponse:
        """Обновление токенов по рефреш токену"""

        decoded_refresh_token = await validate_token(refresh_token)

        user_login = decoded_refresh_token.get("user_login")
        user_role = await self.repository.get_role_by_login(user_login)

        if await self.cache.get_data_by_key(user_login) != refresh_token:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="У пользователя не совпадает рефреш токен из редиса и из cookies",
            )

        encoded_access_token, encoded_refresh_token = (
            await create_access_and_refresh_tokens(user_login, user_role)
        )

        response.set_cookie("refresh_token", encoded_refresh_token)
        response.set_cookie("access_token", encoded_access_token)

        await self.cache.create_or_update_record(user_login, encoded_refresh_token)

        return JSONResponse(content={"message": "Токен обновлен"})

    async def login(self, response, data):
        """Аутентификация пользователя"""

        user = jsonable_encoder(data)
        user = Login(**user)

        await self.repository.check_login(user.user_login, user.password)

        access_token, refresh_token = await create_access_and_refresh_tokens(
            user.user_login, user.password
        )
        auth_logger.info(f"Successfully login")

        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)

        await self.cache.create_or_update_record(user.user_login, refresh_token)
