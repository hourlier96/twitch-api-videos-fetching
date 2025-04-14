import os
import re

from datetime import datetime, timezone
from typing import Annotated
from urllib.parse import quote
from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import get_token
from app.auth import CURRENT_TOKEN
from app.models import TwitchCategoryResponse
from app.http import http_client
from db import MongoDB, get_mongo_instance


router = APIRouter(
    prefix="/categories",
    tags=["Cateogries"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=TwitchCategoryResponse,
)
async def get_categories(
    game_label: Annotated[str, Query()], db: MongoDB = Depends(get_mongo_instance)
) -> TwitchCategoryResponse:
    global CURRENT_TOKEN
    if not CURRENT_TOKEN:
        CURRENT_TOKEN = await get_token()

    # Check if a category matches start of the game label
    query_filter = {
        "name": {
            "$regex": f"^{re.escape(game_label)}",
            "$options": "i",
        }
    }

    cursor = await db.find(
        os.getenv("CATEGORIES_COLLECTION"), query_filter, multiple=True
    )
    cached_categories = await cursor.to_list()
    if cached_categories:
        print("Found categories from cache")
        return {"data": cached_categories}

    encoded_game_label = quote(game_label)
    # If not, fetch from Twitch API
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

    # Filter categories based on the game label
    matching_categories = [
        category
        for category in response.json()["data"]
        if category["name"].lower().startswith(game_label.lower())
    ]
    if not matching_categories:
        raise HTTPException(
            status_code=404,
            detail=f"No categories found for '{game_label}'",
        )
    # Insert matching categories into the database
    cached_at = datetime.now(timezone.utc)
    for c in matching_categories:
        c["cached_at"] = cached_at
        await db.insert(
            os.getenv("CATEGORIES_COLLECTION"),
            c,
        )
    return response.json()
