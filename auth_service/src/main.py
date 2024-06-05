from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import role, user, auth_history
from src.core.config import settings
from src.db.postgres import create_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Импорт моделей необходим для их автоматического создания
    import src.db.models

    await create_database()
    yield


app = FastAPI(
    version="1.0.0",
    title=settings.project_name,
    summary="Auth service for online cinema",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    contact={
        "name": "Amazing python team",
        "email": "amazaingpythonteam@fake.com",
    },
)

app.include_router(user.router, prefix="/api/v1/user")
app.include_router(role.router, prefix="/api/v1/role")
app.include_router(auth_history.router, prefix="/api/v1/auth-history")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
