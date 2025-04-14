
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

4. Install a MongoDB server. The API is configured to read on default port (mongodb://localhost:27017/)

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
