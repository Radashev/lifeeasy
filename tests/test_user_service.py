import pytest

from app.models.user import User
from app.services.user_service import UserService


class FakeUserRepository:
    def __init__(self):
        self.created_name: str | None = None

    async def create(self, name: str) -> User:
        self.created_name = name
        return User(id=1, name=name)


@pytest.mark.asyncio
async def test_create_user_calls_repository():
    repository = FakeUserRepository()
    service = UserService(repository)

    user = await service.create_user("Anton")

    assert repository.created_name == "Anton"
    assert user.id == 1
    assert user.name == "Anton"
