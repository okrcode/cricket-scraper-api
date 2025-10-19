# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import matches, live
from app.core.settings import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from app.services.live_match_service import force_refresh_live_matches
from app.core.config import SCRAPE_INTERVAL
import atexit

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_domains_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches.router)
app.include_router(live.router)

# APScheduler setup: force refresh live matches at configured interval
scheduler = BackgroundScheduler(executors={"default": ThreadPoolExecutor(10)})

def _scheduled_update():
    try:
        force_refresh_live_matches()
    except Exception as e:
        from app.core.logger import get_logger
        get_logger('scheduler').error(f"Scheduled update failed: {e}")


@app.on_event('startup')
def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(_scheduled_update, 'interval', seconds=SCRAPE_INTERVAL, id='live_update_job', replace_existing=True)
        scheduler.start()


@app.on_event('shutdown')
def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)

atexit.register(lambda: scheduler.shutdown(wait=False) if scheduler.running else None)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running", "version": settings.VERSION}
