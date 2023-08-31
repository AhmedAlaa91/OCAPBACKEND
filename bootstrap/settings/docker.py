from __future__ import annotations

from .common import *

SESSION_COOKIE_AGE = 3600

SESSION_SAVE_EVERY_REQUEST = True

# CSRF and TLS/SSL options
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://vagrant-python:8000",
    "https://*.com.intraorange",
]
SECURE_REDIRECT_EXEMPT = os.environ.get(
    "DJANGO_SECURE_REDIRECT_EXEMPT",
    "watchman,prometheus",
).split(",")
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", False)
if SECURE_SSL_REDIRECT:
    CSRF_COOKIE_SECURE = os.environ.get("DJANGO_CSRF_COOKIE_SECURE", True)
    SESSION_COOKIE_SECURE = os.environ.get(
        "DJANGO_SESSION_COOKIE_SECURE",
        True,
    )
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_HOST = os.environ.get("DJANGO_SECURE_SSL_HOST", None)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_PRELOAD = True


# mariadb connection
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "ocapdb"),
        "USER": os.getenv("MYSQL_USER", "ocap"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "ocap-app"),
        "HOST": os.getenv("MYSQL_HOST", "localhost"),
        "PORT": os.getenv("MYSQL_PORT", 3306),
    },
}


ORANGE_MAIL_API_CERT = os.path.join(
    os.getcwd(),
    "certs/Groupe_France_Telecom_Root_CA.pem",
)


# DRF CORS
USE_X_FORWARDED_HOST = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "https://ocap-app.xxx-ocap-prod.caas-cnp-apps.com.intraorange/",
]
