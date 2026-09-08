from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel_link_token import ChannelLinkToken


class ChannelLinkTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        token: str,
        expires_at: datetime,
    ) -> ChannelLinkToken:
        link_token = ChannelLinkToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

        self.session.add(link_token)
        await self.session.commit()
        await self.session.refresh(link_token)

        return link_token

    async def get_by_token(
            self,
            token: str,
    ) -> ChannelLinkToken | None:
        statement = select(ChannelLinkToken).where(
            ChannelLinkToken.token == token,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def mark_as_used(
            self,
            link_token: ChannelLinkToken,
            used_at: datetime,
    ) -> ChannelLinkToken:
        link_token.used_at = used_at

        await self.session.flush()
        await self.session.refresh(link_token)

        return link_token