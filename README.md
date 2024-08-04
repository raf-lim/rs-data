### Project RS-DATA

#### Purpose:
Deliver and/or present selected macroeconomic metrics' and indicators' data.

#### Services:
- Database: Postgres
- Updater (Python): autmatically updates data in the database (crone schedule on updater/main.py)
  - US metrics are set as plugins and can be freely added and removed.
- API (FastAPI): serves data from the database (deployed: https://rs-data-api.up.railway.app/docs)
- Frontend (Django, temporary, it will be replaced by basic JS or React): pulls (form API) and presents data (deployed: https://rs-data.up.railway.app/, sign-up/sign-in with fake credentials to get access to content.)

#### Requirements
Online and Docker up and running.

#### Run the project locally
```
git clone https://github.com/raf-lim/rs-data.git
```
optionally, based on .env.example create .env file in the project's root directory 
(if FRED API key is not set the updater skips creating tables for US metrics in database, api returns relevant status and frontend returns "Page Not Found" for US Metrics.)  

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

Web: http://localhost:5000 (sign up and/or sign in to get access to content).

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
docker image rm rs-data-updater rs-data-api rs-data-frontend
docker volume rm rs_data_pg_data
```
