from typing import List
from pydantic import BaseModel


class TwitchToken(BaseModel):
    access_token: str
    expires_in: int  # seconds until the token expires
    token_type: str


class TwitchVideo(BaseModel):
    id: str
    stream_id: str
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
    data: List[TwitchVideo]
    pagination: dict
