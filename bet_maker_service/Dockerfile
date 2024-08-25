FROM python:3.10.0-slim

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY --chmod=777 bet_maker_service/entrypoint.sh /usr/local/bin/entrypoint

COPY bet_maker_service/src ./src

COPY bet_maker_service/alembic.ini ./alembic.ini

ENTRYPOINT ["entrypoint"]
