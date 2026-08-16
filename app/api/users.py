from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CannotChangeRootRoleError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.db.postgres import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserRoleUpdate
from app.security.authorization import require_admin, require_root
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=list[UserResponse],
)
async def get_users(
        _: Annotated[User, Depends(require_admin)],
        session: AsyncSession = Depends(get_session),
) -> list[User]:
    repository = UserRepository(session)
    service = UserService(repository)

    return await service.get_all_users()


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
async def update_user_role(
        user_id: int,
        role_data: UserRoleUpdate,
        _: Annotated[User, Depends(require_root)],
        session: AsyncSession = Depends(get_session),
) -> User:
    repository = UserRepository(session)
    service = UserService(repository)

    try:
        return await service.update_user_role(
            user_id=user_id,
            role=role_data.role,
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None
    except CannotChangeRootRoleError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ROOT role cannot be changed",
        ) from None


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        user_data: UserCreate,
        _: Annotated[User, Depends(require_admin)],
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
