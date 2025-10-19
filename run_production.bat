@echo off
REM =====================================================
REM Production Run Script for Cricket Scraper API (Windows)
REM =====================================================
REM This script runs the application using Gunicorn with
REM multiple Uvicorn workers for production deployment.
REM =====================================================

echo ==================================================
echo 🚀 Starting Cricket Scraper API (Production Mode)
echo ==================================================

REM Load environment variables from .env if using python-dotenv
REM The application will automatically load .env via pydantic-settings

REM Set defaults (can be overridden by .env file)
set HOST=0.0.0.0
set PORT=8000
set WORKERS=4

echo Host: %HOST%
echo Port: %PORT%
echo Workers: %WORKERS%
echo ==================================================

REM Run with Gunicorn + Uvicorn workers (production-ready)
gunicorn app.main:app ^
    --workers %WORKERS% ^
    --worker-class uvicorn.workers.UvicornWorker ^
    --bind %HOST%:%PORT% ^
    --access-logfile - ^
    --error-logfile - ^
    --log-level info ^
    --timeout 120 ^
    --keep-alive 5 ^
    --graceful-timeout 30
