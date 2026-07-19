from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user() -> None:
    response = client.post(
        "/users/",
        json={"name": "Alice"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    assert isinstance(response.json()["id"], int)
