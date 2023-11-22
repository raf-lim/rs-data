# API
API_BASE_URL="http://rs-data-api:8000"

# DATABASE_URL because entrypoint do not load it to container,
#  at least locally (to be checked).
DATABASE_URL="postgres://rsdata:rsdatapasswd@db:5432/rsdata"

# Django
USE_DOCKER="yes"
IPYTHONDIR="/app/.ipython"

# Django general
USE_S3=0

# Django authentication
DJANGO_ACCOUNT_ALLOW_REGISTRATION=True
# Literal["username", "email", "username_email"]
# "email" requires ACCOUNT_EMAIL_REQUIRED=True
DJANGO_ACCOUNT_AUTHENTICATION_METHOD="email"
DJANGO_ACCOUNT_EMAIL_REQUIRED=True
# Literal["mandatory", "optional", "none"]
# "mandatory" requires ACCOUNT_EMAIL_REQUIRED=True
DJANGO_ACCOUNT_EMAIL_VERIFICATION="none"

# Django views settings
# Number of months displeyd in metrics' tables
US_LIMIT_MONTHS=12
EU_LIMIT_MONTHS=12


