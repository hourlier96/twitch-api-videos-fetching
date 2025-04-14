
## Installation

1. Create a virtual environment:

```bash
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

3. Create .env based on .env_template (you need a registered application in Twitch dev console)

## Run

```bash
# Use launch.json to use debugger

# or run the server with FastAPI CLI
fastapi dev
```
