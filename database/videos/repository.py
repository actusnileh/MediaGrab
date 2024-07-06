from database.database import async_session_maker


class VideosRepository:

    @classmethod
    async def add_video(cls, video):
        async with async_session_maker() as session:
            pass
