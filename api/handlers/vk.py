from fastapi import Depends
from fastapi.routing import APIRouter

from api.schemas.download_schema import VideoSchema
from services.download import download_video

router = APIRouter(tags=["Download"], prefix="/vk")


@router.get(
    "",
    summary="Скачать видео/аудио с VK.",
    description="Скачать видео/аудио с VK. Возможность выбора качества видеоролика.",
)
async def get_video_vk(vk_video: VideoSchema = Depends()):
    try:
        download_video(vk_video)
    except Exception:
        return {
            "ERROR": {
                "url": vk_video.url,
                "quality": vk_video.quality,
                "only_audio": vk_video.only_audio,
            }
        }
    else:
        return {
            "SUCCESS": {
                "url": vk_video.url,
                "quality": vk_video.quality,
                "only_audio": vk_video.only_audio,
            }
        }
