from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "foosball_rating",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.debug",
    ],
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    beat_schedule={
        "debug-ping-every-hour": {
            "task": "app.tasks.debug.ping",
            "schedule": 3600.0,
        },
    },
)
