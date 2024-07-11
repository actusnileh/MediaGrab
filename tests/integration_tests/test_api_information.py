from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "url,status_code",
    [
        ("https://www.youtube.com/watch?v=tY-r09eLqcM", 200),
        ("https://vk.com/video?z=video-221852876_456239028%2Fpl_cat_trends", 200),
        ("nourl", 400),
        ("https://www.youtube.com/watch?v=tY-r0339eLqcM", 200),
        ("https://vk.com/video?z=video-22185333332876_456239028%2Fpl_cat_trends", 200),
    ],
)
async def test_get_video_information(url, status_code, ac: AsyncClient):
    response = await ac.get(
        "/information",
        params={
            "url": url,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "url,status_code",
    [
        ("https://www.youtube.com/watch?v=tY-r09eLqcM", 200),
        ("https://vk.com/video?z=video-221852876_456239028%2Fpl_cat_trends", 400),
        ("nourl", 400),
        ("https://www.youtube.com/watch?v=tY-r0339eLqcM", 200),
        ("https://vk.com/video?z=video-221852876_456239028%2Fpl_cat_trends", 400),
    ],
)
async def test_get_video_sponsorblock(url, status_code, ac: AsyncClient):
    response = await ac.get(
        "/information_segments",
        params={
            "url": url,
        },
    )
    assert response.status_code == status_code
