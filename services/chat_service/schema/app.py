from pydantic import BaseModel


class UserMessage(BaseModel):
    user_id: str
    message: str
    booking_id: str | None = None
