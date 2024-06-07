from typing import Any

from fastapi import Depends
from redis.asyncio import Redis

redis: Redis | None = None


async def get_redis() -> Redis:
    return redis


class AsyncCacheService:
    """Имплементация класса для кеширования данных"""

    def __init__(self, cache: Redis = Depends(get_redis)):
        self.cache = cache

    async def create_or_update_token(self, key: str, expires: int, value: Any) -> None:
        """Сохранение и обновление рефреш токена"""

        await self.cache.setex(key, expires, value)
