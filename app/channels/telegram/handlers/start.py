from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.channels.telegram.dependencies import (
    get_channel_account_service,
)
from app.db.postgres import AsyncSessionLocal

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    if message.from_user is None:
        return

    external_user_id = str(message.from_user.id)

    async with AsyncSessionLocal() as session:
        service = get_channel_account_service(session)

        user_id = await service.get_user_id(
            channel="telegram",
            external_user_id=external_user_id,
        )

    if user_id is None:
        await message.answer(
            "Привіт! Я LifeEasy 🤖\n"
            "Твій Telegram ще не прив'язаний до LifeEasy."
        )
        return

    await message.answer(
        "Привіт! Я LifeEasy 🤖\n"
        "Твій Telegram успішно прив'язаний."
    )
