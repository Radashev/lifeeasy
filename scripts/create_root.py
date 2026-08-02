import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.db.postgres import AsyncSessionLocal, engine
from app.models.user import User
from app.models.user_role import UserRole


async def create_root() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.role == UserRole.ROOT))
        existing_root = result.scalar_one_or_none()

        if existing_root is not None:
            print(f"ROOT already exists: {existing_root.email}")
            return

        result = await session.execute(
            select(User).where(User.email == settings.root_email)
        )
        existing_email = result.scalar_one_or_none()

        if existing_email is not None:
            print(
                "A user with the ROOT email already exists, but this user is not ROOT."
            )
            return

        root_user = User(
            name=settings.root_name,
            email=settings.root_email,
            hashed_password=hash_password(settings.root_password),
            role=UserRole.ROOT,
        )

        session.add(root_user)
        await session.commit()
        await session.refresh(root_user)

        print(f"ROOT created successfully: id={root_user.id}, email={root_user.email}")


async def main() -> None:
    try:
        await create_root()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
