import orjson
from pydantic import BaseModel

from src.utils.orjson_dumps import orjson_dumps


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
