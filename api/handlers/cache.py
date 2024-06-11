import os
import uuid
from fastapi import HTTPException
from fastapi.routing import APIRouter


router = APIRouter(tags=["Clear Cache"], prefix="/cache")


@router.delete(
    "",
    summary="Очистить кэш роликов",
    description="Необходимо отправлять UUID ключ, который содержится в названии ролика перед '.mp4' или '.mp3'",
)
async def clear_cache(uuid: uuid.UUID):
    video_dir = "/app/videos"
    filepath = os.path.join(video_dir, str(uuid))
    if os.path.exists(filepath + ".mp4"):
        os.remove(filepath + ".mp4")
        return {"message": "OK"}
    elif os.path.exists(filepath + ".mp3"):
        os.remove(filepath + ".mp3")
        return {"message": "OK"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
