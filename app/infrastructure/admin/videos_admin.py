from sqladmin import ModelView

from app.model.videos import Videos


class VideosAdmin(ModelView, model=Videos):
    column_list = [c.name for c in Videos.__table__.c] + [Videos.user]
    can_delete = True
    name = "Видео"
    name_plural = "Видео"
    icon = "fa-solid fa-video"
