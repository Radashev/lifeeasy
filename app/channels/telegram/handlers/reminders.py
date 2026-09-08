from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def reminder_handler(message: Message) -> None:
    if message.text is None:
        return

    await message.answer(f"Отримав: {message.text}")
