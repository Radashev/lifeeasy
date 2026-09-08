from datetime import datetime

from pydantic import BaseModel


class ChannelLinkTokenResponse(BaseModel):
    token: str
    expires_at: datetime

    model_config = {
        "from_attributes": True,
    }