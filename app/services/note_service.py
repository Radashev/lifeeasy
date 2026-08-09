from app.models.note import Note
from app.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, repository: NoteRepository):
        self.repository = repository

    async def create_note(
        self,
        title: str,
        content: str,
        owner_id: int,
    ) -> Note:
        return await self.repository.create(
            title=title,
            content=content,
            owner_id=owner_id,
        )

    async def get_my_notes(
        self,
        owner_id: int,
    ) -> list[Note]:
        return await self.repository.get_by_owner(owner_id)


    async def get_all_notes(self) -> list[Note]:
        return await self.repository.get_all()
