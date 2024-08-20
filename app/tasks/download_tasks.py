import os

from app.core.celery_config import celery


@celery.task
def clear_video_cache(filename: str):
    video_dir = "/app/videos"
    filepath = os.path.join(video_dir, filename)
    os.remove(filepath)
