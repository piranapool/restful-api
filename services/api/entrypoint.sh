#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$FLASK_ENV" = "development" && "$CREATE_DB" = "on" ]
then
    echo "Creating db tables..."

    python manage.py create_db

    echo "Db tables created"
fi

exec "$@"
