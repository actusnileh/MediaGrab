import os
from typing import Optional

import aiofiles
from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

from app.core.dependencies import get_current_user_optional
from app.infrastructure.download_infra import YtDLPDownloader
from app.model.users import Users
from app.repository.video_repository import VideoRepository
from app.schema.video_schema import VideoSchema
from app.services.download_service import DownloadService

router = APIRouter(tags=["Download"], prefix="/download")


async def iterfile(file_path):
    async with aiofiles.open(file_path, mode="rb") as f:
        while chunk := await f.read(1024):
            yield chunk


@router.get(
    "",
    summary="Скачать видео/аудио с YouTube и VK.",
    description="""
    Качество видео:
- `lowest` - 144p
- `low` - 240p
- `medium` - 360p
- `high` - 720p
- `highest` - 1080p

    Примечания:
    - Параметр `only_audio` позволяет загрузить только аудиодорожку.
    - Параметр `sponsorblock` позволяет удалить из видеоролика YouTube рекламные интеграции.

    - Если пользователь авторизован, то видеоролик попадёт в историю его запросов.
    """,
)
async def download_video(
    video: VideoSchema = Depends(),
    user: Optional[Users] = Depends(get_current_user_optional),
):
    file_path, file_name = await DownloadService(
        video_repo=VideoRepository, video_downloader=YtDLPDownloader).download_video(video, user)
    media_type = "audio/m4a" if video.only_audio else "video/webm"
    file_size = os.path.getsize(file_path)
    response = StreamingResponse(iterfile(file_path), media_type=media_type)
    response.headers["Content-Disposition"] = f'attachment; filename="{file_name}"'
    response.headers["Content-Length"] = str(file_size)
    return response
