from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from fastapi_cache.decorator import cache

from app.core.dependencies import get_current_user
from app.model.users import Users
from app.repository.video_repository import VideoRepository
from app.schema.history_schema import HistoryResponse
from app.services.history_service import HistoryService


router = APIRouter(tags=["History"], prefix="/history")


@router.get(
    "",
    summary="Получение истории скачанных видео",
    response_model=list[HistoryResponse],
)
@cache(expire=10)
async def get_history(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(6, description="Размер страницы"),
    current_user: Users = Depends(get_current_user),
):
    return await HistoryService(video_repo=VideoRepository).get_history(
        page,
        page_size,
        current_user,
    )


@router.post(
    "/remove",
    summary="Удаление записи из истории",
)
async def remove_history(
    video_id: int = Query(ge=1, description="Номер видеоролика"),
    current_user: Users = Depends(get_current_user),
):
    return await HistoryService(video_repo=VideoRepository).remove_history(
        video_id,
        current_user,
    )
