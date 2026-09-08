from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel_account import ChannelAccount


class ChannelAccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_external_user_id(
        self,
        channel: str,
        external_user_id: str,
    ) -> ChannelAccount | None:
        statement = select(ChannelAccount).where(
            ChannelAccount.channel == channel,
            ChannelAccount.external_user_id == external_user_id,
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def create(
            self,
            user_id: int,
            channel: str,
            external_user_id: str,
            external_chat_id: str | None = None,
    ) -> ChannelAccount:
        account = ChannelAccount(
            user_id=user_id,
            channel=channel,
            external_user_id=external_user_id,
            external_chat_id=external_chat_id,
        )

        self.session.add(account)
        await self.session.flush()
        await self.session.refresh(account)

        return account

