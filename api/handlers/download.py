from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

from yt_dlp.utils import ExtractorError, DownloadError

from api.schemas.download_schema import VideoSchema
from api.schemas.response_schema import Response
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
    """,
)
async def get_video_youtube(video: VideoSchema = Depends()):
    try:
        file_name = download_video(video)
    except DownloadError:
        return Response(
            message="Ошибка при загрузки ролика.",
            url=video.url,
            quality=video.quality,
            only_audio=video.only_audio,
        )
    except ExtractorError:
        return Response(
            message="Ошибка при извлечении информации из ролика.",
            url=video.url,
            quality=video.quality,
            only_audio=video.only_audio,
        )
    except Exception:
        return Response(
            message="Ошибка.",
            url=video.url,
            quality=video.quality,
            only_audio=video.only_audio,
        )
    else:
        return FileResponse(file_name, media_type="video/mp4")
