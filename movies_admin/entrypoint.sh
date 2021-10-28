#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000
#############################
#gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 1