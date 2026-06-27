from mcp.server.fastmcp import FastMCP

from postmcp.services.posts import create_post, delete_post, get_post, list_posts, update_post
from postmcp.types import PostCreate, PostFilter, PostUpdate


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def create_post_tool(
        title: str,
        content: str,
        author: str = "AI",
        tags: list[str] | None = None,
        published: bool = False,
    ) -> str:
        """Create a new social news post in Firebase.

        Args:
            title: Post title (max 200 characters)
            content: Post body content
            author: Author name (defaults to AI)
            tags: Optional list of tags
            published: Whether the post is published immediately
        """
        data = PostCreate(
            title=title,
            content=content,
            author=author,
            tags=tags or [],
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
            f"**Author:** {post.author}",
            f"**Published:** {post.published}",
            f"**Tags:** {', '.join(post.tags) if post.tags else 'none'}",
            f"**Created:** {post.created_at.isoformat()}",
            f"**Content:**\n{post.content}",
        ]
        return "\n".join(lines)

    @mcp.tool()
    async def list_posts_tool(
        author: str | None = None,
        tag: str | None = None,
        published: bool | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> str:
        """List posts from Firebase with optional filters.

        Args:
            author: Filter by author name
            tag: Filter by tag
            published: Filter by published status
            limit: Max results (1-100, default 20)
            offset: Pagination offset (default 0)
        """
        filters = PostFilter(
            author=author,
            tag=tag,
            published=published,
            limit=limit,
            offset=offset,
        )
        posts = list_posts(filters)
        if not posts:
            return "No posts found matching the given filters."
        lines = [f"Found {len(posts)} posts:"]
        for p in posts:
            status = "published" if p.published else "draft"
            lines.append(f"- **{p.id}**: {p.title} (by {p.author}, {status})")
        return "\n".join(lines)

    @mcp.tool()
    async def update_post_tool(
        post_id: str,
        title: str | None = None,
        content: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        published: bool | None = None,
    ) -> str:
        """Update an existing post.

        Args:
            post_id: The Firestore document ID of the post
            title: New title (optional)
            content: New content (optional)
            author: New author (optional)
            tags: New tags list (optional)
            published: New published status (optional)
        """
        update = PostUpdate(
            title=title,
            content=content,
            author=author,
            tags=tags,
            published=published,
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
