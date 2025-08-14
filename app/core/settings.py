from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    ENVIRONMENT: Literal["local", "production"] = "local"

    SECRET_KEY: str
    SECRET_ALGO: str
    SECRET_ALIVE_MIN: int
    ACCESS_KEY: str
    ACCESS_ALGO: str
    ACCESS_ALIVE_MIN: int

    DB_URL: str

    TEST_EMAIL: str
    TEST_PASSWORD: str

    @property
    def is_local(self) -> bool:
        return self.ENVIRONMENT == "local"
    
config = Config() #type: ignore
