from app.model.users import Users
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = Users
