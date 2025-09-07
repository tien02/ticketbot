from pydantic_settings import BaseSettings, SettingsConfigDict


class EmbedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    WHISPER_MODEL_NAME: str


model_settings = EmbedSettings()
