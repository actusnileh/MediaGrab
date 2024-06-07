from fastapi import FastAPI
from common.settings import settings
from api.handlers.download import router


def create_app():
    app = FastAPI(title=settings.title, debug=settings.debug)
    app.include_router(router, prefix="/v1")
    return app
