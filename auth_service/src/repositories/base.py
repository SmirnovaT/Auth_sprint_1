from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import auth_logger
from src.db.postgres import get_session
from src.db import models


class BaseRepository:
    """Базовый класс, который предоставляет основные
    операции CRUD для взаимодействия с базой данных"""

    model = models

    def __init__(self, db: AsyncSession = Depends(get_session)):
        """Функция инициализирует репозиторий с сессией БД"""

        self.db = db

    async def create(self, item: Any) -> Any:
        """Базовая функция по созданию сущности в БД"""

        try:
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item

        except IntegrityError as exc:
            auth_logger.error(exc)
            constraint_name = exc.orig.args[0].split('"')[1]
            field_name = constraint_name.split("_")[1]

            raise HTTPException(
                status_code=400,
                detail=f"Значение поля: '{field_name}' не уникально",
            )
