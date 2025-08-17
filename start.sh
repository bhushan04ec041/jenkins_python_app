#!/bin/sh

# Wait for Postgres
./wait-for-it.sh postgres 5432
echo "Postgres ready"

# Wait for Redis
./wait-for-it.sh redis 6379
echo "Redis ready"

# Start Flask app
exec python -u app.py --host=0.0.0.0 --port=5001
