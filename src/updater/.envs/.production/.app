# Dockerfile path for deployment on railway.app
RAILWAY_DOCKERFILE_PATH=/src/updater/.compose/.production/Dockerfile

# PostgreSQL
# ------------------------------------------
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=

# FRED
FRED_API_KEY= # get it from FRED
FRED_BASE_URL=https://api.stlouisfed.org/fred/series/observations?series_id=
LIMIT_FRED_DAILY=252
LIMIT_FRED_WEEKLY=104
LIMIT_FRED_MONTHLY=60
LIMIT_FRED_QUARTERLY=40

# UMCSI
UMCSI_INDEX_URL=http://www.sca.isr.umich.edu/files/tbmics.csv
UMSCI_COMP_URL=http://www.sca.isr.umich.edu/files/tbmiccice.csv

# Eurostat
EUROSTAT_BASE_URL=https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/
EU_DATA_MONTHS_LIMIT=120 # number of months being saved to database.
