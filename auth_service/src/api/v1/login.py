from http import HTTPStatus

from fastapi import APIRouter, Depends, Response


from src.schemas.user import Login
from src.services.user import UserService

router = APIRouter(tags=["login"])


@router.post(
    "/",
    summary="Аутентификация пользователя",
    status_code=HTTPStatus.OK,
    description="Предоставление пользователю JWT токена при вводе корректных логина и пароля.",
)
async def login(
    data: Login,
    response: Response,
    service: UserService = Depends(UserService),
):
    return await service.login(response, data)
