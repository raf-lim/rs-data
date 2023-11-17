### Project RS-DATA

#### Purpose:
Deliver and/or present selected macroeconomic metrics' and indicators' data.

#### Services:
- Database: Postgres
- Updater (Python): autmatically updates data in the database (crone schedule on updater/main.py)
  - US metrics are set as plugins and can be freely added and removed.
- API (FastAPI): serves data from database
- Frontend (Django): pulls (form API) and presents data.


#### Requirements
Online and Docker up and running.

#### Run the project locally
```
git clone https://github.com/raf-lim/rs-data.git
```
<div>optionally, based on .env.example create .env file in the project's root directory</div>
<div>(if FRED API key is not set the updater skips creating tables for US metrics in database,</div>
<div>api returns relevant status and frontend returns "Page Not Found" for US Metrics.)</div><br>

Spin up containers

```
docker compose -f local.yml -up -d
```
Feed database with data:
```
docker exec rs-data-updater-local python main.py
```
Services should be na available:

API: http://localhost:8000/docs

Web: http://localhost:5000 (sign up and/or sing in to get access to content).

Django superuser can be created but not required.
```
docker exec rs-data-frontend-django-local python manage.py createsuperuser
```

#### Tests
updater (initially implemented)
```
docker exec rs-data-updater-local python -m pytest
```
api (not implemented yet)
```
docker exec rs-data-api-local python -m pytest
```
frontend (initially implemented)
```
docker exec rs-data-frontend-django-local python -m pytest
```
#### To clean up
```
docker compose -f local.yml down
docker image rm rs-data-updater
docker image rm rs-data-api
docker image rm rs-data-frontend-django-local
docker volume rm rs_data_pg_data
```
