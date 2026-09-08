from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel_account import ChannelAccount
from app.services.channel_account_service import ChannelAccountService
from app.services.channel_link_token_service import ChannelLinkTokenService


class ChannelLinkService:
    def __init__(
        self,
        session: AsyncSession,
        token_service: ChannelLinkTokenService,
        account_service: ChannelAccountService,
    ):
        self.session = session
        self.token_service = token_service
        self.account_service = account_service

    async def link(
            self,
            token: str,
            channel: str,
            external_user_id: str,
            external_chat_id: str | None = None,
    ) -> ChannelAccount:
        try:
            link_token = await self.token_service.validate_token(token)

            account = await self.account_service.link_account(
                user_id=link_token.user_id,
                channel=channel,
                external_user_id=external_user_id,
                external_chat_id=external_chat_id,
            )

            await self.token_service.mark_as_used(link_token)

            await self.session.commit()

            return account

        except Exception:
            await self.session.rollback()
            raise