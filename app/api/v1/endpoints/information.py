from fastapi import (
    APIRouter,
    Query,
)

from fastapi_cache.decorator import cache

from app.schema.information_schema import InformationResponse
from app.services.information_service import InformationService


router = APIRouter(tags=["Information"], prefix="/information")


@router.get(
    "",
    description="""
    Получить информацию о ролике:\n\n
    - Прямая ссылка на превью ролика\n
    - Название ролика\n
    - Автор ролика (Название канала)\n
    - Длительность\n
    - Спонсорские сегменты
    """,
    response_model=InformationResponse,
)
@cache(expire=60)
async def get_video_information(url: str = Query(description="Ссылка на видеоролик")):
    return InformationService().get_information(url)
