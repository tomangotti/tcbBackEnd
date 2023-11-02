#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install poetry==1.1.4

poetry install


python manage.py collectstatic --no-input
python manage.py migrate