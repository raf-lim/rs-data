#!/bin/sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unaviable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

if [ "$ENV_TYPE" = "dev" ]
then
  exec uvicorn main:app --host 0.0.0.0 --reload
fi