import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from pymongo.errors import ConnectionFailure


from app.endpoints.categories import router as categories_router
from app.endpoints.videos import router as videos_router
from db import MongoDB, setup_mongodb_indexes

load_dotenv()


app = FastAPI()
app.include_router(categories_router)
app.include_router(videos_router)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to MongoDB...")
    try:
        mongo = MongoDB("mongodb://localhost:27017/", "twitch_records")
        app.state.mongo = mongo
        await setup_mongodb_indexes()
        print(
            "Application startup: Successfully connected to MongoDB database 'twitch_records'!"
        )
    except ConnectionFailure as e:
        if mongo.client:
            mongo.client.close()
        raise RuntimeError("Database connection failed during startup") from e
    yield
    if hasattr(app.state, "mongo_client") and app.state.mongo.client:
        app.state.mongo.client.close()


app.router.lifespan_context = lifespan


@app.get("/")
def health():
    return {"status": "OK"}
