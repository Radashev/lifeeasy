from app.core.exceptions import (
    CannotChangeRootRoleError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import hash_password
from app.models.user import User
from app.models.user_role import UserRole
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self) -> list[User]:
        return await self.repository.get_all()

    async def update_user_role(
            self,
            user_id: int,
            role: UserRole,
    ) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        if user.role == UserRole.ROOT:
            raise CannotChangeRootRoleError()

        return await self.repository.update_role(
            user=user,
            role=role,
        )

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
