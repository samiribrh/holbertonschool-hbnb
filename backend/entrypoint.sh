#!/bin/sh

set -e

poetry run alembic upgrade head

poetry run python app.py &

sleep 1

poetry run python wsgi.py

exec "$@"