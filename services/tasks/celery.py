from celery import Celery

from common.settings import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}",
    include=["services.tasks.tasks"],
)
