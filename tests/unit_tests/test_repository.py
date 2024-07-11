import pytest
from database.users.repository import UserRepository


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
