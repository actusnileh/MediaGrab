from api.schemas.download_schema import (
    QualityEnum,
    VideoSchema,
)

from services.download import download_video


async def test_download_video_audio_only():
    video_data = VideoSchema(
        url="https://www.youtube.com/watch?v=tY-r09eLqcM",
        quality=QualityEnum.low,
        only_audio=True,
        sponsor_block=False,
    )
    filepath, filename = await download_video(video_data)
    assert filepath.endswith(".mp3")
    assert filename.endswith(".mp3")


async def test_download_video_with_video():
    video_data = VideoSchema(
        url="https://www.youtube.com/watch?v=tY-r09eLqcM",
        quality=QualityEnum.high,
        only_audio=False,
        sponsor_block=False,
    )
    filepath, filename = await download_video(video_data)
    assert filepath.endswith(".mp4")
    assert filename.endswith(".mp4")
