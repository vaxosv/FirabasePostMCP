from postmcp.server import mcp


def test_server_has_name():
    assert mcp.name == "PostMCP"
