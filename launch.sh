#!/bin/bash
set -e
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
poetry run python manage.py runserver 0.0.0.0:8000
#poetry run gunicorn primary_server.wsgi --capture-output --reload -w 3 -b 0.0.0.0:8000
