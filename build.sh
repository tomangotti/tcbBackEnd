#!/usr/bin/env bash
# exit on error
set -o errexit

# Ensure poetry uses the correct Python interpreter
/opt/render/project/src/.venv/bin/python -m poetry env use /opt/render/project/src/.venv/bin/python

# Install project dependencies using Poetry
/opt/render/project/src/.venv/bin/python -m poetry install

# Collect static files and perform database migrations
/opt/render/project/src/.venv/bin/python manage.py collectstatic --no-input
/opt/render/project/src/.venv/bin/python manage.py migrate