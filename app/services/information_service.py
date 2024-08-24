from typing import Union

from app.core.exceptions import (
    InternalError,
    NotFoundError,
)
from app.infrastructure.information_infra import (
    KinopoiskInfra,
    RuTubeInfra,
    VkInfra,
    YouTubeInfra,
)
from app.schema.information_schema import InformationResponse
from app.utils.url_patterns import URL_PATTERNS


class InformationService:
    def __init__(self):
        self.infras = {
            "youtube": YouTubeInfra(),
            "vk": VkInfra(),
            "rutube": RuTubeInfra(),
            "kinopoisk": KinopoiskInfra(),
        }

    def get_information(self, url: str):
        platform = self.determine_platform(url)
        infra = self.infras.get(platform)

        if not infra:
            raise NotFoundError(detail="Url not supported")

        try:
            preview_url, author, title, length = infra.get_information(url)
            sponsor_segments = infra.get_sponsor_segments(url)
        except Exception:
            raise InternalError(
                f"Error retrieving information from service '{platform}'",
            )

        return InformationResponse(
            preview_url=preview_url,
            author=author,
            title=title,
            length=length,
            sponsor_segments=sponsor_segments,
        )

    def determine_platform(self, url: str) -> Union[str, None]:
        if URL_PATTERNS["YouTube"].match(url):
            return "youtube"
        elif URL_PATTERNS["VK"].match(url):
            return "vk"
        elif URL_PATTERNS["RuTube"].match(url):
            return "rutube"
        elif URL_PATTERNS["Kinopoisk"].match(url):
            return "kinopoisk"
        else:
            return None
