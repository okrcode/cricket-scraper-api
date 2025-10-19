# app/schemas/match.py
from pydantic import BaseModel
from typing import List, Optional, Dict

class Match(BaseModel):
    match_name: str
    teams: str
    start_time: str
    status: str
    market_id: str
    event_id: str
    competition: str
    live: bool

class LiveMatchOdds(BaseModel):
    match_id: str
    bookmaker: Dict
    fancy: Dict
    sessions: Dict
    result: Optional[Dict] = None
