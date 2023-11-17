### Project RS-DATA

#### Purpose:
Deliver and/or present selected macroeconomic metrics' and indicators' data.

#### Services:
- Database: Postgres
- Updater (Python): autmatically updates data in the database (crone schedule on updater/main.py)
- API (FastAPI): serves data from database
- Frontend (Django): pulls (form API) and presents data.

![services](https://github.com/raf-lim/rs-data/assets/105244879/2caa9be0-b418-44f4-81ba-29ae1b4947bd)



#### Run the project locally
```
git clone https://github.com/raf-lim/rs-data.git
```
- optionally in the project root directory create .env file based on .env.example (if FRED API key is not set the updater skips creating tables for US metrics in database, api returns relevant status and frontend returns "Page Not Found" page for US Metrics.)
- run docker compose to create images and spin up the containers:
```
docker compose -f local.yml -up -d
```
- feed database with data:
```
docker exec rs-data python main.py
```
- postgres persists data in Docker volumes.

#### Tests
```
docker exec rs-data python -m pytest
```
#### To remove project
```
docker compose -f local.yml down
docker image rm rs-data-updater
docker image rm rs-data-api
docker image rm rs-data-frontend-django-local
docker volume rm rs_data_pg_data
```
