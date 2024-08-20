from pydantic import BaseModel


class InformationResponse(BaseModel):
    preview_url: str
    author: str
    title: str
    length: int
    sponsor_segments: list[str]
