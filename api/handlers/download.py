from fastapi import Depends
from fastapi.routing import APIRouter

from yt_dlp.utils import ExtractorError, DownloadError

from api.schemas.download_schema import VideoSchema
from api.schemas.response_schema import Response
from services.download import download_video

router = APIRouter(tags=["Download"], prefix="/video_audio")


@router.get(
    "",
    summary="Скачать видео/аудио с YouTube и VK.",
    description="Скачать видео/аудио с YouTube и VK. Возможность выбора качества видеоролика.",
)
async def get_video_youtube(video: VideoSchema = Depends()) -> Response:
    try:
        download_video(video)
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
        return Response(
            message="Успешно.",
            url=video.url,
            quality=video.quality,
            only_audio=video.only_audio,
        )
