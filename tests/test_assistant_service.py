from app.domain.messages import IncomingMessage
from app.services.assistant_service import AssistantService


def test_process_message():
    service = AssistantService()

    message = IncomingMessage(
        user_id="13",
        channel="whatsapp",
        text="Remind me to call my wife",
        session_id="session-002",
    )

    response = service.process(message)

    assert response.text == ("Hello, user 13. You wrote: Remind me to call my wife")
