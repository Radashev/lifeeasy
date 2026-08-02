from app.core.exceptions import UserAlreadyExistsError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(
        self,
        name: str,
        email: str,
        password: str,
    ) -> User:

        existing_user = await self.repository.get_by_email(email)

        if existing_user:
            raise UserAlreadyExistsError()

        hashed_password = hash_password(password)

        return await self.repository.create(
            name=name,
            email=email,
            hashed_password=hashed_password,
        )
