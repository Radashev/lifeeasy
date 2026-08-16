import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.postgres import get_session
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.security.authorization import require_root
from app.services.note_service import NoteService

logger = logging.getLogger(__name__)

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

    logger.info(
        "Note created: note_id=%s owner_id=%s",
        note.id,
        note.owner_id,
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


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
async def get_note(
    note_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> NoteResponse:
    repository = NoteRepository(session)
    service = NoteService(repository)


    note = await service.get_note(
            note_id=note_id,
            current_user=current_user,
        )

    return NoteResponse.model_validate(note)


@router.patch(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> NoteResponse:
    repository = NoteRepository(session)
    service = NoteService(repository)


    note = await service.update_note(
        note_id=note_id,
        current_user=current_user,
        title=note_data.title,
        content=note_data.content,
    )
    logger.info(
        "Note updated: note_id=%s owner_id=%s",
        note.id,
        note.owner_id,
    )


    return NoteResponse.model_validate(note)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> None:
    repository = NoteRepository(session)
    service = NoteService(repository)


    await service.delete_note(
        note_id=note_id,
        current_user=current_user,
    )
    logger.info(
        "Note deleted: note_id=%s user_id=%s",
        note_id,
        current_user.id,
    )
