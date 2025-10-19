"""Legacy automation service removed.

APScheduler is used in `app/main.py` to manage scheduled scraping. This
module exists only as a harmless stub to avoid import errors.
"""

def start_automation():
    raise RuntimeError("Legacy automation service removed. Use APScheduler in app.main.")

def stop_automation():
    raise RuntimeError("Legacy automation service removed. Use APScheduler in app.main.")

def get_status():
    return {"is_running": False, "message": "Removed - use APScheduler"}

def set_intervals(*args, **kwargs):
    raise RuntimeError("Legacy automation service removed. Configure SCRAPE_INTERVAL in config and restart the app.")
