from contextlib import asynccontextmanager

from src.core.config import settings


import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.db.postgres import create_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Импорт моделей необходим для их автоматического создания
    import src.models.entity

    await create_database()
    yield


app = FastAPI(
    version="1.0.0",
    title=settings.project_name,
    summary="Auth for online cinema",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    contact={
        "name": "Amazing python team",
        "email": "amazaingpythonteam@fake.com",
    },
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
    )
