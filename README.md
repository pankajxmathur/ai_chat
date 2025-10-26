# Frappe AI MCP Chat - AI Chatbot Application

## 📋 Overview

A complete, production-ready AI chatbot application built as a Frappe app with Vue 3 frontend. Features multi-provider LLM support (OpenAI, Anthropic, Google), real-time streaming, conversation management, and MCP protocol integration.

**Status**: ✅ **Production-Ready & Implemented**
**Last Updated**: October 26, 2025
**Version**: 1.0.0

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- MariaDB 10.6+ (or Docker)
- Redis 6.0+ (or Docker)
- Git

### Installation (Docker - Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/pankajxmathur/ai_chat.git
cd ai_chat

# 2. Create environment file
cp .env.example .env

# 3. Edit .env and add your LLM API keys
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...

# 4. Start services with Docker Compose
docker-compose up -d

# 5. Create Frappe site (first time only)
docker-compose exec frappe bench new-site site1.local --admin-password admin

# 6. Install the app
docker-compose exec frappe bench --site site1.local install-app ai_mcp_chat

# 7. Access the application
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Manual Installation (Development)

```bash
# 1. Install Frappe
bench init frappe-bench
cd frappe-bench

# 2. Create site
bench new-site site1.local

# 3. Get the app
bench get-app ai_mcp_chat https://github.com/pankajxmathur/ai_chat.git

# 4. Install dependencies
cd apps/ai_mcp_chat
pip install -r requirements.txt

# 5. Install the app to site
bench --site site1.local install-app ai_mcp_chat

# 6. Set environment variables
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...

# 7. Start Frappe
bench start

# 8. In a new terminal, start frontend
cd apps/ai_mcp_chat/frontend
npm install
npm run dev
```

### Configuration

After installation, configure your LLM models:

1. Log in to Frappe at http://localhost:8000
2. Navigate to: **AI MCP Chat** > **LLM Model Configuration**
3. Click **New** and create a configuration:
   - **Model Name**: GPT-4 (or your choice)
   - **Provider**: OpenAI (or Anthropic/Google)
   - **Model Identifier**: gpt-4 (or claude-3-opus/gemini-pro)
   - **API Key Field Name**: OPENAI_API_KEY
   - **Is Active**: ✓ Checked
4. **Save**

### Start Chatting

1. Access the chat interface at http://localhost:5173
2. Click **"+ New Chat"**
3. Type your message and press Enter
4. The AI will respond in real-time!

---

## ✨ Features

✅ **Multi-Model LLM Support**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)
- Google (Gemini)
- Easy to add custom providers

✅ **Real-Time Chat**
- Streaming responses
- Typing indicators
- Instant message updates

✅ **Conversation Management**
- Create/delete chat threads
- Persistent conversation history
- User-specific threads
- Token tracking and cost estimation

✅ **Modern UI**
- Vue 3 + Pinia state management
- Responsive design
- Clean, intuitive interface
- Mobile-friendly

✅ **Production-Ready**
- Docker deployment
- Comprehensive error handling
- Security best practices
- Audit logging

✅ **MCP Protocol Support**
- Connect external tools
- Extensible architecture
- Tool execution framework

---

## 🏗️ Architecture

```
Frontend (Vue 3)     Backend (Frappe/Python)     External Services
    │                        │                         │
    ├─ ChatInterface         ├─ API Endpoints         ├─ OpenAI API
    ├─ Pinia Stores    →     ├─ Chat Service     →    ├─ Anthropic API
    ├─ Composables           ├─ LLM Service           └─ Google AI
    └─ API Service           └─ MCP Service
         │                        │
         └────── REST/WebSocket ──┘
                      │
              ┌───────┴────────┐
              │                │
         MariaDB            Redis
      (Conversations)     (Cache)
```

## 🛠️ Technology Stack

**Backend:**
- Frappe Framework (Python)
- MariaDB/PostgreSQL
- Redis
- RQ (Background Jobs)

**Frontend:**
- Vue 3
- Pinia (State Management)
- Vite (Build Tool)
- Axios (HTTP Client)

**LLM Providers:**
- OpenAI SDK
- Anthropic SDK
- Google Generative AI

**Infrastructure:**
- Docker & Docker Compose
- Nginx (Production)

## 📂 Project Structure

```
ai_chat/
├── ai_mcp_chat/              # Backend Frappe App
│   ├── api/
│   │   └── chat.py          # REST API endpoints
│   ├── services/
│   │   ├── chat_service.py  # Chat orchestration
│   │   └── llm_service.py   # Multi-provider LLM
│   ├── doctype/
│   │   ├── ai_chat_thread/  # Conversation model
│   │   ├── ai_chat_message/ # Message model
│   │   ├── llm_model_configuration/
│   │   └── mcp_connector/
│   └── hooks.py
├── frontend/                 # Vue 3 Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── composables/
│   │   └── services/
│   └── package.json
├── docker-compose.yml
├── requirements.txt
└── SETUP.md
```

## 🔧 Troubleshooting

### Common Issues

**"No active LLM model configured"**
- Create an LLM Model Configuration in Frappe
- Set `is_active` to checked

**API Key Errors**
- Verify environment variables are set in `.env`
- Check: `echo $OPENAI_API_KEY`

**Frontend can't connect to backend**
- Ensure Frappe is running on port 8000
- Check proxy settings in `frontend/vite.config.js`

**Database connection errors**
- Verify MariaDB is running
- Check credentials in `site_config.json`

For more troubleshooting, see [SETUP.md](SETUP.md)

---

## 📚 Complete Documentation

This repository contains a comprehensive documentation set (5,377 lines across 4 guides):

## 📚 Document Guide

### 1. **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** (2,889 lines) ⭐ START HERE
**Purpose**: Comprehensive technical specification document  
**Audience**: Developers, Architects, Project Managers  
**Format**: Full markdown with code examples

**Contains:**
- Complete system architecture diagram
- Detailed backend implementation (Python/Frappe)
- Frontend implementation (Vue 3/Frappe UI)
- Database schema design
- API specifications (REST + WebSocket)
- All DocType definitions with full JSON
- Core services (LLM, MCP, streaming, file handling)
- Pinia store patterns
- Vue 3 composables
- Security & authentication details
- Deployment guide with Docker
- Testing strategy
- Troubleshooting guide

**Key Sections:**
- Executive Summary: What this app does
- Architecture Overview: System design
- Technology Stack: All technologies used
- Backend Implementation: 5+ complete Python files
- Frontend Implementation: Main Vue 3 components
- API Specifications: All endpoints documented
- Development Workflow: Setup instructions
- Deployment Guide: Docker & production setup

**When to Use:**
- To understand the complete solution architecture
- To reference technical specifications
- For comprehensive API documentation
- To review database schema design
- For implementation details and best practices

---

### 2. **IMPLEMENTATION_SUMMARY.md** (471 lines)
**Purpose**: Quick reference guide with implementation timeline  
**Audience**: Project Managers, Team Leads, Developers  
**Format**: Concise markdown with checklists and tables

**Contains:**
- Quick reference table: What changed from original
- Advantages of Frappe + Vue 3 approach
- Project structure overview
- 6-phase implementation timeline (8 weeks)
- File checklist (65+ files to create)
- Backend files list with descriptions
- Frontend components list with purposes
- Database schema quick reference
- Key API endpoints summary
- Development environment setup
- Security checklist
- Performance optimization tips
- Troubleshooting quick fixes

**Key Sections:**
- Summary: High-level overview
- Migration comparison: Original vs New
- Implementation phases: Week-by-week breakdown
- File checklist: Track progress
- Key API endpoints: Quick lookup
- Development setup: Commands to run
- Troubleshooting: Common issues and fixes

**When to Use:**
- To get a quick overview of the project
- To track implementation progress
- To understand which phase to work on
- To quickly reference key API endpoints
- To find troubleshooting solutions

---

### 3. **CLAUDE_CODE_QUICKSTART.md** (1,162 lines)
**Purpose**: Step-by-step implementation guide for Claude Code or developers  
**Audience**: Developers implementing the app  
**Format**: Executable commands with code files

**Contains:**
- Phase 0: Environment setup (30 minutes)
- Phase 1: Backend setup with 7 complete Python files
- Phase 2: Frontend setup with 8 complete Vue files
- Phase 3: Testing & deployment
- Specific commands to execute at each step
- Complete code for each file (ready to copy-paste)
- Docker Compose setup
- Environment configuration (.env.example)
- Unit tests examples
- Deployment commands
- Step-by-step execution checklist (4 weeks)
- Resource links

**Key Files Provided:**
- `hooks.py` - App configuration
- `ai_chat_thread.json/.py` - First DocType
- `ai_chat_message.json` - Second DocType
- `api/chat.py` - All chat endpoints
- `services/llm_service.py` - Multi-provider LLM
- `services/chat_service.py` - Core chat logic
- `requirements.txt` - Python dependencies
- `package.json` - Frontend dependencies
- `vite.config.js` - Build configuration
- `ChatInterface.vue` - Main UI component
- `chatStore.js` - State management
- `useChat.js` - Composable hooks
- `api.js` - API service layer
- And 8+ more files...

**Key Sections:**
- Phase 0: Initial setup (copy-paste ready)
- Phase 1: Backend files (complete code)
- Phase 2: Frontend files (complete code)
- Phase 3: Tests & deployment
- Local development commands
- Production deployment commands
- Execution checklist

**When to Use:**
- **For actual implementation** - Start here with Claude Code
- When you need exact commands to run
- When you need ready-to-use code files
- To execute phase by phase
- To track implementation progress

---

### 4. **ARCHITECTURE_DIAGRAMS.md** (855 lines)
**Purpose**: Visual reference with ASCII diagrams and flows  
**Audience**: Architects, Technical Leads, Developers  
**Format**: ASCII diagrams and text-based visual references

**Contains:**
- System architecture diagram (full)
- Data flow diagrams:
  - User message flow (complete)
  - File upload & processing flow
  - MCP tool execution flow
- Component communication diagram
- Database relationship diagram (ER)
- Request/response flows for key operations
- Session lifecycle diagram
- Error handling flow
- Performance optimization points
- Security layers architecture
- Deployment architecture
- Component state diagram (Pinia)

**Key Diagrams:**
1. **System Architecture** - Shows all layers (frontend, backend, LLM)
2. **User Message Flow** - How a message goes from UI to response
3. **File Upload Flow** - How files are uploaded and processed
4. **MCP Tool Execution** - How tools are called and results returned
5. **Component Communication** - Vue components interaction
6. **Database Relationships** - How DocTypes relate
7. **Security Layers** - Security architecture (7 layers)
8. **Deployment Layout** - Production infrastructure

**When to Use:**
- To understand system architecture visually
- To explain the system to stakeholders
- To debug data flow issues
- To understand component relationships
- To review security architecture
- To plan deployment infrastructure

---

## 🎯 Getting Started

### For Project Managers/Architects:
1. Read **IMPLEMENTATION_SUMMARY.md** (30 min) - Get the overview
2. Review **ARCHITECTURE_DIAGRAMS.md** (20 min) - Understand the design
3. Reference **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** as needed (1-2 hours)

### For Developers (Using Claude Code):
1. Start with **CLAUDE_CODE_QUICKSTART.md** - Phase 0 setup (30 min)
2. Follow Phase 1 (Days 1-2) - Backend implementation
3. Follow Phase 2 (Days 3-4) - Frontend implementation
4. Follow Phase 3 (Days 5-6) - Testing & deployment
5. Reference **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** for detailed explanations

### For Architects/Technical Leads:
1. Read **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** completely (2-3 hours)
2. Review **ARCHITECTURE_DIAGRAMS.md** (30 min)
3. Understand **IMPLEMENTATION_SUMMARY.md** phases (30 min)
4. Reference **CLAUDE_CODE_QUICKSTART.md** for specific implementations

---

## 📊 Document Statistics

| Document | Lines | Size | Purpose |
|----------|-------|------|---------|
| FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md | 2,889 | 85 KB | Complete specification |
| CLAUDE_CODE_QUICKSTART.md | 1,162 | 26 KB | Implementation guide |
| ARCHITECTURE_DIAGRAMS.md | 855 | 48 KB | Visual references |
| IMPLEMENTATION_SUMMARY.md | 471 | 15 KB | Quick reference |
| **TOTAL** | **5,377** | **174 KB** | **All guides** |

---

## 🔧 What Each Document Covers

### FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md
```
✅ System Architecture
✅ Technology Stack
✅ Project Structure
✅ Complete Backend Implementation
✅ Complete Frontend Implementation
✅ Database Schema (SQL-ready)
✅ API Specifications
✅ Security & Authentication
✅ Performance Requirements
✅ Development Workflow
✅ Deployment Guide
✅ Testing Strategy
✅ Troubleshooting
✅ Best Practices
```

### CLAUDE_CODE_QUICKSTART.md
```
✅ Environment Setup Commands
✅ Phase 0-3 Implementation Steps
✅ 15+ Complete Code Files
✅ Specific Python Services
✅ Vue 3 Components
✅ Pinia Stores
✅ API Services
✅ Docker Setup
✅ Testing Examples
✅ Deployment Commands
✅ Execution Checklist
```

### ARCHITECTURE_DIAGRAMS.md
```
✅ 8+ ASCII Diagrams
✅ Data Flow Diagrams
✅ Component Relationships
✅ Database ER Diagram
✅ Request/Response Flows
✅ Session Lifecycle
✅ Error Handling Flow
✅ Security Architecture
✅ Deployment Layout
✅ Pinia State Tree
```

### IMPLEMENTATION_SUMMARY.md
```
✅ Migration Comparison
✅ 6-Phase Timeline
✅ 65+ File Checklist
✅ Quick API Reference
✅ Setup Instructions
✅ Troubleshooting Guide
✅ Performance Tips
✅ Security Checklist
✅ Key Metrics
```

---

## 🚀 Implementation Timeline

### Week 1: Backend Setup
- Monday-Tuesday: Environment setup + DocTypes
- Wednesday-Thursday: API endpoints + LLM service
- Friday: Unit tests + integration tests

### Week 2: Frontend Development
- Monday-Wednesday: Vue components + Pinia stores
- Thursday-Friday: API services + composables

### Week 3: Advanced Features
- Monday-Tuesday: MCP connector support
- Wednesday: File upload + streaming
- Thursday-Friday: Conversation management + settings

### Week 4: Polish & Deploy
- Monday-Tuesday: Comprehensive testing
- Wednesday: Performance optimization
- Thursday: Security audit
- Friday: Documentation + Docker setup

**Total**: 4 weeks to production-ready app

---

## 📁 How to Use These Documents

### Scenario 1: "I want to build this app"
1. Use **CLAUDE_CODE_QUICKSTART.md** - Phase by phase
2. Reference **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** for details
3. Check **ARCHITECTURE_DIAGRAMS.md** when debugging

### Scenario 2: "I need to understand the architecture"
1. Read **IMPLEMENTATION_SUMMARY.md** - Get overview
2. Study **ARCHITECTURE_DIAGRAMS.md** - Understand design
3. Deep dive **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** - Full details

### Scenario 3: "I need to present this to stakeholders"
1. Use **ARCHITECTURE_DIAGRAMS.md** - For visuals
2. Reference **IMPLEMENTATION_SUMMARY.md** - For timeline
3. Pull stats from **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md** - For details

### Scenario 4: "I'm stuck on something"
1. Check **IMPLEMENTATION_SUMMARY.md** troubleshooting section
2. Reference relevant part in **FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md**
3. Look at **ARCHITECTURE_DIAGRAMS.md** for data flow

---

## 🔑 Key Sections by Topic

### For LLM Integration
- **Full Solution** → Section 5.2 (LLM Service)
- **Quick Start** → Phase 1 (File 6: llm_service.py)
- **Diagrams** → User Message Flow

### For Frontend
- **Full Solution** → Section 6 (Frontend Implementation)
- **Quick Start** → Phase 2 (Chat Component files)
- **Summary** → File checklist (Components section)

### For MCP Tools
- **Full Solution** → Section 10 (MCP Integration)
- **Quick Start** → Not covered (reference Full Solution)
- **Diagrams** → MCP Tool Execution Flow

### For Deployment
- **Full Solution** → Section 13 (Deployment Guide)
- **Quick Start** → Phase 3 (Docker Compose setup)
- **Diagrams** → Deployment Architecture

### For Security
- **Full Solution** → Section 11 (Security & Auth)
- **Quick Start** → .env.example file
- **Summary** → Security Checklist
- **Diagrams** → Security Layers (7 layers)

### For Database
- **Full Solution** → Section 7 (Database Schema)
- **Quick Start** → Not included (use Full Solution)
- **Diagrams** → Database Relationship Diagram

---

## 💡 Tips for Using These Documents

1. **Keep them accessible**: Pin these documents in your IDE
2. **Search by keyword**: Use Ctrl+F to find specific topics
3. **Cross-reference**: Links between documents for related info
4. **Track progress**: Use the implementation checklist
5. **Bookmark sections**: Mark important sections for quick access
6. **Version control**: Keep these in your git repository
7. **Share with team**: All team members should have access
8. **Update as you go**: Keep these in sync with your implementation

---

## 📞 Document Information

**Created**: October 26, 2025  
**Version**: 2.0 (Updated from original Assistant UI solution)  
**Status**: Production-Ready  
**Framework**: Frappe + Vue 3 + Frappe UI  
**Language**: Python (backend) + Vue 3 (frontend)  
**Database**: MariaDB  
**Cache**: Redis  

---

## ✅ Verification Checklist

Before starting development, verify you have:
- [ ] Read IMPLEMENTATION_SUMMARY.md
- [ ] Reviewed ARCHITECTURE_DIAGRAMS.md
- [ ] Understood the technology stack
- [ ] Environment setup completed
- [ ] Docker installed (for deployment)
- [ ] Python 3.10+ and Node.js 18+ installed
- [ ] Access to LLM APIs (OpenAI/Anthropic keys)
- [ ] Team alignment on timeline

---

## 🎓 Learning Resources

**Frappe**: https://frappeframework.com/docs  
**Vue 3**: https://vuejs.org  
**Frappe UI**: https://github.com/frappe/frappe-ui  
**MCP Protocol**: https://spec.modelcontextprotocol.io  
**LiteLLM**: https://github.com/BerriAI/litellm  
**Socket.io**: https://socket.io/docs/  

---

## 📝 Document Format Notes

- **Code blocks**: Use triple backticks (```) with language
- **Diagrams**: ASCII art for compatibility
- **Tables**: Markdown format for easy conversion
- **Links**: Relative links within documents
- **Sections**: Clear heading hierarchy (# ## ###)
- **Examples**: Real, working code that can be copy-pasted

---

## 🔄 Maintenance & Updates

These documents should be updated when:
- New features are added to the app
- Technology versions change significantly
- API endpoints are modified
- Security issues are discovered
- Performance improvements are made
- New deployment methods are adopted

---

## 📌 Quick Navigation

| I want to... | Start here |
|---|---|
| Build the app | CLAUDE_CODE_QUICKSTART.md |
| Understand architecture | ARCHITECTURE_DIAGRAMS.md |
| Get technical details | FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md |
| Track implementation | IMPLEMENTATION_SUMMARY.md |
| Present to stakeholders | ARCHITECTURE_DIAGRAMS.md + IMPLEMENTATION_SUMMARY.md |
| Troubleshoot issues | IMPLEMENTATION_SUMMARY.md |
| Deploy to production | FRAPPE_AI_MCP_CHAT_FULL_SOLUTION.md (Section 13) |

---

## 🎯 Success Criteria

Your implementation is successful when:
- ✅ All API endpoints working
- ✅ Frontend components rendering
- ✅ Messages streaming in real-time
- ✅ File uploads working
- ✅ MCP tools executing
- ✅ All tests passing (90%+ coverage)
- ✅ Deployed to production
- ✅ Performance targets met
- ✅ Security audit passed
- ✅ Documentation complete

---

## 📄 License & Usage

These documents are provided as-is for the Frappe AI MCP Chat project. They contain:
- Complete technical specifications
- Production-ready code examples
- Architecture diagrams
- Implementation guides

Use them for:
- ✅ Building the application
- ✅ Team training
- ✅ Project planning
- ✅ Architecture review
- ✅ Technical documentation

---

**Ready to get started?** 👉 Open **CLAUDE_CODE_QUICKSTART.md** to begin Phase 0!

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test locally
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Create a Pull Request

### Development Guidelines

- Follow Python PEP 8 style guide
- Use Vue 3 Composition API
- Write unit tests for new features
- Update documentation
- Ensure all tests pass

---

## 🔐 Security

- API keys are encrypted in the database
- All endpoints require authentication
- Input validation on all user inputs
- CSRF protection enabled
- Rate limiting implemented
- Audit logging for all operations

For security issues, please email [security contact] or create a private security advisory.

---

## 📊 Stats

- **Total Files**: 35
- **Lines of Code**: ~2,035
- **Backend**: 11 Python files
- **Frontend**: 9 Vue/JavaScript files
- **DocTypes**: 4 complete models
- **API Endpoints**: 5 REST endpoints
- **LLM Providers**: 3 (OpenAI, Anthropic, Google)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Built with [Frappe Framework](https://frappeframework.com)
- UI powered by [Vue 3](https://vuejs.org)
- LLM integrations via official SDKs
- MCP protocol by Anthropic

---

## 📞 Support

- **Documentation**: See guides in this repository
- **Issues**: [GitHub Issues](https://github.com/pankajxmathur/ai_chat/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pankajxmathur/ai_chat/discussions)

---

## 🗺️ Roadmap

### Current (v1.0)
- ✅ Multi-provider LLM support
- ✅ Real-time streaming
- ✅ Conversation management
- ✅ MCP protocol foundation

### Planned (v1.1)
- [ ] File upload and processing
- [ ] Advanced MCP tool UI
- [ ] Conversation search and filtering
- [ ] Export conversations (PDF, Markdown)

### Future (v2.0)
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Collaborative chats
- [ ] Admin analytics dashboard
- [ ] Mobile apps (iOS/Android)

---

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Document Version**: 1.0
**Last Updated**: October 26, 2025
**Status**: Complete & Ready for Use
**Maintained by**: Pankaj Mathur
