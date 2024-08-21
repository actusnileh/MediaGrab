from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

import sentry_sdk
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.api.v1.routes import routers as v1_routers
from app.api.v2.routes import routers as v2_routers
from app.core.config import configs
from app.core.database import engine
from app.core.security.admin_security import authentication_backend
from app.infrastructure.admin.user_admin import UserAdmin
from app.infrastructure.admin.videos_admin import VideosAdmin


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{configs.redis_host}:{configs.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


def create_app():
    sentry_sdk.init(
        dsn=configs.sentry_token,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    app = FastAPI(
        title=configs.title,
        version="1.2",
        debug=configs.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_routers, prefix="/v1")
    app.include_router(v2_routers, prefix="/v2")

    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(VideosAdmin)
    return app
