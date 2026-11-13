import logging
import os
import re
import cloudinary
import cloudinary.uploader
from app.config import settings

logger = logging.getLogger(__name__)

_is_configured = False

def is_cloudinary_configured() -> bool:
    """Checks whether valid Cloudinary credentials have been provided."""
    if settings.CLOUDINARY_URL and settings.CLOUDINARY_URL.startswith("cloudinary://"):
        return True
    return bool(
        settings.CLOUDINARY_CLOUD_NAME
        and settings.CLOUDINARY_API_KEY
        and settings.CLOUDINARY_API_SECRET
    )

def _init_cloudinary():
    """Initializes Cloudinary configuration singleton."""
    global _is_configured
    if _is_configured:
        return True

    if not is_cloudinary_configured():
        return False

    try:
        if settings.CLOUDINARY_URL:
            cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL)
        else:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True,
            )
        _is_configured = True
        logger.info("[INFO] Cloudinary CDN configured successfully.")
        return True
    except Exception as e:
        logger.warning(f"Failed to initialize Cloudinary: {e}")
        return False

def sanitize_filename(filename: str) -> str:
    """Removes special characters to ensure valid Cloudinary public_ids."""
    name, ext = os.path.splitext(filename)
    clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name)[:50]
    return f"{clean_name}{ext}"

def upload_document_to_cloudinary(
    file_bytes: bytes,
    filename: str,
    user_id: str,
) -> dict:
    """
    Uploads raw PDF, DOCX, or TXT document bytes to Cloudinary CDN.
    Preserves exact byte structure and returns global HTTPS CDN download link.
    """
    if not _init_cloudinary():
        logger.info("Cloudinary not configured. Skipping CDN file upload.")
        return {
            "secure_url": "",
            "public_id": "",
            "storage": "local_database_only",
        }

    try:
        clean_name = sanitize_filename(filename)
        public_id = f"civicsphere/documents/{user_id}/{clean_name}"
        
        # resource_type="raw" ensures exact byte preservation for PDF and DOCX
        response = cloudinary.uploader.upload(
            file_bytes,
            public_id=public_id,
            resource_type="raw",
            overwrite=True,
            use_filename=True,
            unique_filename=False,
        )

        return {
            "secure_url": response.get("secure_url", ""),
            "public_id": response.get("public_id", ""),
            "storage": "cloudinary",
        }
    except Exception as e:
        logger.error(f"Cloudinary document upload failed: {e}")
        return {
            "secure_url": "",
            "public_id": "",
            "storage": "error",
            "error": str(e),
        }

def upload_avatar_to_cloudinary(
    file_bytes: bytes,
    user_id: str,
) -> dict:
    """
    Uploads user avatar image to Cloudinary with automatic face-detection cropping,
    web-optimized compression, and square dimensions (300x300).
    """
    if not _init_cloudinary():
        logger.info("Cloudinary not configured. Skipping avatar upload.")
        return {
            "secure_url": "",
            "public_id": "",
            "storage": "unconfigured",
        }

    try:
        public_id = f"civicsphere/avatars/user_{user_id}"
        
        response = cloudinary.uploader.upload(
            file_bytes,
            public_id=public_id,
            resource_type="image",
            overwrite=True,
            transformation=[
                {"width": 300, "height": 300, "crop": "fill", "gravity": "face"},
                {"fetch_format": "auto", "quality": "auto"},
            ],
        )

        return {
            "secure_url": response.get("secure_url", ""),
            "public_id": response.get("public_id", ""),
            "storage": "cloudinary",
        }
    except Exception as e:
        logger.error(f"Cloudinary avatar upload failed: {e}")
        return {
            "secure_url": "",
            "public_id": "",
            "storage": "error",
            "error": str(e),
        }

def delete_cloudinary_asset(public_id: str, resource_type: str = "raw") -> bool:
    """Deletes an asset from Cloudinary when deleted from CivicSphere."""
    if not _init_cloudinary() or not public_id:
        return False

    try:
        cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return True
    except Exception as e:
        logger.warning(f"Error removing asset {public_id} from Cloudinary: {e}")
        return False

