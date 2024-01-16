FROM python:3.11.6-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # Translations dependencies
  gettext \
  postgresql-client \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# needed for poetry
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install poetry and dependencies
COPY src/frontend/pyproject.toml src/frontend/poetry.lock ./
RUN pip3 install --upgrade pip \
  && pip3 install poetry \
  && poetry config virtualenvs.create false
  
RUN poetry install --without dev,django-dev,test,docs,quality

RUN addgroup --system django && adduser --system -ingroup django django

COPY src/frontend .

RUN mv ./compose/production/django/entrypoint /entrypoint \
  && sed -i 's/\r$//g' /entrypoint \
  && chmod +x /entrypoint

RUN mv ./compose/production/django/start /start \
  && sed -i 's/\r$//g' /start \
  && chmod +x /start

# make django owner of the WORKDIR directory as well.
RUN chown django:django /app

USER django

# RUN DATABASE_URL="" \
#   DJANGO_SETTINGS_MODULE="config.settings.test" \
#   python manage.py compilemessages

ENTRYPOINT ["/entrypoint"]
