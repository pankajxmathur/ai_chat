FROM frappe/erpnext:latest

# Set working directory
WORKDIR /home/frappe/frappe-bench

# Copy application files
COPY ai_mcp_chat /home/frappe/frappe-bench/apps/ai_mcp_chat
COPY requirements.txt /home/frappe/frappe-bench/apps/ai_mcp_chat/

# Install dependencies
RUN pip install -r /home/frappe/frappe-bench/apps/ai_mcp_chat/requirements.txt

# Install the app
RUN bench get-app ai_mcp_chat

# Expose port
EXPOSE 8000

# Start command
CMD ["bench", "start"]
