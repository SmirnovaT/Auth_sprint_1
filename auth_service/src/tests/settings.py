from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class RedisSettings(BaseSettings):
    """Конфигурация для Redis"""

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379


class PostgresSettings(BaseSettings):
    """Конфигурация для Postgres"""

    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432


class TestSettings(BaseSettings):
    """Конфигурация проекта для тестирования"""

    AUTH_API_URL: str = "http://127.0.0.1:8010"
    REDIS: RedisSettings = RedisSettings()
    POSTGRES: PostgresSettings = PostgresSettings()


test_settings = TestSettings()
