FROM python:3.11-slim

WORKDIR /code

# update linux packages and
# install psql to have the possibility to connect db
# from app container if needed (from app terminal)
RUN apt-get update && apt-get install -y postgresql-client

# need for poetry
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install poetry and dependencies
COPY pyproject.toml .
RUN pip3 install --upgrade pip \
  && pip3 install poetry \
  && poetry config virtualenvs.create false
RUN poetry install
COPY ./src .

# RUN chmod +x ./.compose/.local/entrypoint.sh

# starts the container
# CMD sh ./.compose/.local/entrypoint.sh