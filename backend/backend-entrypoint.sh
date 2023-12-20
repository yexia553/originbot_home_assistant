#!/bin/bash -e

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py create_user
gunicorn backend.wsgi --timeout 200 -b 0.0.0.0:8000 -c gunicorn.py

