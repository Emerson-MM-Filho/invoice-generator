from pydantic_settings import BaseSettings, SettingsConfigDict


class NotionEnv(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    INTEGRATION_SECRET: str = "ADD_YOUR_INTEGRATION_SECRET"
    CLIENTS_DATABASE_ID: str = "ADD_YOUR_CLIENTS_DATABASE_ID"


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    TARGET_FOLDER_ID: str = "ADD_YOUR_TARGET_FOLDER_ID"
    EMAIL_FROM: str = "ADD_YOUR_EMAIL_ADDRESS"
    EMAIL_PASSWORD: str = "ADD_YOUR_EMAIL_PASSWORD"
    NOTION: NotionEnv = NotionEnv()
