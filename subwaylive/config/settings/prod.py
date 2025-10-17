from .base import *
DEBUG = False
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", default="subway-info-easy.site").split(",")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.str("MYSQL_DATABASE"),
        "USER": env.str("MYSQL_USER"),
        "PASSWORD": env.str("MYSQL_PASSWORD"),
        "HOST": env.str("DB_HOST"),   # ✅ RDS
        "PORT": env.int("DB_PORT", 3306),
        "OPTIONS": {"charset": "utf8mb4"},
        "CONN_MAX_AGE": env.int("DB_CONN_MAX_AGE", 60),
    }
}


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{env('SITE_DOMAIN', default='subway-info-easy.site')}"]
