# PostMCP — For AI Agents Working on This Codebase

## Project Overview

PostMCP is an MCP (Model Context Protocol) server built with Python+FastMCP that
lets AI agents create, read, update, and delete social news posts stored in
Firebase Firestore.

## Architecture

```
src/postmcp/
├── server.py          FastMCP instance + main()
├── config.py          Pydantic Settings from env vars
├── types.py           Pydantic models (Post, PostCreate, etc.)
├── tools/posts.py     MCP tool definitions (one `register_tools` call)
├── resources/posts.py MCP resource definitions
├── prompts/posts.py   MCP prompt templates
├── services/
│   ├── firebase.py    Firebase Admin SDK client singleton
│   └── posts.py       Business logic (CRUD operations)
└── utils/
    ├── logger.py      Structured logging to stderr
    └── errors.py      Error types
```

## Key Conventions

- All logging goes to **stderr** (`logger.py` uses `StreamHandler(sys.stderr)`)
- Tool/function signatures use **type hints** and **descriptive docstrings** (FastMCP auto-generates schemas from them)
- Business logic lives in `services/`, not in `tools/`
- Tools in `tools/posts.py` are thin wrappers that call into `services/posts.py`
- Config comes from environment variables (see `.env.example`)

## Commands

```bash
# Run the server
python -m postmcp

# Dev with inspector
npx @modelcontextprotocol/inspector python -m postmcp

# Run tests
python -m pytest

# Lint
ruff check src/

# Format
ruff format src/
```

## Dependencies

- `mcp[cli]` — MCP Python SDK with CLI extras
- `firebase-admin` — Firebase Firestore access
- `pydantic` / `pydantic-settings` — Models and config
- `httpx` — HTTP client (available if needed)
