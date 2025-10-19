# app/services/live_match_service.py
import requests, json, os
import asyncio
import aiohttp
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from app.core.config import HEADERS, MATCH_DETAIL_URL, ALL_MATCHES_FILE, LIVE_MATCHES_FILE, DATA_DIR
from app.core.logger import get_logger
import requests
from app.core.config import LIVE_MATCH_ODDS_PUSH_URL
from app.core.settings import settings

logger = get_logger("live_match_service")

# Create a persistent session for better connection handling
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Global session for connection pooling and cookie persistence
session = requests.Session()
session.verify = True  # Keep SSL verification enabled

# Configure proxy if enabled
if settings.USE_PROXY:
    if settings.SCRAPER_API_KEY:
        # ScraperAPI integration
        proxy_url = f"http://scraperapi:{settings.SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001"
        logger.info("Using ScraperAPI proxy for requests")
    elif settings.PROXY_URL:
        # Custom proxy
        proxy_url = settings.PROXY_URL
        logger.info(f"Using custom proxy for requests")
    else:
        proxy_url = None
        logger.warning("USE_PROXY is True but no proxy configured")
    
    if proxy_url:
        session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
else:
    logger.info("Direct connection (no proxy)")

def classify_market(name):
    name = (name or "").lower()
    if "match odds" in name:
        return "bookmaker"
    elif "runs" in name or "boundaries" in name:
        return "fancy"
    elif "session" in name or "over" in name:
        return "sessions"
    return "other"

def fetch_live_match(event_id, max_retries=3, retry_delay=1):
    """Fetch live match data for a single event ID with enhanced error handling"""
    
    for attempt in range(max_retries):
        try:
            # Add progressive delay between retries (not on first attempt)
            if attempt > 0:
                delay = retry_delay * (1.5 ** attempt) + random.uniform(0, 0.5)
                logger.info(f"Retrying event {event_id} in {delay:.2f} seconds...")
                time.sleep(delay)
            
            logger.info(f"Fetching data for event_id: {event_id} (attempt {attempt + 1}/{max_retries})")
            
            # Enhanced headers with anti-bot measures
            enhanced_headers = HEADERS.copy()
            
            # Add random user agent rotation (more realistic)
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
            ]
            
            # Realistic browser headers
            enhanced_headers.update({
                'User-Agent': random.choice(user_agents),
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://api.radheexch.xyz/',
                'Origin': 'https://api.radheexch.xyz',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'DNT': '1'
            })
            
            # Make request with timeout and retry logic using persistent session
            res = session.get(
                f"{MATCH_DETAIL_URL}/{event_id}", 
                headers=enhanced_headers, 
                timeout=20,
                allow_redirects=True
            )
            
            # Check for rate limiting or blocking
            if res.status_code == 429:
                logger.warning(f"Rate limited for event {event_id}, waiting longer...")
                time.sleep(10 + random.uniform(0, 5))
                continue
            elif res.status_code == 403:
                logger.warning(f"Access forbidden for event {event_id}, trying different approach...")
                time.sleep(5 + random.uniform(0, 3))
                continue
            elif res.status_code == 404:
                logger.warning(f"Event {event_id} not found")
                return None
                
            res.raise_for_status()
            
            # Validate response content
            if not res.content:
                logger.warning(f"Empty response for event {event_id}")
                continue
                
            data = res.json()
            
            # Validate JSON structure
            if not isinstance(data, dict) or data is None:
                logger.warning(f"Invalid JSON structure for event {event_id}, skipping retries")
                return None
            
            # Validate essential fields exist
            if not data.get('event'):
                logger.warning(f"Missing 'event' data for event {event_id}, skipping retries")
                return None

            # Parse odds and score data with error handling
            try:
                odds_data = json.loads(data.get('odds', '{}')) if data.get('odds') else {}
            except (json.JSONDecodeError, TypeError):
                odds_data = {}
                
            try:
                score_data = json.loads(data.get('score', '{}')) if data.get('score') else {}
            except (json.JSONDecodeError, TypeError):
                score_data = {}

            # Initialize organized structure
            organized = {
                "match_id": data.get('event', {}).get('id', event_id),
                "match_name": data.get('event', {}).get('name', 'Unknown Match'),
                "bookmaker": {},
                "fancy": {},
                "sessions": {},
                "result": score_data or {},
                "odds": odds_data or {},
                "last_updated": datetime.now().isoformat()
            }

            # Helper: parse runner and market odds encoded as strings from API
            def parse_runner_odds(runner_str):
                # Expected format: "<id>~<status>~<back_price>:<back_volume>:<back_exposed>~<lay_price>:<lay_volume>:<lay_exposed>"
                if not runner_str:
                    return None
                parts = runner_str.split('~')
                if len(parts) < 3:
                    return None
                runner_id = parts[0]
                status = parts[1]
                back_parts = parts[2].split(':') if parts[2] else [None, 0, 0]
                lay_parts = parts[3].split(':') if len(parts) > 3 and parts[3] else [None, 0, 0]
                try:
                    back_price = float(back_parts[0]) if back_parts[0] not in (None, '') else None
                except Exception:
                    back_price = None
                try:
                    lay_price = float(lay_parts[0]) if lay_parts[0] not in (None, '') else None
                except Exception:
                    lay_price = None
                def to_int(x):
                    try:
                        return int(x)
                    except Exception:
                        return 0
                return {
                    'id': runner_id,
                    'status': status,
                    'back': {'price': back_price, 'volume': to_int(back_parts[1]) if len(back_parts) > 1 else 0, 'exposed': to_int(back_parts[2]) if len(back_parts) > 2 else 0},
                    'lay': {'price': lay_price, 'volume': to_int(lay_parts[1]) if len(lay_parts) > 1 else 0, 'exposed': to_int(lay_parts[2]) if len(lay_parts) > 2 else 0}
                }

            def parse_market_odds(odds_str):
                # odds_str may be a pipe-separated value with runners after index 7
                if not odds_str or not isinstance(odds_str, str):
                    return None
                parts = odds_str.split('|')
                # if it's a compact representation, expect runners at index 7
                if len(parts) >= 8:
                    status = parts[2]
                    in_play = parts[6].lower() == 'true'
                    runners_str = parts[7]
                    runners = []
                    for r in runners_str.split(','):
                        parsed = parse_runner_odds(r)
                        if parsed:
                            runners.append(parsed)
                    return {'status': status, 'in_play': in_play, 'runners': runners}
                # fallback: if the field is already a JSON-like dict/list, try to parse
                try:
                    parsed_json = json.loads(odds_str)
                    return parsed_json
                except Exception:
                    return None

            # Process catalogues (markets) with error handling
            catalogues = data.get('catalogues', [])
            logger.info(f"Found {len(catalogues)} catalogues for event {event_id}")
            
            for cat in catalogues:
                try:
                    category = classify_market(cat.get('marketName'))
                    market_id = str(cat.get('marketId', ''))

                    # Ensure the category key exists in organized dict
                    if category not in organized:
                        organized[category] = {}

                    # Basic market info
                    market_condition = cat.get('marketCondition')
                    market_name = cat.get('marketName')
                    market_status = cat.get('status', 'ACTIVE')
                    market_inplay = cat.get('inPlay', False)

                    # If odds_data contains a compact encoded string for this market, parse it
                    parsed_market = None
                    if odds_data and isinstance(odds_data, dict):
                        raw = odds_data.get(market_id) or odds_data.get(int(market_id))
                        if raw:
                            parsed_market = parse_market_odds(raw)

                    # Map runners from catalogue
                    runners_map = {str(r.get('id')): r.get('name') for r in cat.get('runners', [])}

                    if parsed_market and isinstance(parsed_market, dict):
                        # attach runner names when ids match
                        for r in parsed_market.get('runners', []):
                            r['name'] = runners_map.get(str(r.get('id')), r.get('name', 'Unknown'))

                        market_entry = {
                            "name": market_name,
                            "runners": parsed_market.get('runners', []),
                            "status": parsed_market.get('status', market_status),
                            "in_play": parsed_market.get('in_play', market_inplay)
                        }
                        # Only include market_condition for 'fancy' category
                        if category == 'fancy':
                            market_entry["market_condition"] = market_condition
                        organized[category][market_id] = market_entry
                    else:
                        market_entry = {
                            "name": market_name,
                            "runners": [ {"id": str(r.get('id')), "name": r.get('name')} for r in cat.get('runners', [])],
                            "status": market_status,
                            "in_play": market_inplay
                        }
                        # Only include market_condition for 'fancy' category
                        if category == 'fancy':
                            market_entry["market_condition"] = market_condition
                        organized[category][market_id] = market_entry
                except Exception as e:
                    logger.warning(f"Error processing catalogue for event {event_id}: {e}")
                    continue

            logger.info(f"Successfully fetched data for event {event_id}")
            return organized

        except requests.exceptions.Timeout as e:
            logger.warning(f"Timeout error for event {event_id} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} timeout attempts for event {event_id}")
                return None
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error for event {event_id} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} connection attempts for event {event_id}")
                return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error for event {event_id} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} request attempts for event {event_id}")
                return None
        except json.JSONDecodeError as e:
            # JSON errors are unlikely to be fixed by retrying
            logger.error(f"JSON decode error for event {event_id}: {e} - skipping retries")
            return None
        except (AttributeError, TypeError, KeyError) as e:
            # Data structure errors indicate invalid/missing data - don't retry
            logger.error(f"Invalid data structure for event {event_id}: {e} - skipping retries")
            return None
        except Exception as e:
            logger.warning(f"Unexpected error for event {event_id} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts for event {event_id}: {e}")
                return None
    
    logger.error(f"Failed to fetch data for event {event_id} after {max_retries} attempts")
    return None

def fetch_live_match_sync(match_info):
    """Wrapper function for concurrent execution"""
    event_id = match_info.get('event_id')
    match_name = match_info.get('match_name', 'Unknown')
    
    logger.info(f"Processing live match: {match_name} (ID: {event_id})")
    result = fetch_live_match(event_id)
    
    if result:
        # Add match metadata
        result.update({
            "match_name": match_name,
            "teams": match_info.get('teams', ''),
            "competition": match_info.get('competition', ''),
            "start_time": match_info.get('start_time', ''),
            "status": match_info.get('status', '')
        })
    
    return result

# Cache for live matches data
_live_matches_cache = None
_last_update_time = 0
_update_interval = 30  # Update every 30 seconds

def update_live_matches():
    """Update all live matches with concurrent processing and caching"""
    global _live_matches_cache, _last_update_time
    
    current_time = time.time()
    
    # Return cached data if it's fresh enough
    if _live_matches_cache and (current_time - _last_update_time) < _update_interval:
        logger.info("Returning cached live matches data")
        return _live_matches_cache
    
    if not os.path.exists(ALL_MATCHES_FILE):
        logger.warning("Match list missing. Run match_list_service first.")
        return []

    try:
        with open(ALL_MATCHES_FILE, 'r', encoding='utf-8') as f:
            matches = json.load(f)
    except Exception as e:
        logger.error(f"Error reading match file: {e}")
        return []

    # Filter live matches
    live_matches = [m for m in matches if m.get('live')]
    logger.info(f"Found {len(live_matches)} live matches to process")

    if not live_matches:
        logger.info("No live matches found")
        _live_matches_cache = []
        _last_update_time = current_time
        return []

    results = []
    failed_matches = []

    # Process matches sequentially to avoid rate limiting
    # Changed from max_workers=5 to max_workers=1 for better success rate
    with ThreadPoolExecutor(max_workers=1) as executor:
        # Submit all tasks
        future_to_match = {
            executor.submit(fetch_live_match_sync, match): match 
            for match in live_matches
        }
        
        # Collect results with delay between matches
        for idx, future in enumerate(future_to_match):
            match = future_to_match[future]
            try:
                # Add delay between matches (except first one) to avoid rate limiting
                if idx > 0:
                    delay = random.uniform(2, 4)  # 2-4 seconds between matches
                    logger.info(f"Waiting {delay:.1f}s before processing next match...")
                    time.sleep(delay)
                
                result = future.result(timeout=30)
                if result:
                    results.append(result)
                    logger.info(f"Successfully processed: {result.get('match_name', 'Unknown')}")
                    # Optionally push each match result to an external API
                    try:
                        if LIVE_MATCH_ODDS_PUSH_URL:
                            headers = {'Content-Type': 'application/json'}
                            requests.post(LIVE_MATCH_ODDS_PUSH_URL, json=result, headers=headers, timeout=5)
                    except Exception as e:
                        logger.warning(f"Failed to push match data for {result.get('match_name', 'Unknown')}: {e}")
                else:
                    failed_matches.append(match.get('match_name', 'Unknown'))
                    logger.warning(f"Failed to process: {match.get('match_name', 'Unknown')}")
            except Exception as e:
                failed_matches.append(match.get('match_name', 'Unknown'))
                logger.error(f"Exception processing {match.get('match_name', 'Unknown')}: {e}")

    # Update cache and save results
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(LIVE_MATCHES_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        # Update cache
        _live_matches_cache = results
        _last_update_time = current_time
        
        logger.info(f"Updated {len(results)} live matches successfully")
        if failed_matches:
            logger.warning(f"Failed to process {len(failed_matches)} matches: {failed_matches}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error saving live matches: {e}")
        return results

def force_refresh_live_matches():
    """Force refresh of live matches cache"""
    global _last_update_time
    _last_update_time = 0  # Force refresh
    return update_live_matches()
