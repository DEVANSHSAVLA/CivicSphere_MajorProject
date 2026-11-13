import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, close_db, get_database
from app.routers import auth, chat, documents, schemes, legal, civic_knowledge, feedback

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize MongoDB connection, indexes, and seed data
    await init_db()
    # Auto-seed canonical statutes into MongoDB vector store for RAG asynchronously
    try:
        from app.services.rag_service import seed_canonical_statutes_for_rag
        asyncio.create_task(seed_canonical_statutes_for_rag())
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Could not initiate RAG statute seeding: {e}")
    yield
    # Graceful shutdown
    await close_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CivicSphere AI Evidence-Grounded Backend with MongoDB and Secure HTTP-Only Cookie JWT Authentication",
    lifespan=lifespan
)

# CORS Configuration
# Important: allow_credentials=True requires explicit origins (cannot be "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

# Register routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(schemes.router)
app.include_router(legal.router)
app.include_router(civic_knowledge.router)
app.include_router(feedback.router)

@app.get("/")
async def root():
    return {
        "platform": "CivicSphere AI",
        "service": "Civic Intelligence API",
        "database": "MongoDB 8.3",
        "database_name": settings.MONGODB_DB_NAME,
        "auth_method": "JWT with HTTP-Only Cookies",
        "status": "operational"
    }

@app.get("/api/health")
async def health_check():
    db_status = "connected"
    try:
        db = get_database()
        await db.command("ping")
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        
    return {
        "status": "healthy",
        "database": {
            "engine": "MongoDB",
            "database_name": settings.MONGODB_DB_NAME,
            "status": db_status
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
