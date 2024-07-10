from typing import List
from fastapi import Depends
from fastapi.routing import APIRouter
from api.handlers.dependencies import get_current_user
from api.schemas.auth import UserResponse
from api.schemas.response_schema import HistoryResponse
from database.users.models import Users
from database.videos.repository import VideoRepository
from services.information import get_information_vk, get_information_youtube

router = APIRouter(tags=["Authorized Section"], prefix="/authorized")


@router.get(
    "/history",
    summary="Получение истории видео пользователя",
    description="Позволяет аутентифицированным пользователям получить свою историю видео.\
        Возвращает список записей о видео",
)
async def get_history(
    current_user: Users = Depends(get_current_user),
) -> List[HistoryResponse]:
    video_history_list = await VideoRepository.find_by_filter(user=current_user.id)
    history_responses = []

    for video_history in video_history_list:
        if "youtu" in video_history.url:
            preview_url, _, _ = get_information_youtube(video_history.url)
        elif "vk" in video_history.url:
            preview_url, _ = get_information_vk(video_history.url)
        history_responses.append(
            HistoryResponse(
                id=video_history.id,
                url=video_history.url,
                preview_url=preview_url,
                download_at=video_history.download_at.isoformat(),
            )
        )

    return history_responses


@router.get(
    "/about_user",
    summary="Информация об авторизованном пользователе",
    description="Возвращает информацию о текущем авторизованном пользователе.",
)
async def about_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return current_user
