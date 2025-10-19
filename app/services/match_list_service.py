# app/services/match_list_service.py
import requests, json, os
from app.core.config import HEADERS, MATCH_LIST_URL, ALL_MATCHES_FILE, DATA_DIR
from app.core.logger import get_logger

logger = get_logger("match_list_service")

def fetch_all_matches():
    try:
        response = requests.get(MATCH_LIST_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        matches = []

        for item in data:
            event = item.get('event', {})
            catalogue = item.get('catalogue', {})
            competition = item.get('competition', {})
            runners = catalogue.get('runners', [])
            matches.append({
                'match_name': event.get('name', 'N/A'),
                'teams': ', '.join([r.get('name', 'N/A') for r in runners]),
                'start_time': event.get('openDate', 'N/A'),
                'status': catalogue.get('status', 'N/A'),
                'market_id': catalogue.get('marketId', 'N/A'),
                'event_id': event.get('id', 'N/A'),
                'competition': competition.get('name', 'N/A'),
                'live': catalogue.get('inPlay', False)
            })

        # Sort matches: Live first, then OPEN before SUSPENDED, then by start time
        def sort_key(match):
            # Priority 1: Live matches first (True=1, False=0, invert to get True first)
            live_priority = 0 if match.get('live') else 1
            
            # Priority 2: Status priority (OPEN before SUSPENDED)
            status = match.get('status', 'N/A')
            status_priority = 0 if status == 'OPEN' else (1 if status == 'SUSPENDED' else 2)
            
            # Priority 3: Start time (earliest first)
            start_time = match.get('start_time', 'Z')
            
            return (live_priority, status_priority, start_time)
        
        matches.sort(key=sort_key)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(ALL_MATCHES_FILE, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=4, ensure_ascii=False)

        logger.info(f"Saved {len(matches)} matches (sorted: live first, then by status and time).")
        return matches

    except Exception as e:
        logger.error(f"Error fetching matches: {e}")
        return []
