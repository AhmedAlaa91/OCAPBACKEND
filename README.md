# Orange Car Pooling Portal

Web portal for Car Pooling for orange employees.

# Setup dev environment

Requirements:
- Linux system
- Python 3.10 or higher
- [Poetry](https://python-poetry.org)

Clone git repo then install python environment with `poetry install` command.

Enable virtual env with `poetry shell` command (this command spawns a subshell).

Run development server with `python manage.py runserver` command then open http://localhost:8000 in your browser.

# Configuration

## Technical configuration

Technical configuration is loaded at startup by reading these environment variables (all of them are optional):

- Common settings:

| Variable  | Default  | Description                                        |
| --------- | -------- | -------------------------------------------------- |
| LOG_LEVEL | `"INFO"` | Log level: DEBUG, INFO, WARNING, ERROR or CRITICAL |

- Django configuration (refer to https://docs.djangoproject.com/en/4.1/ref/settings for details):

| Variable             | Default                    | Description                                                                                            |
| -------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------ |
| DJANGO_ALLOWED_HOSTS | `"*"`                      | Allowed hosts. Refer to https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-ALLOWED_HOSTS  |
| DJANGO_DEBUG         | `False`                    | Django debug mode. Refer to https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG      |
| DJANGO_SECRET_KEY    | random string              | Django secret key. Refer to https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY |
| DJANGO_SQLITE_PATH   | `"<ROOT_PATH>/db.sqlite3"` | Path to Django database SQLite file                                                                    |
| DJANGO_TIMEZONE      | `"UTC"`                    | Timezone. Refer to https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-TIME_ZONE           |

- Authentication settings:

| Variable                         | Default | Description                                                                             |
| -------------------------------- | ------- | --------------------------------------------------------------------------------------- |
| ORANGE_AUTH_API_BYPASS           | `False` | Disable authentication with Orange AUTH if True (default is True in dev environment) |
| ORANGE_ODI_API_CLIENT_ID     | `None`  | Orange AUTH OIDC Client ID                                                           |
| ORANGE_ODI_API_AUTH_HEADER| `None`  | Orange AUTH OIDC Client Secret                                                       |
| ORANGE_ODI_API_REDIRECT_URI  | `None`  | Orange AUTH Redirect URI                                                             |

- MySQL/MariaDB settings (not used in dev environment):

| Variable       | Default               | Description            |
| -------------- | --------------------- | ---------------------- |
| MYSQL_DATABASE | `"ocap-db"` | Database name          |
| MYSQL_HOST     | `"localhost"`         | Hostname or IP address |
| MYSQL_PASSWORD | `"ocap-app"`    | Password               |
| MYSQL_PORT     | 3306                  | Port                   |
| MYSQL_USER     | `"ocap-app"`    | Username               |


# Docker

To build and run application using docker:
```sh
docker compose up -d --build
# View logs:
docker compose logs -f
# Stop application:
docker compose down
```

Note: Django SQLite database is stored in a docker volume for persistency.

# Administration

Access Django admin portal on "/admin" URL path.

Default superuser login is "admin" and default password is "Orange000".

**Do not forget to change this default password!**

# Profile Picture

S3 bucket storage used for upload user's images

[S3Bucket] (https://s3-object-storage.obs-tech.com.intraorange/how_to_use/).

# Software architecture

**TODO**

# Authentication and authorization

Access to portal requires authentication through [Orange Auth](https://developer-inside.sso.infra.ftgroup/apis/authentication-internal/getting-started).

To authorize a user, its CUID must be declared in Django users database (can be done through Django admin portal).

Authentication and authorization process is bypassed in developement environment (setting `ORANGE_AUTH_API_BYPASS=True`).


# Alert

Alert user by sending email through [Orange Mail API](https://developer-inside.sso.infra.ftgroup/apis/mail/getting-started).

| Variable             | Default                     |                     Description                                                                        |
| -------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------ |
| ORANGE_SEND_EMAIL_CLIENT_ID | `cli-ocapapp-v1-prd`  |  Orange Mail client id.                                                                              |
| ORANGE_SEND_EMAILS_CLIENT_SECRET| random string              | Orange Mail secret. |
| SEND_MAILS_ACCESS_TOKENS_URL   | `"https://okapi-v2.api.hbx.geo.infra.ftgroup/v2/token"`                     | OM token endpoint                           |
| SEND_MAIL_SERVICE_URL      | `"'https://mail2fed.preprod.api.hbx.geo.infra.ftgroup/v1/email/send"` | send mail endpoint|
