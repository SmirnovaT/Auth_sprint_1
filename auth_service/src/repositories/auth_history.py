from uuid import UUID

from sqlalchemy import select

from src.db import models
from src.repositories.base import BaseRepository
from src.schemas.auth_history import AuthHistoryInDB


class AuthHistoryRepository(BaseRepository):
    """Репозиторий для взаимодействия с моделью AuthenticationHistory"""

    model = models.AuthenticationHistory

    async def get_history(
        self,
        user_id: UUID,
        page_size: int = 10,
        page_number: int = 1,
    ) -> [AuthHistoryInDB]:
        """Получение истории аутентификаций"""

        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .limit(page_size)
            .offset((page_number - 1) * page_size)
        )
        result = await self.db.execute(query)

        return result.scalars().all()
