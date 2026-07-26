from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "app_name": "LifeEasy",
        "version": "1.0.0",
        "debug": True,
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_assistant_message():
    response = client.post(
        "/assistant/message",
        json={
            "user_id": "13",
            "channel": "whatsapp",
            "text": "Remind me to call my wife",
            "session_id": "session-001"
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "text": "Hello, user 13. You wrote: Remind me to call my wife"
    }