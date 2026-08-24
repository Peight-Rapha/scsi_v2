#!/usr/bin/env sh
set -eu

python - <<'PY'
import os
import time

import psycopg

database_url = os.environ.get('DATABASE_URL', '')
if database_url.startswith('postgres'):
    for attempt in range(60):
        try:
            with psycopg.connect(database_url, connect_timeout=5):
                break
        except psycopg.OperationalError:
            if attempt == 59:
                raise
            time.sleep(2)
PY

exec "$@"
