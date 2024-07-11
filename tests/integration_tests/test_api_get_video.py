from httpx import AsyncClient


async def test_get_video_without_auth(ac: AsyncClient):
    response = await ac.get(
        "/video_audio",
        params={
            "url": "https://www.youtube.com/watch?v=tY-r09eLqcM",
            "quality": "low",
        },
    )
    assert response.status_code == 200
