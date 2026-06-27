from typing import Optional

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, description="Post body content (HTML)")
    description: str = Field(..., min_length=1, max_length=500, description="Short post blurb")
    slug: str = Field(default="", max_length=300, description="URL slug (auto-generated if empty)")
    main_img: str = Field(default="", description="Main image URL")
    main_img_path: str = Field(default="", description="Main image storage path")
    category_ids: list[str] = Field(default_factory=list, description="Category document IDs")
    tags: list[str] = Field(default_factory=list)
    views30: int = Field(default=0, ge=0, description="Views in last 30 days")
    published: bool = False


class Post(PostCreate):
    id: str
    created_at: str


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    slug: Optional[str] = Field(None, max_length=300)
    main_img: Optional[str] = None
    main_img_path: Optional[str] = None
    category_ids: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    views30: Optional[int] = Field(None, ge=0)
    published: Optional[bool] = None


class PostFilter(BaseModel):
    category_id: Optional[str] = None
    tag: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
