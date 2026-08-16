import pytest

from app.models.user import User
from app.services.user_service import UserService


class FakeUserRepository:
    def __init__(self):
        self.created_name: str | None = None
        self.created_email: str | None = None
        self.created_hashed_password: str | None = None

    async def get_by_email(self, email: str):
        return None

    async def create(
        self,
        name: str,
        email: str,
        hashed_password: str,
    ) -> User:
        self.created_name = name
        self.created_email = email
        self.created_hashed_password = hashed_password

        return User(
            id=1,
            name=name,
            email=email,
            hashed_password=hashed_password,
        )


@pytest.mark.asyncio
async def test_create_user_calls_repository():
    repository = FakeUserRepository()
    service = UserService(repository)

    user = await service.create_user(
        name="Anton",
        email="anton@example.com",
        password="StrongPassword123!",
    )

    assert repository.created_name == "Anton"
    assert repository.created_email == "anton@example.com"
    assert repository.created_hashed_password is not None
    assert repository.created_hashed_password != "StrongPassword123!"

    assert user.id == 1
    assert user.name == "Anton"
    assert user.email == "anton@example.com"
