import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
# This ensures Celery uses your Django project's settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lab3.settings')

app = Celery('celery_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

# Load Celery settings from Django settings
app.config_from_object('django.conf:settings')

# Automatically discover and register task modules in your Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
