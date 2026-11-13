import asyncio
import logging
import uuid
from datetime import datetime
import numpy as np
from google import genai
from app.config import settings
from app.database import get_database

logger = logging.getLogger(__name__)

EMBEDDING_MODELS = ["models/gemini-embedding-001", "models/gemini-embedding-2", "text-embedding-004"]

def get_embedding_client():
    if not settings.GEMINI_API_KEY:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY, http_options={'timeout': 10000})

def generate_embedding(text: str) -> list[float]:
    """
    Generates a 3072-dimensional vector embedding using Google Gemini Embedding models.
    """
    client = get_embedding_client()
    if not client or not text.strip():
        return []

    # Clean text
    clean_text = text.replace("\n", " ").strip()[:2000]

    for model_name in EMBEDDING_MODELS:
        try:
            res = client.models.embed_content(
                model=model_name,
                contents=clean_text
            )
            if hasattr(res, "embeddings") and res.embeddings:
                return res.embeddings[0].values
        except Exception as e:
            logger.warning(f"Error generating embedding with {model_name}: {e}")
            continue

    logger.error("Failed to generate embedding with all candidate models.")
    return []

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    """
    Splits text into overlapping semantic chunks on sentence boundaries.
    """
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += ("\n\n" + para if current_chunk else para)
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Handle exceptionally long paragraphs
            if len(para) > chunk_size:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunks.append(para[start:end].strip())
                    start = end - overlap
                current_chunk = ""
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return [c for c in chunks if len(c) > 30]

async def index_document_chunks(
    doc_id: str,
    title: str,
    text: str,
    user_id: str = "system",
    source: str = "user_document",
    category: str = "Document"
) -> int:
    """
    Splits text into chunks, generates embeddings with Gemini,
    and stores them in the MongoDB `rag_chunks` collection.
    """
    try:
        db = get_database()
        chunks = chunk_text(text)
        if not chunks:
            return 0

        inserted_count = 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for idx, chunk in enumerate(chunks):
            embedding = await asyncio.to_thread(generate_embedding, chunk)
            if not embedding:
                continue

            chunk_record = {
                "id": f"chunk-{uuid.uuid4().hex[:12]}",
                "doc_id": doc_id,
                "chunk_index": idx,
                "title": title,
                "text": chunk,
                "category": category,
                "source": source,
                "user_id": user_id,
                "embedding": embedding,
                "created_at": timestamp,
            }
            await db.rag_chunks.insert_one(chunk_record)
            inserted_count += 1

        logger.info(f"RAG: Successfully indexed {inserted_count} chunks for '{title}' (user: {user_id})")
        return inserted_count
    except Exception as e:
        logger.error(f"Error indexing document chunks in MongoDB: {e}")
        return 0

async def search_similar_chunks(
    query: str,
    user_id: str = None,
    doc_id: str = None,
    top_k: int = 4
) -> list[dict]:
    """
    Computes vector cosine similarity against MongoDB chunks and returns Top-K matches.
    """
    query_vector = await asyncio.to_thread(generate_embedding, query)
    if not query_vector:
        return []

    try:
        db = get_database()
        query_filter = {}

        # Allow retrieval from system statutes plus the user's uploaded documents
        if user_id:
            query_filter["user_id"] = {"$in": [user_id, "system"]}
        else:
            query_filter["user_id"] = "system"

        if doc_id:
            query_filter["doc_id"] = doc_id

        cursor = db.rag_chunks.find(
            query_filter,
            {"_id": 0, "embedding": 1, "text": 1, "title": 1, "category": 1, "source": 1, "doc_id": 1}
        )
        candidates = await cursor.to_list(150)
        if not candidates:
            return []

        # Vector Cosine Similarity via NumPy
        q_vec = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []

        scored_matches = []
        for cand in candidates:
            emb = cand.get("embedding")
            if not emb:
                continue
            c_vec = np.array(emb, dtype=np.float32)
            c_norm = np.linalg.norm(c_vec)
            if c_norm == 0:
                continue

            similarity = float(np.dot(q_vec, c_vec) / (q_norm * c_norm))
            scored_matches.append({
                "score": round(similarity, 4),
                "title": cand.get("title", ""),
                "text": cand.get("text", ""),
                "category": cand.get("category", ""),
                "source": cand.get("source", ""),
                "doc_id": cand.get("doc_id", ""),
            })

        # Sort descending by similarity score
        scored_matches.sort(key=lambda x: x["score"], reverse=True)
        return scored_matches[:top_k]
    except Exception as e:
        logger.error(f"Error executing vector similarity search: {e}")
        return []

async def seed_canonical_statutes_for_rag():
    """
    Seeds verified NeGD Nyaykosh laws into MongoDB vector store if not already present.
    Ensures RAG works immediately out-of-the-box without requiring manual document uploads.
    """
    if not settings.GEMINI_API_KEY:
        logger.info("RAG: GEMINI_API_KEY not configured; skipping automatic statute seeding.")
        return

    try:
        db = get_database()
        existing = await db.rag_chunks.count_documents({"source": "nyaykosh_statute"})
        if existing > 0:
            logger.info(f"RAG: Canonical statutes already initialized ({existing} chunks present).")
            return

        from app.services.nyaykosh_service import NYAYKOSH_LAWS

        logger.info("[INFO] Seeding canonical Nyaykosh statutes into MongoDB Vector Store...")
        for law in NYAYKOSH_LAWS:
            # Format law text with overview, key sections and penalty schedule
            sections_text = "\n\n".join([
                f"{p['section']} - {p['title']}: {p['summary']} Citizen Right: {p.get('citizenRight', '')}"
                for p in law.get("keyProvisions", [])
            ])
            penalties_text = "\n".join([
                f"Offence: {pen['offence']} | Penalty: {pen['penalty']}"
                for pen in law.get("penalties", [])
            ])
            full_statute_text = (
                f"Statute: {law['title']} ({law['shortTitle']})\n"
                f"Ministry: {law['ministry']} | Enacted: {law['commencementDate']}\n\n"
                f"Objective & Scope:\n{law['overview']}\n\n"
                f"Key Sections & Citizen Rights:\n{sections_text}\n\n"
                f"Statutory Penalties:\n{penalties_text}"
            )

            await index_document_chunks(
                doc_id=law["slug"],
                title=law["title"],
                text=full_statute_text,
                user_id="system",
                source="nyaykosh_statute",
                category=law["category"]
            )
        logger.info("[INFO] Canonical Nyaykosh statutes seeded into MongoDB Vector Store successfully.")
    except Exception as e:
        logger.warning(f"Could not auto-seed statutory RAG chunks: {e}")

