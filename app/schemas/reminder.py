from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReminderCreate(BaseModel):
    title: str
    description: str | None = None
    remind_at: datetime


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    remind_at: datetime
    owner_id: int
    created_at: datetime
    updated_at: datetime


class ReminderUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    remind_at: datetime | None = None