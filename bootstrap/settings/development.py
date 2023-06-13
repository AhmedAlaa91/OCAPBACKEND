from __future__ import annotations

from bootstrap.settings.common import *


DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']


# TLS/SSL options
SECURE_REDIRECT_EXEMPT = os.environ.get(
    'DJANGO_SECURE_REDIRECT_EXEMPT', 'watchman,prometheus',
).split(',')
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', False)
if SECURE_SSL_REDIRECT:
    CSRF_COOKIE_SECURE = os.environ.get('DJANGO_CSRF_COOKIE_SECURE', True)
    SESSION_COOKIE_SECURE = os.environ.get(
        'DJANGO_SESSION_COOKIE_SECURE', True,
    )
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_HOST = os.environ.get('DJANGO_SECURE_SSL_HOST', None)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_PRELOAD = True
