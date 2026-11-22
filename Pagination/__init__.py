from .celery import app as celery_app

__all__ = ("celery_app",) 

# This makes the Celery application available when our Django project package is imported.