import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response, HTTPException
from pydantic import BaseModel

from src.db.cache import get_redis, AsyncCacheService
from src.services.auth_history import AuthHistoryService
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
    data: Login, responce: Response, service: UserService = Depends(UserService), user_agent: Annotated[str | None, Header()] = None, history_service: AuthHistoryService = Depends(AuthHistoryService)):
    print(data)
    user_login = data.user_login
    password = data.password
    user = await service.get_user(user_login)

    if user and user.check_password(password):
        try:
            access_token, refresh_token = await create_access_and_refresh_tokens(user_login, user.role)
            logging.info(f"Successfully login")
            responce.set_cookie("access_token", access_token)
            responce.set_cookie("refresh_token", refresh_token)
            cache_key = user_login
            AsyncCacheService(get_redis(), "refresh_tokens").set_single_record(cache_key, refresh_token)
            await history_service.set_history(user_id=user.id, user_agent=user_agent, success=True)
            return responce
        except Exception as e:
            await history_service.set_history(user_id=user.id, user_agent=user_agent, success=False)
    else:
        await history_service.set_history(user_id=user.id, user_agent=user_agent, success = False)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Неверный логин или пароль")

