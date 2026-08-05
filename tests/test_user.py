from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from tests.helpers import login_and_get_token


def test_create_user(client: TestClient) -> None:
    unique_email = f"alice-{uuid4()}@example.com"

    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    response = client.post(
        "/users/",
        json={
            "name": "Alice",
            "email": unique_email,
            "password": "StrongPassword123!",
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == unique_email
    assert data["role"] == "user"
    assert isinstance(data["id"], int)
    assert "password" not in data
    assert "hashed_password" not in data
