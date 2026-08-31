from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.models.reminder import Reminder
from app.schemas.ai import ReminderIntent
from app.services.ai_reminder_service import AIReminderService


@pytest.mark.asyncio
async def test_create_reminder_from_ai_text() -> None:
    current_datetime = datetime(2026, 8, 30, 12, 0)

    intent = ReminderIntent(
        intent="create_reminder",
        title="Купити молоко",
        remind_at=datetime(2026, 8, 31, 18, 0),
    )

    reminder = Reminder(
        id=1,
        title=intent.title,
        description=None,
        remind_at=intent.remind_at,
        owner_id=30,
    )

    reminder_service = AsyncMock()
    reminder_service.create_reminder.return_value = reminder

    ai_service = AIReminderService(
        reminder_service=reminder_service,
    )

    ai_service.parse = AsyncMock(
        return_value=intent,
    )

    result = await ai_service.create_from_text(
        text="Нагадай завтра о 18:00 купити молоко",
        current_datetime=current_datetime,
        owner_id=30,
    )

    assert result == reminder




