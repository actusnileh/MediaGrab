from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from common.settings import settings

from api.handlers.download import router as download_router
from api.handlers.information import router as information_router
from api.handlers.cache import router as cache_router
from api.handlers.auth import router as auth_router
from api.handlers.authorized import router as history_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


def create_app():
    app = FastAPI(title=settings.title, debug=settings.debug, lifespan=lifespan)
    app.include_router(download_router)
    app.include_router(information_router)
    app.include_router(cache_router)
    app.include_router(history_router)
    app.include_router(auth_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin,",
            "Authorization",
        ],
    )
    return app
