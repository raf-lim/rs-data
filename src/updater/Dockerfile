FROM python:3.12-slim-bullseye AS builder
WORKDIR /code
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN apt-get update \
  && apt-get install -y --no-install-recommends -y postgresql-client \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY src/updater/pyproject.toml src/updater/poetry.lock ./
RUN pip3 install --upgrade pip \
  && pip3 install poetry \
  && poetry config virtualenvs.create false
COPY src/updater/ ./
RUN chmod +x ./entrypoint.sh

FROM builder AS develop
RUN poetry install
ENTRYPOINT [ "sh", "./entrypoint.sh" ]
# CMD sh ./.compose/.local/entrypoint.sh

FROM builder AS prod
RUN poetry install --without dev,test
RUN addgroup --system app && adduser --system --ingroup app app
RUN mkdir -p /home/app \
  && mv /code/* /home/app \
  && rm -r /code \
  && chown -R app:app /home/app
WORKDIR /home/app
USER app
ENTRYPOINT [ "sh", "./entrypoint.sh" ]