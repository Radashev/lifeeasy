from fastapi import APIRouter

from app.domain.messages import AssistantResponse, IncomingMessage
from app.services.message_router import MessageRouter

router = APIRouter(prefix="/assistant", tags=["assistant"])

message_router = MessageRouter()


@router.post("/message", response_model=AssistantResponse)
def process_message(message: IncomingMessage) -> AssistantResponse:
    return message_router.route(message)
