
## Installation

1. Create a virtual environment:

```bash
cd backend

# With uv (recommended)
pip install uv
uv python install 3.12
uv venv
source .venv/bin/activate 

# Or use any tool you prefer
```

2. Install dependencies

```bash
uv pip install -r requirements.txt
```

3. Create .env based on .env_template (you need a registered application in [Twitch dev console](https://dev.twitch.tv/console), to get client_id & client_secret)

4. Install a MongoDB server. The API is configured staticly to read on default port (mongodb://localhost:27017/)

```bash
# For MACOS
# https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/

# For Linux
# https://www.mongodb.com/docs/manual/administration/install-on-linux/
```

## Run

```bash
# Use launch.json to use debugger

# or run the server with FastAPI CLI

fastapi dev
```

## Explanations

### Authentication

The application asks for an OAuth2 token to call the Twitch API.

It automatically fetch a token on first Twitch API call, then it's stored in-memory to avoid re-asking token every time.

Each time the application is reloaded, the token is lost, then re-fetched.

### Cache strategy

The MongoDB instance is used to cache the Twitch API results.

At application startup, it creates a database 'twitch_records' with 2 collections 'categories_recorded' & 'videos_recorded'.

Each collection has a 3m TTL before documents are deleted, so any new call to the API is just getted from the instance.

So any 'already searched' game & video will be much faster, & preserve Twitch API quotas.
