import os

from app.http import http_client

# Local cache for testing
CURRENT_TOKEN = None


async def get_token():
    global CURRENT_TOKEN
    try:
        if CURRENT_TOKEN:
            # TODO: check if token is expired
            return CURRENT_TOKEN
        else:
            print("Fetching Twitch token...")
            response = await http_client.post(
                url=os.getenv("TWITCH_OAUTH_URL"),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "client_id": os.getenv("CLIENT_ID"),
                    "client_secret": os.getenv("CLIENT_SECRET"),
                    "grant_type": "client_credentials",
                },
            )
            return response.json()["access_token"]
    except Exception as e:
        print("Error fetching Twitch token:", e)
        return {"error": str(e)}
