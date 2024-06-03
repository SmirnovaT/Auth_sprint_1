from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.db import models


class BaseRepository:
    model = models

    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def create(self, item):
        try:
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item
        except IntegrityError:
            raise
