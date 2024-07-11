from httpx import AsyncClient


async def test_get_history_with_auth(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/authorized/history")
    assert response.status_code == 200


async def test_get_history_without_auth(ac: AsyncClient):
    response = await ac.get("/authorized/history")
    assert response.status_code == 401


async def test_about_user_with_auth(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/authorized/about_user")
    assert response.status_code == 200


async def test_about_user_without_auth(ac: AsyncClient):
    response = await ac.get("/authorized/about_user")
    assert response.status_code == 401
