from mcp.server.fastmcp import FastMCP

from postmcp.services.posts import get_post, list_posts
from postmcp.types import PostFilter


def register_resources(mcp: FastMCP):
    @mcp.resource("postmcp://posts/{post_id}")
    async def post_by_id(post_id: str) -> str:
        """Get a post document by its Firestore ID."""
        post = get_post(post_id)
        if not post:
            return f"Post `{post_id}` not found."
        return post.model_dump_json(indent=2)

    @mcp.resource("postmcp://posts/recent")
    async def recent_posts() -> str:
        """Get the 10 most recent posts."""
        posts = list_posts(PostFilter(limit=10))
        return f"[{','.join(p.model_dump_json() for p in posts)}]"
