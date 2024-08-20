from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    url: str
    preview_url: str
    title: str
    download_at: str
