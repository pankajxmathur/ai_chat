app_name = "ai_mcp_chat"
app_title = "AI MCP Chat"
app_publisher = "Your Company"
app_description = "AI Chat interface with MCP support for Frappe"
app_version = "1.0.0"
app_license = "MIT"

# Include doctypes
include_doctypes = {
    "doctype": [
        "AI Chat Thread",
        "AI Chat Message",
        "LLM Model Configuration",
        "MCP Connector",
        "MCP Tool",
        "Chat Attachment",
        "User Preferences"
    ]
}

# Fixtures
fixtures = [
    {"doctype": "LLM Model Configuration"},
    {"doctype": "MCP Connector"}
]

# Initialize hooks
on_session_creation = "ai_mcp_chat.api.auth.on_session_creation"

# WebSocket events
websocket_events = [
    "ai_mcp_chat.api.streaming:stream_message"
]

# Scheduled jobs
scheduler_events = {
    "daily": [
        "ai_mcp_chat.services.cleanup_service:cleanup_old_chats"
    ]
}
