from sqladmin import ModelView

from app.model.users import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.username] + [Users.videos]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
