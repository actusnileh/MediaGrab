import re

from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache
from pytube.exceptions import VideoUnavailable

from api.schemas.response_schema import InformationResponse
from common.exceptions import UrlFormatException
from services.information import get_information_vk, get_information_youtube
from services.sponsorblock import get_sponsor_segments

router = APIRouter(tags=["Information"], prefix="/information")

youtube_regex = re.compile(
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
)
vk_video_regex = re.compile(r"^(?:https?:\/\/)?(?:www\.)?vk\.com\/video-\d+_\d+$")


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
        if youtube_regex.match(url):
            preview_url, author_name, title, length = get_information_youtube(url)
            sponsorblock_segments: list = get_sponsor_segments(url)
        elif vk_video_regex.match(url):
            preview_url, title, length = get_information_vk(url)
            author_name = "ВКонтакте"
            sponsorblock_segments = []
        else:
            raise UrlFormatException
    except VideoUnavailable:
        return InformationResponse(
            preview_url="Ролик недоступен",
            author_name="Ролик недоступен",
            title="Ролик недоступен",
            length="Ролик недоступен",
            sponsor_segments=[],
        )
    except (KeyError, IndexError):
        return InformationResponse(
            preview_url="Ошибка получения информации",
            author_name="Ошибка получения информации",
            title="Ошибка получения информации",
            length="Ошибка получения информации",
            sponsor_segments=[],
        )
    else:
        return InformationResponse(
            preview_url=preview_url,
            author_name=author_name,
            title=title,
            length=length,
            sponsor_segments=sponsorblock_segments,
        )
