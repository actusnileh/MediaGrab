from fastapi import APIRouter

routers = APIRouter()
router_list = []

for router in router_list:
    router.tags = routers.tags.append("v2")
    routers.include_router(router)
