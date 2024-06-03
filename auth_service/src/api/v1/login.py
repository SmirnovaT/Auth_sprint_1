import logging

from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import pbkdf2_sha256

from src.db.postgres import get_pass_hash

router = APIRouter(tags=["login"])

@router.post(
    "/",
    #response_model=Film,
    summary="Аутентификация пользователя",
    description="Предоставление пользователю JWT токена при вводе корректных логина и пароля.",
)
async def login(
    login: str, password: str):
    hash = get_pass_hash(login)
    if pbkdf2_sha256.verify(password, hash):
        logging.warning("Password is correct")
        pass
