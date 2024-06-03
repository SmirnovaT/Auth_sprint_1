from src.db import models
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = models.User

    async def create_user(self, user):
        return await self.create(user)
