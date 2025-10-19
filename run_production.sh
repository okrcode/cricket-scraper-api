#!/usr/bin/env bash
# =====================================================
# Production Run Script for Cricket Scraper API
# =====================================================
# This script runs the application using Gunicorn with
# multiple Uvicorn workers for production deployment.
# =====================================================

set -e  # Exit on error

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Loaded environment variables from .env"
else
    echo "⚠️  Warning: .env file not found. Using default settings."
fi

# Set defaults if not specified in .env
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}

echo "=================================================="
echo "🚀 Starting Cricket Scraper API (Production Mode)"
echo "=================================================="
echo "Host: $HOST"
echo "Port: $PORT"
echo "Workers: $WORKERS"
echo "=================================================="

# Run with Gunicorn + Uvicorn workers (production-ready)
gunicorn app.main:app \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind $HOST:$PORT \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --timeout 120 \
    --keep-alive 5 \
    --graceful-timeout 30
