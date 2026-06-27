import firebase_admin
from firebase_admin import credentials, firestore

from postmcp.config import settings
from postmcp.utils.logger import logger

_db = None


def get_db():
    global _db
    if _db is None:
        cred = credentials.Certificate(
            {
                "type": "service_account",
                "client_email": settings.firebase_client_email,
                "private_key": settings.firebase_private_key.replace("\\n", "\n"),
                "project_id": settings.firebase_project_id,
            }
        )
        firebase_admin.initialize_app(cred, {"projectId": settings.firebase_project_id})
        _db = firestore.client()
        logger.info("Firebase Firestore client initialized")
    return _db


def posts_collection():
    return get_db().collection(settings.posts_collection)
