#!/bin/bash
set -e
echo "Esperando PostgreSQL..."
until python -c "import psycopg2; psycopg2.connect(host='$DB_HOST', port='$DB_PORT', dbname='$DB_NAME', user='$DB_USER', password='$DB_PASS')" 2>/dev/null; do
    sleep 1
done
echo "PostgreSQL listo."
python seed.py
uvicorn main:app --host 0.0.0.0 --port 8075
