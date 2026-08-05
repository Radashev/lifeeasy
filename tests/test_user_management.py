from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from tests.helpers import login_and_get_token


def test_root_can_get_all_users(client: TestClient) -> None:
    token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200, response.text

    users = response.json()

    assert isinstance(users, list)
    assert len(users) > 0
    assert "role" in users[0]

def test_user_cannot_get_all_users(client: TestClient) -> None:
    unique_email = f"user-{uuid4()}@example.com"
    password = "StrongPassword123!"

    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    create_response = client.post(
        "/users/",
        json={
            "name": "Regular User",
            "email": unique_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text
    assert create_response.json()["role"] == "user"

    token = login_and_get_token(
        client=client,
        email=unique_email,
        password=password,
    )

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403, response.text
    assert response.json() == {
        "detail": "Insufficient permissions",
    }