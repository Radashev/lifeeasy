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

def test_root_can_deactivate_user(client: TestClient) -> None:
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
            "name": "User To Deactivate",
            "email": unique_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    user = create_response.json()
    user_id = user["id"]

    assert user["is_active"] is True

    response = client.patch(
        f"/users/{user_id}/status",
        json={
            "is_active": False,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == user_id
    assert response.json()["is_active"] is False

def test_root_cannot_be_deactivated(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    users_response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert users_response.status_code == 200, users_response.text

    users = users_response.json()

    root_user = next(
        user for user in users
        if user["role"] == "root"
    )

    response = client.patch(
        f"/users/{root_user['id']}/status",
        json={
            "is_active": False,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert response.status_code == 409, response.text
    assert response.json() == {
        "detail": "ROOT user cannot be deactivated",
    }

def test_user_cannot_change_user_status(client: TestClient) -> None:
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

    user_id = create_response.json()["id"]

    user_token = login_and_get_token(
        client=client,
        email=unique_email,
        password=password,
    )

    response = client.patch(
        f"/users/{user_id}/status",
        json={
            "is_active": False,
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403, response.text
    assert response.json() == {
        "detail": "Insufficient permissions",
    }

def test_admin_can_deactivate_user(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    admin_email = f"admin-{uuid4()}@example.com"
    admin_password = "StrongPassword123!"

    # 1. ROOT creates future ADMIN
    admin_response = client.post(
        "/users/",
        json={
            "name": "Test Admin",
            "email": admin_email,
            "password": admin_password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert admin_response.status_code == 201, admin_response.text

    admin_id = admin_response.json()["id"]

    # 2. ROOT changes USER role -> ADMIN
    role_response = client.patch(
        f"/users/{admin_id}/role",
        json={
            "role": "admin",
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert role_response.status_code == 200, role_response.text
    assert role_response.json()["role"] == "admin"

    # 3. Create regular USER
    user_email = f"user-{uuid4()}@example.com"

    user_response = client.post(
        "/users/",
        json={
            "name": "User For Admin Test",
            "email": user_email,
            "password": "StrongPassword123!",
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert user_response.status_code == 201, user_response.text

    user_id = user_response.json()["id"]

    # 4. Login as ADMIN
    admin_token = login_and_get_token(
        client=client,
        email=admin_email,
        password=admin_password,
    )

    # 5. ADMIN deactivates USER
    response = client.patch(
        f"/users/{user_id}/status",
        json={
            "is_active": False,
        },
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == user_id
    assert response.json()["is_active"] is False

def test_update_status_of_nonexistent_user_returns_404(
    client: TestClient,
) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    response = client.patch(
        "/users/999999999/status",
        json={
            "is_active": False,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert response.status_code == 404, response.text
    assert response.json() == {
        "detail": "User not found",
    }
