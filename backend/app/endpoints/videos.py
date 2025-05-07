import asyncio, json, os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query, Request
from typing import Annotated, AsyncGenerator

from fastapi.responses import StreamingResponse

from app.http import http_client
from app.auth import CURRENT_TOKEN, get_token
from db import MongoDB, get_mongo_instance

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
    responses={404: {"description": "Not found"}},
)


async def video_stream_generator(db: MongoDB, game_id: str, token: str, request: Request) -> AsyncGenerator[str, None]:
    """Generates Server-Sent Events for videos"""
    last_known_video_ids = set()
    initial_fetch_done = False
    polling_interval_seconds = 5

    try:
        while True:
            if await request.is_disconnected():
                print(f"Client disconnected for game_id {game_id}, stopping stream.")
                break

            # Check if the videos are already
            # in the database based on the game_id
            cursor = await db.find(
                os.getenv("VIDEOS_COLLECTION"), {"game_id": game_id}, multiple=True
            )
            cached_videos = await cursor.to_list()
            if cached_videos:
                print(f"SSE Stream: Found {len(cached_videos)} videos from cache")
                for video in cached_videos:
                    del video['_id']
                    del video['cached_at']
                yield f"event: newVideos\ndata: {json.dumps(cached_videos)}\n\n"
                await asyncio.sleep(polling_interval_seconds)
                continue

            print(f"SSE Stream: Fetching videos for game_id: {game_id}")
            current_videos = []
            error_occurred = False
            try:
                response = await http_client.get(
                    url=f"{os.getenv('TWITCH_API_URL')}/videos?game_id={game_id}&language=fr",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Client-Id": os.getenv("CLIENT_ID"),
                    },
                )
                response.raise_for_status()
                json_response = response.json()

                if "data" not in json_response or not isinstance(json_response["data"], list):
                    raise ValueError("Invalid response structure from Twitch API")

                current_videos = json_response["data"]
                # Cache
                if current_videos: 
                    cached_at = datetime.now(timezone.utc)
                    videos_to_cache = []
                    for video in current_videos:
                        video["cached_at"] = cached_at
                        video["game_id"] = game_id
                        videos_to_cache.append(video)
                    if videos_to_cache:
                        print(f"SSE Stream: {len(current_videos)} videos cached")
                        await db.insert(os.getenv("VIDEOS_COLLECTION"), videos_to_cache)

                current_video_ids = {v['id'] for v in current_videos}
                new_videos = []
                if not initial_fetch_done:
                    new_videos = current_videos
                    last_known_video_ids = current_video_ids
                    initial_fetch_done = True
                    print(f"SSE Stream: Initial fetch completed, sending {len(new_videos)} videos.")
                else:
                    new_videos = [v for v in current_videos if v['id'] not in last_known_video_ids]
                    if new_videos:
                        print(f"SSE Stream: Found {len(new_videos)} new videos.")
                        last_known_video_ids = current_video_ids

                if new_videos:
                    try:
                        for video in new_videos:
                            del video['_id']
                            del video['cached_at']
                        json_data = json.dumps(new_videos)
                    except TypeError as e:
                        print(f"Erreur de sérialisation JSON pour SSE: {e}")
                        json_data = json.dumps({"error": "Failed to serialize video data"})

                    yield f"event: newVideos\ndata: {json_data}\n\n"

            except Exception as e:
                print(f"SSE Stream: Error during fetch/processing for game_id {game_id}: {e}")
                yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"

            print(f"SSE Stream: Waiting {polling_interval_seconds}s before next poll...")
            print("- - - - - - - - - -")
            await asyncio.sleep(polling_interval_seconds)
    
    except asyncio.CancelledError:
         print(f"SSE Stream - GameID {game_id}: Generator task cancelled (outside loop).")
    except Exception as e:
        # Log any exception that might occur outside the main loop but within the generator
        print(f"SSE Stream - GameID {game_id}: Unexpected error in generator: {e}")
    finally:
        # Optional: Add any cleanup logic here if needed
        print(f"SSE Stream - GameID {game_id}: Generator function finished.")


@router.get("")
async def get_videos(
    request: Request, game_id: Annotated[str, Query()], db: MongoDB = Depends(get_mongo_instance)
):
    global CURRENT_TOKEN
    if not CURRENT_TOKEN:
        CURRENT_TOKEN = await get_token()

    return StreamingResponse(video_stream_generator(db, game_id, CURRENT_TOKEN, request), media_type="text/event-stream")
