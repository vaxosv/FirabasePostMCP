from datetime import datetime, timezone

from firebase_admin import firestore

from postmcp.services.firebase import posts_collection
from postmcp.types import Post, PostCreate, PostFilter, PostUpdate
from postmcp.utils.logger import logger


def create_post(data: PostCreate) -> Post:
    doc_ref = posts_collection().document()
    now = datetime.now(timezone.utc)
    post_dict = data.model_dump()
    post_dict["created_at"] = now
    post_dict["updated_at"] = now
    doc_ref.set(post_dict)
    post = Post(id=doc_ref.id, **post_dict)
    logger.info("Created post", post_id=post.id, title=post.title)
    return post


def get_post(post_id: str) -> Post | None:
    doc = posts_collection().document(post_id).get()
    if not doc.exists:
        return None
    return Post(id=doc.id, **doc.to_dict())


def list_posts(filters: PostFilter | None = None) -> list[Post]:
    query = posts_collection().order_by("created_at", direction=firestore.Query.DESCENDING)
    if not filters:
        filters = PostFilter()
    if filters.author:
        query = query.where("author", "==", filters.author)
    if filters.published is not None:
        query = query.where("published", "==", filters.published)
    if filters.tag:
        query = query.where("tags", "array_contains", filters.tag)
    docs = query.offset(filters.offset).limit(filters.limit).stream()
    return [Post(id=d.id, **d.to_dict()) for d in docs]


def update_post(post_id: str, data: PostUpdate) -> Post | None:
    doc_ref = posts_collection().document(post_id)
    doc = doc_ref.get()
    if not doc.exists:
        return None
    update_dict = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    update_dict["updated_at"] = datetime.now(timezone.utc)
    doc_ref.update(update_dict)
    updated = doc_ref.get()
    return Post(id=updated.id, **updated.to_dict())


def delete_post(post_id: str) -> bool:
    doc_ref = posts_collection().document(post_id)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    doc_ref.delete()
    logger.info("Deleted post", post_id=post_id)
    return True
