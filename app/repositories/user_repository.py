from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str) -> User:
        user = User(name=name)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
