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
    jwt_secret: str = Field(default="moonite-dev-secret", validation_alias=AliasChoices("JWT_SECRET", "jwt_secret"))
    access_token_expire_seconds: int = Field(
        default=24*60*60*7,
        validation_alias=AliasChoices("ACCESS_TOKEN_EXPIRE_SECONDS", "access_token_expire_seconds"),
    )
    refresh_token_expire_seconds: int = Field(
        default=24*60*60*30,
        validation_alias=AliasChoices("REFRESH_TOKEN_EXPIRE_SECONDS", "refresh_token_expire_seconds"),
    )


settings = Settings()
