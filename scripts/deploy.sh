#!/bin/bash
set -e

echo "Docker Build"
docker compose build django
docker compose build nginx

echo "Recreate containers"
docker compose down && docker compose up -d

if [ "${MIGRATE:-0}" = 1 ]; then
    echo "Running migrations"
    sleep 5
    docker compose exec django python manage.py migrate --noinput
fi

echo "Deployment complete!"