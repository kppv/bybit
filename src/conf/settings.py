from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    chat_id: str

    bybit_url: str
    bybit_apikey: str
    bybit_secret: str

    default_quantity_percent: float = Field(alias="DEFAULT_QNTY_PRCNT")

    class Config:
        env_file = "../.envs/.env"


@lru_cache
def _get_settings(**kwargs) -> Settings:
    return Settings(**kwargs)


settings = _get_settings()
