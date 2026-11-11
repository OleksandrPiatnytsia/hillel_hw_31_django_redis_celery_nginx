# The Celery app is created when Django starts (manage.py, gunicorn), so
# @shared_task in <app>/tasks.py binds to it and task.delay() knows the
# broker from settings
from .celery import app as celery_app

__all__ = ("celery_app",)
