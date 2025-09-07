from pydantic_settings import BaseSettings, SettingsConfigDict


class EmbedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    OLLAMA_URL: str
    OLLAMA_MODEL: str
    RETRIEVAL_URL: str


model_settings = EmbedSettings()
