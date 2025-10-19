# app/core/config.py
import os

BASE_URL = "https://api.radheexch.xyz"

HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141 Safari/537.36",
}

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
ALL_MATCHES_FILE = os.path.join(DATA_DIR, "all_matches.json")
LIVE_MATCHES_FILE = os.path.join(DATA_DIR, "live_matches.json")

MATCH_LIST_URL = f"{BASE_URL}/delaymarkets/markets/eventtype/4"
MATCH_DETAIL_URL = f"{BASE_URL}/delaymarkets/events/detail"

# How often the scheduler should force refresh live matches (seconds)
SCRAPE_INTERVAL = 5

# Optional external endpoint to POST each live match JSON to after scraping.
# Set to None or an empty string to disable pushing.
LIVE_MATCH_ODDS_PUSH_URL = None
