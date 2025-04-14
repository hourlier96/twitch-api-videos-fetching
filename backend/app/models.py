from typing import List
from pydantic import BaseModel


class TwitchToken(BaseModel):
    access_token: str
    expires_in: int  # seconds until the token expires
    token_type: str


class TwitchVideo(BaseModel):
    id: str
    stream_id: str | None
    user_id: str
    user_login: str
    user_name: str
    title: str
    description: str
    created_at: str
    published_at: str
    url: str
    thumbnail_url: str
    viewable: str
    view_count: int
    language: str
    type: str
    duration: str
    muted_segments: List[dict] | None


class TwitchVideoResponse(BaseModel):
    # Twitch API fields
    data: List[TwitchVideo]
    pagination: dict | None


class TwitchCategory(BaseModel):
    # Twitch API fields
    id: str
    name: str
    box_art_url: str


class TwitchCategoryResponse(BaseModel):
    data: List[TwitchCategory] | None
