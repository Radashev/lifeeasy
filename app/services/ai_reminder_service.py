from datetime import datetime

from app.ai.reminder_parser import parse_reminder
from app.models.reminder import Reminder
from app.schemas.ai import ReminderIntent
from app.services.reminder_service import ReminderService


class AIReminderService:
    def __init__(
        self,
        reminder_service: ReminderService,
    ):
        self.reminder_service = reminder_service

    async def parse(
        self,
        text: str,
        current_datetime: datetime,
    ) -> ReminderIntent:
        return await parse_reminder(
            text=text,
            current_datetime=current_datetime,
        )

    async def create_from_text(
        self,
        text: str,
        current_datetime: datetime,
        owner_id: int,
    ) -> Reminder:
        intent = await self.parse(
            text=text,
            current_datetime=current_datetime,
        )

        return await self.reminder_service.create_reminder(
            title=intent.title,
            description=None,
            remind_at=intent.remind_at,
            owner_id=owner_id,
        )