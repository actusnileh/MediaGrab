from fastapi import Depends
from fastapi.routing import APIRouter

from api.schemas.download_schema import VideoSchema
from services.download import download_video

router = APIRouter(tags=["Download"], prefix="/youtube")


@router.get(
    "",
    summary="Скачать видео/аудио с YouTube.",
    description="Скачать видео/аудио с YouTube. Возможность выбора качества видеоролика.",
)
async def get_video_youtube(youtube_video: VideoSchema = Depends()):
    try:
        download_video(youtube_video)
    except Exception:
        return {
            "ERROR": {
                "url": youtube_video.url,
                "quality": youtube_video.quality,
                "only_audio": youtube_video.only_audio,
            }
        }
    else:
        return {
            "SUCCESS": {
                "url": youtube_video.url,
                "quality": youtube_video.quality,
                "only_audio": youtube_video.only_audio,
            }
        }
