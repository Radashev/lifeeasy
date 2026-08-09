from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.postgres import get_session
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse
from app.security.authorization import require_root
from app.services.note_service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note_data: NoteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> NoteResponse:
    repository = NoteRepository(session)
    service = NoteService(repository)

    note = await service.create_note(
        title=note_data.title,
        content=note_data.content,
        owner_id=current_user.id,
    )

    return NoteResponse.model_validate(note)


@router.get(
    "/",
    response_model=list[NoteResponse],
)
async def get_my_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> list[NoteResponse]:
    repository = NoteRepository(session)
    service = NoteService(repository)

    notes = await service.get_my_notes(
        owner_id=current_user.id,
    )

    return [
        NoteResponse.model_validate(note)
        for note in notes
    ]


@router.get(
    "/all",
    response_model=list[NoteResponse],
)
async def get_all_notes(
    _: Annotated[User, Depends(require_root)],
    session: AsyncSession = Depends(get_session),
) -> list[NoteResponse]:
    repository = NoteRepository(session)
    service = NoteService(repository)

    notes = await service.get_all_notes()

    return [
        NoteResponse.model_validate(note)
        for note in notes
    ]