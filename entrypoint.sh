#!/bin/sh
echo "Starting Speaki Server"
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
