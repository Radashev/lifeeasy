from app.core.exceptions import NoteNotFoundError
from app.models.note import Note
from app.models.user import User
from app.models.user_role import UserRole
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


    async def get_note(
        self,
        note_id: int,
        current_user: User,
    ) -> Note:
        note = await self.repository.get_by_id(note_id)

        if note is None:
            raise NoteNotFoundError()

        if note.owner_id != current_user.id and current_user.role != UserRole.ROOT:
            raise NoteNotFoundError()

        return note

    async def update_note(
            self,
            note_id: int,
            current_user: User,
            title: str | None,
            content: str | None,
    ) -> Note:
        note = await self.get_note(
            note_id=note_id,
            current_user=current_user,
        )

        return await self.repository.update(
            note=note,
            title=title,
            content=content,
        )

    async def delete_note(
            self,
            note_id: int,
            current_user: User,
    ) -> None:
        note = await self.get_note(
            note_id=note_id,
            current_user=current_user,
        )

        await self.repository.delete(note)