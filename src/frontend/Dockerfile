FROM python:3.11.6-slim-bullseye as builder

WORKDIR /code

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

COPY src/frontend .
RUN chmod +x ./entrypoint.sh

FROM builder AS develop
RUN poetry install
ENTRYPOINT ["./entrypoint.sh"]


FROM builder AS prod
RUN poetry install --without dev,django-dev,test,docs,quality
RUN addgroup --system django && adduser --system --ingroup django django
RUN mkdir -p /home/code \
  && mv /code/* /home/code \
  && rm -r /code \
  && chown -R django:django /home/code
WORKDIR /home/code
USER django
ENTRYPOINT ["./entrypoint.sh"]
