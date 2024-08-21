from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.download import router as download_router
from app.api.v1.endpoints.help import router as help_router
from app.api.v1.endpoints.history import router as history_router
from app.api.v1.endpoints.information import router as information_router

routers = APIRouter()
router_list = [
    auth_router,
    download_router,
    help_router,
    history_router,
    information_router,
]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
