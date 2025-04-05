#!/bin/bash

SERVICES=("meal_service" "user_service" "sync_service")

echo "Baue MicroServices-Images..."
for SERVICE in "${SERVICES[@]}"; do
    IMAGE_NAME="${SERVICE}_image:latest"
    echo "Baue $IMAGE_NAME..."
    sudo docker build -t $IMAGE_NAME ./backend/$SERVICE/api
done

echo "Baue Frontend-Image..."
sudo docker build -t frontend_image:latest ./frontend

if ! sudo docker info | grep -q "Swarm: active"; then
    echo "Starte Docker Swarm..."
    sudo docker swarm init
else
    echo "Docker Swarm läuft bereits!"
fi

docker network create -d overlay backend_network
docker network create -d overlay frontend_network
docker network create -d overlay meal_network
docker network create -d overlay user_network


if [ -f .env ]; then
    echo "Lade Umgebungsvariablen aus .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "WARNUNG: Keine .env-Datei gefunden!"
fi

echo "$POSTGRES_USER" | docker secret create db_user -
echo "$POSTGRES_PASSWORD" | docker secret create db_password -

echo "Deploye Stack mit Docker Swarm..."
sudo docker stack deploy -c docker-compose.yml mealplanner

echo "Deployment abgeschlossen!"
