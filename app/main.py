from fastapi import FastAPI

from app.api.assistant import router as assistant_router
from app.api.auth import router as auth_router
from app.api.authorization import router as authorization_router
from app.api.health import router as health_router
from app.api.notes import router as notes_router
from app.api.reminders import router as reminders_router
from app.api.users import router as users_router
from app.core.config import settings
from app.core.exception_handlers import (
    note_not_found_handler,
    reminder_cannot_be_cancelled_handler,
    reminder_not_found_handler,
)
from app.core.exceptions import (
    NoteNotFoundError,
    ReminderCannotBeCancelledError,
    ReminderNotFoundError,
)
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="LifeEasy")


app.add_exception_handler(
    NoteNotFoundError,
    note_not_found_handler,
)

app.add_exception_handler(
    ReminderNotFoundError,
    reminder_not_found_handler,
)

app.add_exception_handler(
    ReminderCannotBeCancelledError,
    reminder_cannot_be_cancelled_handler,
)

@app.get("/")
def root():
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
    }


app.include_router(health_router)
app.include_router(assistant_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(authorization_router)
app.include_router(notes_router)
app.include_router(reminders_router)