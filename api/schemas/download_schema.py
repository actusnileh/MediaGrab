from pydantic import BaseModel
from enum import Enum


class QualityEnum(str, Enum):
    lowest = "lowest"
    low = "low"
    medium = "medium"
    high = "high"
    highest = "highest"

    def to_value(self):
        quality_map = {
            "lowest": 144,
            "low": 240,
            "medium": 360,
            "high": 720,
            "highest": 1080,
        }
        return quality_map[self.value]


class VideoSchema(BaseModel):
    url: str
    quality: QualityEnum = QualityEnum.high
    only_audio: bool = False
    sponsor_block: bool = False
