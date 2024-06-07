from pydantic import BaseModel
from enum import Enum


class QualityEnum(int, Enum):
    Q144 = 144
    Q240 = 240
    Q360 = 360
    Q480 = 480
    Q720 = 720
    Q1080 = 1080


class VideoSchema(BaseModel):
    url: str
    quality: QualityEnum = QualityEnum.Q720
    only_audio: bool = False
