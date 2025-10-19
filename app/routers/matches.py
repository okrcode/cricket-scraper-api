# app/routers/matches.py
from fastapi import APIRouter
from app.services.match_list_service import fetch_all_matches

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/all")
def all_cricket_matches_api_url():
    """All cricket matches API - returns all cricket match details"""
    return fetch_all_matches()
