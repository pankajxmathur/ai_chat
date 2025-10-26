# AI MCP Chat - Architecture & Visual Reference Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER (Vue 3)                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     Chat Interface                           │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │  │
│  │  │  Sidebar   │ │  Messages  │ │   Input Area           │  │  │
│  │  │            │ │            │ │   + File Upload        │  │  │
│  │  │ • Thread   │ │ • Text     │ │   + Model Select       │  │  │
│  │  │   List     │ │ • Code     │ │   + Settings           │  │  │
│  │  │ • Search   │ │ • Images   │ └────────────────────────┘  │  │
│  │  │ • New Chat │ │ • Markdown │                             │  │
│  │  └────────────┘ └────────────┘                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────────────────────┐  │
│  │ Pinia Stores │ │ Composables  │ │ Services                  │  │
│  │              │ │              │ │                           │  │
│  │ • chatStore  │ │ • useChat    │ │ • chatService.js          │  │
│  │ • userStore  │ │ • useFile    │ │ • fileService.js          │  │
│  │ • fileStore  │ │ • useSocket  │ │ • connectorService.js     │  │
│  │ • uiStore    │ │ • useMarkdown│ │ • websocketService.js     │  │
│  └──────────────┘ └──────────────┘ └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
          REST API  │     WebSocket │      File     │
                    │               │     Upload    │
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FRAPPE BACKEND (Python)                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                             │  │
│  │  • /api/method/ai_mcp_chat.api.chat.* (REST)               │  │
│  │  • /socket.io (WebSocket streaming)                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Services Layer                            │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │  │
│  │  │ Chat Service   │  │ LLM Service    │  │ MCP Service    │ │  │
│  │  │                │  │                │  │                │ │  │
│  │  │ • Thread CRUD  │  │ • Multi-       │  │ • Connector    │ │  │
│  │  │ • Message ops  │  │   provider     │  │   management   │ │  │
│  │  │ • History mgmt │  │ • Streaming    │  │ • Tool         │ │  │
│  │  │ • Search       │  │ • Token count  │  │   execution    │ │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │  │
│  │  │ File Service   │  │ Streaming Svc  │  │ Tool Executor  │ │  │
│  │  │                │  │                │  │                │ │  │
│  │  │ • Upload       │  │ • Stream mgmt  │  │ • Execute MCP  │ │  │
│  │  │ • Parse        │  │ • Event queue  │  │   tools        │ │  │
│  │  │ • Validate     │  │ • Buffer mgmt  │  │ • Handle I/O   │ │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Frappe DocTypes                             │  │
│  │  • AI Chat Thread          • LLM Model Configuration         │  │
│  │  • AI Chat Message         • MCP Connector                   │  │
│  │  • Chat Attachment         • User Preferences               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │  MariaDB     │  │    Redis     │  │    RQ Queue  │
        │ (Data Store) │  │ (Cache/Sess) │  │  (Background)│
        └──────────────┘  └──────────────┘  └──────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │  OpenAI API  │  │ Anthropic    │  │  Google AI   │
        │  (GPT-4, etc)│  │  (Claude)    │  │  (Gemini)    │
        └──────────────┘  └──────────────┘  └──────────────┘
                                    │
                                    ▼
        ┌──────────────────────────────────────┐
        │    MCP Servers (External Tools)     │
        │ • Code execution                    │
        │ • Database queries                  │
        │ • Web search                        │
        │ • Custom integrations               │
        └──────────────────────────────────────┘
```

---

## Data Flow Diagrams

### User Message Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ User Types Message in Chat Input                                 │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Input validation │
                  │ (Vue component)  │
                  └──────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │ Add to local messages array │
              │ (Pinia store update)        │
              └─────────────────────────────┘
                            │
                            ▼
          ┌────────────────────────────────────┐
          │ POST /api/method/chat.send_message │
          │ (with threadId, content)           │
          └────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────┐
        │ Backend: save_message() API endpoint    │
        │ 1. Validate thread access (permissions) │
        │ 2. Create AI Chat Message record        │
        │ 3. Insert into database                 │
        │ 4. Trigger response generation          │
        └──────────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────┐
        │ Backend: Chat Service                   │
        │ 1. Get conversation history             │
        │ 2. Format messages for LLM              │
        │ 3. Call LLM API (OpenAI/Anthropic)     │
        │ 4. Stream response chunks               │
        └──────────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────┐
        │ LLM Streaming (via WebSocket)           │
        │ • Token 1: "Hello"                      │
        │ • Token 2: ","                          │
        │ • Token 3: " how"                       │
        │ • Token 4: " can I help?"               │
        └──────────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────┐
        │ Frontend: Receive stream chunks         │
        │ 1. WebSocket message received           │
        │ 2. Accumulate content                   │
        │ 3. Update UI in real-time               │
        │ 4. Show streaming indicator             │
        └──────────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────┐
        │ Backend: Stream Complete                │
        │ 1. Save full response to database        │
        │ 2. Update token count                   │
        │ 3. Calculate cost                       │
        │ 4. Send completion event                │
        └──────────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────┐
        │ Frontend: Streaming Complete            │
        │ 1. Hide typing indicator                │
        │ 2. Mark message as complete             │
        │ 3. Scroll to bottom                     │
        │ 4. Ready for next message               │
        └──────────────────────────────────────────┘
```

### File Upload & Processing Flow

```
┌─────────────────────────────────────────┐
│ User selects file (drag-drop or click)  │
└─────────────────────────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Validate file type   │
    │ Check file size      │
    │ Scan for viruses     │
    └──────────────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Show upload progress │
    │ bar in UI            │
    └──────────────────────┘
              │
              ▼
  ┌──────────────────────────────┐
  │ POST /api/method/file.upload │
  │ FormData with file           │
  └──────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Backend: Process file                │
  │ 1. Save to /files directory          │
  │ 2. Extract text (if PDF/DOCX)       │
  │ 3. Generate preview thumbnail       │
  │ 4. Create Chat Attachment record    │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Return file metadata                 │
  │ {id, name, size, type, preview}     │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Frontend: Add to attachment list     │
  │ Show file in input area              │
  │ (User can remove before sending)     │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ User sends message with attachments  │
  │ Attachments IDs sent with message    │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Backend: Include file content        │
  │ in LLM context                       │
  │ LLM can "see" and process file       │
  └──────────────────────────────────────┘
```

### MCP Tool Execution Flow

```
┌──────────────────────────────────┐
│ LLM Decides to call a tool       │
│ (Tool calling capability)        │
└──────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Backend receives tool_call           │
  │ {tool_name: "search_web",            │
  │  args: {query: "Vue 3 tutorial"}}    │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Tool Executor service                │
  │ 1. Validate tool exists              │
  │ 2. Validate arguments                │
  │ 3. Find MCP connector                │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Connect to MCP Server                │
  │ stdio/tcp/http based on config       │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Execute tool                         │
  │ Get results back from MCP server     │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Save tool_call and tool_results      │
  │ to AI Chat Message                   │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ Return tool results to LLM           │
  │ in conversation context              │
  └──────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────┐
  │ LLM generates response               │
  │ based on tool results                │
  │ (e.g., "Here's what I found...")     │
  └──────────────────────────────────────┘
```

---

## Component Communication Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Components                          │
│                                                                  │
│  ┌──────────────────┐            ┌───────────────────────────┐ │
│  │ ChatInterface    │ ◄─────────► │ ConversationSidebar      │ │
│  │ (Main Container) │            │ (Thread List & Search)   │ │
│  └─────────┬────────┘            └───────────────────────────┘ │
│            │                                                     │
│            ├─► MessageList         ├─► MessageItem             │
│            │   ├─► MessageContent  │   ├─► CodeBlock          │
│            │   └─► Markdown        │   └─► MessageActions     │
│            │                                                     │
│            ├─► InputArea           ├─► FileUpload            │
│            │   └─► Attachments     └─► AttachmentList        │
│            │                                                     │
│            └─► ModelSelector       ├─► UserPreferences       │
│                └─► Settings        └─► ProviderSettings      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼──────────┐               ┌──────────▼──────┐
│  Pinia Stores    │               │  API Services   │
│                  │               │                 │
│ • chatStore      │               │ • chatService   │
│ • messageStore   │               │ • fileService   │
│ • userStore      │               │ • llmService    │
│ • fileStore      │               │ • authService   │
│ • uiStore        │               │ • websocketSvc  │
└───────┬──────────┘               └────────┬────────┘
        │                                   │
        └──────────────┬────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────────┐
        │   Frappe Backend (Python)        │
        │                                  │
        │   REST API Endpoints             │
        │   WebSocket Events               │
        │   Business Logic Services        │
        │   Database Operations            │
        └──────────────────────────────────┘
```

---

## Database Relationship Diagram

```
┌──────────────────────────┐
│   User (Frappe)          │
│   - user_id (PK)         │
│   - email                │
│   - name                 │
└──────────┬───────────────┘
           │ (1:many)
           │ owns
           │
           ▼
┌──────────────────────────────────┐
│   AI Chat Thread                 │
│   - name (PK)                    │
│   - thread_id (unique)           │
│   - user (FK → User)             │
│   - title                        │
│   - model_used (FK → LLM Model)  │
│   - system_prompt                │
│   - temperature, max_tokens      │
│   - token_count, estimated_cost  │
└──────────┬───────────────────────┘
           │ (1:many)
           │ contains
           │
           ▼
┌──────────────────────────────────┐          ┌──────────────────────────────┐
│   AI Chat Message                │          │   LLM Model Configuration    │
│   - name (PK)                    │          │   - name (PK)                │
│   - thread (FK → Thread)         │◄─────────│   - model_name (unique)      │
│   - role (user/assistant/tool)   │ many:1   │   - provider                 │
│   - content                      │          │   - model_identifier         │
│   - tool_calls (JSON)            │          │   - api_key_field            │
│   - tool_results (JSON)          │          │   - cost_per_1k_input/output │
│   - tokens_used                  │          │   - supports_streaming, tools │
│   - timestamp                    │          └──────────────────────────────┘
└──────────┬───────────────────────┘
           │ (1:many)
           │ has
           │
           ▼
┌──────────────────────────────────┐
│   Chat Attachment                │
│   - name (PK)                    │
│   - parent (FK → Message)        │
│   - file_name                    │
│   - file_path                    │
│   - file_type                    │
│   - is_processed                 │
│   - extracted_content            │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│   MCP Connector                  │
│   - name (PK)                    │
│   - connector_name               │
│   - connector_type (stdio/tcp)   │
│   - host, port                   │
│   - command                      │
│   - is_active                    │
│   - connection_status            │
│   - tools_available              │
└──────────┬───────────────────────┘
           │ (1:many)
           │ provides
           │
           ▼
┌──────────────────────────────────┐
│   MCP Tool                       │
│   - name (PK)                    │
│   - connector (FK → Connector)   │
│   - tool_name                    │
│   - description                  │
│   - parameters (JSON)            │
│   - input_schema                 │
│   - output_schema                │
└──────────────────────────────────┘


┌──────────────────────────────────┐
│   User Preferences               │
│   - name (PK)                    │
│   - user (FK → User) [unique]    │
│   - default_model                │
│   - theme (light/dark)           │
│   - auto_save_drafts             │
│   - default_temperature          │
│   - metadata (JSON)              │
└──────────────────────────────────┘
```

---

## Request/Response Flow for Key Operations

### Create Thread Request

```
Frontend Request:
─────────────────────────────────────────────────────
POST /api/method/ai_mcp_chat.api.chat.create_chat_thread
Content-Type: application/json

{
  "title": "Quantum Computing",
  "system_prompt": "You are a quantum physics expert",
  "model": "gpt-4"
}

Backend Processing:
─────────────────────────────────────────────────────
1. Validate authentication
2. Check user permissions (implicit via Frappe)
3. Validate input (title not empty, model exists)
4. Generate UUID for thread_id
5. Create AI Chat Thread document
6. Insert into database
7. Commit transaction

Response (Success):
─────────────────────────────────────────────────────
200 OK
{
  "message": {
    "success": true,
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "docname": "AI Chat Thread-001",
    "created_at": "2025-10-26T10:30:00.000Z"
  }
}

Response (Error):
─────────────────────────────────────────────────────
400 Bad Request / 500 Internal Server Error
{
  "message": "No active LLM model configured",
  "exc": "frappe.exceptions.ValidationError"
}
```

### Send Message Request

```
Frontend Request:
─────────────────────────────────────────────────────
POST /api/method/ai_mcp_chat.api.chat.send_message
Content-Type: application/json

{
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "Explain quantum entanglement",
  "attachments": ["file_123.pdf"],
  "stream": true
}

Backend Processing (Stream):
─────────────────────────────────────────────────────
1. Validate thread access (user ownership)
2. Create user message record
3. Get conversation history
4. Prepare LLM context
5. Call LLM API with streaming enabled
6. For each token:
   - Stream via WebSocket
   - Update frontend in real-time
7. Accumulate full response
8. Save assistant message to database
9. Update token counters
10. Send completion signal

WebSocket Stream:
─────────────────────────────────────────────────────
Message 1: {type: "start", tokens_so_far: 0}
Message 2: {type: "token", content: "Quantum", tokens_so_far: 1}
Message 3: {type: "token", content: " entanglement", tokens_so_far: 2}
...
Message N: {type: "complete", total_tokens: 47}

Response (Non-streaming):
─────────────────────────────────────────────────────
200 OK
{
  "message": {
    "success": true,
    "user_message_id": "msg_123",
    "response": {
      "success": true,
      "content": "Quantum entanglement is...",
      "message_id": "msg_124"
    }
  }
}
```

---

## Session Lifecycle

```
User Opens App
     │
     ▼
┌─────────────────────────────┐
│ Frappe Auth Check           │
│ - Read session cookie       │
│ - Validate JWT token        │
│ - Load user permissions     │
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ Load Initial Data           │
│ - GET /api/method/list_chat_threads
│ - GET /api/method/get_available_models
│ - Load user preferences     │
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ Initialize Pinia Stores     │
│ - chatStore.setThreads()    │
│ - userStore.setUser()       │
│ - settingsStore.load()      │
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ Mount Vue App               │
│ - Render ChatInterface      │
│ - Show last thread or empty │
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ Open WebSocket Connection   │
│ - io('/socket.io') event    │
│ - On connect: subscribe to  │
│   personal room             │
│ - Listen for stream events  │
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ Ready for Interaction       │
│ - User sends message        │
│ - Upload files              │
│ - Switch threads            │
│ - Change settings           │
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ User Logout / Session End   │
│ - Close WebSocket           │
│ - Clear local stores        │
│ - Clear cache               │
│ - Redirect to login         │
└─────────────────────────────┘
```

---

## Error Handling Flow

```
┌──────────────────────────────────────────┐
│ Error Occurs                             │
│ (validation, API call, database, etc.)   │
└──────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ Backend: Log Error                       │
│ - frappe.log_error() called              │
│ - Stack trace captured                   │
│ - Error details saved to audit log       │
└──────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ Return Error Response                    │
│ - HTTP status code (400/500)            │
│ - Error message in response              │
│ - traceback (development only)           │
└──────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ Frontend: Catch Error                    │
│ - Try-catch in composable                │
│ - Error state updated                    │
│ - console.error() for debugging          │
└──────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ Frontend: Show Error to User             │
│ - Toast notification                     │
│ - Error message displayed                │
│ - UI state reset (e.g., loading false)   │
│ - User can retry                         │
└──────────────────────────────────────────┘
```

---

## Performance Optimization Points

```
┌─────────────────────────────────────────────────────┐
│           PERFORMANCE OPTIMIZATION                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 1. DATABASE OPTIMIZATION                           │
│    ├─ Index on: user, thread_id, timestamp         │
│    ├─ Query pagination: 50 messages per request    │
│    └─ Connection pooling: MariaDB config           │
│                                                     │
│ 2. CACHING STRATEGY                                │
│    ├─ Thread messages: 5min TTL (Redis)            │
│    ├─ Model configs: 1 hour TTL                    │
│    ├─ User prefs: Session-based cache              │
│    └─ Message history: LRU cache (latest 100)      │
│                                                     │
│ 3. FRONTEND OPTIMIZATION                           │
│    ├─ Code splitting: Lazy load components         │
│    ├─ Virtual scrolling: For long message lists    │
│    ├─ Image optimization: Thumbnails for files    │
│    └─ Bundle size: Tree-shake unused imports       │
│                                                     │
│ 4. NETWORK OPTIMIZATION                            │
│    ├─ Compression: gzip on responses              │
│    ├─ WebSocket: Replace polling with streaming   │
│    ├─ Batch requests: Combine multiple ops        │
│    └─ CDN: Serve static assets from edge          │
│                                                     │
│ 5. LLM OPTIMIZATION                                │
│    ├─ Token batching: Queue messages for 500ms    │
│    ├─ Context window: Only send recent messages   │
│    ├─ Model selection: Use smaller for simple Q   │
│    └─ Caching responses: Store similar answers    │
│                                                     │
│ 6. BACKGROUND JOBS                                 │
│    ├─ Async: File processing via RQ              │
│    ├─ Delayed: Batch token counting              │
│    ├─ Scheduled: Daily cleanup of old chats      │
│    └─ Retry logic: For failed LLM calls          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Security Layers

```
┌─────────────────────────────────────────────────────┐
│            SECURITY ARCHITECTURE                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Layer 1: TRANSPORT SECURITY                        │
│   ├─ HTTPS/TLS for all connections                │
│   ├─ WSS for WebSocket (TLS wrapped)              │
│   └─ Certificate pinning (optional)               │
│                                                     │
│ Layer 2: AUTHENTICATION                            │
│   ├─ Frappe session authentication                │
│   ├─ JWT token validation                         │
│   ├─ Session timeout: 24 hours                    │
│   └─ Re-auth on sensitive operations              │
│                                                     │
│ Layer 3: AUTHORIZATION                             │
│   ├─ Frappe permission system                     │
│   ├─ User can only access own threads             │
│   ├─ Role-based access control (RBAC)            │
│   └─ Document-level permissions                  │
│                                                     │
│ Layer 4: INPUT VALIDATION                          │
│   ├─ Frontend: HTML/attribute escaping            │
│   ├─ Backend: Type checking, range validation     │
│   ├─ File upload: Type/size limits, scan         │
│   └─ SQL injection prevention (ORM)              │
│                                                     │
│ Layer 5: DATA PROTECTION                           │
│   ├─ API keys: Encrypted in database             │
│   ├─ Sensitive data: Not logged                  │
│   ├─ At rest: Database encryption               │
│   └─ Audit trail: All operations logged          │
│                                                     │
│ Layer 6: RATE LIMITING                             │
│   ├─ API endpoints: 100 req/hour per user        │
│   ├─ File upload: 10 files/hour per user         │
│   ├─ Message send: 30 msg/hour per user          │
│   └─ Failed login: 5 attempts then lockout       │
│                                                     │
│ Layer 7: XSRF/CSRF PROTECTION                      │
│   ├─ CSRF token validation on POST/PUT/DELETE    │
│   ├─ SameSite cookie attribute                   │
│   └─ Origin validation                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────┐
│            PRODUCTION DEPLOYMENT                 │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │           CloudFlare CDN/WAF               │ │
│  │    - DDoS protection                       │ │
│  │    - SSL/TLS termination                   │ │
│  │    - Static asset caching                  │ │
│  └────────────────────────────────────────────┘ │
│                      │                          │
│  ┌────────────────────────────────────────────┐ │
│  │         Nginx Load Balancer                │ │
│  │    - Multiple upstream servers             │ │
│  │    - Health checks                         │ │
│  │    - Rate limiting                         │ │
│  └────────────────────────────────────────────┘ │
│         │           │           │               │
│    ┌────▼───┐   ┌───▼────┐  ┌──▼─────┐        │
│    │ Frappe │   │ Frappe │  │ Frappe │        │
│    │ App 1  │   │ App 2  │  │ App 3  │        │
│    └────┬───┘   └───┬────┘  └──┬─────┘        │
│         │           │          │               │
│    ┌────▼───────────▼──────────▼────┐         │
│    │   Shared Storage                │         │
│    │   - Database (Primary/Replica)  │         │
│    │   - Redis Cache                 │         │
│    │   - File storage (S3/GCS)       │         │
│    └─────────────────────────────────┘         │
│                                                  │
│    ┌─────────────────────────────────┐         │
│    │   Monitoring & Logging          │         │
│    │   - Prometheus metrics          │         │
│    │   - Grafana dashboards          │         │
│    │   - ELK stack (logs)            │         │
│    │   - Alert manager               │         │
│    └─────────────────────────────────┘         │
└──────────────────────────────────────────────────┘
```

---

## Component State Diagram (Pinia)

```
Pinia Store State Tree
──────────────────────

chatStore
├── currentThread: {id, title, model, created}
├── messages: [{id, role, content, timestamp}, ...]
├── threads: [{id, title, updated}, ...]
├── isLoading: boolean
└── error: null | string

messageStore
├── selectedMessage: {id, role, content}
├── editingMessage: {id, content}
└── copiedMessageId: string | null

userStore
├── currentUser: {id, name, email}
├── preferences: {theme, default_model, language}
└── permissions: {read, write, delete}

connectorStore
├── connectors: [{id, name, type, status}, ...]
├── selectedConnector: {id, name}
├── availableTools: [{name, description, params}, ...]
└── isLoading: boolean

settingsStore
├── temperature: 0.7
├── maxTokens: 2048
├── theme: 'light' | 'dark'
├── autoSaveDrafts: true
└── notifications: {enabled, sound}

fileStore
├── uploadQueue: [{file, progress}, ...]
├── selectedFiles: [{id, name, size}, ...]
├── uploadProgress: 0-100
└── maxFileSize: 52428800

uiStore
├── sidebarOpen: boolean
├── settingsOpen: boolean
├── toasts: [{id, message, type}, ...]
├── loading: boolean
└── darkMode: boolean
```

---

**Diagrams Version**: 1.0  
**Last Updated**: October 26, 2025  
**Status**: Complete Reference
