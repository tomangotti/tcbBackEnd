#!/usr/bin/env bash
# exit on error
set -o errexit

# pre_build.sh
#!/usr/bin/env bash
pip install poetry
poetry install


python manage.py collectstatic --no-input
python manage.py migrate