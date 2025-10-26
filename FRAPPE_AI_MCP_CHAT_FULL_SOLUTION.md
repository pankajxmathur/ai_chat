# AI MCP Chat - Full Production-Ready Frappe App Solution

**Version:** 2.0  
**Date:** October 26, 2025  
**Status:** Production-Ready Specification  
**Framework:** Frappe + Vue 3 + Frappe UI

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Backend Implementation](#backend-implementation)
6. [Frontend Implementation](#frontend-implementation)
7. [Database Schema](#database-schema)
8. [API Specifications](#api-specifications)
9. [Frontend Components](#frontend-components)
10. [Integration with MCP Protocol](#integration-with-mcp-protocol)
11. [Security & Authentication](#security--authentication)
12. [Development Workflow](#development-workflow)
13. [Deployment Guide](#deployment-guide)
14. [Testing Strategy](#testing-strategy)
15. [Troubleshooting & Best Practices](#troubleshooting--best-practices)

---

## 1. Executive Summary

This document provides a complete, production-ready specification for building an AI MCP Chat application as a Frappe app. Instead of using Next.js with assistant-ui, this solution leverages **Frappe's native Vue 3 frontend** with **Frappe UI components**, creating a seamless integration where the chat interface lives directly within the Frappe ecosystem.

### Key Features

- Multi-model LLM support (OpenAI, Anthropic Claude, Google Gemini, custom models)
- Real-time streaming responses via WebSocket
- File upload and processing (documents, images, PDFs)
- Connector/Tool management (MCP protocol integration)
- Conversation history and search
- User permissions and audit logging
- Production-grade security
- Responsive UI with Frappe UI components
- Vue 3 with Pinia state management

---

## 2. Architecture Overview

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Vue 3 + Frappe UI)          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Chat UI      │  │ File Upload  │  │  Settings    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Connectors   │  │ Conversation │  │ Model Select │         │
│  │  Manager     │  │   History    │  │   & Config   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
      REST API           WebSocket      File Upload
                                         Endpoint
            │               │               │
┌─────────────────────────────────────────────────────────────────┐
│                  Frappe Backend (Python)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          AI MCP Chat Module                             │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  Message Handler & Chat Logic                   │   │  │
│  │  │  - Message persistence                          │   │  │
│  │  │  - Streaming response management                │   │  │
│  │  │  - Tool calling & execution                     │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  LLM Adapter & Provider Integration             │   │  │
│  │  │  - Multi-model support (Claude, GPT, Gemini)    │   │  │
│  │  │  - LiteLLM routing                              │   │  │
│  │  │  - Response streaming                           │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  Connector Manager & MCP Protocol Handler       │   │  │
│  │  │  - Tool registry and validation                 │   │  │
│  │  │  - Connector lifecycle management               │   │  │
│  │  │  - Resource handling                            │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  File Processing Service                        │   │  │
│  │  │  - Document parsing (PDF, DOCX, TXT)           │   │  │
│  │  │  - Image processing                             │   │  │
│  │  │  - Virus scanning & validation                  │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Database Layer (DocTypes)                      │  │
│  │  - AI Chat Thread, AI Chat Message                      │  │
│  │  - LLM Model Configuration                             │  │
│  │  - MCP Connector, MCP Tool                             │  │
│  │  - Chat Attachment, User Preferences                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐  ┌─────────▼────────┐  ┌─────▼──────────┐
│  LLM Providers│ │  MCP Servers    │ │ External APIs  │
│ - OpenAI API │ │  - Code Tools   │ │ - Databases    │
│ - Anthropic  │ │  - Search       │ │ - File Storage │
│ - Google AI  │ │  - Web Access   │ │ - Analytics    │
│ - LiteLLM    │ │  - Custom Tools │ │ - Webhooks     │
└──────────────┘ └─────────────────┘ └────────────────┘
```

### 2.2 Key Design Principles

- **Modular Architecture**: Cleanly separated concerns between frontend and backend
- **Real-time Communication**: WebSocket support for streaming responses
- **Scalability**: Designed for handling multiple concurrent users
- **Security-First**: Frappe's built-in permission system and audit trails
- **Extensibility**: MCP protocol support for custom tools and integrations
- **Performance**: Optimized caching and database queries

---

## 3. Technology Stack

### 3.1 Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Vue 3 | 3.4+ | Core frontend framework |
| UI Components | Frappe UI | Latest | Component library & design system |
| State Management | Pinia | 2.1+ | Global state management |
| HTTP Client | Frappe API | Built-in | REST API communication |
| WebSocket | Socket.io | Latest | Real-time streaming |
| Build Tool | Frappe's Desk | Built-in | Development environment |
| Markdown Rendering | Marked.js | 11+ | Convert MD to HTML |
| Code Highlighting | Highlight.js | 11+ | Syntax highlighting |
| Icons | Lucide Vue | Latest | SVG icon system |
| Date Handling | Day.js | 1.11+ | DateTime formatting |

### 3.2 Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Frappe | Latest | Web framework & ORM |
| Language | Python | 3.10+ | Backend language |
| Database | MariaDB/PostgreSQL | Latest | Data persistence |
| Cache | Redis | 6+ | Session caching & queue |
| Queue | RQ | Latest | Background job processing |
| API | REST/WebSocket | - | Communication protocol |
| Authentication | Frappe Auth | Built-in | User management |
| ORM | Frappe ORM | Built-in | Database abstraction |

### 3.3 External Integrations

| Service | Purpose | Configuration |
|---------|---------|---|
| OpenAI API | GPT-4, GPT-3.5 models | API key management |
| Anthropic Claude | Claude models | API key management |
| Google AI | Gemini models | API key management |
| LiteLLM | Multi-provider proxy | Optional, for routing |
| MCP Servers | Custom tool providers | TCP/stdio connection |

---

## 4. Project Structure

### 4.1 Frappe App Directory Structure

```
ai_mcp_chat/                               # Main app directory
├── ai_mcp_chat/                           # Python package
│   ├── __init__.py
│   ├── hooks.py                           # App configuration & hooks
│   ├── api/                               # API endpoints
│   │   ├── __init__.py
│   │   ├── chat.py                        # Chat message endpoints
│   │   ├── conversation.py                # Conversation management
│   │   ├── connector.py                   # MCP connector endpoints
│   │   ├── file.py                        # File upload/processing
│   │   ├── llm.py                         # LLM provider management
│   │   └── streaming.py                   # WebSocket streaming
│   ├── services/                          # Business logic services
│   │   ├── __init__.py
│   │   ├── chat_service.py                # Core chat operations
│   │   ├── llm_service.py                 # LLM abstraction layer
│   │   ├── mcp_service.py                 # MCP protocol handling
│   │   ├── file_service.py                # File processing
│   │   ├── streaming_service.py           # Streaming management
│   │   └── tool_executor.py               # Execute MCP tools
│   ├── models/                            # DocType models
│   │   ├── __init__.py
│   │   ├── ai_chat_thread.py
│   │   ├── ai_chat_message.py
│   │   ├── llm_model_configuration.py
│   │   ├── mcp_connector.py
│   │   ├── mcp_tool.py
│   │   ├── chat_attachment.py
│   │   └── user_preferences.py
│   ├── decorators/                        # Custom decorators
│   │   ├── __init__.py
│   │   └── permission_required.py
│   ├── utils/                             # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── exceptions.py
│   │   └── logger.py
│   └── migrations/                        # Database migrations
│       └── __init__.py
│
├── ai_mcp_chat/                           # Frontend Vue app (Desk)
│   └── public/
│       └── js/
│           ├── ai_mcp_chat.js             # App initialization
│           └── [Optional custom JS]
│
├── ai_mcp_chat/                           # Frappe DocType definitions
│   └── doctype/
│       ├── ai_chat_thread/
│       │   ├── ai_chat_thread.json        # DocType definition
│       │   ├── ai_chat_thread.py          # Python class
│       │   └── ai_chat_thread.js          # Client script
│       ├── ai_chat_message/
│       │   ├── ai_chat_message.json
│       │   ├── ai_chat_message.py
│       │   └── ai_chat_message.js
│       ├── llm_model_configuration/
│       │   ├── llm_model_configuration.json
│       │   └── llm_model_configuration.py
│       ├── mcp_connector/
│       │   ├── mcp_connector.json
│       │   └── mcp_connector.py
│       ├── mcp_tool/
│       │   ├── mcp_tool.json
│       │   └── mcp_tool.py
│       ├── chat_attachment/
│       │   ├── chat_attachment.json
│       │   └── chat_attachment.py
│       ├── user_preferences/
│       │   ├── user_preferences.json
│       │   └── user_preferences.py
│       └── [Custom pages and views]
│
├── frontend/                              # Modern Vue 3 SPA
│   ├── src/
│   │   ├── assets/                        # Static assets
│   │   │   ├── images/
│   │   │   ├── styles/
│   │   │   │   ├── main.css               # Global styles
│   │   │   │   ├── variables.css          # CSS variables
│   │   │   │   └── markdown.css           # Markdown rendering styles
│   │   │   └── fonts/
│   │   │
│   │   ├── components/                    # Vue components
│   │   │   ├── chat/
│   │   │   │   ├── ChatInterface.vue      # Main chat component
│   │   │   │   ├── MessageList.vue        # Messages container
│   │   │   │   ├── MessageItem.vue        # Single message
│   │   │   │   ├── MessageContent.vue     # Message content renderer
│   │   │   │   ├── InputArea.vue          # Message input
│   │   │   │   ├── StreamingIndicator.vue # Typing animation
│   │   │   │   ├── MessageActions.vue     # Copy, regenerate, edit
│   │   │   │   └── CodeBlock.vue          # Syntax highlighted code
│   │   │   │
│   │   │   ├── files/
│   │   │   │   ├── FileUpload.vue         # Drag-drop upload
│   │   │   │   ├── FilePreview.vue        # File preview modal
│   │   │   │   ├── AttachmentList.vue     # Attached files list
│   │   │   │   └── FileProgressBar.vue    # Upload progress
│   │   │   │
│   │   │   ├── connectors/
│   │   │   │   ├── ConnectorManager.vue   # Connectors main view
│   │   │   │   ├── ConnectorCard.vue      # Connector card component
│   │   │   │   ├── ConnectorForm.vue      # Add/edit connector
│   │   │   │   ├── ToolsList.vue          # Available tools list
│   │   │   │   └── ToolTestPanel.vue      # Test tool execution
│   │   │   │
│   │   │   ├── settings/
│   │   │   │   ├── ModelSelector.vue      # LLM model chooser
│   │   │   │   ├── ProviderSettings.vue   # Provider config
│   │   │   │   ├── UserPreferences.vue    # User settings
│   │   │   │   └── AdvancedOptions.vue    # Advanced parameters
│   │   │   │
│   │   │   ├── sidebar/
│   │   │   │   ├── ConversationSidebar.vue# Left sidebar
│   │   │   │   ├── ConversationList.vue   # List of conversations
│   │   │   │   ├── ConversationSearch.vue # Search conversations
│   │   │   │   ├── ConversationItem.vue   # Single item renderer
│   │   │   │   └── NewChatButton.vue      # Create new chat
│   │   │   │
│   │   │   └── common/
│   │   │       ├── Header.vue             # App header
│   │   │       ├── Footer.vue             # App footer
│   │   │       ├── ActionChips.vue        # Quick action buttons
│   │   │       ├── ContextMenu.vue        # Right-click menu
│   │   │       ├── Modal.vue              # Modal wrapper
│   │   │       ├── Toast.vue              # Notifications
│   │   │       └── LoadingSpinner.vue     # Loading state
│   │   │
│   │   ├── composables/                   # Vue composables
│   │   │   ├── useChat.js                 # Chat logic hook
│   │   │   ├── useFileUpload.js           # File upload hook
│   │   │   ├── useConnectors.js           # Connectors hook
│   │   │   ├── useWebSocket.js            # WebSocket management
│   │   │   ├── useLocalStorage.js         # Local storage hook
│   │   │   ├── useFormValidation.js       # Form validation
│   │   │   └── useMarkdown.js             # Markdown processing
│   │   │
│   │   ├── stores/                        # Pinia stores
│   │   │   ├── index.js                   # Store configuration
│   │   │   ├── chatStore.js               # Chat state
│   │   │   ├── messageStore.js            # Messages state
│   │   │   ├── userStore.js               # User state
│   │   │   ├── connectorStore.js          # Connectors state
│   │   │   ├── settingsStore.js           # Settings state
│   │   │   ├── fileStore.js               # Files state
│   │   │   └── uiStore.js                 # UI state
│   │   │
│   │   ├── services/                      # API services
│   │   │   ├── api.js                     # Frappe API wrapper
│   │   │   ├── chatService.js             # Chat API calls
│   │   │   ├── fileService.js             # File API calls
│   │   │   ├── connectorService.js        # Connector API calls
│   │   │   ├── llmService.js              # LLM API calls
│   │   │   ├── authService.js             # Auth API calls
│   │   │   └── websocketService.js        # WebSocket management
│   │   │
│   │   ├── utils/                         # Utility functions
│   │   │   ├── markdown.js                # Markdown utilities
│   │   │   ├── fileHandlers.js            # File utilities
│   │   │   ├── formatters.js              # Date/time formatters
│   │   │   ├── constants.js               # App constants
│   │   │   ├── validators.js              # Input validators
│   │   │   └── clipboard.js               # Clipboard utilities
│   │   │
│   │   ├── router/                        # Vue Router (if SPA)
│   │   │   └── index.js                   # Route configuration
│   │   │
│   │   ├── App.vue                        # Root component
│   │   └── main.js                        # App entry point
│   │
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── tailwind.config.js                 # Tailwind CSS config
│
├── tests/                                 # Tests
│   ├── unit/
│   │   ├── test_chat_service.py
│   │   ├── test_llm_adapter.py
│   │   ├── test_file_service.py
│   │   └── test_mcp_service.py
│   ├── integration/
│   │   ├── test_chat_flow.py
│   │   ├── test_streaming.py
│   │   └── test_file_upload.py
│   └── e2e/
│       └── test_ui_flow.spec.js
│
├── fixtures/                              # Test fixtures
│   ├── chat_fixtures.py
│   ├── llm_fixtures.py
│   └── connector_fixtures.py
│
├── migrations/                            # Migration scripts
│   ├── 001_initial_setup.py
│   └── 002_add_features.py
│
├── docs/                                  # Documentation
│   ├── SETUP.md                           # Setup guide
│   ├── API.md                             # API documentation
│   ├── DEPLOYMENT.md                      # Deployment guide
│   ├── MCP_INTEGRATION.md                 # MCP protocol guide
│   └── TROUBLESHOOTING.md                 # Troubleshooting
│
├── config/
│   ├── settings.py                        # App settings
│   └── constants.py                       # Constants
│
├── .env.example                           # Environment template
├── README.md                              # Project README
├── pyproject.toml                         # Python dependencies
├── requirements.txt                       # Python requirements
└── docker-compose.yml                     # Docker setup

```

---

## 5. Backend Implementation

### 5.1 DocType Definitions

#### 5.1.1 AI Chat Thread

```python
# ai_mcp_chat/doctype/ai_chat_thread/ai_chat_thread.json

{
  "doctype": "AI Chat Thread",
  "module": "AI MCP Chat",
  "label": "AI Chat Thread",
  "is_tree": false,
  "track_changes": 1,
  "track_seen": 1,
  "quick_entry": true,
  "fields": [
    {
      "fieldname": "thread_id",
      "label": "Thread ID",
      "fieldtype": "Data",
      "unique": 1,
      "reqd": 1,
      "read_only": 1,
      "description": "Unique identifier for the thread"
    },
    {
      "fieldname": "user",
      "label": "User",
      "fieldtype": "Link",
      "options": "User",
      "reqd": 1,
      "read_only": 1
    },
    {
      "fieldname": "title",
      "label": "Title",
      "fieldtype": "Data",
      "reqd": 1,
      "default": "New Chat"
    },
    {
      "fieldname": "description",
      "label": "Description",
      "fieldtype": "Text",
      "description": "Optional thread description"
    },
    {
      "fieldname": "model_used",
      "label": "Model Used",
      "fieldtype": "Link",
      "options": "LLM Model Configuration",
      "reqd": 1,
      "description": "LLM model configured for this thread"
    },
    {
      "fieldname": "system_prompt",
      "label": "System Prompt",
      "fieldtype": "Text Editor",
      "description": "System context for the AI model"
    },
    {
      "fieldname": "temperature",
      "label": "Temperature",
      "fieldtype": "Float",
      "default": 0.7,
      "description": "Model temperature (0.0-2.0)"
    },
    {
      "fieldname": "max_tokens",
      "label": "Max Tokens",
      "fieldtype": "Int",
      "default": 2048,
      "description": "Maximum tokens in response"
    },
    {
      "fieldname": "is_archived",
      "label": "Is Archived",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "tags",
      "label": "Tags",
      "fieldtype": "Text",
      "description": "Comma-separated tags for organization"
    },
    {
      "fieldname": "metadata",
      "label": "Metadata",
      "fieldtype": "JSON",
      "description": "Custom metadata storage"
    },
    {
      "fieldname": "created_on",
      "label": "Created On",
      "fieldtype": "DateTime",
      "read_only": 1
    },
    {
      "fieldname": "modified_on",
      "label": "Modified On",
      "fieldtype": "DateTime",
      "read_only": 1
    },
    {
      "fieldname": "token_count",
      "label": "Total Tokens Used",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    },
    {
      "fieldname": "estimated_cost",
      "label": "Estimated Cost (USD)",
      "fieldtype": "Currency",
      "read_only": 1,
      "default": 0
    }
  ],
  "permissions": [
    {
      "role": "All",
      "permlevel": 0,
      "perm_type": "select",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1,
      "submit": 0,
      "amend": 0
    }
  ]
}
```

#### 5.1.2 AI Chat Message

```python
# ai_mcp_chat/doctype/ai_chat_message/ai_chat_message.json

{
  "doctype": "AI Chat Message",
  "module": "AI MCP Chat",
  "label": "AI Chat Message",
  "track_changes": 1,
  "fields": [
    {
      "fieldname": "thread",
      "label": "Thread",
      "fieldtype": "Link",
      "options": "AI Chat Thread",
      "reqd": 1
    },
    {
      "fieldname": "role",
      "label": "Role",
      "fieldtype": "Select",
      "options": "user\nassistant\ntool",
      "reqd": 1,
      "description": "Message sender role"
    },
    {
      "fieldname": "content",
      "label": "Content",
      "fieldtype": "Text Editor",
      "reqd": 1
    },
    {
      "fieldname": "content_type",
      "label": "Content Type",
      "fieldtype": "Select",
      "options": "text\nmarkdown\njson\ncode",
      "default": "text"
    },
    {
      "fieldname": "tool_calls",
      "label": "Tool Calls",
      "fieldtype": "JSON",
      "description": "MCP tool calls made in this message"
    },
    {
      "fieldname": "tool_results",
      "label": "Tool Results",
      "fieldtype": "JSON",
      "description": "Results from tool execution"
    },
    {
      "fieldname": "model_used",
      "label": "Model Used",
      "fieldtype": "Data",
      "description": "Specific model used for this response"
    },
    {
      "fieldname": "tokens_used",
      "label": "Tokens Used",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "input_tokens",
      "label": "Input Tokens",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "output_tokens",
      "label": "Output Tokens",
      "fieldtype": "Int",
      "default": 0
    },
    {
      "fieldname": "attachments",
      "label": "Attachments",
      "fieldtype": "Table",
      "options": "Chat Attachment"
    },
    {
      "fieldname": "is_edited",
      "label": "Is Edited",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "edited_at",
      "label": "Edited At",
      "fieldtype": "DateTime"
    },
    {
      "fieldname": "timestamp",
      "label": "Timestamp",
      "fieldtype": "DateTime",
      "read_only": 1
    }
  ]
}
```

#### 5.1.3 LLM Model Configuration

```python
# ai_mcp_chat/doctype/llm_model_configuration/llm_model_configuration.json

{
  "doctype": "LLM Model Configuration",
  "module": "AI MCP Chat",
  "label": "LLM Model Configuration",
  "fields": [
    {
      "fieldname": "model_name",
      "label": "Model Name",
      "fieldtype": "Data",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "provider",
      "label": "Provider",
      "fieldtype": "Select",
      "options": "OpenAI\nAnthropic\nGoogle\nLocal\nCustom",
      "reqd": 1
    },
    {
      "fieldname": "api_key_field",
      "label": "API Key Field Name",
      "fieldtype": "Data",
      "description": "Environment variable name for API key"
    },
    {
      "fieldname": "base_url",
      "label": "Base URL",
      "fieldtype": "Data",
      "description": "Custom API endpoint (if applicable)"
    },
    {
      "fieldname": "model_identifier",
      "label": "Model Identifier",
      "fieldtype": "Data",
      "reqd": 1,
      "description": "Provider-specific model ID (e.g., gpt-4, claude-3-opus)"
    },
    {
      "fieldname": "max_tokens",
      "label": "Max Tokens",
      "fieldtype": "Int",
      "default": 4096
    },
    {
      "fieldname": "supports_streaming",
      "label": "Supports Streaming",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "supports_vision",
      "label": "Supports Vision",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "supports_tools",
      "label": "Supports Tools",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "cost_per_1k_input",
      "label": "Cost per 1K Input Tokens (USD)",
      "fieldtype": "Currency",
      "default": 0
    },
    {
      "fieldname": "cost_per_1k_output",
      "label": "Cost per 1K Output Tokens (USD)",
      "fieldtype": "Currency",
      "default": 0
    },
    {
      "fieldname": "is_active",
      "label": "Is Active",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "description",
      "label": "Description",
      "fieldtype": "Text"
    }
  ]
}
```

#### 5.1.4 MCP Connector

```python
# ai_mcp_chat/doctype/mcp_connector/mcp_connector.json

{
  "doctype": "MCP Connector",
  "module": "AI MCP Chat",
  "label": "MCP Connector",
  "fields": [
    {
      "fieldname": "connector_name",
      "label": "Connector Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "connector_type",
      "label": "Connector Type",
      "fieldtype": "Select",
      "options": "stdio\ntcp\nhttp",
      "reqd": 1,
      "description": "How to connect to MCP server"
    },
    {
      "fieldname": "host",
      "label": "Host",
      "fieldtype": "Data",
      "description": "Hostname/IP for tcp/http connectors"
    },
    {
      "fieldname": "port",
      "label": "Port",
      "fieldtype": "Int",
      "description": "Port number for tcp/http connectors"
    },
    {
      "fieldname": "command",
      "label": "Command",
      "fieldtype": "Data",
      "description": "Command to run for stdio connector"
    },
    {
      "fieldname": "arguments",
      "label": "Arguments",
      "fieldtype": "JSON",
      "description": "Command arguments as JSON"
    },
    {
      "fieldname": "environment_vars",
      "label": "Environment Variables",
      "fieldtype": "JSON",
      "description": "Env vars needed for connection"
    },
    {
      "fieldname": "is_active",
      "label": "Is Active",
      "fieldtype": "Check",
      "default": 1
    },
    {
      "fieldname": "connection_status",
      "label": "Connection Status",
      "fieldtype": "Select",
      "options": "Connected\nDisconnected\nError\nUnknown",
      "default": "Unknown",
      "read_only": 1
    },
    {
      "fieldname": "last_tested",
      "label": "Last Tested",
      "fieldtype": "DateTime",
      "read_only": 1
    },
    {
      "fieldname": "tools_available",
      "label": "Available Tools",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    }
  ]
}
```

#### 5.1.5 Chat Attachment

```python
# ai_mcp_chat/doctype/chat_attachment/chat_attachment.json

{
  "doctype": "Chat Attachment",
  "fieldtype": "Table",
  "module": "AI MCP Chat",
  "fields": [
    {
      "fieldname": "file_name",
      "label": "File Name",
      "fieldtype": "Data"
    },
    {
      "fieldname": "file_path",
      "label": "File Path",
      "fieldtype": "Attach"
    },
    {
      "fieldname": "file_size",
      "label": "File Size (bytes)",
      "fieldtype": "Int"
    },
    {
      "fieldname": "file_type",
      "label": "File Type",
      "fieldtype": "Data"
    },
    {
      "fieldname": "is_processed",
      "label": "Is Processed",
      "fieldtype": "Check",
      "default": 0
    },
    {
      "fieldname": "extracted_content",
      "label": "Extracted Content",
      "fieldtype": "Text",
      "description": "Extracted text from file"
    }
  ]
}
```

### 5.2 API Endpoints (Python)

#### 5.2.1 Chat API Endpoints

```python
# ai_mcp_chat/api/chat.py

import frappe
from frappe import throw
from frappe.utils import get_url_to_form
from datetime import datetime
import json
import uuid
from ai_mcp_chat.services.chat_service import ChatService
from ai_mcp_chat.services.streaming_service import StreamingService
from ai_mcp_chat.decorators.permission_required import permission_required


@frappe.whitelist()
@permission_required("AI Chat Thread", "create")
def create_chat_thread(title=None, system_prompt=None, model=None):
    """Create a new chat thread
    
    Args:
        title: Chat title
        system_prompt: System prompt for the AI model
        model: LLM Model Configuration name
    
    Returns:
        dict: Thread creation response with thread_id and docname
    """
    try:
        thread_id = str(uuid.uuid4())
        
        # Get default model if not specified
        if not model:
            default_model = frappe.db.get_value(
                "LLM Model Configuration",
                {"is_active": 1},
                "name"
            )
            if not default_model:
                throw("No active LLM model configured")
            model = default_model
        
        # Create thread document
        thread_doc = frappe.get_doc({
            "doctype": "AI Chat Thread",
            "thread_id": thread_id,
            "user": frappe.session.user,
            "title": title or "New Chat",
            "system_prompt": system_prompt or "You are a helpful AI assistant.",
            "model_used": model,
        })
        thread_doc.insert(permit_on_submit=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "thread_id": thread_id,
            "docname": thread_doc.name,
            "created_at": thread_doc.creation
        }
    except Exception as e:
        frappe.log_error(str(e), "Create Chat Thread Error")
        throw(f"Failed to create chat thread: {str(e)}")


@frappe.whitelist()
def get_chat_thread(thread_id):
    """Fetch complete chat thread with all messages
    
    Args:
        thread_id: The thread ID
    
    Returns:
        dict: Thread data with messages
    """
    try:
        thread_doc = frappe.get_doc(
            "AI Chat Thread",
            {"thread_id": thread_id, "user": frappe.session.user}
        )
        
        # Get all messages
        messages = frappe.get_all(
            "AI Chat Message",
            filters={"thread": thread_doc.name},
            fields=["name", "role", "content", "content_type", "tool_calls", 
                   "tool_results", "model_used", "tokens_used", "timestamp"],
            order_by="timestamp asc"
        )
        
        return {
            "success": True,
            "thread": {
                "id": thread_doc.thread_id,
                "title": thread_doc.title,
                "model": thread_doc.model_used,
                "system_prompt": thread_doc.system_prompt,
                "created_at": thread_doc.creation,
                "updated_at": thread_doc.modified,
                "temperature": thread_doc.temperature,
                "max_tokens": thread_doc.max_tokens,
                "total_tokens": thread_doc.token_count,
                "estimated_cost": thread_doc.estimated_cost
            },
            "messages": messages
        }
    except Exception as e:
        frappe.log_error(str(e), "Get Chat Thread Error")
        throw(f"Failed to retrieve thread: {str(e)}")


@frappe.whitelist()
def list_chat_threads(limit=20, offset=0, search=None):
    """List all chat threads for current user
    
    Args:
        limit: Number of threads to return
        offset: Pagination offset
        search: Search query
    
    Returns:
        dict: List of threads with metadata
    """
    try:
        filters = {"user": frappe.session.user}
        
        if search:
            filters["title"] = ["like", f"%{search}%"]
        
        threads = frappe.get_all(
            "AI Chat Thread",
            filters=filters,
            fields=["name", "thread_id", "title", "model_used", "is_archived",
                   "token_count", "creation", "modified"],
            order_by="modified desc",
            limit_page_length=limit,
            offset=offset
        )
        
        # Get message count for each thread
        for thread in threads:
            thread["message_count"] = frappe.db.count(
                "AI Chat Message",
                {"thread": thread["name"]}
            )
        
        return {
            "success": True,
            "threads": threads,
            "count": len(threads)
        }
    except Exception as e:
        frappe.log_error(str(e), "List Threads Error")
        throw(f"Failed to list threads: {str(e)}")


@frappe.whitelist()
def send_message(thread_id, content, attachments=None, stream=True):
    """Send a message and get AI response
    
    Args:
        thread_id: Chat thread ID
        content: Message content
        attachments: List of attachment file paths
        stream: Whether to use streaming
    
    Returns:
        dict: Message creation response
    """
    try:
        # Validate thread access
        thread_doc = frappe.get_doc(
            "AI Chat Thread",
            {"thread_id": thread_id, "user": frappe.session.user}
        )
        
        # Create user message
        user_message = frappe.get_doc({
            "doctype": "AI Chat Message",
            "thread": thread_doc.name,
            "role": "user",
            "content": content,
            "content_type": "text"
        })
        
        # Add attachments if provided
        if attachments:
            for attachment in attachments:
                user_message.append("attachments", {
                    "file_path": attachment,
                    "file_name": attachment.split("/")[-1]
                })
        
        user_message.insert(permit_on_submit=True)
        frappe.db.commit()
        
        # Get AI response
        chat_service = ChatService()
        response = chat_service.generate_response(
            thread_doc,
            stream=stream
        )
        
        return {
            "success": True,
            "user_message_id": user_message.name,
            "response": response
        }
    except Exception as e:
        frappe.log_error(str(e), "Send Message Error")
        throw(f"Failed to send message: {str(e)}")


@frappe.whitelist()
def delete_thread(thread_id):
    """Delete a chat thread and all associated messages
    
    Args:
        thread_id: Thread ID to delete
    
    Returns:
        dict: Deletion confirmation
    """
    try:
        thread_doc = frappe.get_doc(
            "AI Chat Thread",
            {"thread_id": thread_id, "user": frappe.session.user}
        )
        
        # Delete associated messages
        frappe.db.delete("AI Chat Message", {"thread": thread_doc.name})
        
        # Delete thread
        thread_doc.delete(force=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "message": "Thread deleted successfully"
        }
    except Exception as e:
        frappe.log_error(str(e), "Delete Thread Error")
        throw(f"Failed to delete thread: {str(e)}")


@frappe.whitelist()
def search_conversations(query, limit=10):
    """Search conversations by content
    
    Args:
        query: Search query
        limit: Number of results
    
    Returns:
        dict: Search results
    """
    try:
        # Search in thread titles and descriptions
        threads = frappe.get_all(
            "AI Chat Thread",
            filters={
                "user": frappe.session.user,
                "title": ["like", f"%{query}%"]
            },
            fields=["name", "thread_id", "title", "creation"],
            limit_page_length=limit
        )
        
        # Search in message content
        messages = frappe.db.sql("""
            SELECT DISTINCT m.thread, t.thread_id, t.title, m.content
            FROM `tabAI Chat Message` m
            JOIN `tabAI Chat Thread` t ON m.thread = t.name
            WHERE t.user = %s AND m.content LIKE %s
            LIMIT %s
        """, (frappe.session.user, f"%{query}%", limit), as_dict=True)
        
        return {
            "success": True,
            "threads": threads,
            "messages": messages,
            "total": len(threads) + len(messages)
        }
    except Exception as e:
        frappe.log_error(str(e), "Search Conversations Error")
        throw(f"Search failed: {str(e)}")
```

#### 5.2.2 Streaming Service

```python
# ai_mcp_chat/services/streaming_service.py

import frappe
import json
import asyncio
from typing import Generator, Dict, Any
from ai_mcp_chat.services.llm_service import LLMService


class StreamingService:
    """Handles real-time streaming of LLM responses"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def stream_response(self, thread_doc, messages: list) -> Generator[str, None, None]:
        """Stream LLM response as server-sent events
        
        Args:
            thread_doc: AI Chat Thread document
            messages: List of message objects
        
        Yields:
            JSON strings with streaming data
        """
        try:
            # Get LLM configuration
            llm_config = frappe.get_doc("LLM Model Configuration", thread_doc.model_used)
            
            # Prepare system message
            system_message = {
                "role": "system",
                "content": thread_doc.system_prompt
            }
            
            # Format messages for API
            api_messages = self._format_messages_for_api(messages, llm_config)
            
            # Get streaming response
            accumulated_content = ""
            token_count = 0
            
            for chunk in self.llm_service.stream_completion(
                model=llm_config.model_identifier,
                messages=api_messages,
                system_prompt=thread_doc.system_prompt,
                temperature=thread_doc.temperature,
                max_tokens=thread_doc.max_tokens,
                provider=llm_config.provider
            ):
                if chunk.get("content"):
                    accumulated_content += chunk["content"]
                    token_count = chunk.get("tokens_used", 0)
                    
                    yield json.dumps({
                        "type": "token",
                        "content": chunk["content"],
                        "tokens_used": token_count
                    }) + "\n"
            
            # Send completion event
            yield json.dumps({
                "type": "complete",
                "content": accumulated_content,
                "total_tokens": token_count
            }) + "\n"
            
        except Exception as e:
            frappe.log_error(str(e), "Streaming Error")
            yield json.dumps({
                "type": "error",
                "error": str(e)
            }) + "\n"
    
    def _format_messages_for_api(self, messages: list, llm_config) -> list:
        """Convert database messages to API format"""
        formatted = []
        for msg in messages:
            if isinstance(msg, dict):
                formatted.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            else:
                formatted.append({
                    "role": msg.role,
                    "content": msg.content
                })
        return formatted
```

#### 5.2.3 LLM Service (Multi-Provider)

```python
# ai_mcp_chat/services/llm_service.py

import frappe
import json
from typing import Generator, Dict, Any, List
import os


class LLMService:
    """Abstract LLM provider layer supporting multiple backends"""
    
    def __init__(self):
        self.providers = {
            "OpenAI": self._openai_completion,
            "Anthropic": self._anthropic_completion,
            "Google": self._google_completion,
        }
    
    def stream_completion(self, model: str, messages: List[Dict],
                         system_prompt: str = None, temperature: float = 0.7,
                         max_tokens: int = 2048, provider: str = None) -> Generator:
        """Stream LLM completion
        
        Args:
            model: Model identifier
            messages: Message history
            system_prompt: System context
            temperature: Model temperature
            max_tokens: Max output tokens
            provider: Provider name
        
        Yields:
            Chunks of response with token counts
        """
        try:
            if provider in self.providers:
                yield from self.providers[provider](
                    model, messages, system_prompt, temperature, max_tokens
                )
            else:
                raise ValueError(f"Unknown provider: {provider}")
        except Exception as e:
            frappe.log_error(str(e), "LLM Completion Error")
            raise
    
    def _openai_completion(self, model: str, messages: List[Dict],
                          system_prompt: str, temperature: float,
                          max_tokens: int) -> Generator:
        """OpenAI streaming completion"""
        import openai
        
        api_key = frappe.conf.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
        client = openai.OpenAI(api_key=api_key)
        
        system_message = {"role": "system", "content": system_prompt or ""}
        all_messages = [system_message] + messages if system_prompt else messages
        
        with client.messages.stream(
            model=model,
            messages=all_messages,
            temperature=temperature,
            max_tokens=max_tokens
        ) as stream:
            for text in stream.text_stream:
                yield {
                    "content": text,
                    "tokens_used": 0  # Updated after stream completion
                }
    
    def _anthropic_completion(self, model: str, messages: List[Dict],
                             system_prompt: str, temperature: float,
                             max_tokens: int) -> Generator:
        """Anthropic Claude streaming completion"""
        import anthropic
        
        api_key = frappe.conf.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic(api_key=api_key)
        
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt or "",
            messages=messages,
            temperature=temperature
        ) as stream:
            for text in stream.text_stream:
                yield {
                    "content": text,
                    "tokens_used": 0
                }
    
    def _google_completion(self, model: str, messages: List[Dict],
                          system_prompt: str, temperature: float,
                          max_tokens: int) -> Generator:
        """Google Gemini streaming completion"""
        import google.generativeai as genai
        
        api_key = frappe.conf.get("google_api_key") or os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        
        client = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt
        )
        
        response = client.generate_content(
            messages,
            stream=True,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        
        for chunk in response:
            if chunk.text:
                yield {
                    "content": chunk.text,
                    "tokens_used": 0
                }
```

---

## 6. Frontend Implementation (Vue 3 + Frappe UI)

### 6.1 Main Chat Component

```vue
<!-- frontend/src/components/chat/ChatInterface.vue -->

<template>
  <div class="chat-interface">
    <!-- Header -->
    <div class="chat-header">
      <div class="header-left">
        <button 
          class="sidebar-toggle"
          @click="sidebarOpen = !sidebarOpen"
        >
          <i class="lucide-icon icon-menu"></i>
        </button>
        <h1 class="thread-title">{{ currentThread?.title || 'New Chat' }}</h1>
      </div>
      
      <div class="header-right">
        <div class="model-selector">
          <select 
            v-model="selectedModel"
            class="form-select"
            @change="updateModel"
          >
            <option 
              v-for="model in availableModels" 
              :key="model.name" 
              :value="model.name"
            >
              {{ model.model_name }} ({{ model.provider }})
            </option>
          </select>
        </div>
        
        <button 
          class="btn btn-icon"
          title="Settings"
          @click="showSettings = true"
        >
          <i class="lucide-icon icon-settings"></i>
        </button>
        
        <button 
          class="btn btn-icon"
          title="Delete"
          @click="deleteCurrentThread"
        >
          <i class="lucide-icon icon-trash-2"></i>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="chat-content">
      <!-- Sidebar -->
      <div v-if="sidebarOpen" class="sidebar">
        <ConversationSidebar 
          :threads="chatThreads"
          :current-thread="currentThread"
          @select-thread="selectThread"
          @new-chat="createNewChat"
          @delete-thread="deleteThread"
        />
      </div>

      <!-- Chat Messages -->
      <div class="messages-container">
        <div 
          v-if="messages.length === 0" 
          class="empty-state"
        >
          <div class="empty-icon">
            <i class="lucide-icon icon-message-circle"></i>
          </div>
          <h2>{{ suggestions[0]?.category }}</h2>
          <p>How can I help you today?</p>
          <div class="suggested-actions">
            <button 
              v-for="action in suggestionActions" 
              :key="action"
              class="action-chip"
              @click="insertSuggestedText(action)"
            >
              {{ action }}
            </button>
          </div>
        </div>

        <div v-else class="messages-list">
          <MessageItem
            v-for="(message, index) in messages"
            :key="index"
            :message="message"
            @regenerate="regenerateMessage(index)"
            @copy="copyMessageContent(message.content)"
            @edit="editMessage(index)"
          />

          <!-- Streaming indicator -->
          <div v-if="isStreaming" class="streaming-message">
            <StreamingIndicator />
            <div v-html="streamingContent"></div>
          </div>
        </div>

        <!-- Scroll to bottom -->
        <div ref="messagesEnd"></div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-section">
      <FileUpload 
        v-show="showFileUpload"
        @files-selected="handleFilesSelected"
        @close="showFileUpload = false"
      />

      <AttachmentList 
        v-if="selectedAttachments.length > 0"
        :attachments="selectedAttachments"
        @remove="removeAttachment"
      />

      <InputArea
        v-model="messageInput"
        :disabled="isStreaming"
        @send="sendMessage"
        @attachment-click="showFileUpload = !showFileUpload"
      />
    </div>

    <!-- Modals -->
    <SettingsModal 
      v-if="showSettings"
      :thread="currentThread"
      @close="showSettings = false"
      @update="updateThreadSettings"
    />

    <FilePreview 
      v-if="previewFile"
      :file="previewFile"
      @close="previewFile = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useChat } from '@/composables/useChat'
import { useFileUpload } from '@/composables/useFileUpload'
import { useWebSocket } from '@/composables/useWebSocket'
import { useChatStore } from '@/stores/chatStore'
import { useUIStore } from '@/stores/uiStore'

// Components
import MessageItem from './MessageItem.vue'
import InputArea from './InputArea.vue'
import StreamingIndicator from './StreamingIndicator.vue'
import FileUpload from '../files/FileUpload.vue'
import AttachmentList from '../files/AttachmentList.vue'
import FilePreview from '../files/FilePreview.vue'
import ConversationSidebar from '../sidebar/ConversationSidebar.vue'
import SettingsModal from '../settings/SettingsModal.vue'

const chatStore = useChatStore()
const uiStore = useUIStore()

// Composables
const { 
  sendMessage: sendChatMessage, 
  createThread,
  getThread,
  listThreads 
} = useChat()

const { uploadFile } = useFileUpload()
const { connect: connectWebSocket, disconnect: disconnectWebSocket } = useWebSocket()

// State
const messageInput = ref('')
const sidebarOpen = ref(true)
const showSettings = ref(false)
const showFileUpload = ref(false)
const isStreaming = ref(false)
const streamingContent = ref('')
const selectedAttachments = ref([])
const previewFile = ref(null)
const messagesEnd = ref(null)

const selectedModel = ref('')
const availableModels = ref([])
const chatThreads = ref([])

// Computed
const currentThread = computed(() => chatStore.currentThread)
const messages = computed(() => chatStore.messages)

const suggestionActions = [
  'Explain quantum computing',
  'Write a Python script',
  'Help me debug code',
  'Create a business plan'
]

const suggestions = [
  { category: 'Let\'s start', actions: suggestionActions }
]

// Methods
const createNewChat = async () => {
  try {
    const thread = await createThread('New Chat')
    chatStore.setCurrentThread(thread)
    messageInput.value = ''
    selectedAttachments.value = []
  } catch (error) {
    console.error('Failed to create chat:', error)
  }
}

const selectThread = async (thread) => {
  try {
    const threadData = await getThread(thread.thread_id)
    chatStore.setCurrentThread(threadData.thread)
    chatStore.setMessages(threadData.messages)
    selectedModel.value = threadData.thread.model
  } catch (error) {
    console.error('Failed to load thread:', error)
  }
}

const deleteCurrentThread = async () => {
  if (confirm('Are you sure you want to delete this conversation?')) {
    await deleteThread(currentThread.value.id)
    await createNewChat()
  }
}

const deleteThread = async (threadId) => {
  // Call API to delete
  try {
    await frappe.call({
      method: 'ai_mcp_chat.api.chat.delete_thread',
      args: { thread_id: threadId },
      callback: () => {
        loadThreads()
      }
    })
  } catch (error) {
    console.error('Failed to delete thread:', error)
  }
}

const sendMessage = async () => {
  if (!messageInput.value.trim()) return

  try {
    isStreaming.value = true
    streamingContent.value = ''

    // Add user message
    const userMessage = {
      role: 'user',
      content: messageInput.value,
      timestamp: new Date().toISOString()
    }
    chatStore.addMessage(userMessage)

    // Connect WebSocket for streaming
    connectWebSocket()

    // Send message via API
    await sendChatMessage({
      thread_id: currentThread.value.id,
      content: messageInput.value,
      attachments: selectedAttachments.value,
      stream: true
    })

    messageInput.value = ''
    selectedAttachments.value = []
    
  } catch (error) {
    console.error('Failed to send message:', error)
  } finally {
    isStreaming.value = false
  }
}

const handleFilesSelected = async (files) => {
  try {
    for (const file of files) {
      const uploaded = await uploadFile(file)
      selectedAttachments.value.push(uploaded)
    }
  } catch (error) {
    console.error('File upload failed:', error)
  }
}

const removeAttachment = (index) => {
  selectedAttachments.value.splice(index, 1)
}

const copyMessageContent = (content) => {
  navigator.clipboard.writeText(content)
  // Show toast notification
  uiStore.showNotification('Copied to clipboard', 'success')
}

const regenerateMessage = (index) => {
  // Get context and regenerate
  const previousMessage = messages.value[index - 1]
  if (previousMessage) {
    messageInput.value = previousMessage.content
  }
}

const editMessage = (index) => {
  const message = messages.value[index]
  if (message.role === 'user') {
    messageInput.value = message.content
    messages.value.splice(index, 1)
  }
}

const updateModel = async () => {
  if (currentThread.value) {
    await frappe.call({
      method: 'frappe.client.set_value',
      args: {
        doctype: 'AI Chat Thread',
        name: currentThread.value.id,
        fieldname: 'model_used',
        value: selectedModel.value
      }
    })
  }
}

const updateThreadSettings = async (settings) => {
  await frappe.call({
    method: 'frappe.client.set_value',
    args: {
      doctype: 'AI Chat Thread',
      name: currentThread.value.id,
      ...settings
    }
  })
  showSettings.value = false
}

const insertSuggestedText = (text) => {
  messageInput.value = text
}

const scrollToBottom = () => {
  nextTick(() => {
    messagesEnd.value?.scrollIntoView({ behavior: 'smooth' })
  })
}

const loadThreads = async () => {
  try {
    const response = await frappe.call({
      method: 'ai_mcp_chat.api.chat.list_chat_threads',
      args: { limit: 20 }
    })
    chatThreads.value = response.message.threads
  } catch (error) {
    console.error('Failed to load threads:', error)
  }
}

const loadModels = async () => {
  try {
    availableModels.value = await frappe.call({
      method: 'frappe.client.get_list',
      args: {
        doctype: 'LLM Model Configuration',
        filters: { is_active: 1 },
        fields: ['name', 'model_name', 'provider']
      }
    })
  } catch (error) {
    console.error('Failed to load models:', error)
  }
}

// Lifecycle
onMounted(async () => {
  await loadThreads()
  await loadModels()

  // Create initial thread if none exists
  if (chatThreads.value.length === 0) {
    await createNewChat()
  } else {
    selectedModel.value = currentThread.value?.model
  }

  // Watch for messages and scroll
  watch(() => messages.value.length, scrollToBottom)
})

onUnmounted(() => {
  disconnectWebSocket()
})
</script>

<style scoped>
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #fff;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e5e5;
  background: #fafafa;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-right {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.model-selector select {
  padding: 0.5rem;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: white;
}

.chat-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 300px;
  border-right: 1px solid #e5e5e5;
  overflow-y: auto;
  background: #f5f5f5;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.suggested-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.action-chip {
  padding: 1rem;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.action-chip:hover {
  border-color: #10a37f;
  background: #f0f8f6;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.streaming-message {
  display: flex;
  gap: 1rem;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.input-section {
  border-top: 1px solid #e5e5e5;
  padding: 1rem;
  background: white;
}

.sidebar-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  
  .chat-header {
    padding: 0.75rem;
  }
  
  .messages-container {
    padding: 1rem;
  }
}
</style>
```

### 6.2 Pinia Store (State Management)

```javascript
// frontend/src/stores/chatStore.js

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  // State
  const currentThread = ref(null)
  const messages = ref([])
  const threads = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // Computed
  const messageCount = computed(() => messages.value.length)
  const lastMessage = computed(() => messages.value[messages.value.length - 1])
  const userMessages = computed(() => 
    messages.value.filter(m => m.role === 'user')
  )
  const assistantMessages = computed(() => 
    messages.value.filter(m => m.role === 'assistant')
  )

  // Actions
  const setCurrentThread = (thread) => {
    currentThread.value = thread
  }

  const setMessages = (newMessages) => {
    messages.value = newMessages
  }

  const addMessage = (message) => {
    messages.value.push({
      ...message,
      id: `msg_${Date.now()}`,
      timestamp: message.timestamp || new Date().toISOString()
    })
  }

  const updateLastMessage = (content) => {
    if (messages.value.length > 0) {
      messages.value[messages.value.length - 1].content = content
    }
  }

  const setThreads = (newThreads) => {
    threads.value = newThreads
  }

  const setLoading = (loading) => {
    isLoading.value = loading
  }

  const setError = (err) => {
    error.value = err
  }

  const clearError = () => {
    error.value = null
  }

  const clearMessages = () => {
    messages.value = []
  }

  return {
    // State
    currentThread,
    messages,
    threads,
    isLoading,
    error,
    
    // Computed
    messageCount,
    lastMessage,
    userMessages,
    assistantMessages,
    
    // Actions
    setCurrentThread,
    setMessages,
    addMessage,
    updateLastMessage,
    setThreads,
    setLoading,
    setError,
    clearError,
    clearMessages
  }
})
```

### 6.3 Composables (Custom Hooks)

```javascript
// frontend/src/composables/useChat.js

import { ref } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import apiService from '@/services/api'

export function useChat() {
  const chatStore = useChatStore()
  const isLoading = ref(false)
  const error = ref(null)

  const createThread = async (title = 'New Chat', systemPrompt = null) => {
    try {
      isLoading.value = true
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.create_chat_thread',
        args: { title, system_prompt: systemPrompt }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getThread = async (threadId) => {
    try {
      isLoading.value = true
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.get_chat_thread',
        args: { thread_id: threadId }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const sendMessage = async (threadId, content, attachments = [], stream = true) => {
    try {
      isLoading.value = true
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.send_message',
        args: {
          thread_id: threadId,
          content,
          attachments,
          stream
        }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const listThreads = async (limit = 20, offset = 0) => {
    try {
      isLoading.value = true
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.list_chat_threads',
        args: { limit, offset }
      })
      chatStore.setThreads(response.message.threads)
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteThread = async (threadId) => {
    try {
      await apiService.call({
        method: 'ai_mcp_chat.api.chat.delete_thread',
        args: { thread_id: threadId }
      })
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const searchConversations = async (query) => {
    try {
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.search_conversations',
        args: { query }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    isLoading,
    error,
    createThread,
    getThread,
    sendMessage,
    listThreads,
    deleteThread,
    searchConversations
  }
}
```

---

## 7. Database Schema

### 7.1 Core Tables

```sql
-- AI Chat Thread
CREATE TABLE `tabAI Chat Thread` (
  `name` VARCHAR(255) PRIMARY KEY,
  `thread_id` VARCHAR(255) UNIQUE NOT NULL,
  `user` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255),
  `description` TEXT,
  `model_used` VARCHAR(255),
  `system_prompt` LONGTEXT,
  `temperature` FLOAT DEFAULT 0.7,
  `max_tokens` INT DEFAULT 2048,
  `is_archived` TINYINT DEFAULT 0,
  `tags` TEXT,
  `metadata` JSON,
  `token_count` INT DEFAULT 0,
  `estimated_cost` DECIMAL(10, 4) DEFAULT 0,
  `creation` DATETIME,
  `modified` DATETIME,
  `modified_by` VARCHAR(255),
  `created_by` VARCHAR(255),
  INDEX `idx_user` (`user`),
  INDEX `idx_thread_id` (`thread_id`),
  INDEX `idx_created` (`creation`)
);

-- AI Chat Message
CREATE TABLE `tabAI Chat Message` (
  `name` VARCHAR(255) PRIMARY KEY,
  `thread` VARCHAR(255) NOT NULL,
  `role` ENUM('user', 'assistant', 'tool'),
  `content` LONGTEXT,
  `content_type` ENUM('text', 'markdown', 'json', 'code'),
  `tool_calls` JSON,
  `tool_results` JSON,
  `model_used` VARCHAR(255),
  `tokens_used` INT DEFAULT 0,
  `input_tokens` INT DEFAULT 0,
  `output_tokens` INT DEFAULT 0,
  `is_edited` TINYINT DEFAULT 0,
  `edited_at` DATETIME,
  `timestamp` DATETIME,
  `creation` DATETIME,
  FOREIGN KEY (`thread`) REFERENCES `tabAI Chat Thread`(`name`),
  INDEX `idx_thread` (`thread`),
  INDEX `idx_role` (`role`),
  INDEX `idx_timestamp` (`timestamp`)
);

-- LLM Model Configuration
CREATE TABLE `tabLLM Model Configuration` (
  `name` VARCHAR(255) PRIMARY KEY,
  `model_name` VARCHAR(255) UNIQUE,
  `provider` ENUM('OpenAI', 'Anthropic', 'Google', 'Local', 'Custom'),
  `api_key_field` VARCHAR(255),
  `base_url` VARCHAR(255),
  `model_identifier` VARCHAR(255),
  `max_tokens` INT DEFAULT 4096,
  `supports_streaming` TINYINT DEFAULT 1,
  `supports_vision` TINYINT DEFAULT 0,
  `supports_tools` TINYINT DEFAULT 1,
  `cost_per_1k_input` DECIMAL(10, 6),
  `cost_per_1k_output` DECIMAL(10, 6),
  `is_active` TINYINT DEFAULT 1,
  `description` TEXT,
  `creation` DATETIME,
  `modified` DATETIME,
  INDEX `idx_provider` (`provider`),
  INDEX `idx_active` (`is_active`)
);

-- MCP Connector
CREATE TABLE `tabMCP Connector` (
  `name` VARCHAR(255) PRIMARY KEY,
  `connector_name` VARCHAR(255),
  `connector_type` ENUM('stdio', 'tcp', 'http'),
  `host` VARCHAR(255),
  `port` INT,
  `command` VARCHAR(255),
  `arguments` JSON,
  `environment_vars` JSON,
  `is_active` TINYINT DEFAULT 1,
  `connection_status` ENUM('Connected', 'Disconnected', 'Error', 'Unknown'),
  `last_tested` DATETIME,
  `tools_available` INT DEFAULT 0,
  `creation` DATETIME,
  `modified` DATETIME,
  INDEX `idx_active` (`is_active`)
);

-- Chat Attachment
CREATE TABLE `tabChat Attachment` (
  `name` VARCHAR(255) PRIMARY KEY,
  `parent` VARCHAR(255),
  `parenttype` VARCHAR(255),
  `file_name` VARCHAR(255),
  `file_path` VARCHAR(255),
  `file_size` INT,
  `file_type` VARCHAR(50),
  `is_processed` TINYINT DEFAULT 0,
  `extracted_content` LONGTEXT,
  `idx` INT,
  FOREIGN KEY (`parent`) REFERENCES `tabAI Chat Message`(`name`)
);

-- User Preferences
CREATE TABLE `tabUser Preferences` (
  `name` VARCHAR(255) PRIMARY KEY,
  `user` VARCHAR(255) UNIQUE,
  `default_model` VARCHAR(255),
  `theme` ENUM('light', 'dark'),
  `auto_save_drafts` TINYINT DEFAULT 1,
  `show_message_timestamps` TINYINT DEFAULT 1,
  `max_file_size` INT DEFAULT 52428800,
  `default_temperature` FLOAT DEFAULT 0.7,
  `metadata` JSON,
  `creation` DATETIME,
  `modified` DATETIME
);
```

---

## 8. API Specifications

### 8.1 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|---|
| POST | `/api/method/ai_mcp_chat.api.chat.create_chat_thread` | Create new thread |
| GET | `/api/method/ai_mcp_chat.api.chat.get_chat_thread` | Get thread with messages |
| GET | `/api/method/ai_mcp_chat.api.chat.list_chat_threads` | List user's threads |
| POST | `/api/method/ai_mcp_chat.api.chat.send_message` | Send message & get response |
| DELETE | `/api/method/ai_mcp_chat.api.chat.delete_thread` | Delete thread |
| GET | `/api/method/ai_mcp_chat.api.chat.search_conversations` | Search conversations |
| POST | `/api/method/ai_mcp_chat.api.connector.add_connector` | Add MCP connector |
| GET | `/api/method/ai_mcp_chat.api.connector.list_connectors` | List connectors |
| POST | `/api/method/ai_mcp_chat.api.file.upload_file` | Upload file |
| GET | `/api/method/ai_mcp_chat.api.llm.get_available_models` | List available models |

### 8.2 WebSocket Events

| Event | Direction | Purpose |
|-------|-----------|---------|
| `message:start` | Server → Client | Message streaming started |
| `message:token` | Server → Client | New token received |
| `message:complete` | Server → Client | Message complete |
| `message:error` | Server → Client | Error occurred |
| `typing:start` | Server → Client | Assistant typing |
| `typing:stop` | Server → Client | Assistant stopped typing |

---

## 9. Frontend Components

### 9.1 Component Hierarchy

```
ChatInterface (root)
├── Header
│   ├── SidebarToggle
│   ├── ThreadTitle
│   ├── ModelSelector
│   ├── SettingsButton
│   └── DeleteButton
├── MainContent
│   ├── Sidebar (ConversationSidebar)
│   │   ├── NewChatButton
│   │   ├── ConversationList
│   │   │   └── ConversationItem (repeating)
│   │   └── ConversationSearch
│   └── MessagesContainer
│       ├── EmptyState (when no messages)
│       │   ├── EmptyIcon
│       │   ├── SuggestedActions
│       │   └── ActionChips
│       └── MessagesList
│           ├── MessageItem (repeating)
│           │   ├── MessageContent
│           │   │   ├── MarkdownRenderer
│           │   │   └── CodeBlock
│           │   ├── MessageActions
│           │   │   ├── CopyButton
│           │   │   ├── RegenerateButton
│           │   │   └── EditButton
│           │   └── MessageMetadata
│           ├── StreamingMessage (during streaming)
│           │   ├── StreamingIndicator
│           │   └── StreamingContent
│           └── Timestamp
├── InputSection
│   ├── FileUpload (modal)
│   ├── AttachmentList
│   │   └── AttachmentItem (repeating)
│   └── InputArea
│       ├── TextInput
│       ├── CharacterCount
│       ├── AttachmentButton
│       └── SendButton
└── Modals
    ├── SettingsModal
    │   ├── ModelSelector
    │   ├── TemperatureSlider
    │   ├── MaxTokensInput
    │   └── SystemPromptEditor
    ├── FilePreviewModal
    └── ConnectorManager
        ├── ConnectorCard (repeating)
        └── ConnectorForm
```

---

## 10. Integration with MCP Protocol

### 10.1 MCP Tool Calling

```python
# ai_mcp_chat/services/tool_executor.py

import frappe
import json
from ai_mcp_chat.services.mcp_client import MCPClient


class ToolExecutor:
    """Execute MCP tools and handle results"""
    
    def __init__(self, thread_doc):
        self.thread_doc = thread_doc
        self.mcp_client = MCPClient()
    
    def get_available_tools(self) -> list:
        """Get all available MCP tools"""
        try:
            connectors = frappe.get_all(
                "MCP Connector",
                filters={"is_active": 1},
                fields=["name"]
            )
            
            tools = []
            for connector in connectors:
                connector_tools = self.mcp_client.get_tools(connector["name"])
                tools.extend(connector_tools)
            
            return tools
        except Exception as e:
            frappe.log_error(str(e), "Get Tools Error")
            return []
    
    def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a specific MCP tool
        
        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
        
        Returns:
            dict: Tool execution result
        """
        try:
            # Find which connector has this tool
            connector_name = self._find_tool_connector(tool_name)
            if not connector_name:
                raise ValueError(f"Tool {tool_name} not found")
            
            # Execute via MCP client
            result = self.mcp_client.execute_tool(
                connector_name,
                tool_name,
                arguments
            )
            
            # Log tool execution
            frappe.log(
                "info",
                f"Tool executed: {tool_name}",
                {"tool": tool_name, "connector": connector_name, "result": result}
            )
            
            return result
        except Exception as e:
            frappe.log_error(str(e), "Tool Execution Error")
            return {"error": str(e)}
    
    def _find_tool_connector(self, tool_name: str) -> str:
        """Find which connector has a tool"""
        connectors = frappe.get_all(
            "MCP Connector",
            filters={"is_active": 1},
            fields=["name"]
        )
        
        for connector in connectors:
            tools = self.mcp_client.get_tools(connector["name"])
            if any(t["name"] == tool_name for t in tools):
                return connector["name"]
        
        return None
```

---

## 11. Security & Authentication

### 11.1 Permission Model

```python
# ai_mcp_chat/decorators/permission_required.py

import frappe
from functools import wraps


def permission_required(doctype, operation):
    """Decorator to check document permissions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if user has permission
            if not frappe.has_permission(doctype, operation):
                frappe.throw(
                    f"You don't have permission to {operation} {doctype}",
                    frappe.PermissionError
                )
            
            # Check rate limiting
            if not check_rate_limit(frappe.session.user, operation):
                frappe.throw(
                    "Rate limit exceeded. Please try again later.",
                    frappe.RateLimitError
                )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def check_rate_limit(user, operation, limit=100, window=3600):
    """Check if user has exceeded rate limit
    
    Args:
        user: User name
        operation: Operation being performed
        limit: Max requests per window
        window: Time window in seconds
    
    Returns:
        bool: True if within limit, False otherwise
    """
    key = f"rate_limit:{user}:{operation}"
    current_count = frappe.cache().get(key) or 0
    
    if current_count >= limit:
        return False
    
    frappe.cache().setex(key, window, current_count + 1)
    return True
```

### 11.2 Data Protection

```python
# Encryption of sensitive data
frappe.get_doc({
    "doctype": "AI Chat Thread",
    ...
}).insert(encrypt_fields=["system_prompt", "metadata"])

# API key management
OPENAI_API_KEY = frappe.get_password("OpenAI Configuration", "api_key")
```

---

## 12. Development Workflow

### 12.1 Setup Instructions

```bash
# 1. Create Frappe bench
bench new-app ai_mcp_chat
cd ai_mcp_chat

# 2. Create DocTypes
bench make-doctype "AI Chat Thread"
bench make-doctype "AI Chat Message"
bench make-doctype "LLM Model Configuration"
bench make-doctype "MCP Connector"

# 3. Create API endpoints
mkdir -p ai_mcp_chat/api
touch ai_mcp_chat/api/__init__.py
touch ai_mcp_chat/api/chat.py
touch ai_mcp_chat/api/connector.py

# 4. Setup frontend
cd frontend
npm install
npm run dev

# 5. Migrate database
bench migrate

# 6. Run development server
bench start
```

### 12.2 Development Commands

```bash
# Start Frappe development server
bench start

# Start Vue development server (in frontend/)
npm run dev

# Build for production
npm run build

# Run tests
pytest tests/

# Run Frappe tests
bench test-site site1.local --module ai_mcp_chat
```

---

## 13. Deployment Guide

### 13.1 Production Deployment

```yaml
# docker-compose.yml

version: '3.8'

services:
  frappe:
    image: frappe/erpnext:latest
    volumes:
      - ./ai_mcp_chat:/home/frappe/frappe-bench/apps/ai_mcp_chat
      - ./sites:/home/frappe/frappe-bench/sites
      - ./bench-config:/home/frappe/frappe-bench/config
    environment:
      - DB_HOST=mariadb
      - DB_PORT=3306
      - REDIS_CACHE=redis-cache:6379
      - REDIS_QUEUE=redis-queue:6379
      - SOCKETIO_REDIS=redis-socketio:6379
    ports:
      - "8000:8000"
    depends_on:
      - mariadb
      - redis-cache
      - redis-queue
      - redis-socketio
    networks:
      - frappe-net

  mariadb:
    image: mariadb:10.6
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_PASSWORD}
      - MYSQL_DATABASE=${DB_NAME}
    volumes:
      - mariadb-data:/var/lib/mysql
    networks:
      - frappe-net

  redis-cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-cache-data:/data
    networks:
      - frappe-net

  redis-queue:
    image: redis:7-alpine
    volumes:
      - redis-queue-data:/data
    networks:
      - frappe-net

  redis-socketio:
    image: redis:7-alpine
    volumes:
      - redis-socketio-data:/data
    networks:
      - frappe-net

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frappe
    networks:
      - frappe-net

volumes:
  mariadb-data:
  redis-cache-data:
  redis-queue-data:
  redis-socketio-data:

networks:
  frappe-net:
    driver: bridge
```

### 13.2 Environment Configuration

```bash
# .env.production

# Database
DB_HOST=mariadb
DB_NAME=ai_mcp_chat_prod
DB_PASSWORD=secure_password_here

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Redis
REDIS_CACHE_URL=redis://redis-cache:6379/0
REDIS_QUEUE_URL=redis://redis-queue:6379/0

# Frappe Settings
FRAPPE_ENVIRONMENT=production
ALLOW_CORS=["https://yourdomain.com"]
ENABLE_TELEMETRY=false

# Security
SECRET_KEY=your_secret_key_here
```

---

## 14. Testing Strategy

### 14.1 Unit Tests

```python
# tests/unit/test_chat_service.py

import unittest
from unittest.mock import patch, MagicMock
from ai_mcp_chat.services.chat_service import ChatService


class TestChatService(unittest.TestCase):
    
    def setUp(self):
        self.chat_service = ChatService()
    
    @patch('ai_mcp_chat.services.llm_service.LLMService')
    def test_generate_response(self, mock_llm):
        """Test response generation"""
        mock_llm.return_value.completion.return_value = {
            "content": "Test response",
            "tokens": 10
        }
        
        thread_doc = MagicMock()
        thread_doc.model_used = "gpt-4"
        thread_doc.system_prompt = "You are helpful"
        
        response = self.chat_service.generate_response(thread_doc)
        
        self.assertEqual(response["content"], "Test response")
        self.assertEqual(response["tokens"], 10)
```

### 14.2 Integration Tests

```python
# tests/integration/test_chat_flow.py

import frappe
from frappe.test_runner import make_test_records


class TestChatFlow(frappe.TestCase):
    
    def setUp(self):
        """Setup test data"""
        make_test_records("User")
    
    def test_create_and_message_flow(self):
        """Test complete chat flow"""
        # Create thread
        thread = frappe.get_doc({
            "doctype": "AI Chat Thread",
            "thread_id": "test-123",
            "user": "Administrator",
            "title": "Test Chat"
        }).insert()
        
        # Add message
        message = frappe.get_doc({
            "doctype": "AI Chat Message",
            "thread": thread.name,
            "role": "user",
            "content": "Hello"
        }).insert()
        
        self.assertEqual(message.thread, thread.name)
        self.assertEqual(message.role, "user")
```

### 14.3 E2E Tests

```javascript
// tests/e2e/test_ui_flow.spec.js

describe('Chat UI Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000/app/ai-mcp-chat')
    cy.login('Administrator')
  })

  it('should create a new chat', () => {
    cy.get('[data-testid="new-chat-button"]').click()
    cy.get('[data-testid="chat-input"]').should('be.visible')
  })

  it('should send a message', () => {
    cy.get('[data-testid="chat-input"]').type('Hello, how are you?')
    cy.get('[data-testid="send-button"]').click()
    cy.get('[data-testid="message-item"]').should('have.length', 2)
  })

  it('should handle file uploads', () => {
    cy.get('[data-testid="upload-button"]').click()
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf')
    cy.get('[data-testid="attachment-item"]').should('be.visible')
  })
})
```

---

## 15. Troubleshooting & Best Practices

### 15.1 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| WebSocket connection fails | CORS misconfiguration | Update `allow_cors` in config |
| Streaming responses lag | Network latency | Check Redis/WebSocket performance |
| File upload fails | Size limit exceeded | Increase `post_max_size` in config |
| Model not responding | API key invalid | Verify API keys in environment |
| Permission errors | User lacks DocType permissions | Grant appropriate user roles |

### 15.2 Performance Optimization

```python
# 1. Database indexing
db.create_index("tabAI Chat Thread", ["user", "modified"])
db.create_index("tabAI Chat Message", ["thread", "timestamp"])

# 2. Query optimization
# Use select to get only needed fields
messages = frappe.get_all(
    "AI Chat Message",
    filters={"thread": thread_id},
    fields=["name", "role", "content"],  # Only needed fields
    limit_page_length=50
)

# 3. Caching
frappe.cache().set_value(
    f"thread_messages:{thread_id}",
    messages,
    expires_in_sec=300
)

# 4. Async processing
frappe.enqueue(
    'ai_mcp_chat.services.file_service.process_file_async',
    file_path=file_path,
    thread_id=thread_id
)
```

### 15.3 Best Practices

1. **Rate Limiting**: Always implement rate limiting on chat endpoints
2. **Error Handling**: Return meaningful error messages to users
3. **Logging**: Log all API calls for debugging and compliance
4. **Validation**: Validate user input before processing
5. **Security**: Never log API keys or sensitive data
6. **Testing**: Write tests for critical paths
7. **Documentation**: Keep API documentation up-to-date
8. **Monitoring**: Setup alerts for errors and performance issues

---

## Conclusion

This unified document provides a complete specification for building a production-ready AI MCP Chat application using Frappe + Vue 3 + Frappe UI. The solution combines the best of both worlds:

- **Frappe's robust backend** for data management, permissions, and audit trails
- **Vue 3's modern frontend** with Frappe UI components for a native Frappe experience
- **Real-time streaming** via WebSocket for a responsive chat interface
- **Multi-model LLM support** through LiteLLM abstraction layer
- **MCP protocol integration** for extensible tool support

The architecture is designed for scalability, security, and extensibility. Follow the development phases as outlined, and refer to the API specifications and component hierarchy for implementation details.

For any clarifications or additional requirements, refer to the official Frappe documentation, Vue 3 guide, and Model Context Protocol specification.

---

**Document Metadata**
- **Version**: 2.0
- **Last Updated**: October 26, 2025
- **Status**: Production-Ready
- **Maintainers**: Development Team
- **Next Review**: Q1 2026
