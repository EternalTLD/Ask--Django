import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_project.settings")

app = Celery("ask_project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
