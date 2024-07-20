from datetime import datetime
import os
import re
from typing import Optional

import aiofiles
from fastapi import Depends, Request, status
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
    request: Request,
    video: VideoSchema = Depends(),
    user: Optional[Users] = Depends(get_current_user_optional),
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

        file_size = os.path.getsize(file_path)
        headers = {
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
        }

        range_header = request.headers.get("Range")
        if range_header:
            range_match = re.match(r"bytes=(\d+)-(\d+)?", range_header)
            if range_match:
                start = int(range_match.group(1))
                end = range_match.group(2)
                end = int(end) if end else file_size - 1
                headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
                headers["Content-Length"] = str(end - start + 1)

                async def iterfile_range(start, end):
                    async with aiofiles.open(file_path, mode="rb") as f:
                        await f.seek(start)
                        while start <= end:
                            chunk_size = min(1024, end - start + 1)
                            data = await f.read(chunk_size)
                            if not data:
                                break
                            yield data
                            start += chunk_size

                response = StreamingResponse(
                    iterfile_range(start, end),
                    media_type=media_type,
                    status_code=status.HTTP_206_PARTIAL_CONTENT,
                )
                response.headers.update(headers)
                if user:
                    await VideoRepository.add(
                        user=user.id,
                        url=video.url,
                        download_at=datetime.now(),
                    )
                clear_video_cache.apply_async(args=[file_name], countdown=300)
                return response

        response = StreamingResponse(iterfile(file_path), media_type=media_type)
        response.headers.update(headers)
        if user:
            await VideoRepository.add(
                user=user.id,
                url=video.url,
                download_at=datetime.now(),
            )
        clear_video_cache.apply_async(args=[file_name], countdown=300)
        return response
