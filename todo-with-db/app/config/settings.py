from pydantic_settings import BaseSettings,SettingsConfigDict
import os


env_state=os.getenv("APP_ENV","development")

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=f".env.{env_state}",extra="ignore")

    database_url: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15


def get_config_settings():
    return Settings()

settings=get_config_settings()