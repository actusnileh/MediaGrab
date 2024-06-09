from fastapi.routing import APIRouter

from api.schemas.response_schema import Information_Response
from services.information import get_information_vk, get_information_youtube


router = APIRouter(tags=["Information"], prefix="/information")


@router.get(
    "",
    summary="Получить информацию о ролике",
    description="""
    Получить информацию о ролике:\n\n
    - Прямая ссылка на превью ролика\n
    - Название ролика\n
    - Автор ролика (Название канала)

    """,
)
async def get_video_information(url: str) -> Information_Response:
    try:
        if "youtube" in url:
            preview_url, author_name, title = get_information_youtube(url)
        elif "vk" in url:
            preview_url, title = get_information_vk(url)
            author_name = "ВКонтакте"
    except Exception:
        return Information_Response(
            message="EROOR",
            preview_url="ERROR",
            author_name="ERROR",
            title="ERROR",
        )
    else:
        return Information_Response(
            message="OK",
            preview_url=preview_url,
            author_name=author_name,
            title=title,
        )
