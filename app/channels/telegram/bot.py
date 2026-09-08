from aiogram import Bot

from app.core.config import settings

bot = Bot(
    token=settings.telegram_bot_token,
)
