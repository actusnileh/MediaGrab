from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator

from redis import asyncio as aioredis

from api.admin.views import UserAdmin, VideosAdmin
from common.settings import settings

from api.handlers.download import router as download_router
from api.handlers.information import router as information_router
from api.handlers.auth import router as auth_router
from api.handlers.authorized import router as history_router
from api.admin.auth import authentication_backend
from database.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


def create_app():
    sentry_sdk.init(
        dsn=settings.sentry_key,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    app = FastAPI(title=settings.title, debug=settings.debug, lifespan=lifespan)
    app.include_router(download_router)
    app.include_router(information_router)
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

    instrumentator = Instrumentator(
        should_group_status_codes=False,
        excluded_handlers=[".*admin.*", "/metrics"],
    )

    instrumentator.instrument(app).expose(app)

    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(VideosAdmin)
    return app
