import re

from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache
from pytube.exceptions import VideoUnavailable

from api.schemas.response_schema import InformationResponse
from common.exceptions import UrlFormatException
from services.information import get_information_vk, get_information_youtube
from services.sponsorblock import get_sponsor_segments

router = APIRouter(tags=["Information"], prefix="/information")

url_patterns = {
    "youtube": re.compile(
        r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    ),
    "vk": re.compile(r"^(?:https?:\/\/)?(?:www\.)?vk\.com\/video-\d+_\d+$"),
}


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
        if url_patterns["youtube"].match(url):
            data["preview_url"], data["author_name"], data["title"], data["length"] = (
                get_information_youtube(url)
            )
            data["sponsor_segments"] = get_sponsor_segments(url)
        elif url_patterns["vk"].match(url):
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
