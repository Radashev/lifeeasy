from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from app.core.exceptions import (
    ChannelLinkTokenAlreadyUsedError,
    ChannelLinkTokenExpiredError,
    ChannelLinkTokenInvalidError,
)
from app.models.channel_link_token import ChannelLinkToken
from app.repositories.channel_link_token_repository import (
    ChannelLinkTokenRepository,
)


class ChannelLinkTokenService:
    def __init__(
        self,
        repository: ChannelLinkTokenRepository,
    ):
        self.repository = repository

    async def create_token(
        self,
        user_id: int,
    ) -> ChannelLinkToken:
        token = token_urlsafe(16)

        expires_at = datetime.now(UTC) + timedelta(
            minutes=10,
        )

        return await self.repository.create(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

    async def validate_token(
            self,
            token: str,
    ) -> ChannelLinkToken:
        link_token = await self.repository.get_by_token(token)

        if link_token is None:
            raise ChannelLinkTokenInvalidError()

        if link_token.used_at is not None:
            raise ChannelLinkTokenAlreadyUsedError()

        if link_token.expires_at <= datetime.now(UTC):
            raise ChannelLinkTokenExpiredError()

        return link_token

    async def mark_as_used(
            self,
            link_token: ChannelLinkToken,
    ) -> ChannelLinkToken:
        return await self.repository.mark_as_used(
            link_token=link_token,
            used_at=datetime.now(UTC),
        )