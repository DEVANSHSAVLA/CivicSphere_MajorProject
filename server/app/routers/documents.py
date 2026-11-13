import asyncio
import io
import math
import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from pypdf import PdfReader
from app.dependencies import get_current_user
from app.database import get_database
from app.services.gemini_service import summarize_civic_document
from app.services.cloudinary_service import (
    upload_document_to_cloudinary,
    delete_cloudinary_asset,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["Documents"])

def extract_text_from_file(filename: str, contents: bytes) -> tuple[str, int]:
    """Extracts raw text and estimates page count from uploaded bytes."""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    text = ""
    pages = 1

    if ext == "pdf":
        try:
            reader = PdfReader(io.BytesIO(contents))
            pages = max(1, len(reader.pages))
            page_texts = [page.extract_text() or "" for page in reader.pages]
            text = "\n\n".join(page_texts).strip()
        except Exception as e:
            logger.warning(f"Error reading PDF with pypdf: {e}")
            text = f"PDF Document: {filename}"
    elif ext in ("docx", "doc"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(contents))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n\n".join(paragraphs).strip()
            pages = max(1, math.ceil(len(text) / 2500))
        except Exception as e:
            logger.warning(f"Error reading DOCX with python-docx: {e}")
            text = f"DOCX Document: {filename}"
    elif ext in ("txt", "md", "csv"):
        try:
            text = contents.decode("utf-8", errors="ignore")
            pages = max(1, math.ceil(len(text) / 2500))
        except Exception as e:
            logger.warning(f"Error decoding text file: {e}")
            text = filename
    else:
        try:
            # Fallback text extraction
            text = contents.decode("utf-8", errors="ignore")
            pages = 1
        except Exception:
            text = f"Uploaded document: {filename}"

    return text or f"Document: {filename}", pages

@router.post("/summarize")
async def upload_and_summarize_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Accepts uploaded legal/civic document (PDF, DOCX, TXT),
    extracts content, generates AI summary via Gemini,
    stores document record in MongoDB, and returns summary & key clauses.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename must not be empty."
        )

    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {str(e)}"
        )

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB limit
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 20MB maximum limit."
        )

    file_size_mb = f"{(len(contents) / (1024 * 1024)):.2f} MB"
    ext = file.filename.split(".")[-1].upper() if "." in file.filename else "DOC"

    # Extract text from document
    text_content, pages = extract_text_from_file(file.filename, contents)

    # Call Gemini for grounded legal summary in non-blocking thread
    try:
        ai_summary = await asyncio.to_thread(summarize_civic_document, text_content, file.filename)
    except Exception as ge:
        logger.error(f"Gemini summarization error: {ge}")
        ai_summary = {
            "summary": f"Document '{file.filename}' processed and indexed.",
            "keyPoints": ["Indexed for citation search in Chat Assistant"],
            "category": "Legal Document",
            "citations": []
        }

    doc_id = "doc-" + uuid.uuid4().hex[:10]
    uploaded_date = datetime.now().strftime("%d %b %Y")

    # Upload original binary file to Cloudinary CDN
    cdn_upload = upload_document_to_cloudinary(
        file_bytes=contents,
        filename=file.filename,
        user_id=current_user["id"],
    )
    download_url = cdn_upload.get("secure_url") or "#"
    cloudinary_public_id = cdn_upload.get("public_id", "")

    doc_record = {
        "id": doc_id,
        "name": file.filename,
        "type": ext,
        "size": file_size_mb,
        "uploadedDate": uploaded_date,
        "status": "Processed & Indexed",
        "category": ai_summary.get("category", "Legal Document"),
        "pages": pages,
        "summary": ai_summary.get("summary", ""),
        "keyPoints": ai_summary.get("keyPoints", []),
        "citations": ai_summary.get("citations", []),
        "downloadUrl": download_url,
        "cloudinary_public_id": cloudinary_public_id,
        "storage": cdn_upload.get("storage", "local"),
        "user_id": current_user["id"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Persist to MongoDB
    try:
        db = get_database()
        await db.documents.insert_one(dict(doc_record))
    except Exception as dbe:
        logger.warning(f"Could not persist document to MongoDB: {dbe}")

    # Index document chunks into MongoDB vector store for RAG
    try:
        from app.services.rag_service import index_document_chunks
        await index_document_chunks(
            doc_id=doc_id,
            title=file.filename,
            text=text_content,
            user_id=current_user["id"],
            source="user_document",
            category=ai_summary.get("category", "Legal Document")
        )
    except Exception as rage:
        logger.warning(f"RAG document indexing warning: {rage}")

    # Remove internal _id for response
    doc_record.pop("_id", None)

    return {
        "status": "success",
        "document": doc_record
    }

@router.get("")
async def get_user_documents(current_user: dict = Depends(get_current_user)):
    """Fetches all documents uploaded by the authenticated user from MongoDB."""
    try:
        db = get_database()
        docs = await db.documents.find(
            {"user_id": current_user["id"]},
            {"_id": 0}
        ).sort("created_at", -1).to_list(100)
        return {"status": "success", "documents": docs}
    except Exception as e:
        logger.warning(f"Error reading documents: {e}")
        return {"status": "success", "documents": []}

@router.delete("/{doc_id}")
async def delete_user_document(
    doc_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Deletes a document from MongoDB and cleans up Cloudinary CDN storage."""
    try:
        db = get_database()
        doc = await db.documents.find_one({"id": doc_id, "user_id": current_user["id"]})
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{doc_id}' not found."
            )

        if doc.get("cloudinary_public_id"):
            delete_cloudinary_asset(doc["cloudinary_public_id"], resource_type="raw")

        await db.documents.delete_one({"id": doc_id, "user_id": current_user["id"]})
        # Clean up corresponding vector RAG chunks
        await db.rag_chunks.delete_many({"doc_id": doc_id, "user_id": current_user["id"]})
        return {"status": "success", "message": "Document deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )

