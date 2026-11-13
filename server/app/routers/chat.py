import asyncio
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import ChatMessageRequest, ChatMessageResponse, CivicAIResponse
from app.dependencies import get_current_user
from app.database import get_database
from app.services.gemini_service import generate_civic_guidance
from app.services.rag_service import search_similar_chunks
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["Civic AI Chat"])

@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    req: ChatMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Receives user query, performs MongoDB Vector Similarity RAG lookup across
    statutes and user documents, feeds retrieved evidence to Google Gemini,
    saves chat record in MongoDB, and returns structured citation-backed response.
    """
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Gemini API key is not configured. Please get a free API key at "
                "https://aistudio.google.com/ and set GEMINI_API_KEY in server/.env"
            )
        )

    # 1. Retrieve RAG Vector Similarity matches from MongoDB
    rag_chunks = []
    try:
        rag_chunks = await search_similar_chunks(
            query=req.message,
            user_id=current_user["id"],
            top_k=4
        )
    except Exception as re:
        logger.warning(f"RAG vector similarity lookup warning: {re}")

    try:
        # 2. Call Google Gemini with grounded RAG evidence context in non-blocking thread
        ai_data = await asyncio.to_thread(
            generate_civic_guidance,
            query=req.message,
            document_context=req.documentContext or "",
            rag_chunks=rag_chunks
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error querying Gemini: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate civic response: {str(e)}"
        )

    # 3. Persist message, RAG evidence metadata, and response in MongoDB
    try:
        db = get_database()
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.chat_history.insert_one({
            "user_id": current_user["id"],
            "chat_id": req.chatId,
            "user_query": req.message,
            "rag_chunks_retrieved": len(rag_chunks),
            "ai_response": ai_data,
            "created_at": timestamp_str,
        })
    except Exception as dbe:
        logger.warning(f"Could not log chat message to MongoDB: {str(dbe)}")

    return ChatMessageResponse(
        status="success",
        aiResponse=CivicAIResponse(**ai_data)
    )

@router.get("/history")
async def get_chat_history(current_user: dict = Depends(get_current_user)):
    """
    Returns user's distinct conversations summary from MongoDB.
    """
    try:
        db = get_database()
        pipeline = [
            {"$match": {"user_id": current_user["id"]}},
            {"$sort": {"created_at": -1}},
            {
                "$group": {
                    "_id": "$chat_id",
                    "chat_id": {"$first": "$chat_id"},
                    "last_query": {"$first": "$user_query"},
                    "last_updated": {"$first": "$created_at"},
                    "message_count": {"$sum": 1}
                }
            },
            {"$sort": {"last_updated": -1}},
            {"$limit": 50}
        ]
        chats = await db.chat_history.aggregate(pipeline).to_list(50)
        result = []
        for c in chats:
            q = c.get("last_query", "Civic Consultation")
            title = q if len(q) <= 40 else q[:37] + "..."
            result.append({
                "id": c.get("chat_id"),
                "title": title,
                "preview": q,
                "timestamp": c.get("last_updated"),
                "messagesCount": c.get("message_count", 1)
            })
        return {"status": "success", "chats": result}
    except Exception as e:
        logger.warning(f"Error fetching chat history: {e}")
        return {"status": "success", "chats": []}

@router.get("/conversation/{chat_id}")
async def get_conversation(chat_id: str, current_user: dict = Depends(get_current_user)):
    """
    Fetches full chronological messages for a specific conversation.
    """
    try:
        db = get_database()
        docs = await db.chat_history.find(
            {"user_id": current_user["id"], "chat_id": chat_id},
            {"_id": 0}
        ).sort("created_at", 1).to_list(100)

        messages = []
        for idx, doc in enumerate(docs):
            created_at = doc.get("created_at", "")
            messages.append({
                "id": f"msg-u-{idx}",
                "sender": "user",
                "text": doc.get("user_query", ""),
                "timestamp": created_at
            })
            if "ai_response" in doc and isinstance(doc["ai_response"], dict):
                ai_dict = dict(doc["ai_response"])
                ai_dict["sender"] = "ai"
                messages.append(ai_dict)

        return {"status": "success", "chatId": chat_id, "messages": messages}
    except Exception as e:
        logger.warning(f"Error fetching conversation {chat_id}: {e}")
        return {"status": "success", "chatId": chat_id, "messages": []}

@router.delete("/conversation/{chat_id}")
async def delete_conversation(chat_id: str, current_user: dict = Depends(get_current_user)):
    """
    Deletes a conversation history from MongoDB.
    """
    try:
        db = get_database()
        result = await db.chat_history.delete_many({
            "user_id": current_user["id"],
            "chat_id": chat_id
        })
        return {"status": "success", "deletedCount": result.deleted_count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )

@router.delete("/history")
async def clear_all_chat_history(current_user: dict = Depends(get_current_user)):
    """
    Clears all conversations for the authenticated user.
    """
    try:
        db = get_database()
        result = await db.chat_history.delete_many({"user_id": current_user["id"]})
        return {"status": "success", "deletedCount": result.deleted_count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear chat history: {str(e)}"
        )

