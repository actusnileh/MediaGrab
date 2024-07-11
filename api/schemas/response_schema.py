from pydantic import BaseModel


class InformationResponse(BaseModel):
    preview_url: str
    author_name: str
    title: str


class HistoryResponse(BaseModel):
    id: int
    url: str
    preview_url: str
    title: str
    download_at: str
