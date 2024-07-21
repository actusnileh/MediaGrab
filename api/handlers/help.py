from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache

from common.exceptions import UnknownException

router = APIRouter(tags=["Help"], prefix="/help")

help_info = [
    {
        "name": "Sponsorblock",
        "description": [
            "«Sponsorblock» - это функция, которая автоматически удаляет из ролика спонсорские сегменты (интеграции).",
            "Позволяет наслаждаться видео без отвлекающих частей.",
            "Нажав на текст кнопки 'Sponsorblock', вы получите информацию о рекламных интеграциях в ролике.",
            "Только YouTube",
        ],
    },
    {
        "name": "Только звук",
        "description": [
            "Функция «Только звук» позволяет извлечь аудиодорожку из видеоролика и сохранить её в формате m4a."
        ],
    },
    {
        "name": "Регистрация",
        "description": [
            "После регистрации видеоролики автоматически сохраняются в «Историю запросов» для быстрого доступа к загруженным роликам.",
            "Из истории их можно удалять по мере необходимости.",
        ],
    },
]


@router.get(
    "",
    summary="Получить список функций и описание по работе с ними",
    description="Возвращает список доступных функций и их описание для работы с видеороликами.",
)
@cache(expire=120)
async def get_help():
    try:
        return help_info
    except Exception:
        raise UnknownException
