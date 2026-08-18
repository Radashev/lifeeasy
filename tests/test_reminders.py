from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from tests.helpers import login_and_get_token


def test_root_can_create_reminder(client: TestClient) -> None:
    token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    response = client.post(
        "/reminders/",
        json={
            "title": "Test reminder",
            "description": "Reminder integration test",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["title"] == "Test reminder"
    assert data["description"] == "Reminder integration test"
    assert data["owner_id"]
    assert data["id"]
    assert data["remind_at"]


def test_user_sees_only_own_reminders(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    password = "StrongPassword123!"

    user_a_email = f"user-a-{uuid4()}@example.com"
    user_b_email = f"user-b-{uuid4()}@example.com"

    for name, email in (
        ("User A", user_a_email),
        ("User B", user_b_email),
    ):
        response = client.post(
            "/users/",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
            headers={
                "Authorization": f"Bearer {root_token}",
            },
        )

        assert response.status_code == 201, response.text

    user_a_token = login_and_get_token(
        client=client,
        email=user_a_email,
        password=password,
    )

    user_b_token = login_and_get_token(
        client=client,
        email=user_b_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    response_a = client.post(
        "/reminders/",
        json={
            "title": "User A reminder",
            "description": "Only User A should see this",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert response_a.status_code == 201, response_a.text

    response_b = client.post(
        "/reminders/",
        json={
            "title": "User B reminder",
            "description": "Only User B should see this",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert response_b.status_code == 201, response_b.text

    response = client.get(
        "/reminders/",
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert response.status_code == 200, response.text

    reminders = response.json()

    titles = [reminder["title"] for reminder in reminders]

    assert "User A reminder" in titles
    assert "User B reminder" not in titles


def test_user_can_get_own_reminder_by_id(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    user_email = f"user-{uuid4()}@example.com"
    password = "StrongPassword123!"

    user_response = client.post(
        "/users/",
        json={
            "name": "Reminder Owner",
            "email": user_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert user_response.status_code == 201, user_response.text

    user_token = login_and_get_token(
        client=client,
        email=user_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    create_response = client.post(
        "/reminders/",
        json={
            "title": "My reminder",
            "description": "Private reminder",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    reminder_id = create_response.json()["id"]

    response = client.get(
        f"/reminders/{reminder_id}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == reminder_id
    assert data["title"] == "My reminder"
    assert data["description"] == "Private reminder"


def test_user_cannot_get_other_users_reminder_by_id(
    client: TestClient,
) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    password = "StrongPassword123!"

    user_a_email = f"user-a-{uuid4()}@example.com"
    user_b_email = f"user-b-{uuid4()}@example.com"

    for name, email in (
        ("User A", user_a_email),
        ("User B", user_b_email),
    ):
        response = client.post(
            "/users/",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
            headers={
                "Authorization": f"Bearer {root_token}",
            },
        )

        assert response.status_code == 201, response.text

    user_a_token = login_and_get_token(
        client=client,
        email=user_a_email,
        password=password,
    )

    user_b_token = login_and_get_token(
        client=client,
        email=user_b_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    create_response = client.post(
        "/reminders/",
        json={
            "title": "User A secret reminder",
            "description": "Only User A should see this",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    reminder_id = create_response.json()["id"]

    response = client.get(
        f"/reminders/{reminder_id}",
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert response.status_code == 404, response.text
    assert response.json() == {
        "detail": "Reminder not found",
    }


def test_user_can_update_own_reminder(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    user_email = f"user-{uuid4()}@example.com"
    password = "StrongPassword123!"

    user_response = client.post(
        "/users/",
        json={
            "name": "Reminder Editor",
            "email": user_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert user_response.status_code == 201, user_response.text

    user_token = login_and_get_token(
        client=client,
        email=user_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    create_response = client.post(
        "/reminders/",
        json={
            "title": "Old reminder",
            "description": "Old description",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    reminder_id = create_response.json()["id"]

    new_remind_at = datetime.now(UTC) + timedelta(hours=2)

    response = client.patch(
        f"/reminders/{reminder_id}",
        json={
            "title": "Updated reminder",
            "description": "Updated description",
            "remind_at": new_remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == reminder_id
    assert data["title"] == "Updated reminder"
    assert data["description"] == "Updated description"


def test_user_cannot_update_other_users_reminder(
    client: TestClient,
) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    password = "StrongPassword123!"
    user_a_email = f"user-a-{uuid4()}@example.com"
    user_b_email = f"user-b-{uuid4()}@example.com"

    for name, email in (
        ("User A", user_a_email),
        ("User B", user_b_email),
    ):
        response = client.post(
            "/users/",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
            headers={"Authorization": f"Bearer {root_token}"},
        )

        assert response.status_code == 201, response.text

    user_a_token = login_and_get_token(
        client=client,
        email=user_a_email,
        password=password,
    )

    user_b_token = login_and_get_token(
        client=client,
        email=user_b_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    create_response = client.post(
        "/reminders/",
        json={
            "title": "User A reminder",
            "description": "Private",
            "remind_at": remind_at.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    assert create_response.status_code == 201, create_response.text

    reminder_id = create_response.json()["id"]

    response = client.patch(
        f"/reminders/{reminder_id}",
        json={
            "title": "Hacked by User B",
        },
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 404, response.text
    assert response.json() == {
        "detail": "Reminder not found",
    }


def test_user_can_delete_own_reminder(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    user_email = f"user-{uuid4()}@example.com"
    password = "StrongPassword123!"

    user_response = client.post(
        "/users/",
        json={
            "name": "Reminder Deleter",
            "email": user_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert user_response.status_code == 201, user_response.text

    user_token = login_and_get_token(
        client=client,
        email=user_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    create_response = client.post(
        "/reminders/",
        json={
            "title": "Delete me",
            "description": "This reminder will be deleted",
            "remind_at": remind_at.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    reminder_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/reminders/{reminder_id}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/reminders/{reminder_id}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Reminder not found",
    }


def test_user_cannot_delete_other_users_reminder(
    client: TestClient,
) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    password = "StrongPassword123!"
    user_a_email = f"user-a-{uuid4()}@example.com"
    user_b_email = f"user-b-{uuid4()}@example.com"

    for name, email in (
        ("User A", user_a_email),
        ("User B", user_b_email),
    ):
        response = client.post(
            "/users/",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
            headers={"Authorization": f"Bearer {root_token}"},
        )

        assert response.status_code == 201, response.text

    user_a_token = login_and_get_token(
        client=client,
        email=user_a_email,
        password=password,
    )

    user_b_token = login_and_get_token(
        client=client,
        email=user_b_email,
        password=password,
    )

    remind_at = datetime.now(UTC) + timedelta(hours=1)

    create_response = client.post(
        "/reminders/",
        json={
            "title": "User A private reminder",
            "description": "User B must not delete this",
            "remind_at": remind_at.isoformat(),
        },
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    assert create_response.status_code == 201, create_response.text

    reminder_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/reminders/{reminder_id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert delete_response.status_code == 404
    assert delete_response.json() == {
        "detail": "Reminder not found",
    }

    get_response = client.get(
        f"/reminders/{reminder_id}",
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == reminder_id