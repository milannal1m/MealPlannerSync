#!/bin/bash

SERVICES=("meal_service" "user_service" "sync_service")

echo "Baue Docker-Images..."
for SERVICE in "${SERVICES[@]}"; do
    IMAGE_NAME="${SERVICE}_image:latest"
    echo "Baue $IMAGE_NAME..."
    sudo docker build -t $IMAGE_NAME ./backend/$SERVICE/api
done

if ! sudo docker info | grep -q "Swarm: active"; then
    echo "Starte Docker Swarm..."
    sudo docker swarm init
else
    echo "Docker Swarm läuft bereits!"
fi

if [ -f .env ]; then
    echo "Lade Umgebungsvariablen aus .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "WARNUNG: Keine .env-Datei gefunden!"
fi

echo "Deploye Stack mit Docker Swarm..."
sudo docker stack deploy -c docker-compose.yml mealplanner

echo "Deployment abgeschlossen!"
