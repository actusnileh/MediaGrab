from fastapi.routing import APIRouter

from api.schemas.response_schema import Information_Response
from services.information import get_information


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
async def get_video_youtube(url: str) -> Information_Response:
    try:
        preview_url, author_name, titile = get_information(url)
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
            title=titile,
        )
