from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import NoteNotFoundError


async def note_not_found_handler(
    request: Request,
    exc: NoteNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Note not found",
        },
    )
