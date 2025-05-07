from typing import List
from pydantic import BaseModel


class TwitchToken(BaseModel):
    access_token: str
    expires_in: int  # seconds until the token expires
    token_type: str


class TwitchCategory(BaseModel):
    # Twitch API fields
    id: str
    name: str
    box_art_url: str


class TwitchCategoryResponse(BaseModel):
    data: List[TwitchCategory] | None
