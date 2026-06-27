from mcp.server.fastmcp import FastMCP

from postmcp.services.posts import create_post, delete_post, get_post, list_posts, update_post
from postmcp.types import PostCreate, PostFilter, PostUpdate


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def create_post_tool(
        title: str,
        content: str,
        description: str,
        slug: str = "",
        main_img: str = "",
        main_img_path: str = "",
        category_ids: list[str] | None = None,
        tags: list[str] | None = None,
        views30: int = 0,
        published: bool = False,
    ) -> str:
        """Create a new social news post in Firebase.

        Args:
            title: Post title (max 200 characters)
            content: Post body content (HTML)
            description: Short description or blurb (max 500 chars)
            slug: URL slug (auto-generated from title if empty)
            main_img: Main image URL
            main_img_path: Main image storage path
            category_ids: List of category document IDs
            tags: Optional list of tags
            views30: Views in last 30 days (default 0)
            published: Whether the post is published (default false)
        """
        data = PostCreate(
            title=title,
            content=content,
            description=description,
            slug=slug,
            main_img=main_img,
            main_img_path=main_img_path,
            category_ids=category_ids or [],
            tags=tags or [],
            views30=views30,
            published=published,
        )
        post = create_post(data)
        return f"Created post **{post.id}**: {post.title}"

    @mcp.tool()
    async def get_post_tool(post_id: str) -> str:
        """Get a single post by its ID.

        Args:
            post_id: The Firestore document ID of the post
        """
        post = get_post(post_id)
        if not post:
            return f"Post `{post_id}` not found."
        lines = [
            f"**ID:** {post.id}",
            f"**Title:** {post.title}",
            f"**Description:** {post.description}",
            f"**Slug:** {post.slug}",
            f"**Tags:** {', '.join(post.tags) if post.tags else 'none'}",
            f"**Categories:** {', '.join(post.category_ids) if post.category_ids else 'none'}",
            f"**Views (30d):** {post.views30}",
            f"**Created:** {post.created_at}",
            f"**Content:**\n{post.content}",
        ]
        return "\n".join(lines)

    @mcp.tool()
    async def list_posts_tool(
        category_id: str | None = None,
        tag: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> str:
        """List posts from Firebase with optional filters.

        Args:
            category_id: Filter by category document ID
            tag: Filter by tag
            limit: Max results (1-100, default 20)
            offset: Pagination offset (default 0)
        """
        filters = PostFilter(
            category_id=category_id,
            tag=tag,
            limit=limit,
            offset=offset,
        )
        posts = list_posts(filters)
        if not posts:
            return "No posts found matching the given filters."
        lines = [f"Found {len(posts)} posts:"]
        for p in posts:
            lines.append(f"- **{p.id}**: {p.title} ({p.slug})")
        return "\n".join(lines)

    @mcp.tool()
    async def update_post_tool(
        post_id: str,
        title: str | None = None,
        content: str | None = None,
        description: str | None = None,
        slug: str | None = None,
        main_img: str | None = None,
        main_img_path: str | None = None,
        category_ids: list[str] | None = None,
        tags: list[str] | None = None,
        views30: int | None = None,
        published: bool | None = None,
    ) -> str:
        """Update an existing post.

        Args:
            post_id: The Firestore document ID of the post
            title: New title (optional)
            content: New content (optional)
            description: New description (optional)
            slug: New URL slug (optional)
            main_img: New main image URL (optional)
            main_img_path: New image storage path (optional)
            category_ids: New category IDs list (optional)
            tags: New tags list (optional)
            views30: New views count (optional)
            published: New published status (optional)
        """
        update = PostUpdate(
            title=title,
            content=content,
            description=description,
            slug=slug,
            main_img=main_img,
            main_img_path=main_img_path,
            category_ids=category_ids,
            tags=tags,
            published=published,
            views30=views30,
        )
        post = update_post(post_id, update)
        if not post:
            return f"Post `{post_id}` not found."
        return f"Updated post **{post.id}**: {post.title}"

    @mcp.tool()
    async def delete_post_tool(post_id: str) -> str:
        """Delete a post by its ID.

        Args:
            post_id: The Firestore document ID of the post
        """
        if delete_post(post_id):
            return f"Deleted post `{post_id}`."
        return f"Post `{post_id}` not found."
