# Architecture

## Layers

```
┌──────────────────────────────┐
│   MCP Transport (stdio)      │
├──────────────────────────────┤
│   FastMCP Server             │  ← tools/, resources/, prompts/
├──────────────────────────────┤
│   Service Layer              │  ← services/posts.py, services/firebase.py
├──────────────────────────────┤
│   Firebase Firestore         │  ← external database
└──────────────────────────────┘
```

## Data Flow

1. MCP client (e.g. Claude Desktop) sends a tool call via stdio
2. FastMCP deserializes the JSON-RPC request and routes to the registered tool
3. The tool function validates input via Pydantic models (`PostCreate`, etc.)
4. The tool calls into `services/posts.py` which handles Firestore operations
5. The result is returned as a JSON-RPC response

## Firestore Document Schema

```
posts/{doc_id}
├── title: string
├── content: string
├── author: string
├── tags: string[]
├── published: boolean
├── created_at: Timestamp
└── updated_at: Timestamp
```
