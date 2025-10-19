#!/usr/bin/env bash
# Run uvicorn (development). For production use gunicorn/uvicorn workers behind a reverse proxy.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
