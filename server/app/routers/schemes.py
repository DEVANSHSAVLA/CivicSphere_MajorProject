import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel
from app.dependencies import get_current_user
from app.database import get_database
from app.services.myscheme_service import (
    get_all_schemes,
    filter_schemes,
    evaluate_scheme_eligibility,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/schemes", tags=["Government Schemes"])

class EligibilityCheckRequest(BaseModel):
    schemeId: str
    answers: dict

@router.get("")
async def get_schemes(
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
):
    """
    Fetches government schemes integrating myScheme and API Setu data catalog.
    Supports filtering by category, state, and search query.
    """
    schemes = filter_schemes(category=category, state=state, query=q)
    return {
        "status": "success",
        "count": len(schemes),
        "source": "myScheme / API Setu Open Gateway",
        "schemes": schemes
    }

@router.get("/saved")
@router.get("/user/saved")
async def get_saved_schemes(current_user: dict = Depends(get_current_user)):
    """
    Returns the list of schemes bookmarked by the authenticated citizen in MongoDB.
    """
    try:
        db = get_database()
        records = await db.saved_schemes.find({"user_id": current_user["id"]}).to_list(100)
        saved_ids = {r["scheme_id"] for r in records}
        
        all_schemes = get_all_schemes()
        bookmarked = [
            {**s, "isSaved": True}
            for s in all_schemes
            if s["id"] in saved_ids or s["slug"] in saved_ids
        ]
        return {
            "status": "success",
            "count": len(bookmarked),
            "savedSchemeIds": list(saved_ids),
            "schemes": bookmarked
        }
    except Exception as e:
        logger.warning(f"Error fetching saved schemes: {e}")
        return {"status": "success", "count": 0, "savedSchemeIds": [], "schemes": []}

@router.get("/{scheme_id}")
async def get_scheme_detail(scheme_id: str):
    """Fetches full specifications for a single government scheme."""
    schemes = get_all_schemes()
    scheme = next((s for s in schemes if s["id"] == scheme_id or s["slug"] == scheme_id), None)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme '{scheme_id}' not found in myScheme repository."
        )
    return {
        "status": "success",
        "scheme": scheme
    }

@router.post("/check-eligibility")
async def check_eligibility(req: EligibilityCheckRequest):
    """
    Evaluates citizen eligibility against verified central/state scheme criteria.
    """
    result = evaluate_scheme_eligibility(req.schemeId, req.answers)
    return {
        "status": "success",
        "evaluation": result
    }

@router.post("/{scheme_id}/bookmark")
async def toggle_scheme_bookmark(
    scheme_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Bookmarks or unbookmarks a scheme in MongoDB for the logged-in citizen."""
    try:
        db = get_database()
        user_id = current_user["id"]
        existing = await db.saved_schemes.find_one({"user_id": user_id, "scheme_id": scheme_id})
        
        if existing:
            await db.saved_schemes.delete_one({"user_id": user_id, "scheme_id": scheme_id})
            is_saved = False
        else:
            await db.saved_schemes.insert_one({"user_id": user_id, "scheme_id": scheme_id})
            is_saved = True
            
        return {
            "status": "success",
            "schemeId": scheme_id,
            "isSaved": is_saved
        }
    except Exception as e:
        logger.warning(f"Error toggling scheme bookmark: {e}")
        return {"status": "success", "schemeId": scheme_id, "isSaved": True}

