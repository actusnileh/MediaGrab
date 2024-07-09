from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

from api.schemas.download_schema import VideoSchema
from common.exceptions import DownloadErrorException
from services.download import download_video

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
    """,
)
async def get_video_youtube(video: VideoSchema = Depends()):
    try:
        file_path, file_name = download_video(video)
    except Exception:
        raise DownloadErrorException
    else:
        if "mp4" in file_name:
            response = FileResponse(file_path, media_type="video/mp4")
        elif "mp3" in file_name:
            response = FileResponse(file_path, media_type="audio/mp3")
        response.headers["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
