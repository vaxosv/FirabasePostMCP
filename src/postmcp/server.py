from mcp.server.fastmcp import FastMCP

from postmcp.prompts.posts import register_prompts
from postmcp.resources.posts import register_resources
from postmcp.tools.posts import register_tools
from postmcp.utils.logger import logger

mcp = FastMCP("PostMCP")


def main():
    logger.info("Starting PostMCP server")

    register_tools(mcp)
    register_resources(mcp)
    register_prompts(mcp)

    mcp.run(transport="stdio")
