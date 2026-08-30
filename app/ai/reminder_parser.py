from datetime import datetime

from app.ai.client import client
from app.schemas.ai import ReminderIntent


async def parse_reminder(
    text: str,
    current_datetime: datetime,
) -> ReminderIntent:
    response = await client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Extract reminder information from the user's message. "
                    f"Current datetime is {current_datetime.isoformat()}. "
                    "Resolve relative dates such as today and tomorrow. "
                    "Return a create_reminder intent with a short title "
                    "and an exact reminder datetime."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        text_format=ReminderIntent,
    )

    return response.output_parsed