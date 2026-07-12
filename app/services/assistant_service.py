from app.domain.messages import AssistantResponse, IncomingMessage


class AssistantService:
    def process(self, message: IncomingMessage) -> AssistantResponse:
        return AssistantResponse(
            text=f"Hello, user {message.user_id}. You wrote: {message.text}"
        )