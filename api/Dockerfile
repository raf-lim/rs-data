FROM python:3.12-slim-bullseye AS builder
WORKDIR /code
RUN apt-get update \
  && apt-get install -y --no-install-recommends -y postgresql-client \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY api/pyproject.toml api/poetry.lock ./
RUN pip3 install --upgrade pip \
  && pip3 install poetry \
  && poetry config virtualenvs.create false
COPY api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY api/src/ .

FROM builder AS develop
RUN poetry install
ENTRYPOINT [ "sh", "/entrypoint.sh" ]

FROM builder AS prod
RUN poetry install --without dev,test
RUN addgroup --system app && adduser --system --ingroup app app
RUN mkdir -p /home/code \
  && mv /code/* /home/code \
  && rm -r /code \
  && chown -R app:app /home/code
WORKDIR /home/code
USER app
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
