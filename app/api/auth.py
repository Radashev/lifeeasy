from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.postgres import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService, InvalidCredentialsError

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:

    repository = UserRepository(session)
    service = AuthService(repository)

    try:
        access_token = await service.login(
            email=form_data.username,
            password=form_data.password,
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user
