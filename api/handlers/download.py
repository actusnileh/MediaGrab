from datetime import datetime
from typing import Optional

import aiofiles
from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from yt_dlp.utils import YoutubeDLError, ExtractorError

from api.handlers.dependencies import get_current_user_optional
from api.schemas.download_schema import VideoSchema
from common.exceptions import DownloadErrorException, UrlFormatException
from database.users.models import Users
from database.videos.repository import VideoRepository
from services.download import download_video
from services.tasks.tasks import clear_video_cache

router = APIRouter(tags=["Download"], prefix="/video_audio")


async def iterfile(file_path):
    async with aiofiles.open(file_path, mode="rb") as f:
        while chunk := await f.read(1024):
            yield chunk


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
    except ExtractorError:
        raise UrlFormatException
    except (YoutubeDLError, Exception):
        raise DownloadErrorException
    else:
        if video.only_audio is True:
            media_type = "audio/m4a"
        else:
            media_type = "video/webm"
        response = StreamingResponse(iterfile(file_path), media_type=media_type)
        response.headers["Content-Disposition"] = f'attachment; filename="{file_name}"'
        if user:
            await VideoRepository.add(
                user=user.id,
                url=video.url,
                download_at=datetime.now(),
            )
        clear_video_cache.apply_async(args=[file_name], countdown=300)
        return response
