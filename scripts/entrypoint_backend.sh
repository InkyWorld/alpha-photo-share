#!/bin/sh

set -e

# Завантажуємо .env
if [ -f .env ]; then
  echo "Loading environment variables from .env"
  export $(grep -v '^#' .env | xargs)
fi

echo "Waiting for Postgres to be ready at $POSTGRES_HOST:$POSTGRES_PORT..."
echo "Connecting to Postgres with:"
echo "  HOST=$POSTGRES_HOST"
echo "  PORT=$POSTGRES_PORT"
echo "  USER=$POSTGRES_USER"
# Очікування повного запуску PostgreSQL
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

echo "Postgres is ready, running migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec python main.py