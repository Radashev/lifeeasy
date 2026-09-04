from app.core.exceptions import ChannelAccountAlreadyLinkedError
from app.models.channel_account import ChannelAccount
from app.repositories.channel_account_repository import (
    ChannelAccountRepository,
)


class ChannelAccountService:
    def __init__(
        self,
        repository: ChannelAccountRepository,
    ):
        self.repository = repository

    async def get_user_id(
        self,
        channel: str,
        external_user_id: str,
    ) -> int | None:
        account = await self.repository.get_by_external_user_id(
            channel=channel,
            external_user_id=external_user_id,
        )

        if account is None:
            return None

        return account.user_id

    async def link_account(
            self,
            user_id: int,
            channel: str,
            external_user_id: str,
            external_chat_id: str | None = None,
    ) -> ChannelAccount:
        existing_account = await self.repository.get_by_external_user_id(
            channel=channel,
            external_user_id=external_user_id,
        )

        if existing_account is not None:
            raise ChannelAccountAlreadyLinkedError()

        return await self.repository.create(
            user_id=user_id,
            channel=channel,
            external_user_id=external_user_id,
            external_chat_id=external_chat_id,
        )