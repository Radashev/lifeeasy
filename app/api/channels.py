from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_channel_link_token_service,
    get_current_user,
)
from app.models.user import User
from app.schemas.channel import ChannelLinkTokenResponse
from app.services.channel_link_token_service import ChannelLinkTokenService

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@router.post(
    "/telegram/link-token",
    response_model=ChannelLinkTokenResponse,
)
async def create_telegram_link_token(
    current_user: User = Depends(get_current_user),
    service: ChannelLinkTokenService = Depends(
        get_channel_link_token_service
    ),
) -> ChannelLinkTokenResponse:
    link_token = await service.create_token(
        user_id=current_user.id,
    )

    return ChannelLinkTokenResponse.model_validate(link_token)