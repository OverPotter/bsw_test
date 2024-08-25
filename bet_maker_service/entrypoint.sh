#!/bin/bash
alembic upgrade head
uvicorn --host 0.0.0.0 --port 8080 src.main:app
