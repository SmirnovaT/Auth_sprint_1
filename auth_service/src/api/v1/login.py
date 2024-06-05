import logging
from redis.asyncio import Redis

from src.db.cache import get_redis, AsyncCacheService
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from pydantic import BaseModel
from src.services.user import UserService
from src.utils.jwt import create_access_and_refresh_tokens

router = APIRouter(tags=["login"])
class Login(BaseModel):
    user_login: str
    password: str

@router.post(
    "/",
    #response_model=Film,
    summary="Аутентификация пользователя",
    description="Предоставление пользователю JWT токена при вводе корректных логина и пароля.",
)
async def login(
    data: Login, responce: Response, service: UserService = Depends(UserService)):
    print(data)
    user_login = data.user_login
    password = data.password
    user = await service.get_user(user_login)

    if user.check_password(password):
        access_token, refresh_token = create_access_and_refresh_tokens(user_login, user.role)
        logging.warning(f"{access_token} {refresh_token}")
        responce.set_cookie("access_token", access_token)
        responce.set_cookie("refresh_token", refresh_token)
        cache_key = user_login
        AsyncCacheService(get_redis(), "refresh_tokens").set_single_record(cache_key, refresh_token)
        return responce

