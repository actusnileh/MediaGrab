from pydantic import BaseModel, HttpUrl

from api.schemas.download_schema import QualityEnum


class Response(BaseModel):
    message: str
    url: HttpUrl
    quality: QualityEnum
    only_audio: bool
