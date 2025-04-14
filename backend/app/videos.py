import os

from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from urllib.parse import quote

from app.http import http_client
from app.auth import CURRENT_TOKEN, get_token
from app.models import TwitchVideoResponse

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=TwitchVideoResponse)
async def get_videos(game_label: Annotated[str, Query()]) -> TwitchVideoResponse:
    global CURRENT_TOKEN
    if not CURRENT_TOKEN:
        CURRENT_TOKEN = await get_token()

    # TODO: move categories in separate endpoint
    encoded_game_label = quote(game_label)

    response = await http_client.get(
        url=f"{os.getenv('TWITCH_API_URL')}/search/categories?query={encoded_game_label}",
        headers={
            "Authorization": f"Bearer {CURRENT_TOKEN}",
            "Client-Id": os.getenv("CLIENT_ID"),
        },
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Error fetching Twitch categories",
        )

    matching_categories = [
        category
        for category in response.json()["data"]
        if category["name"].lower().startswith(game_label.lower())
    ]
    if not matching_categories:
        return {"error": "No matching categories found"}

    # TODO: handle multiple categories
    response = await http_client.get(
        url=f"{os.getenv('TWITCH_API_URL')}/videos?game_id={matching_categories[0]['id']}&language=fr",
        headers={
            "Authorization": f"Bearer {CURRENT_TOKEN}",
            "Client-Id": os.getenv("CLIENT_ID"),
        },
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Error fetching Twitch videos",
        )

    return response.json()
