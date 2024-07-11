import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "username,email,password,status_code",
    [
        ("youtubewatcher", "testik@youtube.com", "y0utube", 200),
        ("youtubewatcher", "testik@youtube.com", "youtube", 409),
        ("nikolay", "nikolay@gmail.com", "password", 200),
        ("EgorStreamer", "Egorchik", "abcdf", 422),
    ],
)
async def test_register_user(username, email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("tstrainge0@sakura.ne.jp", "string", 200),
        ("testik@youtube.com", "y0utube", 200),
        ("tstrainge0@sakura.ne.jp", "12213123", 401),
        ("anonymus@anon.su", "anonchik", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == status_code
