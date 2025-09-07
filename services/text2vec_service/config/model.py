from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    MODEL_NAME_OR_PATH: str


model_settings = ModelSettings()
