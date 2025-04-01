# MealPlannerSync

MealPlannerSync is a distributed application designed to help users plan meals, manage user connections, and synchronize data across multiple services. The project consists of a frontend and several backend microservices orchestrated using Docker Swarm.

---

## Table of Contents

- [Installation](#installation)
- [Deploy the Service](#deploy-the-service)
- [Links](#links)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Installation

1. Install **Docker** and **docker-compose**:
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)

2. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/MealPlannerSync.git
   cd MealPlannerSync
   ```

3. Create a `.env` file based on the provided `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Update the `.env` file with your environment-specific variables.

---

## Deploy the Service

To deploy the application, use one of the following commands depending on your operating system:

- **Linux/Mac**:
   ```bash
   ./deploy.sh
   ```

- **Windows**:
   ```powershell
   .\deploy.ps1
   ```

These scripts will build the Docker images and start all services using `docker-compose`.

---

## Links

Once the services are running, you can access the following:

- **Frontend**: [http://localhost:8080](http://localhost:8080)
- **Meal Service API Documentation**: [http://localhost/meal/docs](http://localhost/meal/docs)
- **User Service API Documentation**: [http://localhost/user/docs](http://localhost/user/docs)
- **Sync Service API Documentation**: [http://localhost/sync/docs](http://localhost/sync/docs)

---

## Project Structure

```
MealPlannerSync/
├── .env                  # Environment variables
├── .env.example          # Example environment variables
├── docker-compose.yml    # Docker Compose configuration
├── deploy.sh             # Deployment script for Linux/Mac
├── deploy.ps1            # Deployment script for Windows
├── nginx.conf            # NGINX configuration
├── backend/              # Backend services
│   ├── meal_service/     # Meal Service
│   ├── user_service/     # User Service
│   └── sync_service/     # Sync Service
└── frontend/             # Frontend application
```

---

## Technologies Used

- **Frontend**: Vue.js
- **Backend**: FastAPI, RabbitMQ
- **Databases**: PostgreSQL
- **Containerization**: Docker, Docker Swarm
- **Load Balancer**: NGINX

---