#!/usr/bin/env bash
# exit on error
set -o errexit

rm -rf ~/.cache/pypoetry

poetry install

python manage.py collectstatic --no-input
python manage.py migrate