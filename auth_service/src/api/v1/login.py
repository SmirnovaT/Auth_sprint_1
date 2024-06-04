import logging

from fastapi import APIRouter, Depends, HTTPException
from src.services.user import UserService
from src.utils.jwt import create_access_and_refresh_tokens

router = APIRouter(tags=["login"])


@router.post(
    "/",
    #response_model=Film,
    summary="Аутентификация пользователя",
    description="Предоставление пользователю JWT токена при вводе корректных логина и пароля.",
)
async def login(
    login: str, password: str, service: UserService = Depends(UserService)):
    user = await service.get_user(login)
    if user.check_password(password):
        create_access_and_refresh_tokens(login, user.role)

