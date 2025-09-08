from pydantic import BaseModel


class WorkflowResponse(BaseModel):
    user_id: str
    input_text: str
    chat_response: str
