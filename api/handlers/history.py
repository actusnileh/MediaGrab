from fastapi import Depends
from fastapi.routing import APIRouter
from api.handlers.dependencies import get_current_user
from api.schemas.auth import UserResponse
from database.users.models import Users

router = APIRouter(tags=["Authorized Section"], prefix="/authorized")


@router.get(
    "/history",
)
async def get_history(user: Users = Depends(get_current_user)):
    return {"data": "пусто"}


@router.get(
    "/about_user",
    summary="Информация об авторизованном пользователе",
    description="Возвращает информацию о текущем авторизованном пользователе.",
)
async def about_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return current_user
