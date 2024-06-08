from uuid import UUID

from fastapi import Depends

from src.db.models import User
from src.repositories.auth_history import AuthHistoryRepository
from src.schemas.auth_history import AuthHistoryInDB


class AuthHistoryService:
    """Сервис для взаимодействия с моделью AuthenticationHistory"""

    def __init__(
        self,
        repository: AuthHistoryRepository = Depends(),
    ):
        self.repository = repository

    async def get_history(
        self,
        user_id: UUID,
        page_size: int = 10,
        page_number: int = 1,
    ) -> list[AuthHistoryInDB]:
        """Получение истории аутентификаций"""

        return await self.repository.get_history(user_id, page_size, page_number)
    async def set_history(
            self,
            login: str,
            user_agent: str,
            success: bool):
        return await self.repository.set_history(login, user_agent, success)
