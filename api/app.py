from fastapi import FastAPI
from common.settings import settings
from api.handlers.youtube import router as youtube_router


def create_app():
    app = FastAPI(title=settings.title, debug=settings.debug)
    app.include_router(youtube_router, prefix="/v1")
    return app
