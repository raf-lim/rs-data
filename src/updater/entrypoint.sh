#!/bin/sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unaviable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# running process to keep the container alive (in dev):
if [ "${BUILD_ENVIRONMENT=prod}" = "develop" ]; then
  exec sh
fi