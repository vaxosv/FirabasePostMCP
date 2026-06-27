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

1. MCP client (e.g. Claude Desktop, Hermes Agent) sends a tool call via stdio
2. FastMCP deserializes the JSON-RPC request and routes to the registered tool
3. The tool function validates input via Pydantic models (`PostCreate`, etc.)
4. The tool calls into `services/posts.py` which handles Firestore operations
5. The result is returned as a JSON-RPC response

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
└── created_at: string (ISO 8601)
```

## Auth

PostMCP uses Firebase Admin SDK with service account credentials passed via
environment variables (`FIREBASE_CLIENT_EMAIL`, `FIREBASE_PRIVATE_KEY`,
`FIREBASE_PROJECT_ID`). No file-based auth.
