# PostMCP

An MCP (Model Context Protocol) server for managing AI-generated social news
posts in Firebase Firestore (`AiPosts` collection).

## Quick Start

```bash
# Install dependencies
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your Firebase project details

# Run the server
python -m postmcp
```

> **`.env` is optional.** If you only launch PostMCP through an MCP client
> (Claude Desktop, Hermes Agent), pass the env vars in the client config
> instead. `.env` is only needed when running `python -m postmcp` directly
> in the terminal (e.g., for testing).

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

- `create_post_tool` — Create a new post with title, content, description, slug, images, categories, tags
- `get_post_tool` — Get a post by ID
- `list_posts_tool` — List posts filtered by category or tag
- `update_post_tool` — Update any field on a post
- `delete_post_tool` — Delete a post by ID

## Firestore Document Schema

```
AiPosts/{doc_id}
├── title: string
├── content: string (HTML)
├── description: string
├── slug: string
├── main_img: string (URL)
├── main_img_path: string (storage path)
├── category_ids: string[]
├── tags: string[]
├── views30: number
├── published: boolean
└── created_at: string (ISO 8601)
```

See `AGENTS.md` for full tool documentation for AI agents using this server.
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
