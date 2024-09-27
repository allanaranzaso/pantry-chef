from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = 'pantry-chef'
    DB_USERNAME: str = ''
    DB_PASSWORD: str = ''
    DB_URL: str = ''
    DB_PORT: int = 5432
    DB_NAME: str = ''
    DATABASE_URL: str = ''
    ENV: str = 'dev'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @field_validator('DATABASE_URL')
    @classmethod
    def format_database_url(
        cls,
        _v: str,
        info: ValidationInfo,
    ) -> str:
        values = info.data
        return (
            f"postgresql+asyncpg://{values['DB_USERNAME']}:"
            f"{values['DB_PASSWORD']}@{values['DB_URL']}:"
            f"{values['DB_PORT']}/{values['DB_NAME']}"
        )


settings = Settings()
