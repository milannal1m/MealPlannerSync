# deploy.ps1

# Setze das Arbeitsverzeichnis relativ zum Skriptstandort
$scriptRoot = $PSScriptRoot

# Definiere die Services als Array
$services = @("meal_service", "user_service", "sync_service")

Write-Host "Baue MicroServices-Images..."
foreach ($service in $services) {
    $imageName = "${service}_image:latest"
    Write-Host "Baue $imageName..."
    $servicePath = Join-Path -Path $scriptRoot -ChildPath "backend\$service\api"
    docker build -t $imageName $servicePath
}

Write-Host "Baue Frontend-Image..."
$frontendPath = Join-Path -Path $scriptRoot -ChildPath "frontend"
docker build -t frontend_image:latest $frontendPath

# Überprüfe, ob Docker Swarm aktiv ist.
$dockerInfo = docker info 2>&1
if ($dockerInfo -notmatch "Swarm: active") {
    Write-Host "Starte Docker Swarm..."
    docker swarm init
} else {
    Write-Host "Docker Swarm läuft bereits!"
}

# Erstelle Overlay-Netzwerke
docker network create -d overlay backend_network
docker network create -d overlay frontend_network
docker network create -d overlay meal_network
docker network create -d overlay user_network

# Lade Umgebungsvariablen aus .env, falls vorhanden
$envPath = Join-Path -Path $scriptRoot -ChildPath ".env"
if (Test-Path $envPath) {
    Write-Host "Lade Umgebungsvariablen aus .env..."
    Get-Content $envPath | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '=' } | ForEach-Object {
        $parts = $_ -split '=', 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
} else {
    Write-Host "WARNUNG: Keine .env-Datei gefunden!"
}

$env:POSTGRES_USER | docker secret create db_user -
$env:POSTGRES_PASSWORD | docker secret create db_password -

Write-Host "Deploye Stack mit Docker Swarm..."
$composePath = Join-Path -Path $scriptRoot -ChildPath "docker-compose.yml"
docker stack deploy -c $composePath mealplanner

Write-Host "Deployment abgeschlossen!"