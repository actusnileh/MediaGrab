from fastapi import Depends
from fastapi.routing import APIRouter
from api.handlers.dependencies import get_current_user
from database.users.models import Users

router = APIRouter(tags=["История скачивания"], prefix="/history")


@router.get(
    "/history",
)
async def get_history(user: Users = Depends(get_current_user)):
    return {"data": "пусто"}
