from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reminder import Reminder


class ReminderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        title: str,
        description: str | None,
        remind_at: datetime,
        owner_id: int,
    ) -> Reminder:
        reminder = Reminder(
            title=title,
            description=description,
            remind_at=remind_at,
            owner_id=owner_id,
        )

        self.session.add(reminder)
        await self.session.commit()
        await self.session.refresh(reminder)

        return reminder

    async def get_by_owner(
        self,
        owner_id: int,
    ) -> list[Reminder]:
        result = await self.session.execute(
            select(Reminder)
            .where(Reminder.owner_id == owner_id)
            .order_by(Reminder.remind_at)
        )

        return list(result.scalars().all())

    async def get_by_id(
        self,
        reminder_id: int,
    ) -> Reminder | None:
        result = await self.session.execute(
            select(Reminder).where(Reminder.id == reminder_id)
        )

        return result.scalar_one_or_none()


    async def update(
        self,
        reminder: Reminder,
        title: str | None,
        description: str | None,
        remind_at: datetime | None,
    ) -> Reminder:
        if title is not None:
            reminder.title = title

        if description is not None:
            reminder.description = description

        if remind_at is not None:
            reminder.remind_at = remind_at

        await self.session.commit()
        await self.session.refresh(reminder)

        return reminder

    async def delete(
            self,
            reminder: Reminder,
    ) -> None:
        await self.session.delete(reminder)
        await self.session.commit()