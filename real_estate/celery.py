from __future__ import absolute_import

import os

from celery import Celery
from real_estate.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate.settings.development")

app = Celery("real_estate")

# namespace="CELERY": This parameter is optional and specifies a prefix for configuration keys. It's useful when you want to avoid naming conflicts with other parts of your application. In this case, it's using the prefix "CELERY" for Celery-specific configurations.
app.config_from_object("real_estate.settings.development", namespace="CELERY"),

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)