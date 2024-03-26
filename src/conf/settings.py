from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".envs/.env")

    bot_app_id: str
    api_hash: str
    chat_id: str

    bybit_url: str
    bybit_apikey: str
    bybit_secret: str

    default_quantity_percent: float = Field(alias="DEFAULT_QNTY_PRCNT")


@lru_cache
def _get_settings(**kwargs) -> Settings:
    return Settings(**kwargs)


settings = _get_settings()
