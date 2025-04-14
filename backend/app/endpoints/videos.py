import os

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from app.http import http_client
from app.auth import CURRENT_TOKEN, get_token
from app.models import TwitchVideoResponse
from db import MongoDB, get_mongo_instance

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=TwitchVideoResponse)
async def get_videos(
    game_id: Annotated[str, Query()], db: MongoDB = Depends(get_mongo_instance)
):
    global CURRENT_TOKEN
    if not CURRENT_TOKEN:
        CURRENT_TOKEN = await get_token()

    # Check if the videos are already in the database
    # based on the category_id
    cursor = await db.find(
        os.getenv("VIDEOS_COLLECTION"), {"game_id": game_id}, multiple=True
    )
    cached_videos = await cursor.to_list()
    if cached_videos:
        print("Found videos from cache")
        return {"data": cached_videos, "pagination": None}

    response = await http_client.get(
        url=f"{os.getenv('TWITCH_API_URL')}/videos?game_id={game_id}&language=fr",
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

    # Filter videos based on the game_id
    matching_videos = [video for video in response.json()["data"]]
    if not matching_videos:
        raise HTTPException(
            status_code=404,
            detail="No videos found for the specified category",
        )
    # Add the current timestamp to each video
    for video in matching_videos:
        video["game_id"] = game_id

    # Insert the videos into the database
    await db.insert(os.getenv("VIDEOS_COLLECTION"), matching_videos)

    return response.json()
