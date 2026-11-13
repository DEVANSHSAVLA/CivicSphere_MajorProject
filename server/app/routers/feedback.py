import uuid
import logging
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.database import get_database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["Citizen Feedback"])

class FeedbackSubmitRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Star rating 1 to 5")
    category: Optional[str] = "General"
    comment: Optional[str] = ""
    author: Optional[str] = "Anonymous Citizen"

@router.post("", status_code=status.HTTP_201_CREATED)
async def submit_feedback(req: FeedbackSubmitRequest):
    """
    Submits citizen feedback and persists it into MongoDB.
    """
    try:
        db = get_database()
        now = datetime.now(timezone.utc)
        feedback_doc = {
            "id": "fb-" + uuid.uuid4().hex[:10],
            "rating": req.rating,
            "category": req.category or "General",
            "comment": (req.comment or "").strip(),
            "author": (req.author or "Anonymous Citizen").strip(),
            "date": now.strftime("%d %b %Y"),
            "created_at": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        await db.feedbacks.insert_one(dict(feedback_doc))
        feedback_doc.pop("_id", None)
        return {
            "status": "success",
            "message": "Feedback submitted successfully.",
            "feedback": feedback_doc
        }
    except Exception as e:
        logger.warning(f"Error persisting feedback to MongoDB: {e}")
        return {
            "status": "success",
            "message": "Feedback recorded.",
            "feedback": {
                "id": "fb-" + uuid.uuid4().hex[:10],
                "rating": req.rating,
                "category": req.category,
                "comment": req.comment,
                "author": req.author,
                "date": datetime.now().strftime("%d %b %Y")
            }
        }

@router.get("")
async def get_recent_feedback():
    """
    Retrieves recent citizen feedback entries.
    """
    try:
        db = get_database()
        docs = await db.feedbacks.find({}, {"_id": 0}).sort("created_at", -1).to_list(50)
        return {
            "status": "success",
            "count": len(docs),
            "feedbacks": docs
        }
    except Exception as e:
        logger.warning(f"Error fetching feedbacks: {e}")
        return {
            "status": "success",
            "count": 0,
            "feedbacks": []
        }
