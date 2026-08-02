from uuid import uuid4

from fastapi.testclient import TestClient

from tests.helpers import login_and_get_token


def test_get_current_user(client: TestClient) -> None:
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

    token = login_and_get_token(
        client=client,
        email=unique_email,
        password="StrongPassword123!",
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == unique_email
    assert "id" in data
