from datetime import datetime
from typing import Optional

from app.core.exceptions import InternalError
from app.infrastructure.download_infra import YtDLPDownloader
from app.model.users import Users
from app.repository.video_repository import VideoRepository
from app.schema.video_schema import VideoSchema
from app.tasks.download_tasks import clear_video_cache


class DownloadService:
    def __init__(self, video_repo: VideoRepository, video_downloader: YtDLPDownloader):
        self.video_repo = video_repo
        self.video_downloader = video_downloader

    async def download_video(
        self,
        video: VideoSchema,
        user: Optional[Users],
    ) -> tuple[str, str]:
        try:
            file_path, file_name = await self.video_downloader.download_video(
                video=video,
            )
        except Exception:
            raise InternalError("Error downloading video")

        if user:
            await self.video_repo.add(
                user=user.id,
                url=video.url,
                download_at=datetime.now(),
            )

        clear_video_cache.apply_async(args=[file_name], countdown=30)

        return file_path, file_name
