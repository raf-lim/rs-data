BUILD_ENVIRONMENT=develop

# PostgreSQL
# ------------------------------------------
POSTGRES_USER=rsdata
POSTGRES_PASSWORD=rsdatapasswd
POSTGRES_HOST=db # or db container name if external network set up.
POSTGRES_PORT=5432
POSTGRES_DB=rsdata

THIS_API_BASE_URL=http://localhost:8000

# Set number of months requested from database.
US_LIMIT_MONTHS=12
EU_LIMIT_MONTHS=12