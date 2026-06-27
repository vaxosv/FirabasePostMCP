# PostMCP

An MCP (Model Context Protocol) server for managing AI-generated social news
posts in Firebase Firestore.

## Quick Start

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your Firebase project details

# Run the server
uv run postmcp
```

## Configuration

| Variable | Description |
|---|---|
| `FIREBASE_CLIENT_EMAIL` | Firebase service account email |
| `FIREBASE_PRIVATE_KEY` | Firebase service account private key |
| `FIREBASE_PROJECT_ID` | Firebase project ID |
| `POSTS_COLLECTION` | Firestore collection name (default: `AiPosts`) |
| `LOG_LEVEL` | Logging level (default: `INFO`) |

## Connect from Claude Desktop

Add to your `claude_desktop_config.json` (see `examples/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "postmcp": {
      "command": "/ABSOLUTE/PATH/TO/PostMCP/.venv/bin/python",
      "args": ["-m", "postmcp"],
      "env": {
        "FIREBASE_CLIENT_EMAIL": "your-service-account@your-project.iam.gserviceaccount.com",
        "FIREBASE_PRIVATE_KEY": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
        "FIREBASE_PROJECT_ID": "your-project-id"
      }
    }
  }
}
```

## Connect from Hermes Agent

Add to your `~/.hermes/config.yaml` (see `examples/hermes_config.yaml`):

```yaml
mcp_servers:
  postmcp:
    command: "/ABSOLUTE/PATH/TO/PostMCP/.venv/bin/python"
    args: ["-m", "postmcp"]
    env:
      FIREBASE_CLIENT_EMAIL: "your-service-account@..."
      FIREBASE_PRIVATE_KEY: "-----BEGIN PRIVATE KEY-----\n..."
      FIREBASE_PROJECT_ID: "your-project-id"
```

## Tools

- `create_post_tool` — Create a new post
- `get_post_tool` — Get a post by ID
- `list_posts_tool` — List posts with filters
- `update_post_tool` — Update a post
- `delete_post_tool` — Delete a post

See `AGENTS.md` for full documentation for AI agents using this server.
See `CLAUDE.md` for development conventions.

## Project Structure

```
src/postmcp/
├── server.py          Entry point and MCP registration
├── config.py          Configuration from env vars
├── types.py           Pydantic models
├── tools/             MCP tool implementations
├── resources/         MCP resource providers
├── prompts/           MCP prompt templates
├── services/          Business logic layer
└── utils/             Logging, errors
```
