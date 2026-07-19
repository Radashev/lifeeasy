from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, name: str) -> User:
        return await self.repository.create(name)
