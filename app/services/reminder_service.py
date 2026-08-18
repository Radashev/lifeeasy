from datetime import datetime

from app.core.exceptions import ReminderNotFoundError
from app.models.reminder import Reminder
from app.models.user import User
from app.repositories.reminder_repository import ReminderRepository


class ReminderService:
    def __init__(self, repository: ReminderRepository):
        self.repository = repository

    async def create_reminder(
        self,
        title: str,
        description: str | None,
        remind_at: datetime,
        owner_id: int,
    ) -> Reminder:
        return await self.repository.create(
            title=title,
            description=description,
            remind_at=remind_at,
            owner_id=owner_id,
        )

    async def get_user_reminders(
            self,
            owner_id: int,
    ) -> list[Reminder]:
        return await self.repository.get_by_owner(
            owner_id=owner_id,
        )

    async def get_reminder(
            self,
            reminder_id: int,
            current_user: User,
    ) -> Reminder:
        reminder = await self.repository.get_by_id(reminder_id)

        if reminder is None:
            raise ReminderNotFoundError()

        if reminder.owner_id != current_user.id:
            raise ReminderNotFoundError()

        return reminder


    async def update_reminder(
        self,
        reminder_id: int,
        current_user: User,
        title: str | None,
        description: str | None,
        remind_at: datetime | None,
    ) -> Reminder:
        reminder = await self.get_reminder(
            reminder_id=reminder_id,
            current_user=current_user,
        )

        return await self.repository.update(
            reminder=reminder,
            title=title,
            description=description,
            remind_at=remind_at,
        )


    async def delete_reminder(
            self,
            reminder_id: int,
            current_user: User,
    ) -> None:
        reminder = await self.get_reminder(
            reminder_id=reminder_id,
            current_user=current_user,
        )

        await self.repository.delete(reminder)