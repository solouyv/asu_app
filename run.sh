#!/usr/bin/env sh

python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py collectstatic --noinput
gunicorn asu_app.wsgi:application --timeout 6000 --bind 0.0.0.0:8000
