#!/bin/sh

set -e

poetry run python app.py &

sleep 3

poetry run python run_gunicorn.py

exec "$@"