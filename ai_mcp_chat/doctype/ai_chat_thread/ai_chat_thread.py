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
