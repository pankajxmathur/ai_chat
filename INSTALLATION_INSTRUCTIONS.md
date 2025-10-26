# Installation Instructions - Working Method

## ⚠️ Important Note

The setup files (setup.py, pyproject.toml) are currently on the `claude/review-readme-011CUVTCkvLhC1uJ6L3JQVMV` branch and need to be merged to main first.

## 🚀 Installation Options

### Option 1: Install from Specific Branch (Current Workaround)

```bash
# Navigate to your Frappe bench
cd ~/frappe-bench

# Clone from the specific branch that has the setup files
git clone -b claude/review-readme-011CUVTCkvLhC1uJ6L3JQVMV https://github.com/pankajxmathur/ai_chat.git ai_mcp_chat

# Move to apps directory (if not already there)
mv ai_mcp_chat apps/ 2>/dev/null || true

# Install dependencies
cd apps/ai_mcp_chat
pip install -r requirements.txt

# Go back to bench root
cd ../..

# Install the app to your site
bench --site site1.local install-app ai_mcp_chat

# Set environment variables
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."

# Start Frappe
bench start
```

### Option 2: Manual Installation (Most Reliable)

```bash
# Navigate to your Frappe bench apps directory
cd ~/frappe-bench/apps

# Clone the repository with the correct branch
git clone -b claude/review-readme-011CUVTCkvLhC1uJ6L3JQVMV https://github.com/pankajxmathur/ai_chat.git ai_mcp_chat

# Navigate into the app
cd ai_mcp_chat

# Install Python dependencies
pip install -r requirements.txt

# Go back to bench directory
cd ~/frappe-bench

# Install the app to your site
bench --site site1.local install-app ai_mcp_chat

# Set environment variables
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Start Frappe backend
bench start

# In a new terminal, start frontend
cd ~/frappe-bench/apps/ai_mcp_chat/frontend
npm install
npm run dev
```

### Option 3: Wait for Main Branch Merge (Recommended for Future)

Once the branch is merged to main, you'll be able to use:

```bash
bench get-app ai_mcp_chat https://github.com/pankajxmathur/ai_chat.git
```

## 🔄 To Merge the Branch to Main

Since the setup files are on the feature branch, you need to merge it to main:

```bash
# Clone the repository
git clone https://github.com/pankajxmathur/ai_chat.git
cd ai_chat

# Checkout main branch
git checkout main

# Merge the feature branch
git merge claude/review-readme-011CUVTCkvLhC1uJ6L3JQVMV

# Push to main (requires permissions)
git push origin main
```

## ✅ Quick Start (Use This Now)

```bash
# 1. Navigate to bench
cd ~/frappe-bench/apps

# 2. Remove old installation if exists
rm -rf ai_chat ai_mcp_chat 2>/dev/null

# 3. Clone from the correct branch
git clone -b claude/review-readme-011CUVTCkvLhC1uJ6L3JQVMV \
    https://github.com/pankajxmathur/ai_chat.git \
    ai_mcp_chat

# 4. Install dependencies
cd ai_mcp_chat
pip install -r requirements.txt

# 5. Go back to bench
cd ~/frappe-bench

# 6. Install app
bench --site site1.local install-app ai_mcp_chat

# 7. Set API keys (edit with your keys)
export OPENAI_API_KEY="sk-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# 8. Start bench
bench start
```

## 🎯 Configure After Installation

1. Open browser to http://localhost:8000
2. Login with your credentials
3. Go to: **AI MCP Chat** → **LLM Model Configuration**
4. Click **New**
5. Fill in:
   - **Model Name**: GPT-4
   - **Provider**: OpenAI
   - **Model Identifier**: gpt-4
   - **API Key Field Name**: OPENAI_API_KEY
   - **Is Active**: ✓
6. Save
7. Access chat at http://localhost:5173

## 🐛 Troubleshooting

### If you get "directory already exists"
```bash
cd ~/frappe-bench/apps
rm -rf ai_chat ai_mcp_chat
# Then try installation again
```

### If dependencies fail to install
```bash
cd ~/frappe-bench/apps/ai_mcp_chat
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### If app doesn't show up
```bash
# Verify installation
bench --site site1.local list-apps

# Reinstall if needed
bench --site site1.local uninstall-app ai_mcp_chat
bench --site site1.local install-app ai_mcp_chat
```

## 📋 Verification Steps

After installation, verify everything works:

```bash
# 1. Check app is listed
bench --site site1.local list-apps | grep ai_mcp_chat

# 2. Check files exist
ls ~/frappe-bench/apps/ai_mcp_chat/setup.py
ls ~/frappe-bench/apps/ai_mcp_chat/ai_mcp_chat/hooks.py

# 3. Check Python can import it
python -c "import ai_mcp_chat; print(ai_mcp_chat.__version__)"

# 4. Start bench
bench start
```

## 🎉 Success Indicators

You know it worked when:
- ✅ No errors during `bench install-app`
- ✅ App appears in list-apps output
- ✅ Frappe starts without errors
- ✅ "AI MCP Chat" module appears in Frappe UI
- ✅ You can create LLM configurations
- ✅ Frontend loads at port 5173

---

**Current Status**: Setup files are on branch `claude/review-readme-011CUVTCkvLhC1uJ6L3JQVMV`

**Action Needed**: Merge this branch to main, or use the branch-specific installation commands above.
