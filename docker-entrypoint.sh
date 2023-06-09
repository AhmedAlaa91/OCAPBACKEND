#!/bin/bash

set -e

# Utility functions

function header()
{
    echo
    echo ">>>>> $*"
}

function manage()
{
    gosu ocap4ops poetry run python manage.py "$@"
}


########################
# MAIN
########################

echo "================================================"
echo "STARTING OCAP4OPS PORTAL"
echo "================================================"

if [ -n "$DJANGO_SQLITE_PATH" ]; then
    header "SET OWNER OF SQLITE DATABASE FILE AND FOLDER: $DJANGO_SQLITE_PATH"
    touch "$DJANGO_SQLITE_PATH"     # in case file does not exist yet
    chown ocap4ops:ocap4ops "$DJANGO_SQLITE_PATH" "$(dirname "$DJANGO_SQLITE_PATH")"
fi

header "START NGINX SERVICE"
service nginx start

header "DJANGO CHECK"
manage check

header "MIGRATE DATABASE"
manage migrate

#header "START ASGI SERVER"
# Use "exec" so the process becomes container's PID 1 and is able to receive signals like SIGTERM
#exec gosu ocap4ops poetry run daphne -u /tmp/daphne.sock bootstrap.asgi:application

header "START SERVER"
# Use "exec" so the process becomes container's PID 1 and is able to receive signals like SIGTERM
exec gosu ocap4ops poetry run python manage.py runserver 0.0.0.0:8000 --noreload
