import pytest
from mcp.server.fastmcp import FastMCP

from postmcp.tools.posts import register_tools


@pytest.fixture
def mcp():
    server = FastMCP("test")
    register_tools(server)
    return server
