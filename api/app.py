from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.settings import settings

from api.handlers.download import router as download_router
from api.handlers.information import router as information_router
from api.handlers.cache import router as cache_router
from api.handlers.auth import router as auth_router
from api.handlers.authorized import router as history_router


def create_app():
    app = FastAPI(title=settings.title, debug=settings.debug)
    app.include_router(download_router)
    app.include_router(information_router)
    app.include_router(cache_router)
    app.include_router(history_router)
    app.include_router(auth_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
