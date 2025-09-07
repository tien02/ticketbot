from pydantic_settings import BaseSettings, SettingsConfigDict


class EmbedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    EMBEDDING_URL: str


embed_settings = EmbedSettings()
