from .base import *
import environ, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()

# ✅ prod에서는 .env 자동 로딩 비활성 (OS 환경만 사용)
READ_DOT_ENV_FILE = env.bool("READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])

# DB: 양쪽 네이밍을 모두 수용
DB_NAME = env.str("DB_NAME", default=env.str("MYSQL_DATABASE", default=None))
DB_USER = env.str("DB_USER", default=env.str("MYSQL_USER", default=None))
DB_PASSWORD = env.str("DB_PASSWORD", default=env.str("MYSQL_PASSWORD", default=None))
DB_HOST = env.str("DB_HOST", default=env.str("MYSQL_HOST", default="localhost"))
DB_PORT = env.int("DB_PORT", default=env.int("MYSQL_PORT", default=3306))




DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.str("MYSQL_DATABASE", default=env.str("DB_NAME", default=env.str("MYSQL_DB", default=""))),
        "USER": env.str("MYSQL_USER", default=env.str("DB_USER", default="")),
        "PASSWORD": env.str("MYSQL_PASSWORD", default=env.str("DB_PASSWORD", default="")),
        "HOST": env.str("DB_HOST", default=env.str("MYSQL_HOST", default="localhost")),
        "PORT": env.int("DB_PORT", default=int(env.int("MYSQL_PORT", default=3306))),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{env('SITE_DOMAIN', default='subway-info-easy.site')}"]
