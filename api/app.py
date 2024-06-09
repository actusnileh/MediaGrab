from fastapi import FastAPI
from common.settings import settings
from api.handlers.download import router as download_router
from api.handlers.information import router as information_router


def create_app():
    app = FastAPI(title=settings.title, debug=settings.debug)
    app.include_router(download_router, prefix="/v1")
    app.include_router(information_router, prefix="/v1")
    return app
