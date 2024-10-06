from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    TARGET_FOLDER_ID: str = "ADD_YOUR_TARGET_FOLDER_ID"
