### Project RS-DATA

#### Purpose:
Deliver and/or present selected macroeconomic metrics' and indicators' data.

#### Services:
- Database: Postgres
- Updater (Python): autmatically updates data in the database (crone schedule on updater/main.py)
  - US metrics are set as plugins and can be freely added and removed.
- API (FastAPI): serves data from the database
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
docker compose up -d
```
Feed database with data:
```
docker exec updater python main.py
```
Services should be now available:

API: http://localhost:8000/docs

Web: http://localhost:5000 (sign up and/or sing in to get access to content).

Django superuser can be created but not required (e.g. for users' handling purpose).
```
docker exec frontend python manage.py createsuperuser
```

#### Tests services
updater
```
docker exec updater python -m pytest
```
api
```
docker exec api python -m pytest
```
frontend
```
docker exec frontend python -m pytest
```

#### Tests' coverage
```
docker exec <service_name> coverage run -m pytest
docker exec <service_name> coverage report
```
Or run
```
docker exec <service> coverage html
```
and open the <service_name>/htmlcov/index.html in the browser.

#### To clean up
```
docker compose down
docker image rm rs-data-updater
docker image rm rs-data-api
docker image rm rs-data-frontend
docker volume rm rs_data_pg_data
```
