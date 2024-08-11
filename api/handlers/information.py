from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache
from pytube.exceptions import VideoUnavailable

from api.schemas.response_schema import InformationResponse
from common.exceptions import UrlFormatException
from common.regex import URL_PATTERNS
from services.information import get_information_vk, get_information_youtube
from services.sponsorblock import get_sponsor_segments

router = APIRouter(tags=["Information"], prefix="/information")


@router.get(
    "",
    summary="Получить информацию о ролике",
    description="""
    Получить информацию о ролике:\n\n
    - Прямая ссылка на превью ролика\n
    - Название ролика\n
    - Автор ролика (Название канала)\n
    - Длительность\n
    - Спонсорские сегменты
    """,
)
@cache(expire=60)
async def get_video_information(url: str) -> InformationResponse:
    try:
        data = {}
        if URL_PATTERNS["youtube"].match(url):
            data["preview_url"], data["author_name"], data["title"], data["length"] = (
                get_information_youtube(url)
            )
            data["sponsor_segments"] = get_sponsor_segments(url)
        elif URL_PATTERNS["vk"].match(url):
            data["preview_url"], data["title"], data["length"] = get_information_vk(url)
            data["author_name"] = "ВКонтакте"
            data["sponsor_segments"] = []
        else:
            raise UrlFormatException
    except VideoUnavailable:
        data = {
            "preview_url": "Ролик недоступен",
            "author_name": "Ролик недоступен",
            "title": "Ролик недоступен",
            "length": "Ролик недоступен",
            "sponsor_segments": [],
        }
    except (KeyError, IndexError):
        data = {
            "preview_url": "Ошибка получения информации",
            "author_name": "Ошибка получения информации",
            "title": "Ошибка получения информации",
            "length": "Ошибка получения информации",
            "sponsor_segments": [],
        }

    return InformationResponse(**data)
