import asyncio

from aiogram import Dispatcher

from app.channels.telegram.bot import bot
from app.channels.telegram.handlers.reminders import (
    router as reminders_router,
)
from app.channels.telegram.handlers.start import (
    router as start_router,
)


async def main() -> None:
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(reminders_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
