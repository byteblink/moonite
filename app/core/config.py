from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "moonite"
    debug: bool = False
    database_url: str = Field(
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )
    api_host: str = Field(default="0.0.0.0", validation_alias=AliasChoices("API_HOST", "api_host"))
    api_port: int = Field(default=8000, validation_alias=AliasChoices("API_PORT", "api_port"))


settings = Settings()
