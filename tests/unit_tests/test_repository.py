import pytest

from database.users.repository import UserRepository
from database.videos.repository import VideoRepository


@pytest.mark.parametrize(
    "user_id, is_present",
    [
        (1, True),
        (2, True),
        (10000, False),
    ],
)
async def test_find_user_by_id(user_id, is_present):
    user = await UserRepository.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
    else:
        assert not user


@pytest.mark.parametrize(
    "video_id",
    [
        (1),
        (2),
        (10000),
    ],
)
async def test_remove_by_id(video_id):
    await VideoRepository.remove_by_id(video_id)

    video = await VideoRepository.find_by_id(video_id)
    assert not video


@pytest.mark.parametrize(
    "video_id, user_id, is_present",
    [
        (1, 270, False),
        (2, 573, False),
        (3, 200, True),
    ],
)
async def test_remove_by_filter(video_id, user_id, is_present):
    await VideoRepository.remove_by_filter(id=video_id, user=user_id)

    video = await VideoRepository.find_by_id(video_id)
    if is_present:
        assert video
    else:
        assert not video
