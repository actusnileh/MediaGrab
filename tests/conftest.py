import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from api.app import create_app
from common.settings import settings
from database.database import Base, async_session_maker, engine
from database.users.models import Users
from database.videos.models import Videos


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.mode == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users_data = open_mock_json("users")
    videos_data = open_mock_json("videos")

    for user in users_data:
        user.pop("id", None)

    for video in videos_data:
        video.pop("id", None)
        video["download_at"] = datetime.strptime(video["download_at"], "%Y-%m-%d")
    async with async_session_maker() as session:
        add_users = insert(Users).values(users_data)
        await session.execute(add_users)

        add_videos = insert(Videos).values(videos_data)
        await session.execute(add_videos)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=create_app()), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(
        transport=ASGITransport(app=create_app()), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "tstrainge0@sakura.ne.jp",
                "password": "string",
            },
        )
        assert ac.cookies["multigrab_user_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
