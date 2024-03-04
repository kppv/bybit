from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    chat_id: str

    class Config:
        env_file = ".envs/dev.env"


@lru_cache
def _get_settings(**kwargs) -> Settings:
    return Settings(**kwargs)


settings = _get_settings()
