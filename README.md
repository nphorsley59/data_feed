# data_feed

Microservice to collect articles from medical journals

## Docker

To connect to your Docker development terminal:
    1. Start the container in detached mode with `docker compose up -d <service_name>`
    2. Enter the container with `docker compose exec <service_name> bash`.

If you suspect the container is outdated:
    1. Rebuild it with `docker compose build --no-cache <service_name>`
