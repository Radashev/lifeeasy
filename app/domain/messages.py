from pydantic import BaseModel


class IncomingMessage(BaseModel):
    user_id: str
    channel: str
    text: str
    session_id: str


class AssistantResponse(BaseModel):
    text: str
