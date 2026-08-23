from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.postgres import get_session
from app.models.user import User
from app.repositories.reminder_repository import ReminderRepository
from app.schemas.reminder import (
    ReminderCreate,
    ReminderResponse,
    ReminderUpdate,
)
from app.services.reminder_service import ReminderService

router = APIRouter(
    prefix="/reminders",
    tags=["reminders"],
)


@router.post(
    "/",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_reminder(
    reminder_data: ReminderCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> ReminderResponse:
    repository = ReminderRepository(session)
    service = ReminderService(repository)

    reminder = await service.create_reminder(
        title=reminder_data.title,
        description=reminder_data.description,
        remind_at=reminder_data.remind_at,
        owner_id=current_user.id,
    )

    return ReminderResponse.model_validate(reminder)

@router.get(
    "/",
    response_model=list[ReminderResponse],
)
async def get_reminders(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> list[ReminderResponse]:
    repository = ReminderRepository(session)
    service = ReminderService(repository)

    reminders = await service.get_user_reminders(
        owner_id=current_user.id,
    )

    return [
        ReminderResponse.model_validate(reminder)
        for reminder in reminders
    ]


@router.get(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
async def get_reminder(
    reminder_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> ReminderResponse:
    repository = ReminderRepository(session)
    service = ReminderService(repository)

    reminder = await service.get_reminder(
        reminder_id=reminder_id,
        current_user=current_user,
    )

    return ReminderResponse.model_validate(reminder)


@router.patch(
    "/{reminder_id}",
    response_model=ReminderResponse,
)
async def update_reminder(
    reminder_id: int,
    reminder_data: ReminderUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> ReminderResponse:
    repository = ReminderRepository(session)
    service = ReminderService(repository)

    reminder = await service.update_reminder(
        reminder_id=reminder_id,
        current_user=current_user,
        title=reminder_data.title,
        description=reminder_data.description,
        remind_at=reminder_data.remind_at,
    )

    return ReminderResponse.model_validate(reminder)


@router.delete(
    "/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reminder(
    reminder_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> None:
    repository = ReminderRepository(session)
    service = ReminderService(repository)

    await service.delete_reminder(
        reminder_id=reminder_id,
        current_user=current_user,
    )


@router.post(
    "/{reminder_id}/cancel",
    response_model=ReminderResponse,
)
async def cancel_reminder(
    reminder_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> ReminderResponse:
    repository = ReminderRepository(session)
    service = ReminderService(repository)

    reminder = await service.cancel_reminder(
        reminder_id=reminder_id,
        current_user=current_user,
    )

    return ReminderResponse.model_validate(reminder)