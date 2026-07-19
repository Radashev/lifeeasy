from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    user = await repository.create(user_data.name)

    return UserResponse.model_validate(user)