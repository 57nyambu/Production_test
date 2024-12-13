import dj_database_url
from Root.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES['default'] = dj_database_url.parse("postgresql://tom:GfhXnMiRHYnunbU5aB6CF5jdNlwZcrRM@dpg-ctcjrj23esus73bh5v6g-a/deployment_db_98dm")

#external:postgresql://tom:GfhXnMiRHYnunbU5aB6CF5jdNlwZcrRM@dpg-ctcjrj23esus73bh5v6g-a.oregon-postgres.render.com/deployment_db_98dm

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}