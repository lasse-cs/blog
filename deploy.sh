#!/bin/bash
set -e

echo "Fetching source"
git fetch origin main
git reset --hard origin/main

echo "Docker Build"
docker compose build django
docker compose build nginx

echo "Recreate containers"
docker compose up -d

if [ "${MIGRATE:-0}" = 1 ]; then
    echo "Running migrations"
    sleep 5
    docker compose exec django python manage.py migrate --noinput
fi

echo "Deployment complete!"