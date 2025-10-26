# AI MCP Chat - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- Node.js 18 or higher
- MariaDB 10.6 or higher
- Redis 6.0 or higher
- Docker and Docker Compose (for containerized deployment)

## Quick Start with Docker

The fastest way to get started is using Docker Compose:

```bash
# 1. Clone the repository
git clone <repository-url>
cd ai_chat

# 2. Create environment file
cp .env.example .env

# 3. Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...

# 4. Start services
docker-compose up -d

# 5. Create site (first time only)
docker-compose exec frappe bench new-site site1.local

# 6. Install app
docker-compose exec frappe bench --site site1.local install-app ai_mcp_chat

# 7. Access the application
# Open http://localhost:8000 in your browser
```

## Manual Setup (Development)

### Backend Setup

```bash
# 1. Install Frappe Framework
git clone https://github.com/frappe/frappe.git
cd frappe
pip install -e .

# 2. Create bench
bench init frappe-bench
cd frappe-bench

# 3. Create site
bench new-site site1.local

# 4. Link the ai_mcp_chat app
cd apps
ln -s /path/to/ai_chat/ai_mcp_chat ai_mcp_chat

# 5. Install dependencies
cd ai_mcp_chat
pip install -r requirements.txt

# 6. Install the app
bench --site site1.local install-app ai_mcp_chat

# 7. Set environment variables
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...

# 8. Start development server
bench start
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd ai_chat/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# The frontend will be available at http://localhost:5173
```

## Configuration

### LLM Model Configuration

After installation, you need to configure at least one LLM model:

1. Log in to Frappe at http://localhost:8000
2. Navigate to: AI MCP Chat > LLM Model Configuration
3. Click "New"
4. Fill in the details:
   - **Model Name**: GPT-4 (or your preferred name)
   - **Provider**: OpenAI (or Anthropic, Google)
   - **Model Identifier**: gpt-4 (or claude-3-opus, gemini-pro)
   - **API Key Field Name**: OPENAI_API_KEY
   - **Is Active**: ✓ Checked
5. Save

### Creating Your First Chat

1. Access the chat interface at http://localhost:5173
2. Click "+ New Chat"
3. Type your message
4. Press Enter or click "Send"

## Testing

### Run Backend Tests

```bash
cd ai_chat
python -m pytest tests/
```

### Run Frontend Tests

```bash
cd frontend
npm run test
```

## Troubleshooting

### Common Issues

**1. "No active LLM model configured" error**
- Solution: Create and activate an LLM Model Configuration (see Configuration section)

**2. API key errors**
- Solution: Ensure environment variables are set correctly in .env file
- Verify: `echo $OPENAI_API_KEY`

**3. Frontend can't connect to backend**
- Solution: Check that Frappe is running on port 8000
- Verify proxy settings in `frontend/vite.config.js`

**4. Database connection errors**
- Solution: Ensure MariaDB is running
- Check credentials in site_config.json

**5. Redis connection errors**
- Solution: Ensure Redis is running
- Default: localhost:6379

### Logs

View logs for debugging:

```bash
# Backend logs
tail -f logs/frappe.log

# Frontend logs
# Check browser console

# Docker logs
docker-compose logs -f frappe
```

## Production Deployment

### Using Docker Compose

```bash
# 1. Set production environment variables
cp .env.example .env.production

# 2. Edit .env.production with production values
# 3. Build and run
docker-compose -f docker-compose.yml up -d

# 4. Setup SSL/TLS (recommended)
# Configure nginx with Let's Encrypt certificates
```

### Security Checklist

- [ ] Change default database password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable backup automation
- [ ] Review and restrict permissions
- [ ] Keep dependencies updated

## Development Workflow

### Adding New Features

1. Create new branch: `git checkout -b feature/your-feature`
2. Make changes to code
3. Test locally
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Create pull request

### Database Migrations

When you modify DocTypes:

```bash
bench --site site1.local migrate
```

## API Documentation

API endpoints are available at:
- `POST /api/method/ai_mcp_chat.api.chat.create_chat_thread`
- `GET /api/method/ai_mcp_chat.api.chat.get_chat_thread`
- `GET /api/method/ai_mcp_chat.api.chat.list_chat_threads`
- `POST /api/method/ai_mcp_chat.api.chat.send_message`
- `DELETE /api/method/ai_mcp_chat.api.chat.delete_thread`

See full documentation in `docs/API.md`

## Support

For issues and questions:
- Check documentation in `/docs` directory
- Review troubleshooting section above
- Check existing issues on GitHub
- Create new issue with details

## License

MIT License - See LICENSE file for details
