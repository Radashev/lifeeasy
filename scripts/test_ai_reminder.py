import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from app.ai.reminder_parser import parse_reminder


async def main() -> None:
    current_datetime = datetime.now(
        ZoneInfo("Europe/Warsaw")
    )

    result = await parse_reminder(
        text="Нагадай завтра о 18:00 купити молоко",
        current_datetime=current_datetime,
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())