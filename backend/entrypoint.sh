#!/bin/sh
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input
cp -v -r /app/collected_static/. /backend_static/static/
gunicorn --bind 0.0.0.0:8000 foodgram.wsgi