from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError
from app.db.postgres import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

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
    service = UserService(repository)

    try:
        user = await service.create_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        ) from None

    return UserResponse.model_validate(user)
