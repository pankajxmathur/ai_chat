# Claude Code Quick Start Guide - Frappe AI MCP Chat App

## Overview

This guide provides step-by-step instructions for Claude Code (or any developer) to build the AI MCP Chat Frappe application from scratch. Each phase has specific commands and file implementations.

---

## Phase 0: Environment Setup (30 minutes)

### Step 1: Initialize Project

```bash
# Create main Frappe bench directory
mkdir -p ~/frappe-workspace && cd ~/frappe-workspace

# Clone Frappe framework
git clone https://github.com/frappe/frappe.git --depth 1
cd frappe

# Create Python virtual environment
python3 -m venv env
source env/bin/activate

# Install Frappe
pip install --upgrade pip
pip install -e .

# Create bench
cd ~/frappe-workspace
bench init frappe-bench
cd frappe-bench

# Create site
bench new-site site1.local

# Create app
bench new-app ai_mcp_chat
cd apps/ai_mcp_chat
```

### Step 2: Create Directory Structure

```bash
# Backend directories
mkdir -p ai_mcp_chat/{api,services,decorators,utils,migrations}
touch ai_mcp_chat/__init__.py
touch ai_mcp_chat/api/__init__.py
touch ai_mcp_chat/services/__init__.py
touch ai_mcp_chat/decorators/__init__.py
touch ai_mcp_chat/utils/__init__.py

# Frontend directories (Vue 3 SPA)
mkdir -p frontend/src/{components,stores,services,composables,utils,assets}
cd frontend
touch package.json vite.config.js tailwind.config.js
cd src
touch main.js App.vue
mkdir -p {components/{chat,files,connectors,settings,sidebar,common},assets/styles,router}
```

### Step 3: Create DocTypes

```bash
cd ~/frappe-workspace/frappe-bench

# Create DocTypes
bench make-doctype "AI Chat Thread"
bench make-doctype "AI Chat Message"  
bench make-doctype "LLM Model Configuration"
bench make-doctype "MCP Connector"
bench make-doctype "MCP Tool"
bench make-doctype "Chat Attachment"
bench make-doctype "User Preferences"

# Activate
bench --site site1.local enable-development-mode
```

---

## Phase 1: Backend Setup (Days 1-2)

### File 1: `ai_mcp_chat/hooks.py`

```python
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
```

### File 2: `ai_mcp_chat/doctype/ai_chat_thread/ai_chat_thread.json`

```json
{
  "doctype": "AI Chat Thread",
  "module": "AI MCP Chat",
  "label": "AI Chat Thread",
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
      "read_only": 1
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
      "reqd": 1
    },
    {
      "fieldname": "description",
      "label": "Description",
      "fieldtype": "Text"
    },
    {
      "fieldname": "model_used",
      "label": "Model",
      "fieldtype": "Link",
      "options": "LLM Model Configuration",
      "reqd": 1
    },
    {
      "fieldname": "system_prompt",
      "label": "System Prompt",
      "fieldtype": "Text Editor"
    },
    {
      "fieldname": "temperature",
      "label": "Temperature",
      "fieldtype": "Float",
      "default": 0.7
    },
    {
      "fieldname": "max_tokens",
      "label": "Max Tokens",
      "fieldtype": "Int",
      "default": 2048
    },
    {
      "fieldname": "is_archived",
      "label": "Archived",
      "fieldtype": "Check"
    },
    {
      "fieldname": "token_count",
      "label": "Total Tokens",
      "fieldtype": "Int",
      "read_only": 1,
      "default": 0
    }
  ],
  "permissions": [
    {
      "role": "All",
      "permlevel": 0,
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ]
}
```

### File 3: `ai_mcp_chat/doctype/ai_chat_thread/ai_chat_thread.py`

```python
import frappe
from frappe.model.document import Document
import uuid
from datetime import datetime


class AIChatThread(Document):
    """AI Chat Thread model"""
    
    def before_insert(self):
        """Generate thread_id before creation"""
        if not self.thread_id:
            self.thread_id = str(uuid.uuid4())
        
        if not self.user:
            self.user = frappe.session.user
    
    def after_insert(self):
        """Log thread creation"""
        frappe.log("info", f"Chat thread created: {self.thread_id}")
    
    def before_delete(self):
        """Delete associated messages"""
        frappe.db.delete("AI Chat Message", {"thread": self.name})
```

### File 4: `ai_mcp_chat/api/chat.py`

```python
import frappe
import json
import uuid
from frappe import throw
from datetime import datetime


@frappe.whitelist()
def create_chat_thread(title=None, system_prompt=None, model=None):
    """Create new chat thread"""
    try:
        thread_id = str(uuid.uuid4())
        
        if not model:
            model = frappe.db.get_value(
                "LLM Model Configuration",
                {"is_active": 1},
                "name"
            )
            if not model:
                throw("No active LLM model configured")
        
        doc = frappe.get_doc({
            "doctype": "AI Chat Thread",
            "thread_id": thread_id,
            "user": frappe.session.user,
            "title": title or "New Chat",
            "system_prompt": system_prompt or "You are helpful",
            "model_used": model,
        })
        doc.insert()
        frappe.db.commit()
        
        return {
            "success": True,
            "thread_id": thread_id,
            "docname": doc.name
        }
    except Exception as e:
        frappe.log_error(str(e), "Create Thread")
        throw(str(e))


@frappe.whitelist()
def get_chat_thread(thread_id):
    """Get thread with messages"""
    try:
        thread_doc = frappe.get_doc(
            "AI Chat Thread",
            {"thread_id": thread_id, "user": frappe.session.user}
        )
        
        messages = frappe.get_all(
            "AI Chat Message",
            filters={"thread": thread_doc.name},
            fields=["name", "role", "content", "timestamp"],
            order_by="timestamp asc"
        )
        
        return {
            "success": True,
            "thread": {
                "id": thread_doc.thread_id,
                "title": thread_doc.title,
                "model": thread_doc.model_used,
                "created": thread_doc.creation
            },
            "messages": messages
        }
    except Exception as e:
        frappe.log_error(str(e), "Get Thread")
        throw(str(e))


@frappe.whitelist()
def list_chat_threads(limit=20, offset=0):
    """List user's threads"""
    try:
        threads = frappe.get_all(
            "AI Chat Thread",
            filters={"user": frappe.session.user},
            fields=["name", "thread_id", "title", "modified"],
            order_by="modified desc",
            limit_page_length=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "threads": threads
        }
    except Exception as e:
        frappe.log_error(str(e), "List Threads")
        throw(str(e))


@frappe.whitelist()
def send_message(thread_id, content, stream=True):
    """Send message and get response"""
    try:
        from ai_mcp_chat.services.chat_service import ChatService
        
        thread_doc = frappe.get_doc(
            "AI Chat Thread",
            {"thread_id": thread_id, "user": frappe.session.user}
        )
        
        # Save user message
        user_msg = frappe.get_doc({
            "doctype": "AI Chat Message",
            "thread": thread_doc.name,
            "role": "user",
            "content": content
        })
        user_msg.insert()
        frappe.db.commit()
        
        # Get AI response
        service = ChatService()
        response = service.generate_response(thread_doc)
        
        return {
            "success": True,
            "user_message_id": user_msg.name,
            "response": response
        }
    except Exception as e:
        frappe.log_error(str(e), "Send Message")
        throw(str(e))


@frappe.whitelist()
def delete_thread(thread_id):
    """Delete thread"""
    try:
        thread_doc = frappe.get_doc(
            "AI Chat Thread",
            {"thread_id": thread_id, "user": frappe.session.user}
        )
        frappe.db.delete("AI Chat Message", {"thread": thread_doc.name})
        thread_doc.delete(force=True)
        frappe.db.commit()
        
        return {"success": True}
    except Exception as e:
        frappe.log_error(str(e), "Delete Thread")
        throw(str(e))
```

### File 5: `ai_mcp_chat/services/llm_service.py`

```python
import frappe
import os
from typing import Generator, List, Dict


class LLMService:
    """Multi-provider LLM service"""
    
    def stream_completion(self, model: str, messages: List[Dict],
                         system_prompt: str, temperature: float,
                         max_tokens: int, provider: str) -> Generator:
        """Stream LLM completion"""
        
        if provider == "OpenAI":
            yield from self._openai_stream(
                model, messages, system_prompt, temperature, max_tokens
            )
        elif provider == "Anthropic":
            yield from self._anthropic_stream(
                model, messages, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _openai_stream(self, model: str, messages: List[Dict],
                      system_prompt: str, temperature: float,
                      max_tokens: int) -> Generator:
        """OpenAI streaming"""
        try:
            import openai
            
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            
            client = openai.OpenAI(api_key=api_key)
            
            system_msg = {"role": "system", "content": system_prompt}
            all_msgs = [system_msg] + messages if system_prompt else messages
            
            with client.messages.stream(
                model=model,
                messages=all_msgs,
                temperature=temperature,
                max_tokens=max_tokens
            ) as stream:
                for text in stream.text_stream:
                    yield {
                        "content": text,
                        "tokens": 0
                    }
        except Exception as e:
            frappe.log_error(str(e), "OpenAI Stream")
            raise
    
    def _anthropic_stream(self, model: str, messages: List[Dict],
                         system_prompt: str, temperature: float,
                         max_tokens: int) -> Generator:
        """Anthropic Claude streaming"""
        try:
            import anthropic
            
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            
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
                        "tokens": 0
                    }
        except Exception as e:
            frappe.log_error(str(e), "Anthropic Stream")
            raise
```

### File 6: `ai_mcp_chat/services/chat_service.py`

```python
import frappe
from ai_mcp_chat.services.llm_service import LLMService


class ChatService:
    """Core chat operations"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def generate_response(self, thread_doc):
        """Generate AI response"""
        try:
            # Get messages
            messages = frappe.get_all(
                "AI Chat Message",
                filters={"thread": thread_doc.name},
                fields=["role", "content"],
                order_by="timestamp asc"
            )
            
            # Get model config
            model_config = frappe.get_doc(
                "LLM Model Configuration",
                thread_doc.model_used
            )
            
            # Format messages
            formatted_msgs = [
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ]
            
            # Stream response
            accumulated = ""
            for chunk in self.llm_service.stream_completion(
                model=model_config.model_identifier,
                messages=formatted_msgs,
                system_prompt=thread_doc.system_prompt,
                temperature=thread_doc.temperature,
                max_tokens=thread_doc.max_tokens,
                provider=model_config.provider
            ):
                accumulated += chunk.get("content", "")
            
            # Save assistant message
            response_msg = frappe.get_doc({
                "doctype": "AI Chat Message",
                "thread": thread_doc.name,
                "role": "assistant",
                "content": accumulated,
                "model_used": model_config.model_identifier
            })
            response_msg.insert()
            frappe.db.commit()
            
            return {
                "success": True,
                "content": accumulated,
                "message_id": response_msg.name
            }
        except Exception as e:
            frappe.log_error(str(e), "Generate Response")
            raise
```

### File 7: `requirements.txt`

```
frappe==14.0.0
erpnext==14.0.0
openai>=1.0.0
anthropic>=0.7.0
python-socketio>=5.9.0
redis>=5.0.0
```

---

## Phase 2: Frontend Setup (Days 3-4)

### File 8: `frontend/package.json`

```json
{
  "name": "ai-mcp-chat-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src",
    "test": "vitest"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.0",
    "axios": "^1.6.0",
    "socket.io-client": "^4.7.0",
    "marked": "^11.0.0",
    "highlight.js": "^11.8.0",
    "lucide-vue-next": "^0.263.0",
    "dayjs": "^1.11.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.52.0",
    "vitest": "^0.34.0"
  }
}
```

### File 9: `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/method': 'http://localhost:8000',
      '/socket.io': {
        target: 'http://localhost:8000',
        ws: true
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
```

### File 10: `frontend/src/main.js`

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/styles/main.css'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
```

### File 11: `frontend/src/App.vue`

```vue
<template>
  <div id="app" class="app-container">
    <ChatInterface />
  </div>
</template>

<script setup>
import ChatInterface from './components/chat/ChatInterface.vue'
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

#app {
  height: 100vh;
}
</style>
```

### File 12: `frontend/src/stores/chatStore.js`

```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const currentThread = ref(null)
  const messages = ref([])
  const isLoading = ref(false)

  const messageCount = computed(() => messages.value.length)

  const setCurrentThread = (thread) => {
    currentThread.value = thread
  }

  const setMessages = (msgs) => {
    messages.value = msgs
  }

  const addMessage = (msg) => {
    messages.value.push(msg)
  }

  const clearMessages = () => {
    messages.value = []
  }

  return {
    currentThread,
    messages,
    isLoading,
    messageCount,
    setCurrentThread,
    setMessages,
    addMessage,
    clearMessages
  }
})
```

### File 13: `frontend/src/services/api.js`

```javascript
import axios from 'axios'

const BASE_URL = '/api'

const apiService = {
  call: async (config) => {
    try {
      const response = await axios.post(`${BASE_URL}/method/${config.method}`, 
        config.args || {}
      )
      return response.data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  get: async (endpoint, params = {}) => {
    const response = await axios.get(`${BASE_URL}${endpoint}`, { params })
    return response.data
  },

  post: async (endpoint, data = {}) => {
    const response = await axios.post(`${BASE_URL}${endpoint}`, data)
    return response.data
  }
}

export default apiService
```

### File 14: `frontend/src/composables/useChat.js`

```javascript
import { ref } from 'vue'
import apiService from '@/services/api'

export function useChat() {
  const isLoading = ref(false)
  const error = ref(null)

  const createThread = async (title) => {
    try {
      isLoading.value = true
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.create_chat_thread',
        args: { title }
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
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.get_chat_thread',
        args: { thread_id: threadId }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const sendMessage = async (threadId, content) => {
    try {
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.send_message',
        args: { thread_id: threadId, content }
      })
      return response.message
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const listThreads = async () => {
    try {
      const response = await apiService.call({
        method: 'ai_mcp_chat.api.chat.list_chat_threads'
      })
      return response.message.threads
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
    listThreads
  }
}
```

### File 15: `frontend/src/components/chat/ChatInterface.vue`

```vue
<template>
  <div class="chat-interface">
    <div class="chat-header">
      <h1>{{ currentThread?.title || 'New Chat' }}</h1>
      <button @click="createNewChat" class="btn-new">+ New Chat</button>
    </div>
    
    <div class="chat-content">
      <div class="messages">
        <div v-for="msg in messages" :key="msg.name" class="message"
             :class="msg.role">
          <p>{{ msg.content }}</p>
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <textarea v-model="inputText" 
                @keydown.enter="sendMessage"
                placeholder="Message..."></textarea>
      <button @click="sendMessage" :disabled="isLoading">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import { useChat } from '@/composables/useChat'

const chatStore = useChatStore()
const { createThread, getThread, sendMessage: sendChatMessage, listThreads } = useChat()

const inputText = ref('')
const isLoading = ref(false)

const currentThread = computed(() => chatStore.currentThread)
const messages = computed(() => chatStore.messages)

const createNewChat = async () => {
  try {
    const thread = await createThread('New Chat')
    chatStore.setCurrentThread(thread)
    chatStore.setMessages([])
    inputText.value = ''
  } catch (error) {
    console.error('Failed:', error)
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim()) return

  try {
    isLoading.value = true
    const response = await sendChatMessage(
      currentThread.value.thread_id,
      inputText.value
    )
    
    const threadData = await getThread(currentThread.value.thread_id)
    chatStore.setMessages(threadData.messages)
    inputText.value = ''
  } catch (error) {
    console.error('Failed:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  try {
    const threads = await listThreads()
    if (threads.length > 0) {
      const threadData = await getThread(threads[0].thread_id)
      chatStore.setCurrentThread(threadData.thread)
      chatStore.setMessages(threadData.messages)
    } else {
      await createNewChat()
    }
  } catch (error) {
    console.error('Failed to load:', error)
  }
})
</script>

<style scoped>
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-header {
  padding: 1rem;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  padding: 1rem;
  border-radius: 8px;
  max-width: 70%;
}

.message.user {
  background: #10a37f;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background: #f0f0f0;
  color: black;
}

.input-area {
  padding: 1rem;
  border-top: 1px solid #e5e5e5;
  display: flex;
  gap: 0.5rem;
}

textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
}

.btn-new {
  padding: 0.5rem 1rem;
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

---

## Phase 3: Testing & Deployment (Days 5-6)

### File 16: `docker-compose.yml`

```yaml
version: '3.8'

services:
  frappe:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=mariadb
      - REDIS_CACHE=redis:6379
      - REDIS_QUEUE=redis:6379
    depends_on:
      - mariadb
      - redis
    volumes:
      - ./ai_mcp_chat:/home/frappe/frappe-bench/apps/ai_mcp_chat

  mariadb:
    image: mariadb:10.6
    environment:
      - MYSQL_ROOT_PASSWORD=admin
    volumes:
      - mariadb-data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  mariadb-data:
  redis-data:
```

### File 17: `.env.example`

```bash
# Database
DB_HOST=mariadb
DB_NAME=ai_mcp_chat
DB_PASSWORD=admin

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Application
FRAPPE_ENVIRONMENT=development
SECRET_KEY=your-secret-key
```

### File 18: `tests/unit/test_chat_service.py`

```python
import unittest
from unittest.mock import patch, MagicMock
from ai_mcp_chat.services.chat_service import ChatService


class TestChatService(unittest.TestCase):
    
    def test_generate_response(self):
        """Test response generation"""
        service = ChatService()
        
        thread_doc = MagicMock()
        thread_doc.name = "test-thread"
        thread_doc.system_prompt = "Test prompt"
        
        with patch('frappe.get_all') as mock_get_all:
            mock_get_all.return_value = [
                {"role": "user", "content": "Hello"}
            ]
            
            # Test would call service method
            # Result should have success=True


if __name__ == '__main__':
    unittest.main()
```

---

## Deployment Commands

### Local Development

```bash
# Terminal 1: Start Frappe
cd ~/frappe-workspace/frappe-bench
bench start

# Terminal 2: Start Vue dev server
cd ~/frappe-workspace/frappe-bench/apps/ai_mcp_chat/frontend
npm install
npm run dev

# Access at http://localhost:8000/app/ai-mcp-chat
```

### Production Deployment

```bash
# Build Docker image
docker-compose build

# Run containers
docker-compose up -d

# Create database
docker-compose exec frappe bench new-site site1.local

# Migrate
docker-compose exec frappe bench --site site1.local migrate

# Enable app
docker-compose exec frappe bench --site site1.local install-app ai_mcp_chat
```

---

## Step-by-Step Execution Checklist

### Week 1
- [ ] Setup environment (Phase 0)
- [ ] Create all DocTypes
- [ ] Implement backend API (chat.py)
- [ ] Implement LLM service
- [ ] Test backend endpoints

### Week 2
- [ ] Create Vue components
- [ ] Setup Pinia stores
- [ ] Implement API service layer
- [ ] Create composables
- [ ] Test frontend integration

### Week 3
- [ ] Add MCP connector support
- [ ] Implement file upload
- [ ] Add streaming responses
- [ ] Build conversation sidebar
- [ ] Add settings panel

### Week 4
- [ ] Write comprehensive tests
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation
- [ ] Docker setup

---

## Resources & Documentation

- **Full Spec**: `FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md`
- **Implementation Guide**: `IMPLEMENTATION_SUMMARY.md`
- **Frappe Docs**: https://frappeframework.com
- **Vue 3 Docs**: https://vuejs.org
- **MCP Spec**: https://spec.modelcontextprotocol.io

---

**Status**: Ready to implement  
**Last Updated**: October 26, 2025  
**Version**: 1.0
