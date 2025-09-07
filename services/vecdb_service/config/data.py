from pydantic_settings import BaseSettings, SettingsConfigDict


class DataSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    COLLECTION_NAME: str
    VECTOR_DB_HOST: str
    VECTOR_DB_PORT: int


data_settings = DataSettings()
