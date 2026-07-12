from enum import Enum


class Intent(str, Enum):
    CHAT = "chat"
    REMINDER = "reminder"
    TASK = "task"
    CALENDAR = "calendar"
    UNKNOWN = "unknown"
