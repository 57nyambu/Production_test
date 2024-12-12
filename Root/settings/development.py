from .base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES['default'] = dj_database_url.parse("postgresql://tom:GfhXnMiRHYnunbU5aB6CF5jdNlwZcrRM@dpg-ctcjrj23esus73bh5v6g-a.oregon-postgres.render.com/deployment_db_98dm")

