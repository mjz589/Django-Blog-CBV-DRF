# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import os

# apps in order to load
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from .celery import app as celery_app


__all__ = ("celery_app",)
