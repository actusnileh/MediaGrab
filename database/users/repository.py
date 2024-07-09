from database.repository import BaseRepository
from database.users.models import Users


class UserRepository(BaseRepository):
    model = Users
