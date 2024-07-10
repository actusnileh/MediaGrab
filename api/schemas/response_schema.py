from pydantic import BaseModel


class InformationResponse(BaseModel):
    message: str
    preview_url: str
    author_name: str
    title: str


class HistoryResponse(BaseModel):
    id: int
    url: str
    preview_url: str
    download_at: str
