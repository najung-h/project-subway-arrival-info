from .base import *
DEBUG = False
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", default="wisheasy.site").split(",")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("MYSQL_DATABASE"),
        "USER": env("MYSQL_USER"),
        "PASSWORD": env("MYSQL_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env.int("DB_PORT", default=3306),
        "OPTIONS": {"charset": "utf8mb4"},
        "CONN_MAX_AGE": 60,
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{env('SITE_DOMAIN', default='wisheasy.site')}"]
