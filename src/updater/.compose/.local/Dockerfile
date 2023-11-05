FROM python:3.11-slim

WORKDIR /app

# update linux packages and
# install psql to have the possibility to connect db
# from app container if needed (from app terminal)
RUN apt-get update && apt-get install -y postgresql-client

# needed for poetry
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install poetry and dependencies
COPY src/updater/pyproject.toml src/updater/poetry.lock ./
RUN pip3 install --upgrade pip \
  && pip3 install poetry \
  && poetry config virtualenvs.create false
RUN poetry install
COPY src/updater .

RUN chmod +x ./.compose/.local/entrypoint.sh
ENTRYPOINT [ "sh", "./.compose/.local/entrypoint.sh" ]

# or
# CMD sh ./.compose/.local/entrypoint.sh
