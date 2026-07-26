from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user() -> None:
    unique_email = f"alice-{uuid4()}@example.com"

    response = client.post(
        "/users/",
        json={
            "name": "Alice",
            "email": unique_email,
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == unique_email
    assert isinstance(data["id"], int)
    assert "password" not in data
    assert "hashed_password" not in data
