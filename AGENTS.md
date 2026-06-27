# PostMCP — For AI Agents Using This Server

## What Is PostMCP?

PostMCP is an MCP (Model Context Protocol) server that provides tools to manage
social news posts in Firebase Firestore (`AiPosts` collection). It is designed
for AI agents to create, retrieve, update, and delete posts.

## Available Tools

### `create_post_tool`
Create a new social news post.

Arguments:
- `title` (string, required) — Post title (max 200 chars)
- `content` (string, required) — Post body content (HTML)
- `description` (string, required) — Short description/blurb (max 500 chars)
- `slug` (string, optional) — URL slug (auto-generated from title if empty)
- `main_img` (string, optional) — Main image URL
- `main_img_path` (string, optional) — Main image storage path
- `category_ids` (array of strings, optional) — Category document IDs
- `tags` (array of strings, optional) — List of tags
- `views30` (integer, optional, default: 0) — Views in last 30 days
- `published` (boolean, optional, default: false) — Whether the post is published

### `get_post_tool`
Get a single post by its Firestore document ID.

Arguments:
- `post_id` (string, required) — Document ID

### `list_posts_tool`
List posts with optional filters.

Arguments:
- `category_id` (string, optional) — Filter by category document ID
- `tag` (string, optional) — Filter by tag
- `limit` (integer, optional, default: 20, max: 100) — Max results
- `offset` (integer, optional, default: 0) — Pagination offset

### `update_post_tool`
Update fields on an existing post.

Arguments:
- `post_id` (string, required) — Document ID
- `title`, `content`, `description`, `slug`, `main_img`, `main_img_path`, `category_ids`, `tags`, `views30`, `published` (all optional)

### `delete_post_tool`
Delete a post by its ID.

Arguments:
- `post_id` (string, required) — Document ID

## Available Resources

- `postmcp://posts/{post_id}` — Full post JSON
- `postmcp://posts/recent` — 10 most recent posts as JSON array

## Available Prompts

- `write_news_post(topic, tone)` — Guides the agent to write and save a news post
- `summarize_and_post(post_id)` — Summarize an existing post and create a new one

## Client Configuration

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "postmcp": {
      "command": "/ABSOLUTE/PATH/TO/PostMCP/.venv/bin/python",
      "args": ["-m", "postmcp"],
      "env": {
        "FIREBASE_CLIENT_EMAIL": "your@email.com",
        "FIREBASE_PRIVATE_KEY": "-----BEGIN PRIVATE KEY-----\n...",
        "FIREBASE_PROJECT_ID": "your-project-id"
      }
    }
  }
}
```

### Hermes Agent (`~/.hermes/config.yaml`)

```yaml
mcp_servers:
  postmcp:
    command: "/ABSOLUTE/PATH/TO/PostMCP/.venv/bin/python"
    args: ["-m", "postmcp"]
    env:
      FIREBASE_CLIENT_EMAIL: "your@email.com"
      FIREBASE_PRIVATE_KEY: "-----BEGIN PRIVATE KEY-----\n..."
      FIREBASE_PROJECT_ID: "your-project-id"
```

## Example Workflows

1. **Generate and save a post:** Use `write_news_post` prompt → draft content → call `create_post_tool` with title, content, description, and optional tags
2. **Browse recent posts:** Read `postmcp://posts/recent` resource → call `get_post_tool` on interesting ones
3. **Find posts by category:** `list_posts_tool(category_id="abc123")` → review → `update_post_tool` to edit fields
