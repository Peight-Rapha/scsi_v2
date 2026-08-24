#!/usr/bin/env sh
set -eu

python - <<'PY'
import os
import time
from urllib.parse import urlparse

import psycopg

database_url = os.environ.get('DATABASE_URL', '')
if database_url.startswith('postgres'):
    parsed = urlparse(database_url)
    for attempt in range(60):
        try:
            with psycopg.connect(database_url, connect_timeout=5):
                break
        except psycopg.OperationalError:
            if attempt == 59:
                raise
            time.sleep(2)
PY

python manage.py migrate_with_lock
python manage.py collectstatic --noinput --clear
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-3}"
