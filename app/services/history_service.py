from app.core.exceptions import NotFoundError
from app.infrastructure.information_infra import (
    RuTubeInfra,
    VkInfra,
    YouTubeInfra,
)
from app.model.users import Users
from app.repository.video_repository import VideoRepository
from app.schema.history_schema import HistoryResponse
from app.utils.url_patterns import (
    RUTUBE_REGEX,
    VK_REGEX,
    YOUTUBE_REGEX,
)


class HistoryService:
    def __init__(self, video_repo: VideoRepository):
        self.video_repo = video_repo

    async def get_history(self, page: int, page_size: int, current_user: Users):
        video_history_list = await self.video_repo.find_by_filter_with_pagination(
            user=current_user.id,
            offset=(page - 1) * page_size,
            limit=page_size,
        )
        history_responses = []
        for video_history in video_history_list:
            if YOUTUBE_REGEX.match(video_history.url):
                preview_url, _, title, _ = YouTubeInfra().get_information(
                    url=video_history.url,
                )
            elif VK_REGEX.match(video_history.url):
                preview_url, _, title, _ = VkInfra().get_information(video_history.url)
            elif RUTUBE_REGEX.match(video_history.url):
                preview_url, _, title, _ = RuTubeInfra().get_information(
                    video_history.url,
                )
            history_responses.append(
                HistoryResponse(
                    id=video_history.id,
                    url=video_history.url,
                    preview_url=preview_url,
                    title=title,
                    download_at=video_history.download_at.isoformat(),
                ),
            )
        return history_responses

    async def remove_history(self, id: int, current_user: Users):
        result = await VideoRepository.remove_by_filter(id=id, user=current_user.id)
        if result == 0:
            raise NotFoundError(f"Video with id '{id}' not found")
        else:
            return {"status": "OK"}
