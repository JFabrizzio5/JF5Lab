#!/bin/bash
set -e

echo "Esperando PostgreSQL..."
until python -c "import psycopg2; psycopg2.connect(host='$DB_HOST', port='$DB_PORT', dbname='$DB_NAME', user='$DB_USER', password='$DB_PASS')" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL listo."

python seed.py

# Add new columns if missing (safe migrations)
python -c "
import psycopg2, os
conn = psycopg2.connect(host=os.environ['DB_HOST'], port=os.environ['DB_PORT'], dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASS'])
cur = conn.cursor()
alters = [
    \"ALTER TABLE professional_profiles ADD COLUMN IF NOT EXISTS cover_url VARCHAR\",
    \"ALTER TABLE professional_profiles ADD COLUMN IF NOT EXISTS tagline VARCHAR\",
    \"ALTER TABLE professional_profiles ADD COLUMN IF NOT EXISTS theme_color VARCHAR DEFAULT '#6366f1'\",
    \"ALTER TABLE professional_profiles ADD COLUMN IF NOT EXISTS services_json TEXT\",
]
for sql in alters:
    cur.execute(sql)
conn.commit()
cur.close(); conn.close()
print('Migrations OK')
"

uvicorn main:app --host 0.0.0.0 --port 8020
