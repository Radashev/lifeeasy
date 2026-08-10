from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from tests.helpers import login_and_get_token


def test_root_can_create_note(client: TestClient) -> None:
    token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert me_response.status_code == 200, me_response.text

    root_id = me_response.json()["id"]

    response = client.post(
        "/notes/",
        json={
            "title": "First LifeEasy note",
            "content": "My first note created through the API.",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["title"] == "First LifeEasy note"
    assert data["content"] == "My first note created through the API."
    assert data["owner_id"] == root_id
    assert isinstance(data["id"], int)
    assert "created_at" in data
    assert "updated_at" in data


def test_user_can_get_own_notes(client: TestClient) -> None:
    token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    create_response = client.post(
        "/notes/",
        json={
            "title": "Private note",
            "content": "Only my note.",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    response = client.get(
        "/notes/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200, response.text

    notes = response.json()

    assert isinstance(notes, list)
    assert any(
        note["title"] == "Private note"
        for note in notes
    )



def test_user_sees_only_own_notes(client: TestClient) -> None:
    root_token = login_and_get_token(
        client=client,
        email=settings.root_email,
        password=settings.root_password,
    )

    user_a_email = f"user-a-{uuid4()}@example.com"
    user_b_email = f"user-b-{uuid4()}@example.com"
    password = "StrongPassword123!"

    user_a_response = client.post(
        "/users/",
        json={
            "name": "User A",
            "email": user_a_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert user_a_response.status_code == 201, user_a_response.text

    user_b_response = client.post(
        "/users/",
        json={
            "name": "User B",
            "email": user_b_email,
            "password": password,
        },
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert user_b_response.status_code == 201, user_b_response.text

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

    note_a_response = client.post(
        "/notes/",
        json={
            "title": "User A note",
            "content": "Private content A",
        },
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert note_a_response.status_code == 201, note_a_response.text

    note_b_response = client.post(
        "/notes/",
        json={
            "title": "User B note",
            "content": "Private content B",
        },
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert note_b_response.status_code == 201, note_b_response.text

    response = client.get(
        "/notes/",
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert response.status_code == 200, response.text

    notes = response.json()

    titles = [note["title"] for note in notes]

    assert "User A note" in titles
    assert "User B note" not in titles


def test_root_can_get_all_notes(client: TestClient) -> None:
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
            "name": "Notes User",
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

    note_response = client.post(
        "/notes/",
        json={
            "title": "Visible to ROOT",
            "content": "ROOT should be able to inspect this note.",
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert note_response.status_code == 201, note_response.text

    response = client.get(
        "/notes/all",
        headers={
            "Authorization": f"Bearer {root_token}",
        },
    )

    assert response.status_code == 200, response.text

    notes = response.json()

    titles = [note["title"] for note in notes]

    assert "Visible to ROOT" in titles


def test_user_cannot_get_all_notes(client: TestClient) -> None:
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
            "name": "Regular Notes User",
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

    response = client.get(
        "/notes/all",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403, response.text
    assert response.json() == {
        "detail": "Insufficient permissions",
    }

def test_user_can_get_own_note_by_id(client: TestClient) -> None:
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
            "name": "Note Owner",
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

    create_response = client.post(
        "/notes/",
        json={
            "title": "My detailed note",
            "content": "Private details",
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    note_id = create_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "My detailed note"



def test_user_cannot_get_other_users_note_by_id(client: TestClient) -> None:
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

    create_response = client.post(
        "/notes/",
        json={
            "title": "User A secret",
            "content": "Only User A should read this.",
        },
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    note_id = create_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert response.status_code == 404, response.text
    assert response.json() == {
        "detail": "Note not found",
    }


def test_user_can_update_own_note(client: TestClient) -> None:
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
            "name": "Note Editor",
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

    create_response = client.post(
        "/notes/",
        json={
            "title": "Old title",
            "content": "Old content",
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    note_id = create_response.json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "New title",
            "content": "New content",
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == "New title"
    assert data["content"] == "New content"


def test_user_can_delete_own_note(client: TestClient) -> None:
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
            "name": "Note Deleter",
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

    create_response = client.post(
        "/notes/",
        json={
            "title": "Delete me",
            "content": "This note will be deleted.",
        },
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert create_response.status_code == 201, create_response.text

    note_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert get_response.status_code == 404