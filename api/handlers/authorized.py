from typing import List

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache

from api.handlers.dependencies import get_current_user
from api.schemas.auth import UserResponse
from api.schemas.response_schema import HistoryResponse
from common.exceptions import VideoNotFoundException
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
@cache(expire=10)
async def get_history(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(6, description="Размер страницы"),
    current_user: Users = Depends(get_current_user),
) -> List[HistoryResponse]:
    video_history_list = await VideoRepository.find_by_filter_with_pagination(
        user=current_user.id,
        offset=(page - 1) * page_size,
        limit=page_size,
    )
    history_responses = []

    for video_history in video_history_list:
        if "youtu" in video_history.url:
            preview_url, _, title = get_information_youtube(video_history.url)
        elif "vk" in video_history.url:
            preview_url, title = get_information_vk(video_history.url)
        history_responses.append(
            HistoryResponse(
                id=video_history.id,
                url=video_history.url,
                preview_url=preview_url,
                title=title,
                download_at=video_history.download_at.isoformat(),
            )
        )
    return history_responses


@router.post(
    "/history_remove",
    summary="Удаление записи из истории",
    description="Позволяет аутентифицированным пользователям удалить ролик из истории запросов",
)
async def remove_history(
    video_id: int, current_user: Users = Depends(get_current_user)
):
    result = await VideoRepository.remove_by_filter(id=video_id, user=current_user.id)
    if result == 0:
        raise VideoNotFoundException
    else:
        return {"status": "Запись в истории запросов успешно удалена"}


@router.get(
    "/about_user",
    summary="Информация об авторизованном пользователе",
    description="Возвращает информацию о текущем авторизованном пользователе.",
)
@cache(expire=10)
async def about_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return current_user
