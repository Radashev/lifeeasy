from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from tests.helpers import login_and_get_token


def test_get_current_user(client: TestClient) -> None:
    unique_email = f"alice-{uuid4()}@example.com"
    password = "StrongPassword123!"

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
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert response.status_code == 201, response.text

    token = login_and_get_token(
        client=client,
        email=unique_email,
        password=password,
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == unique_email
    assert "id" in data
