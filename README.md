# Cricket Scraper + API

A FastAPI-based web scraper that fetches cricket match data and odds, with automated background tasks using APScheduler.

## Structure

- `app/`: FastAPI app, routers, services, schemas, core config
- `app/data/`: stores all_matches.json and live_matches.json (created at runtime)
- `app/core/`: configuration, settings, and logging
- `app/routers/`: API endpoint definitions
- `app/services/`: business logic for scraping and data processing
- `app/schemas/`: Pydantic models for data validation

## Local Development

1. Create virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   # Development mode
   bash run.sh
   # or
   uvicorn app.main:app --reload --port 8000
   ```

3. Production mode:
   ```bash
   # Unix/Linux/Mac
   bash run_production.sh
   
   # Windows
   run_production.bat
   ```

## API Endpoints

- `GET /` - Health check
- `GET /matches/all` - Fetches & saves all matches to data/all_matches.json
- `GET /live/odds` - Fetches live match details and saves to data/live_matches.json

## Deployment

### Render Deployment (Using CLI)

For detailed instructions, see [DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md)

**Quick Start:**

1. Install Render CLI:
   ```bash
   npm install -g @render-cloud/cli
   ```

2. Login to Render:
   ```bash
   render login
   ```

3. Deploy:
   ```bash
   # Windows
   deploy_render.bat
   
   # Unix/Linux/Mac
   ./deploy_render.sh
   ```

### Other Deployment Options

- **Fly.io**: See deployment scripts (`deploy.sh`, `deploy.bat`) and `fly.toml`
- **Docker**: Build and run using the included Dockerfile
- **Traditional Server**: Use `run_production.sh` with systemd/supervisor

## Configuration

Create a `.env` file in the project root:

```env
APP_NAME=Cricket Odds API
VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
WORKERS=4
ALLOWED_DOMAINS=http://localhost,http://127.0.0.1,https://yourdomain.com
BASE_URL=https://api.radheexch.xyz
SCRAPE_INTERVAL=5
LOG_LEVEL=INFO
```

## Features

- ✅ FastAPI web framework for high performance
- ✅ Automated background scraping with APScheduler
- ✅ CORS support for frontend integration
- ✅ Persistent JSON data storage
- ✅ Production-ready with Gunicorn + Uvicorn workers
- ✅ Configurable via environment variables
- ✅ Comprehensive logging
- ✅ Ready for cloud deployment (Render, Fly.io, etc.)
