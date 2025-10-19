# app/routers/live.py
from fastapi import APIRouter, HTTPException
from app.services.live_match_service import update_live_matches

router = APIRouter(prefix="/live", tags=["Live Matches"])

@router.get("/odds")
def live_match_odds_api_url():
    """Live match odds API - continuously updates for all live matches"""
    try:
        results = update_live_matches()
        return {
            "count": len(results),
            "live_matches": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live odds: {str(e)}")


