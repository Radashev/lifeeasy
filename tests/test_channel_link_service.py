from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.models.channel_account import ChannelAccount
from app.models.channel_link_token import ChannelLinkToken
from app.services.channel_link_service import ChannelLinkService


@pytest.mark.asyncio
async def test_link_creates_account_and_marks_token_as_used() -> None:
    session = AsyncMock()
    token_service = AsyncMock()
    account_service = AsyncMock()

    link_token = ChannelLinkToken(
        id=1,
        user_id=30,
        token="abc123",
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        used_at=None,
    )

    account = ChannelAccount(
        id=1,
        user_id=30,
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )

    token_service.validate_token.return_value = link_token
    account_service.link_account.return_value = account

    service = ChannelLinkService(
        session=session,
        token_service=token_service,
        account_service=account_service,
    )

    result = await service.link(
        token="abc123",
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )

    assert result == account

    token_service.validate_token.assert_awaited_once_with(
        "abc123"
    )

    account_service.link_account.assert_awaited_once_with(
        user_id=30,
        channel="telegram",
        external_user_id="777777",
        external_chat_id="777777",
    )

    token_service.mark_as_used.assert_awaited_once_with(
        link_token
    )

    session.commit.assert_awaited_once()
    session.rollback.assert_not_awaited()

@pytest.mark.asyncio
async def test_link_does_not_mark_token_used_when_account_linking_fails() -> None:
    session = AsyncMock()
    token_service = AsyncMock()
    account_service = AsyncMock()

    link_token = ChannelLinkToken(
        id=1,
        user_id=30,
        token="abc123",
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        used_at=None,
    )

    token_service.validate_token.return_value = link_token
    account_service.link_account.side_effect = RuntimeError(
        "Account linking failed"
    )

    service = ChannelLinkService(
        session=session,
        token_service=token_service,
        account_service=account_service,
    )

    with pytest.raises(RuntimeError):
        await service.link(
            token="abc123",
            channel="telegram",
            external_user_id="777777",
            external_chat_id="777777",
        )

    token_service.mark_as_used.assert_not_awaited()

    session.commit.assert_not_awaited()
    session.rollback.assert_awaited_once()