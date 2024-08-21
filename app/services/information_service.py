from typing import Union

from app.core.exceptions import (
    InternalError,
    NotFoundError,
)
from app.infrastructure.information_infra import (
    VkInfra,
    YouTubeInfra,
)
from app.schema.information_schema import InformationResponse
from app.utils.url_patterns import YOUTUBE_REGEX


class InformationService:
    def __init__(self):
        self.infras = {
            "youtube": YouTubeInfra(),
            "vk": VkInfra(),
        }

    def get_information(self, url: str):
        platform = self.determine_platform(url)
        infra = self.infras.get(platform)

        if not infra:
            raise NotFoundError(detail=f"Url '{url}' not supported")

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
        if YOUTUBE_REGEX.match(url):
            return "youtube"
        elif "vk" in url:  # TODO: добавить regex
            return "vk"
        else:
            return None
