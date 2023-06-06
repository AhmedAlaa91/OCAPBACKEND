FROM dockerproxy.repos.tech.orange/python:3.11-slim-bullseye

LABEL name="ocap-app"
LABEL description="Orange Carpooling Portal"
LABEL url="https://gitlab.tech.orange/orange-cap-portal/ocap-app"
LABEL version="0.1.0"

ENV APP_HOME="/opt/ocap-app/webapp"

# Configure Debian mirror repositories & install packages
RUN echo "" \
    && echo "Acquire::Check-Valid-Until \"false\";" >> /etc/apt/apt.conf.d/02IgnoreChecks \
    && echo "Acquire::Check-Date \"false\";" >> /etc/apt/apt.conf.d/02IgnoreChecks \
    && echo "deb https://repos.tech.orange/artifactory/debianproxy bullseye main" > /etc/apt/sources.list \
    && echo "deb https://repos.tech.orange/artifactory/debian-proxy-official-security bullseye-security main" >> /etc/apt/sources.list \
    && echo "deb https://repos.tech.orange/artifactory/debianproxy bullseye-updates main" >> /etc/apt/sources.list \
    && apt-get update -y \
    && apt-get install -y gosu nginx

# Install Poetry
ENV PIP_INDEX_URL="https://repos.tech.orange/artifactory/api/pypi/pythonproxy/simple"
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV POETRY_HOME="/opt/poetry"
RUN python -m venv "${POETRY_HOME}" \
    && "${POETRY_HOME}/bin/pip" install "poetry==1.4.*" \
    && ln -s "${POETRY_HOME}/bin/poetry" /usr/bin/poetry

# Create system user
RUN groupadd -r ocap4ops && useradd -r -l -g ocap4ops -s /bin/bash -m ocap4ops

# Copy contents
COPY --chown=ocap4ops:ocap4ops . "${APP_HOME}/"

# Configure nginx
RUN rm /etc/nginx/sites-enabled/default \
    && ln -s "${APP_HOME}/nginx/nginx-docker.conf" /etc/nginx/sites-enabled/ocap-app

# Installation
WORKDIR "${APP_HOME}"
RUN gosu ocap4ops poetry install --only main,prod \
    && gosu ocap4ops poetry run python manage.py collectstatic -c -l --no-input \
    && chmod 755 docker-entrypoint.sh \
    && cat RELEASE

EXPOSE 8000
ENTRYPOINT [ "./docker-entrypoint.sh" ]