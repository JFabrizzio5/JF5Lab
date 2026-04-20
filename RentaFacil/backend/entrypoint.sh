#!/bin/bash
set -e
echo "Waiting for database..."
while ! python -c "
import asyncio, asyncpg, os
async def check():
    url = os.environ.get('DATABASE_URL', '').replace('postgresql+asyncpg://', '')
    parts = url.replace('@', ':').replace('/', ':').split(':')
    await asyncpg.connect(host=parts[2], port=int(parts[3]), user=parts[0], password=parts[1], database=parts[4])
asyncio.run(check())
" 2>/dev/null; do
    sleep 1
done
echo "Running migrations..."
alembic upgrade head
echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
