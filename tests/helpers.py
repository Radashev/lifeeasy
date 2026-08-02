from fastapi.testclient import TestClient


def login_and_get_token(
    client: TestClient,
    email: str,
    password: str,
) -> str:
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return data["access_token"]
