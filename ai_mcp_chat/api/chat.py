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
            "system_prompt": system_prompt or "You are a helpful AI assistant.",
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
                "thread_id": thread_doc.thread_id,
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
