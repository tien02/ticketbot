from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    APP_PORT: int
    CHAT_URL: str
    MEDIA_URL: str


app_settings = AppSettings()
