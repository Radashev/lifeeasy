from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    NoteNotFoundError,
    ReminderCannotBeCancelledError,
    ReminderNotFoundError,
)


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

async def reminder_not_found_handler(
    request: Request,
    exc: ReminderNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Reminder not found",
        },
    )

async def reminder_cannot_be_cancelled_handler(
    request: Request,
    exc: ReminderCannotBeCancelledError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Reminder cannot be cancelled",
        },
    )