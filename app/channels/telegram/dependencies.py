from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.reminder_repository import ReminderRepository
from app.services.ai_reminder_service import AIReminderService
from app.services.reminder_service import ReminderService


def get_ai_reminder_service(
    session: AsyncSession,
) -> AIReminderService:
    repository = ReminderRepository(session)
    reminder_service = ReminderService(repository)

    return AIReminderService(
        reminder_service=reminder_service,
    )
