from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class InvalidCredentialsError(Exception):
    """Raised when email or password is incorrect."""


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login(self, email: str, password: str) -> str:
        user = await self.repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=str(user.id),
        )

        return access_token