from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.channels.telegram.dependencies import (
    get_channel_link_service,
)
from app.core.exceptions import (
    ChannelAccountAlreadyLinkedError,
    ChannelLinkTokenAlreadyUsedError,
    ChannelLinkTokenExpiredError,
    ChannelLinkTokenInvalidError,
)
from app.db.postgres import AsyncSessionLocal

router = Router()


@router.message(Command("link"))
async def link_handler(message: Message) -> None:
    if message.text is None:
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Використання: /link <token>"
        )
        return

    token = parts[1].strip()

    if message.from_user is None:
        return

    external_user_id = str(message.from_user.id)
    external_chat_id = str(message.chat.id)

    try:
        async with AsyncSessionLocal() as session:
            service = get_channel_link_service(session)

            await service.link(
                token=token,
                channel="telegram",
                external_user_id=external_user_id,
                external_chat_id=external_chat_id,
            )

    except ChannelLinkTokenInvalidError:
        await message.answer(
            "Token недійсний."
        )
        return

    except ChannelLinkTokenExpiredError:
        await message.answer(
            "Термін дії token закінчився."
        )
        return

    except ChannelLinkTokenAlreadyUsedError:
        await message.answer(
            "Цей token уже був використаний."
        )
        return

    except ChannelAccountAlreadyLinkedError:
        await message.answer(
            "Цей Telegram уже прив'язаний до LifeEasy."
        )
        return

    await message.answer(
        "Telegram успішно прив'язаний до LifeEasy ✅"
    )