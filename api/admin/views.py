from sqladmin import ModelView

from database.users.models import Users
from database.videos.models import Videos


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.username] + [Users.videos]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class VideosAdmin(ModelView, model=Videos):
    column_list = [c.name for c in Videos.__table__.c] + [Videos.user]
    can_delete = True
    name = "Видео"
    name_plural = "Видео"
    icon = "fa-solid fa-video"
