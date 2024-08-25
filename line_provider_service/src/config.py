from pydantic_settings import BaseSettings, SettingsConfigDict
from src.constants import ENV_PATH


class Settings(BaseSettings):
    PG_HOST: str
    PG_USER: str
    PG_PASS: str
    PG_PORT: int
    PG_DB_NAME: str
    PG_DB_SCHEMA: str = "public"

    RMQ_LOGIN: str
    RMQ_PASSWORD: str
    RMQ_HOST: str
    RMQ_PORT: int

    def get_engine_link(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"

    model_config = SettingsConfigDict(extra="ignore")


def settings_factory() -> Settings:
    return Settings(_env_file=ENV_PATH)
