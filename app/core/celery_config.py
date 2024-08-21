from celery import Celery

from app.core.config import configs


celery = Celery(
    "tasks",
    broker=f"redis://{configs.redis_host}:{configs.redis_port}",
    include=["app.tasks.download_tasks"],
)
