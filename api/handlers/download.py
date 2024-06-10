from fastapi import Depends, HTTPException, Response, status
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

from yt_dlp.utils import ExtractorError, DownloadError

from api.schemas.download_schema import VideoSchema
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
        file_path, file_name = download_video(video)
    except DownloadError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Response(
                message="Error downloading video.",
                url=video.url,
                quality=video.quality,
                only_audio=video.only_audio,
            ).dict(),
        )
    except ExtractorError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Response(
                message="An unexpected error occurred.",
                url=video.url,
                quality=video.quality,
                only_audio=video.only_audio,
            ).dict(),
        )
    except Exception:
        return Response(
            message="Ошибка.",
            url=video.url,
            quality=video.quality,
            only_audio=video.only_audio,
        )
    else:
        if "mp4" in file_name:
            response = FileResponse(file_path, media_type="video/mp4")
            response.headers["Content-Disposition"] = (
                f'attachment; filename="{file_name}"'
            )
            return response
        elif "mp3" in file_name:
            response = FileResponse(file_path, media_type="audio/mp3")
            response.headers["Content-Disposition"] = (
                f'attachment; filename="{file_name}"'
            )
            return response
