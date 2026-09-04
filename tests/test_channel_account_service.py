from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import ChannelAccountAlreadyLinkedError
from app.models.channel_account import ChannelAccount
from app.services.channel_account_service import ChannelAccountService


@pytest.mark.asyncio
async def test_link_account_creates_new_account() -> None:
    repository = AsyncMock()

    repository.get_by_external_user_id.return_value = None

    expected_account = ChannelAccount(
        id=1,
        user_id=30,
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )

    repository.create.return_value = expected_account

    service = ChannelAccountService(repository)

    result = await service.link_account(
        user_id=30,
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )

    assert result == expected_account

    repository.create.assert_awaited_once_with(
        user_id=30,
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )


@pytest.mark.asyncio
async def test_link_account_rejects_existing_account() -> None:
    repository = AsyncMock()

    existing_account = ChannelAccount(
        id=1,
        user_id=30,
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )

    repository.get_by_external_user_id.return_value = existing_account

    service = ChannelAccountService(repository)

    with pytest.raises(ChannelAccountAlreadyLinkedError):
        await service.link_account(
            user_id=30,
            channel="telegram",
            external_user_id="777777",
            external_chat_id="777777",
        )

    repository.create.assert_not_awaited()