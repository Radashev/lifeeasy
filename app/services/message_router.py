from app.domain.messages import AssistantResponse, IncomingMessage
from app.services.assistant_service import AssistantService


class MessageRouter:
    def __init__(self):
        self.assistant = AssistantService()

    def route(self, message: IncomingMessage) -> AssistantResponse:
        return self.assistant.process(message)