from __future__ import annotations

from bootstrap.settings.common import *


DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']


ORANGE_MAIL_API_CERT = os.path.join(
    BASE_DIR, 'certs\\Groupe_France_Telecom_Root_CA.pem',
)
