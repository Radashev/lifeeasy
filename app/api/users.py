from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_session
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(
    name: str,
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    user = await repository.create(name)

    return {
        "id": user.id,
        "name": user.name,
    }