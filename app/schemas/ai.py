from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ReminderIntent(BaseModel):
    intent: Literal["create_reminder"]
    title: str
    remind_at: datetime


class ReminderTextRequest(BaseModel):
    text: str