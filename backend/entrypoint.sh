#!/bin/sh

set -e

poetry run python app.py &

sleep 1

poetry run python wsgi.py

exec "$@"