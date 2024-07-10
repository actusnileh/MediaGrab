from database.repository import BaseRepository
from database.videos.models import Videos


class VideoRepository(BaseRepository):
    model = Videos
