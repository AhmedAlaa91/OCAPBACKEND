from __future__ import annotations

from bootstrap.settings.common import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(BASE_DIR, "db.sqlite3"),
    },
}
