from datetime import datetime
from typing import Optional

from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from yt_dlp.utils import YoutubeDLError

from api.handlers.dependencies import get_current_user_optional
from api.schemas.download_schema import VideoSchema
from common.exceptions import DownloadErrorException
from database.users.models import Users
from database.videos.repository import VideoRepository
from services.download import download_video
from services.tasks.tasks import clear_video_cache

router = APIRouter(tags=["Download"], prefix="/video_audio")


@router.get(
    "",
    summary="Скачать видео/аудио с YouTube и VK.",
    description="""
    Скачать видео/аудио с YouTube и VK с возможностью выбора качества видеоролика.

    Качество видео:
    - `lowest` - 144p
    - `low` - 240p
    - `medium` - 360p
    - `high` - 720p
    - `highest` - 1080p

    Примечания:
    - Параметр `only_audio` позволяет загрузить только аудиодорожку в формате MP3.
    - Параметр `sponsorblock` позволяет удалить из видеоролика YouTube рекламные интеграции.

    - Если пользователь авторизован, то видеоролик попадёт в историю его запросов.
    """,
)
async def get_video(
    video: VideoSchema = Depends(),
    user: Optional[Users] = Depends(
        get_current_user_optional,
    ),
):
    try:
        file_path, file_name = await download_video(video)
    except (YoutubeDLError, Exception):
        raise DownloadErrorException
    else:
        if "mp4" in file_name:
            response = FileResponse(file_path, media_type="video/mp4")
        elif "mp3" in file_name:
            response = FileResponse(file_path, media_type="audio/mp3")
        response.headers["Content-Disposition"] = f'attachment; filename="{file_name}"'
        if user:
            await VideoRepository.add(
                user=user.id,
                url=video.url,
                download_at=datetime.now(),
            )
        clear_video_cache.apply_async(args=[file_name], countdown=300)
        return response
