from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(tags=["login"])

@router.post(
    "/",
    #response_model=Film,
    summary="Аутентификация пользователя",
    description="Предоставление пользователю JWT токена при вводе корректных логина и пароля.",
)
async def login(
    login: str, password: str):
    pass
