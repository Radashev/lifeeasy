from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.channel_account_repository import (
    ChannelAccountRepository,
)
from app.repositories.channel_link_token_repository import (
    ChannelLinkTokenRepository,
)
from app.repositories.reminder_repository import ReminderRepository
from app.services.ai_reminder_service import AIReminderService
from app.services.channel_account_service import ChannelAccountService
from app.services.channel_link_service import ChannelLinkService
from app.services.channel_link_token_service import ChannelLinkTokenService
from app.services.reminder_service import ReminderService


def get_ai_reminder_service(
    session: AsyncSession,
) -> AIReminderService:
    repository = ReminderRepository(session)
    reminder_service = ReminderService(repository)

    return AIReminderService(
        reminder_service=reminder_service,
    )

def get_channel_account_service(
    session: AsyncSession,
) -> ChannelAccountService:
    repository = ChannelAccountRepository(session)

    return ChannelAccountService(
        repository=repository,
    )

def get_channel_link_service(
    session: AsyncSession,
) -> ChannelLinkService:
    token_repository = ChannelLinkTokenRepository(session)
    token_service = ChannelLinkTokenService(token_repository)

    account_repository = ChannelAccountRepository(session)
    account_service = ChannelAccountService(account_repository)

    return ChannelLinkService(
        session=session,
        token_service=token_service,
        account_service=account_service,
    )