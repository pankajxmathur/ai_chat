# Installation Fix - bench get-app Now Works!

## ✅ Issue Resolved

The `bench get-app` command was failing because the repository was missing proper Frappe app packaging files.

## 🔧 What Was Fixed

### Files Added:

1. **setup.py** - Python package setup configuration
   - Enables `pip install` functionality
   - Defines package metadata and dependencies
   - Required for Frappe's bench get-app

2. **pyproject.toml** - Modern Python packaging metadata
   - PEP 621 compliant project metadata
   - Lists all dependencies
   - Defines build system requirements

3. **MANIFEST.in** - Package file inclusion rules
   - Specifies which files to include in distribution
   - Includes all necessary JSON, HTML, CSS, JS files

4. **LICENSE** - MIT License file
   - Standard open-source license
   - Required for proper package distribution

5. **ai_mcp_chat/__init__.py** - Updated with version
   - Added `__version__ = "1.0.0"`
   - Required by setup.py

### Files Updated:

6. **README.md** - Fixed installation command
   - Changed: `bench get-app https://github.com/pankajxmathur/ai_chat.git ai_mcp_chat`
   - To: `bench get-app ai_mcp_chat https://github.com/pankajxmathur/ai_chat.git`

---

## 🚀 How to Install (Now Working!)

### Method 1: Using bench get-app (Recommended)

```bash
# Navigate to your Frappe bench directory
cd ~/frappe-bench

# Create a new site (if you don't have one)
bench new-site site1.local

# Get the app from GitHub
bench get-app ai_mcp_chat https://github.com/pankajxmathur/ai_chat.git

# Install the app to your site
bench --site site1.local install-app ai_mcp_chat

# Start bench
bench start
```

### Method 2: Direct clone (Alternative)

```bash
# Navigate to Frappe bench apps directory
cd ~/frappe-bench/apps

# Clone the repository
git clone https://github.com/pankajxmathur/ai_chat.git ai_mcp_chat

# Navigate to the app
cd ai_mcp_chat

# Install dependencies
pip install -r requirements.txt

# Go back to bench directory
cd ../..

# Install app to site
bench --site site1.local install-app ai_mcp_chat

# Start bench
bench start
```

---

## ✨ What bench get-app Does

When you run `bench get-app`, Frappe:

1. ✅ Clones the repository to `apps/ai_mcp_chat/`
2. ✅ Reads `setup.py` or `pyproject.toml` for metadata
3. ✅ Installs Python dependencies from `requirements.txt`
4. ✅ Registers the app with the bench
5. ✅ Makes it available for installation to sites

---

## 📋 Complete Installation Workflow

### Step 1: Prerequisites
```bash
# Ensure you have Frappe bench installed
# If not, install it first:
pip install frappe-bench
```

### Step 2: Initialize Bench (First time only)
```bash
bench init frappe-bench
cd frappe-bench
```

### Step 3: Create Site
```bash
bench new-site site1.local
# You'll be prompted for MySQL root password
```

### Step 4: Get the App
```bash
bench get-app ai_mcp_chat https://github.com/pankajxmathur/ai_chat.git
```

### Step 5: Install to Site
```bash
bench --site site1.local install-app ai_mcp_chat
```

### Step 6: Configure Environment Variables
```bash
# Add to your site's common_site_config.json or set as environment variables
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

### Step 7: Start Development Server
```bash
bench start
```

### Step 8: Setup Frontend (Development)
```bash
# In a new terminal
cd ~/frappe-bench/apps/ai_mcp_chat/frontend
npm install
npm run dev
```

### Step 9: Access the Application
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

---

## 🎯 Configure LLM Models

After installation:

1. Log in to Frappe at http://localhost:8000
2. Navigate to: **AI MCP Chat** → **LLM Model Configuration**
3. Click **New**
4. Fill in the form:
   - **Model Name**: GPT-4
   - **Provider**: OpenAI
   - **Model Identifier**: gpt-4
   - **API Key Field Name**: OPENAI_API_KEY
   - **Is Active**: ✓ (checked)
5. Click **Save**

---

## 🔍 Verifying Installation

### Check if app is installed:
```bash
bench --site site1.local list-apps
# Should show "ai_mcp_chat" in the list
```

### Check app status:
```bash
cd ~/frappe-bench/apps/ai_mcp_chat
ls -la
# Should show all files including setup.py, pyproject.toml
```

### Check Python package:
```bash
pip show ai-mcp-chat
# Should display package information
```

---

## 🐛 Troubleshooting

### Issue: "Could not find app ai_mcp_chat"
**Solution**: Make sure you're using the correct command:
```bash
bench get-app ai_mcp_chat https://github.com/pankajxmathur/ai_chat.git
```

### Issue: "No module named 'ai_mcp_chat'"
**Solution**: Install dependencies:
```bash
cd ~/frappe-bench/apps/ai_mcp_chat
pip install -r requirements.txt
```

### Issue: "Permission denied"
**Solution**: Check ownership:
```bash
sudo chown -R $USER:$USER ~/frappe-bench
```

### Issue: Missing dependencies
**Solution**: Install manually:
```bash
pip install openai anthropic google-generativeai python-socketio redis pydantic
```

---

## 📦 What's Included in the Package

The repository is now a proper Frappe app package with:

✅ **Backend** (Python/Frappe)
- API endpoints for chat operations
- Multi-provider LLM service
- Chat service orchestration
- DocTypes for data models

✅ **Frontend** (Vue 3)
- Modern chat interface
- Pinia state management
- Real-time messaging
- Responsive design

✅ **Configuration**
- Docker Compose setup
- Environment templates
- Setup scripts

✅ **Documentation**
- Comprehensive guides
- API documentation
- Architecture diagrams
- Troubleshooting tips

---

## 🎉 Success Indicators

You know the installation worked when:

1. ✅ `bench get-app` completes without errors
2. ✅ App appears in `bench --site site1.local list-apps`
3. ✅ You can access Frappe at http://localhost:8000
4. ✅ "AI MCP Chat" appears in the modules list
5. ✅ You can create LLM Model Configurations
6. ✅ Frontend loads at http://localhost:5173
7. ✅ You can send messages and get responses

---

## 📚 Next Steps

After successful installation:

1. **Configure at least one LLM model** (OpenAI, Anthropic, or Google)
2. **Set environment variables** for API keys
3. **Access the chat interface** and create your first chat
4. **Explore the documentation** for advanced features
5. **Check out SETUP.md** for detailed configuration options

---

## 🔗 Useful Links

- **Repository**: https://github.com/pankajxmathur/ai_chat
- **Frappe Docs**: https://frappeframework.com/docs
- **Vue 3 Docs**: https://vuejs.org
- **Issue Tracker**: https://github.com/pankajxmathur/ai_chat/issues

---

## 📝 Summary of Changes

| File | Status | Purpose |
|------|--------|---------|
| setup.py | ✅ Added | Python package setup |
| pyproject.toml | ✅ Added | Modern packaging metadata |
| MANIFEST.in | ✅ Added | File inclusion rules |
| LICENSE | ✅ Added | MIT license |
| ai_mcp_chat/__init__.py | ✅ Updated | Added version |
| README.md | ✅ Updated | Fixed command syntax |

---

**Fixed**: October 26, 2025
**Status**: ✅ Working
**Tested**: bench get-app command verified

Now you can successfully install the app using `bench get-app`! 🎉
