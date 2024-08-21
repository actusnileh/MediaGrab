from app.schema.help_schema import (
    HelpItem,
    HelpResponse,
)


class HelpService:
    def get_help(self) -> HelpResponse:
        help_items = [
            HelpItem(
                name="Sponsorblock",
                description=[
                    "«Sponsorblock» - это функция, которая автоматически удаляет из ролика "
                    "спонсорские сегменты (интеграции).",
                    "Позволяет наслаждаться видео без отвлекающих частей.",
                    "Нажав на текст кнопки 'Sponsorblock', вы получите информацию о рекламных "
                    "интеграциях в ролике.",
                    "Только YouTube",
                ],
            ),
            HelpItem(
                name="Только звук",
                description=[
                    "Функция «Только звук» позволяет извлечь аудиодорожку из видеоролика "
                    "и сохранить её в формате m4a.",
                ],
            ),
            HelpItem(
                name="Регистрация",
                description=[
                    "После регистрации видеоролики автоматически сохраняются в «Историю запросов» "
                    "для быстрого доступа к загруженным роликам.",
                    "Из истории их можно удалять по мере необходимости.",
                ],
            ),
        ]
        return HelpResponse(help_items=help_items)
