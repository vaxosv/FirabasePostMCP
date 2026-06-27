from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP):
    @mcp.prompt()
    async def write_news_post(topic: str, tone: str = "informative") -> str:
        """Write a news-style social post about a given topic."""
        return (
            f"You are a social news writer. Write a post about '{topic}' "
            f"in a {tone} tone. Use the `create_post_tool` to save the result "
            f"once you are satisfied with it."
        )

    @mcp.prompt()
    async def summarize_and_post(post_id: str) -> str:
        """Summarize an existing post and create a new one based on it."""
        return (
            f"Read the post with ID `{post_id}` using `get_post_tool`, "
            f"then write a concise summary version and save it as a new post "
            f"via `create_post_tool`."
        )
