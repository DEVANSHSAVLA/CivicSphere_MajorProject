import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from server root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings:
    PROJECT_NAME: str = "CivicSphere AI API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", "civicsphere_super_secret_jwt_key_2026_evidence_grounded_ai_platform"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Cookie security configuration: in production, force secure cookies
    _is_dev = ENVIRONMENT.lower() in ("development", "dev", "local")
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "False" if _is_dev else "True").lower() in ("true", "1", "yes")
    COOKIE_SAMESITE: str = os.getenv("COOKIE_SAMESITE", "none" if not _is_dev else "lax")
    COOKIE_PATH: str = os.getenv("COOKIE_PATH", "/")
    
    # Cookie keys
    ACCESS_COOKIE_NAME: str = "access_token"
    REFRESH_COOKIE_NAME: str = "refresh_token"
    
    # Allowed CORS Origins (include local vite ports & deployed Vercel domains)
    _default_origins = (
        "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174,"
        "https://civicsphere-teal.vercel.app,https://client-ruddy-one-70.vercel.app"
    )
    _origins = os.getenv("ALLOWED_ORIGINS", _default_origins)
    ALLOWED_ORIGINS: list = [origin.strip() for origin in _origins.split(",") if origin.strip()]
    
    # MongoDB Settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "civicsphere")

    # Google Gemini AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "49632315444-rgquob9l21btkc2oojcim59h4sddovt1.apps.googleusercontent.com")

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")
    CLOUDINARY_URL: str = os.getenv("CLOUDINARY_URL", "")

settings = Settings()
