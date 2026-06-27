from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, description="Post body content")
    author: str = Field(default="AI", max_length=100)
    tags: list[str] = Field(default_factory=list)
    published: bool = False


class Post(PostCreate):
    id: str
    created_at: datetime
    updated_at: datetime


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, max_length=100)
    tags: Optional[list[str]] = None
    published: Optional[bool] = None


class PostFilter(BaseModel):
    author: Optional[str] = None
    tag: Optional[str] = None
    published: Optional[bool] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
