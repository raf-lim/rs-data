### About RS-DATA

Design to automatically update database with data
pulled from external APIs, process them and save in the database.

Processed data are being served via another app RS-API (REST API).

### Start Docker containers and run the app locally (dockerized)

- in the root create .env file based on .env.example
- get your API keys and save them in .env file
...
- to start the containers (if executed first time the docker images 
are created and containers started):
```bash
docker compose -f local.yml -up -d
```
- to start updating data:
```bash
docker exec -it rs-data python main.py
```
- postgres data persists in Docker volumes.

### Tests

```bash
docker exec rs-data python -m pytest
```

### To stop or remove the containers
```bash
docker compose -f local.yml stop
docker compose -f local.yml down
```
