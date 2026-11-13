from fastapi import Request, HTTPException, status
from app.config import settings
from app.security import decode_token
from app.database import get_user_by_id

async def get_current_user(request: Request) -> dict:
    """
    Extracts and validates JWT access token from HTTP-only cookie or Authorization header.
    Strictly verifies that the token type is 'access' to prevent refresh token abuse.
    Queries MongoDB asynchronously for the authenticated user document.
    """
    token = request.cookies.get(settings.ACCESS_COOKIE_NAME)
    if not token and "authorization" in request.headers:
        auth_header = request.headers.get("authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. No session cookie found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(token)
    
    # Strictly require valid token with type 'access'
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid access token. Please refresh session.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )
        
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with this session no longer exists.",
        )
        
    return user
