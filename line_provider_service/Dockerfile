FROM python:3.10.0-slim

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY --chmod=777 line_provider_service/entrypoint.sh /usr/local/bin/entrypoint

COPY line_provider_service/src ./src

ENTRYPOINT ["entrypoint"]
