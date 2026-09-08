from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import (
    ChannelLinkTokenAlreadyUsedError,
    ChannelLinkTokenExpiredError,
    ChannelLinkTokenInvalidError,
)
from app.models.channel_link_token import ChannelLinkToken
from app.services.channel_link_token_service import ChannelLinkTokenService


@pytest.mark.asyncio
async def test_validate_token_returns_valid_token() -> None:
    repository = AsyncMock()

    link_token = ChannelLinkToken(
        id=1,
        user_id=30,
        token="abc123",
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        used_at=None,
    )

    repository.get_by_token.return_value = link_token

    service = ChannelLinkTokenService(repository)

    result = await service.validate_token("abc123")

    assert result == link_token

@pytest.mark.asyncio
async def test_validate_token_rejects_invalid_token() -> None:
    repository = AsyncMock()
    repository.get_by_token.return_value = None

    service = ChannelLinkTokenService(repository)

    with pytest.raises(ChannelLinkTokenInvalidError):
        await service.validate_token("invalid-token")

@pytest.mark.asyncio
async def test_validate_token_rejects_expired_token() -> None:
    repository = AsyncMock()

    link_token = ChannelLinkToken(
        id=1,
        user_id=30,
        token="expired-token",
        expires_at=datetime.now(UTC) - timedelta(minutes=1),
        used_at=None,
    )

    repository.get_by_token.return_value = link_token

    service = ChannelLinkTokenService(repository)

    with pytest.raises(ChannelLinkTokenExpiredError):
        await service.validate_token("expired-token")

@pytest.mark.asyncio
async def test_validate_token_rejects_used_token() -> None:
    repository = AsyncMock()

    link_token = ChannelLinkToken(
        id=1,
        user_id=30,
        token="used-token",
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        used_at=datetime.now(UTC),
    )

    repository.get_by_token.return_value = link_token

    service = ChannelLinkTokenService(repository)

    with pytest.raises(ChannelLinkTokenAlreadyUsedError):
        await service.validate_token("used-token")

@pytest.mark.asyncio
async def test_mark_as_used_updates_token() -> None:
    repository = AsyncMock()

    link_token = ChannelLinkToken(
        id=1,
        user_id=30,
        token="abc123",
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
        used_at=None,
    )

    repository.mark_as_used.return_value = link_token

    service = ChannelLinkTokenService(repository)

    result = await service.mark_as_used(link_token)

    assert result == link_token

    repository.mark_as_used.assert_awaited_once()

    called_kwargs = repository.mark_as_used.await_args.kwargs

    assert called_kwargs["link_token"] == link_token
    assert called_kwargs["used_at"].tzinfo is not None