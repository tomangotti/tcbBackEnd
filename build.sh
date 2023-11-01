#!/usr/bin/env bash
# exit on error
set -o errexit

rm -rf ~/.cache/pypoetry
curl -sSL https://install.python-poetry.org | python3 -

poetry install

python manage.py collectstatic --no-input
python manage.py migrate