# Dockerfile path for deployment on railway.app
RAILWAY_DOCKERFILE_PATH=/src/frontend/compose/production/django/Dockerfile

# DATABASE_URL because entrypoint do not load it to container,
#  at least locally (to be checked).
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PASSWORD=
POSTGRES_PORT=
POSTGRES_USER=

# API
API_BASE_URL=

# Django
DJANGO_SECRET_KEY=
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_ALLOWED_HOSTS=
DJANGO_ADMIN_URL=
USE_S3=0
USE_DOCKER=no

# Django user authentication
DJANGO_ACCOUNT_ALLOW_REGISTRATION=True
# Literal["username", "email", "username_email"]
# "email" requires ACCOUNT_EMAIL_REQUIRED=True
DJANGO_ACCOUNT_AUTHENTICATION_METHOD="email"
DJANGO_ACCOUNT_EMAIL_REQUIRED=True
# Literal["mandatory", "optional", "none"]
# "mandatory" requires ACCOUNT_EMAIL_REQUIRED=True
DJANGO_ACCOUNT_EMAIL_VERIFICATION="none"

# Django views settings
# Number of months displeyd in EU metrics' tables
EU_LIMIT_METRICS=12





