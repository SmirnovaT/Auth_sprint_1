import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response, HTTPException
from pydantic import BaseModel

from src.db.cache import AsyncCacheService
from src.services.user import UserService
from src.utils.jwt import create_access_and_refresh_tokens

router = APIRouter(tags=["login"])


class Login(BaseModel):
    user_login: str
    password: str


@router.post(
    "/",
    summary="Аутентификация пользователя",
    status_code=HTTPStatus.OK,
    description="Предоставление пользователю JWT токена при вводе корректных логина и пароля.",
)
async def login(
    data: Login,
    responce: Response,
    service: UserService = Depends(UserService),
    cache: AsyncCacheService = Depends(AsyncCacheService),
):
    print(data)
    user_login = data.user_login
    password = data.password
    user = await service.get_user(user_login)

    if user and user.check_password(password):
        access_token, refresh_token = create_access_and_refresh_tokens(
            user_login, user.role
        )
        logging.info(f"Successfully login")
        responce.set_cookie("access_token", access_token)
        responce.set_cookie("refresh_token", refresh_token)
        cache_key = user_login
        await cache.create_or_update_record(cache_key, refresh_token)
        return responce
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Неверный логин или пароль"
        )
