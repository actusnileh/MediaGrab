from fastapi.routing import APIRouter

router = APIRouter(tags=["download"], prefix="/youtube")


@router.get(
    "video",
    summary="Получить ролик по ссылке YouTube",
    description="Получить ролик по ссылке YouTube",
)
async def get_video_youtube():
    pass
