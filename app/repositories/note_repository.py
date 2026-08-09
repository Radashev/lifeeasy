from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note


class NoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        title: str,
        content: str,
        owner_id: int,
    ) -> Note:
        note = Note(
            title=title,
            content=content,
            owner_id=owner_id,
        )

        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)

        return note

    async def get_by_owner(self, owner_id: int) -> list[Note]:
        result = await self.session.execute(
            select(Note)
            .where(Note.owner_id == owner_id)
            .order_by(Note.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_all(self) -> list[Note]:
        result = await self.session.execute(
            select(Note).order_by(Note.created_at.desc())
        )

        return list(result.scalars().all())